#!/usr/bin/env python3
import minimalmodbus as m

plc = m.Instrument('/dev/ttymxc3', 1)
plc.serial.baudrate = 9600
print(plc)
# minimalmodbus.Instrument<id=0xffffae7c2b80, address=1, mode=rtu, close_port_after_each_call=False,
# precalculate_read_size=True, clear_buffers_before_each_transaction=True, handle_local_echo=False,
# debug=False, serial=Serial<id=0xffffae7c26d0, open=True>(port='/dev/ttymxc3', baudrate=9600, bytesize=8, 
# parity='N', stopbits=1, timeout=0.05, xonxoff=False, rtscts=False, dsrdtr=False)>

# Read T1 Holding Registers (4 registers 400000 - 400003) - interpretation depends on timer mode
# See docs
# Here we are reading Trailing edge impulse 1 mode
# Modbus FC3
# 400001 Preset Time On
# 400002 N/A
# 400003 Resolution
# 400004 Timer mode
# Read T1, T2, T3, T4
print(plc.read_registers(0, 4, functioncode=3))
print(plc.read_registers(4, 4, functioncode=3))
print(plc.read_registers(8, 4, functioncode=3))
print(plc.read_registers(12, 4, functioncode=3))
# [5, 0, 0, 10] T1 ON 5 * 1/10 sec , N/A 0, RESOLUTION 0 (1/10 Sec), MODE 10 (Trailing edge impulse 1)
# [5, 0, 0, 10]
# [5, 0, 0, 10]
# [5, 0, 0, 10]

# Write T1 Multiple Registers (4 registers 400000 - 400003)
# Uses Modbus FC16
# 400001 Register address
# List of values starting at register address
# Set T1 on for 2 sec in Trailing edge impulse 1 mode 
plc.write_registers(0, [20,0,0,10])

# Read T1 Input Registers (2 registers 300000 - 300001)
# Modbus FC4
# 300001 Timer Current Value (1/10 sec)
# 300002 Always 0 in mode 10
# Read current value of T1
print(plc.read_registers(0, 2, functioncode=4))
#[16, 0] <- T1 has been on for 1.6 sec
