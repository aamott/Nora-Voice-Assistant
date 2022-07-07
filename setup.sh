#!/bin/bash
##############################
# Setup script
# Currently untested - use at your own risk
##############################

sudo apt install python3-pip flac libespeak1 python3-pip python3-numpy libportaudio2 libsndfile1 libffi-dev libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0

###########################
# Python executable
echo ""
echo ""

# show the user the full path to the python executable.
full_path=0
user_set_python=0
while [ $full_path = 0 ]
do
    
    # Get python executable
    read -p "Path to python executable (Enter to use default): " user_set_python

    # default
    if [ ${#user_set_python} -eq 0 ]; then 
        # default python installation
        full_path=$(which python3)
        echo "Using default python executable: " $full_path
    # user chosen
    elif [ -f $user_set_python ]; then
        full_path=$user_set_python
    else
        echo "File not found"
    fi
done


############################
# Requirements install
if [ $full_path != "" ]; then

    echo ""
    echo ""

    echo "Installing requirements..."
    eval "sudo pip3 install -r requirements.txt"
    echo "Requirements installed."
elif [ $user_set_python == "s" ]; then
    echo "Skipping python installation"
fi

############################
# Run setup.py
echo ""
echo ""

# call the python setup script to create the user.yaml file.
eval $full_path ./setup.py
