# coc-hotline
The PyCascades Code of Conduct Hotline

# Requirements
Python 3.6+ because F strings are the best strings.

# Installation
1. Create and activate a virtual environment.
2. Run `pip install -r requirements.txt` to install the dependencies
3. (Optional) Add the "Incoming Webhooks" integration to your slack team of choice
    * Follow the configuration instructions and write down your WebHook URL
4. Set the following environment variables:
    * `COC_NUMBERS`: A comma separated list of phone numbers prefixed with `+`, numbers should include country code.
    * `COC_HTTP_SCHEME`: either `http` or `https`, we recommend deploying with lambda which will provide https for you.
    * `COC_SLACK_URL`: (Optional) The WebHook URL provided by the Incoming Webhooks Slack integration.
5. Run `python coc-hotline.py`


# Deployment
This tool was built to be run on AWS Lambda, but could easily be adapted to run anywhere you can run
Python 3.6+. To deploy to AWS Lambda follow the below instructions:

1. Create an AWS account and configure your AWS credentials file.
2. Create and activate a virtual environment.
3. Run `pip install -r requirements.txt`
4. Run `zappa init`
5. Answer all of the questions asked.
6. Add an `environment_variables` attribute to your zappa config and fill out the environment
  variables listed in the installation instructions above.
7. Run `zappa deploy [your environment name here]`
