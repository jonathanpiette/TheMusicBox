import smbus2
import time

# Define the I2C bus
I2C_BUS = 1

# PiSugar3 I2C address
PISUGAR3_ADDR = 0x57

# Register addresses
BATTERY_PERCENTAGE_REG = 0x2A
POWER_STATUS_REG = 0x02
IS_CHARGING_MASK = 0x08

# Status register mask for power connected
POWER_CONNECTED_MASK = 0x80

# Create an SMBus instance
bus = smbus2.SMBus(I2C_BUS)

def read_battery_percentage():
    return bus.read_byte_data(PISUGAR3_ADDR, BATTERY_PERCENTAGE_REG)

def is_power_connected():
    status = bus.read_byte_data(PISUGAR3_ADDR, POWER_STATUS_REG)
    return bool(status & POWER_CONNECTED_MASK)
    
def is_charging_mask():
    #todo: fix is charging
    status = bus.read_byte_data(PISUGAR3_ADDR, POWER_STATUS_REG)
    return bool(status & IS_CHARGING_MASK)
    
def main():
    try:
        while True:
            # Get the battery percentage
            percentage = read_battery_percentage()
            print(f"Battery percentage: {percentage}%")
            
            # Check if the power supply is connected
            power_connected = is_power_connected()
            print(f"Power Supply Connected: {'Yes' if power_connected else 'No'}")
            
            is_charging = is_charging_mask()
            print(f"is charging: {'Yes' if is_charging else 'No'}")
            
            # Sleep for a short interval before checking again
            time.sleep(2)
    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
