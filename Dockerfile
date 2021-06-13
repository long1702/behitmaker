FROM python:3.7-slim

RUN mkdir -m 777 -p /source/hit-maker
ADD requirements.txt /source/hit-maker
RUN pip install -r /source/hit-maker/requirements.txt

ADD ./ /source/hit-maker
WORKDIR /source/hit-maker
RUN chmod 777 ./scripts/run_service.sh
RUN chmod 777 ./scripts/run_all_tests.sh
RUN chmod 777 ./scripts/run_integration_tests.sh
RUN chmod 777 ./scripts/wait_for_it.sh