import minimalmodbus as m

plc = m.Instrument('/dev/ttymxc3', 1)
plc.serial.baudrate = 9600
print(plc)

# Read T1 Holding Registers (4 registers 400000 - 400003)
# Modbus FC3
# 400001 Preset Time OFF (ms)
# 400002 Preset Time ON (ms)
# 400003 Resolution
# 400004 Timer mode
print(plc.read_registers(0, 4, functioncode=3))
#[50, 50, 0, 3] T1 OFF 2, ON 2, RES 0, MODE 3

# Write T1 Multiple Registers (4 registers 400000 - 400003)
# Uses Modbus FC16
# 400001 Register address
# List of values starting at register address 
plc.write_registers(0, [20,50,0,3])

# Read T1 Input Registers (2 registers 300000 - 300001)
# Modbus FC4
# 300001 Timer Current Value (ms)
# 300002 Timer On(1) / Off (0)
print(plc.read_registers(0, 2, functioncode=4))
#[30, 1]

