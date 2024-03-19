#!/usr/bin/python3
import logger
log = logger.getLogger('gpio.py')

class GpioManager():
    def __init__(self, pin, direction='out', value=0):
        self.pin = pin
        self.direction = direction
        self.value = value

    def export_pin(self):
        try:
            f = open('/sys/class/gpio/export','w')
            f.write(str(self.pin))
            f.close()
        except Exception as e:
            log.info('export pin error: %s' % e)

    def unexport_pin(self):
        try:
            f = open('/sys/class/gpio/unexport','w')
            f.write(str(self.pin))
            f.close()
        except Exception as e:
            log.info('unexport pin error: %s' % e)

    def set_pin_direction(self):
        try:
            path = '/sys/class/gpio/gpio' + str(self.pin) + '/direction'
            f = open(path,'w')
            f.write(self.direction)
            f.close()
        except Exception as e:
            log.info('set pin direction error: %s' % e)

    def set_pin_value(self):
        try:
            path = '/sys/class/gpio/gpio' + str(self.pin) + '/value'
            f = open(path,'w')
            f.write(str(self.value))
            f.close()
        except Exception as e:
            log.info('set pin value error: %s' % e)

    def read_pin_value(self):
        try:
            path = '/sys/class/gpio/gpio' + str(self.pin) + '/value'
            f = open(path,'r')
            value = f.readline().strip()
            return value
        except Exception as e:
            log.info('read pin value error: %s' % e)

    def run_with_unexport(self):
        self.unexport_pin()
        self.export_pin()
        self.set_pin_direction()
        self.set_pin_value()
        self.unexport_pin()

    def run_without_unexport(self):
        self.unexport_pin()
        self.export_pin()
        self.set_pin_direction()
        self.set_pin_value()

