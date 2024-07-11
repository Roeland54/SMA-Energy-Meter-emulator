ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
#RUN apk add --no-cache python3 bash py3-pip

# download requirements.txt
RUN wget --no-cache https://raw.githubusercontent.com/Roeland54/SMA-Energy-Meter-emulator/feature/initial-setup-of-the-emulator/sma/requirements.txt

# install dependencies
RUN pip install -r requirements.txt --break-system-packages

COPY / .
RUN chmod a+x /src/run.sh

CMD [ "/src/run.sh" ]