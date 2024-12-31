import smbus2

class HDC1080:
    def __init__(self, address=0x40):
        self.bus = smbus2.SMBus(1)
        self.address = address
        self.bus.write_byte_data(self.address, 0x02, 0x00)  # Configuración inicial

    def read_temperature(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
        temp = (data[0] << 8 | data[1]) / 65536.0 * 165.0 - 40.0
        return temp

    def read_humidity(self):
        data = self.bus.read_i2c_block_data(self.address, 0x01, 2)
        humidity = (data[0] << 8 | data[1]) / 65536.0 * 100.0
        return humidity

    def get_packed_data(self):
        temperature = self.read_temperature()
        humidity = self.read_humidity()
        return temperature, humidity