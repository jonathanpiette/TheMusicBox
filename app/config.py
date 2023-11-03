# Define GPIO pin constants
CLK_PIN = 22  # Example GPIO pin number
DT_PIN = 23   # Example GPIO pin number
SW_PIN = 24   # Example GPIO pin number

# GPIO Pin Configuration
PIN_CONFIG = {
    CLK_PIN: {'mode': GPIO.IN, 'pull_up_down': GPIO.PUD_UP, 'event': {'type': GPIO.FALLING, 'callback': None, 'bouncetime': 50}},
    DT_PIN: {'mode': GPIO.IN, 'pull_up_down': GPIO.PUD_UP},
    SW_PIN: {'mode': GPIO.IN, 'pull_up_down': GPIO.PUD_UP, 'event': {'type': GPIO.FALLING, 'callback': None, 'bouncetime': 300}},
    # Add other pin configurations
}
