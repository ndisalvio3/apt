#!/bin/bash

# Add the GPG key
wget -qO - https://apt.hostmc4free.com/debian/archive.key | sudo tee /etc/apt/trusted.gpg.d/hostmc4free.asc

# Add the repository
echo "deb [signed-by=/etc/apt/trusted.gpg.d/hostmc4free.asc] https://apt.hostmc4free.com/debian ./" | sudo tee /etc/apt/sources.list.d/hostmc4free.list

# Update package lists
sudo apt update

echo "Repository added successfully!"
