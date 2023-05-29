FROM python:3.11.3-alpine3.18
RUN pip3 install minimalmodbus
COPY modbus /modbus/
CMD /modbus/modbus_test.py
