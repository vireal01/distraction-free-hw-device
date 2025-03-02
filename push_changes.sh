#!/bin/bash

# Define variables
PORT="/dev/cu.usbserial-0001"
BOARD_PATH="/pyboard"
PROJECT_ROOT="/Users/vireal/projects/distractoin-free"

# Connect and clean old files
echo "Cleaning old files..."
rshell --port $PORT <<EOF
rm -rf $BOARD_PATH/inputs
rm -rf $BOARD_PATH/ui
rm -rf $BOARD_PATH/assets
rm -rf $BOARD_PATH/models
rm -rf $BOARD_PATH/*.py
EOF

# Copy new files
echo "Copying new files..."
rshell --port $PORT <<EOF
cp -r $PROJECT_ROOT/inputs $BOARD_PATH/
cp -r $PROJECT_ROOT/ui $BOARD_PATH/
cp -r $PROJECT_ROOT/assets $BOARD_PATH/
cp -r $PROJECT_ROOT/models $BOARD_PATH/
cp $PROJECT_ROOT/*.py $BOARD_PATH/
EOF

echo "Deployment complete!"