# coc-hotline
The PyCascades Code of Conduct Hotline

# Requirements
Python 3.6+ because F strings are the best strings.

# How it works
When the hotline is called, it will ring the phones listed in the `COC_NUMBERS` env variable.
The caller will be connected to the first person who responds.

At PyCascades, it will also post to a private slack channel so we have
a record of who called, who answered, how long was the call, and when.

# Why a hotline?
It is easier to share one consistent phone number to call, as opposed to listing
various phone numbers. We can repurpose the same number year after year,
and have the flexibility to add/remove people who will answer the call.

# Installation
1. Create and activate a virtual environment.
2. Run `pip install -r requirements.txt` to install the dependencies
3. (Optional) Add the "Incoming Webhooks" integration to your slack team of choice
    * Follow the configuration instructions and write down your WebHook URL
4. Set the following environment variables:
    * `COC_NUMBERS`: A comma separated list of phone numbers prefixed with `+`, numbers should include country code.
    * `COC_HTTP_SCHEME`: either `http` or `https`, we recommend deploying with [AWS Lambda](https://aws.amazon.com/lambda/) which will provide https for you.
    * `COC_SLACK_URL`: (Optional) The WebHook URL provided by the Incoming Webhooks Slack integration.
5. Run `python coc-hotline.py`

# Deployment
This tool was built to be run on [AWS Lambda](https://aws.amazon.com/lambda/),
but could easily be adapted to run anywhere you can run
Python 3.6+. To deploy to AWS Lambda follow the below instructions:

1. Create an AWS account and configure your AWS credentials file.
2. Create and activate a virtual environment.
3. Run `pip install -r requirements.txt`
4. Run `zappa init`
5. Answer all of the questions asked.
6. Add an `environment_variables` attribute to your zappa config and fill out the environment
  variables listed in the installation instructions above.
7. Run `zappa deploy [your environment name here]`
