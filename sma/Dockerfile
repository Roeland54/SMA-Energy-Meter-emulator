ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN apk add --no-cache python3 bash py3-pip

# install dependencies
RUN pip install paho-mqtt dynaconf --break-system-packages

COPY / .
RUN chmod a+x /src/run.sh

CMD [ "/src/run.sh" ]