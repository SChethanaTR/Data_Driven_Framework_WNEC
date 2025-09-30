FROM python:bookworm AS build
# Amazon Secrets Manager Authentication
ARG aws_access_key
ARG aws_secret_access_key
ARG aws_region
ARG git_user
ARG git_token
# AWS Credentials are loaded from environment variables
ENV AWS_ACCESS_KEY_ID $aws_access_key
ENV AWS_SECRET_ACCESS_KEY $aws_secret_access_key
ENV AWS_REGION $aws_region
ENV GIT_USER $git_user
ENV GIT_TOKEN $git_token

RUN apt-get -y update
RUN apt-get -y install git
RUN git config --global credential.helper '!f() { echo "username=$GIT_USER"; echo "password=$GIT_TOKEN"; };f'
RUN git clone https://github.com/tr/wnec_backend-automation.git
RUN cd wnec_backend-automation
WORKDIR /wnec_backend-automation
RUN pip install --upgrade pip
RUN pip install --compile -r requirements.txt && rm -rf /root/.cache
RUN playwright install
RUN playwright install-deps
CMD ["python", "test_runner.py", "--reportportal"]