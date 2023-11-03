import RPi.GPIO as GPIO

class GPIOManager:
    def __init__(self, pin_config):
        self.pin_config = pin_config
        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        for pin, config in self.pin_config.items():
            GPIO.setup(pin, config['mode'], pull_up_down=config.get('pull_up_down', GPIO.PUD_OFF))
            if config.get('event'):
                GPIO.add_event_detect(pin, config['event']['type'], callback=config['event']['callback'], bouncetime=config['event']['bouncetime'])

    def cleanup(self):
        GPIO.cleanup()