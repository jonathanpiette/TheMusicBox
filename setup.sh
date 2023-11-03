#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Update package list and upgrade all packages
echo "Updating package list and upgrading existing packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Create a Python virtual environment
echo "Creating a Python virtual environment..."
python3 -m venv ~/themusicbox

# Activate the virtual environment
source ~/themusicbox/bin/activate

# Installing Python3 and Pip if they are not already installed
echo "Installing Python3 and Pip..."
sudo apt-get install python3 python3-pip git vsftpd mpg123 -y



# Now use pip to install packages within the virtual environment
echo "Installing required Python libraries in the virtual environment..."
pip3 install adafruit-circuitpython-pn532 pygame RPi.GPIO pillow ST7789

# Deactivate the virtual environment when done
deactivate

# Enable SPI and I2C interface
echo "Enabling SPI and I2C interfaces..."
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

# Install WM8960 Audio HAT drivers
echo "Cloning and installing WM8960 Audio HAT drivers..."
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh
cd ..

# Configure FTP access by modifying the vsftpd configuration
echo "Configuring FTP access..."
echo "write_enable=YES" | sudo tee -a /etc/vsftpd.conf
sudo systemctl restart vsftpd

# Installing Pisugar Battery Management Software
echo "Installing Pisugar Battery Management Software..."
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash

# Additional setup could be included here, such as adding the user to the SPI and GPIO groups
echo "Adding user to 'spi' and 'gpio' groups..."
sudo usermod -a -G spi,gpio,i2c $(whoami)

# Define the MOTD content
MOTD_CONTENT="                                                       
 _____ _          _____         _        _____         
|_   _| |_ ___   |     |_ _ ___|_|___   | __  |___ _ _ 
  | | |   | -_|  | | | | | |_ -| |  _|  | __ -| . |_'_|
  |_| |_|_|___|  |_|_|_|___|___|_|___|  |_____|___|_,_|
        An audio box with love                                               
-----------------------------------------------
The music box is a special project for you Arthur. I made
it with love just for you so you can discover
great music!
-----------------------------------------------"

# Cloning a Git repository
echo "Cloning specified Git repository..."
git clone https://github.com/jonathanpiette/TheMusicBox/tree/main

echo "Installation completed successfully."
echo "Please reboot the Raspberry Pi for the changes to take effect."

# Reminder to reboot
echo "Do you want to reboot now? [y/N]"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    sudo reboot
fi
