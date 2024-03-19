#!/usr/bin/python3

from .gpio import GpioManager

def get_cpu_temp():
    try:
        temp_file = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = temp_file.read()
        temp_file.close()
        return str(float(cpu_temp)/1000) + " °C"
    except:
        return 'N/A'

def LED_on(pin):
    gpio = GpioManager(pin, 'out', 1)
    gpio.run_without_unexport()

def LED_off(pin):
    gpio = GpioManager(pin, 'out', 0)
    gpio.run_without_unexport()

def LED_status(LED_pin):
    gpio = GpioManager(LED_pin)
    value = gpio.read_pin_value()
    if value:
        value = int(value)
    return value
