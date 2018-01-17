from flask import Flask, Response, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Dial

import requests

import os

app = Flask(__name__)
_HOTLINE_NUMBERS = None
_HTTP_SCHEME = None
_SLACK_URL = None


class ConfigurationError(ValueError):
    pass


def get_hotlilne_numbers():
    global _HOTLINE_NUMBERS

    if _HOTLINE_NUMBERS is None:
        numbers_str = os.environ.get('COC_NUMBERS', None)

        if numbers_str is None:
            msg = 'Environment variable COC_NUMBERS must be present and must be a comma delimited' \
                  ' string of numbers with country codes'
            raise ConfigurationError(msg)

        _HOTLINE_NUMBERS = [num.strip() for num in numbers_str.split(',')]

    return _HOTLINE_NUMBERS


def get_http_scheme():
    global _HTTP_SCHEME

    if _HTTP_SCHEME is None:
        http_scheme_str = os.environ.get('COC_HTTP_SCHEME', 'http').strip().lower()

        if http_scheme_str not in {'http', 'https'}:
            raise ConfigurationError('COC_HTTP_SCHEME must be http or https')

        _HTTP_SCHEME = http_scheme_str

    return _HTTP_SCHEME


def get_slack_url():
    global _SLACK_URL

    if _SLACK_URL is None:
        _SLACK_URL = os.environ.get('COC_SLACK_URL', '')

    return _SLACK_URL


def send_slack_message(msg, attachments=None):
    if _SLACK_URL != '':
        payload = {
            'text': msg,
            'username': 'CoC Hotline Bot',
            'icon_emoji': ':rotating_light:',
        }

        if attachments is not None:
            payload['attachments'] = attachments

        requests.post(get_slack_url(), json=payload)


def handle_answered(data):
    incoming_number = data.get('From')
    outgoing_number = data.get('To')
    msg = f'Call from {incoming_number} answered by {outgoing_number}'
    print(msg)
    msg_attachments = [{
        'color': 'good',
        'title': 'Call Answered',
        'fallback': msg,
        'text': f'Call from *{incoming_number}* answered by *{outgoing_number}*',
        "mrkdwn_in": ["text", "pretext"],
    }]
    send_slack_message('', msg_attachments)


def handle_completed(data):
    incoming_number = data.get('From')
    outgoing_number = data.get('To')
    call_duration = data.get('CallDuration')
    msg = f'Call from {incoming_number} to {outgoing_number} has completed'
    print(msg)
    msg_attachments = [{
        'color': 'good',
        'title': 'Call Completed',
        'fallback': msg,
        'text': f'Call from *{incoming_number}* to *{outgoing_number}* has completed\n'
                f'Call lasted for {call_duration} seconds',
        "mrkdwn_in": ["text", "pretext"],
    }]
    send_slack_message('', msg_attachments)


@app.route('/call_status', methods=['POST'])
def call_status():
    values = request.values
    status = values.get('CallStatus')

    if status == 'in-progress':
        handle_answered(values)
    elif status == 'completed':
        handle_completed(values)

    return Response(str(VoiceResponse()), 200, mimetype="application/xml")


@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    response = VoiceResponse()
    dial = Dial()
    incoming_number = request.values.get('From')
    msg = f'Incoming call from {incoming_number}'
    print(msg)
    msg_attachments = [{
        'color': 'danger',
        'title': 'Incoming Call',
        'fallback': msg,
        'text': f'From *{incoming_number}*',
        "mrkdwn_in": ["text", "pretext"],
    }]
    send_slack_message(f'<!channel>', msg_attachments)
    status_url = url_for('call_status', _external=True, _scheme=get_http_scheme())

    for number in get_hotlilne_numbers():
        dial.number(
            number,
            status_callback_event='initiated ringing answered completed',
            status_callback_method='POST',
            status_callback=status_url,
        )

    response.append(dial)

    return Response(str(response), 200, mimetype="application/xml")


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, threads=8)
