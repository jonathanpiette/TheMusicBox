import RPi.GPIO as GPIO
import time

# Use GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for input
SENSOR_PIN = 5
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SENSOR_PIN):
            print("Light Intensity: Low")
        else:
            print("Light Intensity: High")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()
