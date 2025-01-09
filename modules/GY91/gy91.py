from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import GFS_250, AFS_2G, MFS_16BITS, AK8963_MODE_C100HZ


MFS_16BITS = 0x10 # Valor hexadecimal estándar para la sensibilidad del magnetómetro

from modules.BMP280 import BMP280

class GY91:
    def __init__(self, mpu_address=0x68, bmp_address=0x76):
        # Inicializar BMP280
        self.bmp280 = BMP280(address=bmp_address)

        # Inicializar MPU9250
        self.mpu9250 = MPU9250(
            address_ak=0x0C,  # Dirección del magnetómetro
            address_mpu_master=mpu_address,  # Dirección del MPU9250
            bus=1,
            gfs=GFS_250,  # Sensibilidad del giroscopio
            afs=AFS_2G,   # Sensibilidad del acelerómetro
            mfs=MFS_16BITS,  # Sensibilidad del magnetómetro
            mode=AK8963_MODE_C100HZ  # Modo del magnetómetro (100 Hz)
        )
        self.mpu9250.calibrate()
        self.mpu9250.configure()

    def get_imu_data(self):
        accel = self.mpu9250.readAccelerometer()
        gyro = self.mpu9250.readGyroscope()
        mag = self.mpu9250.readMagnetometer()
        return {
            'accel_x': accel[0], 'accel_y': accel[1], 'accel_z': accel[2],
            'gyro_x': gyro[0], 'gyro_y': gyro[1], 'gyro_z': gyro[2],
            'mag_x': mag[0], 'mag_y': mag[1], 'mag_z': mag[2]
        }

    def get_bmp_data(self):
        temperature, pressure, altitude = self.bmp280.get_packed_data()
        return {
            'temperature': temperature,
            'pressure': pressure,
            'altitude': altitude
        }

    def get_all_data(self):
        imu_data = self.get_imu_data()
        bmp_data = self.get_bmp_data()
        return {**imu_data, **bmp_data}
