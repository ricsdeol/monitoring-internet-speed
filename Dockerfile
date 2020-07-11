FROM  python:3-alpine

ENV APP_PATH /network_monitor/
ENV APP_USER network_monitor
ENV APP_USER_HOME /home/network_monitor


# UID of the user that will be created
ARG UID

# Validating if UID argument was provided
RUN : "${UID:?You must provide a UID argument when building this image.}"

RUN adduser -h $APP_USER_HOME -D -u $UID $APP_USER

WORKDIR $APP_PATH

COPY requiriments.txt $APP_PATH

RUN pip install -r requiriments.txt


COPY --chown=network_monitor . $APP_PATH

USER $APP_USER
