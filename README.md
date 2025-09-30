# WNE Client V7 - Backend tests

**This repository contains all backend tests from the WNE Client V7.**

These include:
1. Behavior driven tests in `tests/behavior`
2. Unit tests in `tests`


# How to Set up

**To set up test environment on window system**

> cd "wnec_backend-automation absolute_path"

> Run test_runner_setup.bat

**To set up test environment on linux system**

> cd "wnec_backend-automation absolute_path"

> run 'chmod +x test_runner_setup.sh' (to make test_runner_setup.sh executable file)

> Run ./test_runner_setup.sh 

# How to Run

**To run from window system**

> cd "wnec_backend-automation absolute_path"

> call .\venv\Scripts\activate.bat

> python test_runner.py [--optional arg]

**To run from linux system**

> cd "wnec_backend-automation absolute_path"

> python3 test_runner.py [--optional arg]

**To run all test on docker**

> Update root director docker-compose.yml args with actual credential (aws_access_key, aws_secret_access_key, aws_region, git_user, git_token)

> docker-compose up --build  [--build is optional if want to recreate fresh image from automation repository]


## Runner arg Options

**--reportportal**: If this argument is present, the results will be sent to ReportPortal, omit to only show the terminal output

**-v**, **--verbose**: Verbose mode, shows stacktrace of fails, each individual test name and `print` statements (_prints_ are hidden by default)

**-m "tag_name"**: Tags to be executed (use 'and' to run multiple tags)

**-m "not tag_name"**: Tags to be ignored (use 'and not' to ignore multiple tags)

**path**: Path of test(s)  

**--headed**: If this argument is present, playwright will run test headed mode( test run in visible mode)

**--browser-channel "browser name(e.g. chrome or msedge)"**: If this argument is present, playwright will run test in mention browser (if not present by default will run in Chromium. if want run in chromium based browser than need to pass additional argument --browser "browser type name(e.g. webkit or firefox)")

## Examples

Run only smoke [tagged] tests without reporting to ReportPortal

> python test_runner.py -m "smoke" (For Window)

> python3 test_runner.py -m "smoke" (For Linux)

Run all tests, except the one tagged gold_image and smoke, with reporting and verbose mode

> python test_runner.py -m "not gold_image and not smoke" --reportportal -v (For Window)

> python3 test_runner.py -m "not gold_image and not smoke" --reportportal -v (For Linux)

Run just a specific test file (or directory)

> python test_runner.py tests/gold_image/log_test.py (For Window)

> python3 test_runner.py tests/gold_image/log_test.py (For Linux)

## FAQ

### How do I override the Amazon Secrets? _(load my own config variables)_
If an `.env` file is present in the root, the variables will be read from there.
You can start from the [.env.template file](.env.template) and edit your own information.

If this file is not present, all variables will be loaded from Amazon Secrets


### What technologies are used?

The entire project is built on Python and essentially only two libraries are used:
* pytest
* pytest-bdd


### What are the requirements for running? / The test_runner_setup was not able to install the requirements.
With a python version 3.7 or greater, install the dependencies with:
> pip install -r requirements.txt

Then install [AWS CLI](https://awscli.amazonaws.com) and configure it with valid credentials

After that you should be good to go!
