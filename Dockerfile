FROM python:3.11.3-alpine3.18
RUN pip3 install minimalmodbus
COPY gateway /gateway/
CMD /gateway/modbus_test.py
