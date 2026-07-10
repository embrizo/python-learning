# iot_sensor.py
# Day 5 OOP Exercises: IoT Sensor Class
# สำหรับฝึกฝนเขียน Class, Methods, Dunder Methods และ Encapsulation (@property)

# -------------------------------------------------------------
# TODO: เขียนคลาส Sensor ตามคำแนะนำในแบบฝึกหัดที่ 1, 2 และ 3
# -------------------------------------------------------------


import dataclasses
class Sensor:
    def __init__(self, sensor_id: str, sensor_type: str, sensor_status):
        self.sensor_id: str = sensor_id #กำหนด Instance Variable ผ่าน self
        self.sensor_type: str = sensor_type #กำหนด Instance Variable ผ่าน self
        self.__sensor_value: float = 0 #กำหนด Instance Variable ผ่าน self
        self.sensor_status:str = sensor_status #กำหนด Instance Variable ผ่าน self
    
    @property
    def sensor_value(self)->float:
        return self.__sensor_value

    @sensor_value.setter
    def sensor_value(self, value:float)->None:
        if value < -40 or value >85:
            raise ValueError("Anomalous temperature reading detected!")
        self.__sensor_value = value

    def __str__(self)->str:
        status = "ONLINE" if self.sensor_value != 0.0 else "OFFLINE"
        return f"Device:{self.sensor_id}, (Type:{self.sensor_type}) | Value:{self.sensor_value} | Status:{status}"

    def __repr__(self)->str:
        return f"Sensor('{self.sensor_id}')"
        
    def update_reading(self, new_value: float) -> None:
        self.sensor_value = new_value #กำหนด Instance Variable ผ่าน self
        
        
    def get_status(self)->str:
        if self.sensor_value == 0.0:
            self.sensor_status: str = "OFFLINE"
            return f"{self.sensor_id}:{self.sensor_status}"

        else:
            return f"{self.sensor_id}:ONLINE"






if __name__ =="__main__":
    print(f"--- Testing Sensor Class ---")

    temp_sensor = Sensor(sensor_id="TEMP-01", sensor_type="temperature", sensor_status="OFFLINE")
    print(temp_sensor)
    print(str(temp_sensor))
    print(repr(temp_sensor))
    print(f"Status:{temp_sensor.get_status()}")

    temp_sensor.update_reading(25.5)
    print(f"New Reading: {temp_sensor.sensor_value}")
    print(f"Status:{temp_sensor.get_status()}")
    
    try:
        temp_sensor.update_reading(100)
    except ValueError as e:
        print(f"Error: {e}")

    print(f"Final Reading:{temp_sensor.sensor_value}")
    print(f"Final Status:{temp_sensor.get_status()}")

"""

class TemperatureSensor:
    def __init__(self):
        self.__celsius: float = 0.0 #Private Instance Variable
    
    @property
    def celsius(self)->float:
        return self.__celsius

    @celsius.setter
    def celsius(self, value:float)->None:
        if value <= -273.15:
            raise ValueError("องศาเซลเซียสไม่สามารถต่ำกว่า -273.15 ได้")
        self.__celsius = value
    
temp = TemperatureSensor()
temp.celsius = 25
print(temp.celsius)
temp.celsius = -300
print(temp.celsius)

"""
        