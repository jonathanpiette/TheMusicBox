#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Update package list and upgrade all packages
echo "Updating package list and upgrading existing packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Installing Python3 and Pip if they are not already installed
echo "Installing Python3 and Pip..."
sudo apt-get install python3 python3-pip -y

# Installing Python packages
echo "Installing required Python libraries..."
pip3 install adafruit-circuitpython-pn532 pygame RPi.GPIO pillow ST7789

# Enable SPI interface
echo "Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

# Additional setup could be included here, such as adding the user to the SPI and GPIO groups
echo "Adding user to 'spi' and 'gpio' groups..."
sudo usermod -a -G spi,gpio $(whoami)

echo "Installation completed successfully."
echo "Please reboot the Raspberry Pi for the changes to take effect."

# Reminder to reboot
echo "Do you want to reboot now? [y/N]"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    sudo reboot
fi