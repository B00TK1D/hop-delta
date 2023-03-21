#!/bin/bash
# Install Flask
pip install flask

# Kill any existing Python processes
pkill python

# Perform a git pull to update the code
git pull

# Run the app
sudo python3 src/app.py