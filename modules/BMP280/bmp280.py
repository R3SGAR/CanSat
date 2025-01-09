import smbus2

class BMP280:
    def __init__(self, address=0x76):
        self.bus = smbus2.SMBus(1)
        self.address = address

        # Configuración inicial del BMP280
        self.bus.write_byte_data(self.address, 0xF4, 0x27)  # Control measurement
        self.bus.write_byte_data(self.address, 0xF5, 0xA0)  # Config register

    def read_raw_data(self, reg):
        # Lee 2 bytes de datos del registro
        data = self.bus.read_i2c_block_data(self.address, reg, 2)
        return data[0] << 8 | data[1]

    def get_temperature(self):
        raw_temp = self.read_raw_data(0xFA)
        # Conversión simplificada, se debe ajustar con la calibración del sensor
        temp = raw_temp / 100.0
        return temp

    def get_pressure(self):
        raw_press = self.read_raw_data(0xF7)
        # Conversión simplificada
        pressure = raw_press / 256.0
        return pressure

    def get_altitude(self, sea_level_pressure=1013.25):
        pressure = self.get_pressure()
        altitude = 44330 * (1.0 - (pressure / sea_level_pressure) ** (1/5.255))
        return altitude

    def get_packed_data(self):
        temperature = self.get_temperature()
        pressure = self.get_pressure()
        altitude = self.get_altitude()
        return temperature, pressure, altitude
