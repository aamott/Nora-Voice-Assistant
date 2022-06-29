#!/bin/bash
##############################
# Setup script
# Currently untested - use at your own risk
##############################
echo "Warning: This script is not tested. Use at your own risk."
############################
# Python executable
echo ""
echo ""

# show the user the full path to the python executable.
full_path = false
user_set_python = false
while [$full_path == false && $user_set_python != "s"]
do
    
    # Get python executable
    read -p "Path to python executable (Enter to use default): " user_set_python

    # default
    if [$user_set_python == ""]; then 
        # default python installation
        full_path = which python
        echo "Using default python executable: $full_path"
    fi
    
    
    # user chosen
    if [ -f $user_set_python ]; then
        full_path = $user_set_python
    else
        echo "File not found"
    fi
done


############################
# Requirements install
if [$full_path != ""]; then

    echo ""
    echo ""

    # check if user is root. Only install for the user if they are not admin.
    is_admin = false
    if [ "$(id -u)" -eq 0 ]; then
        is_admin = true
    fi
    as_user_option = "--user"
    if [$is_admin == true]; then
        as_user_option = ""
    fi

    echo "Installing requirements..."
    eval "sudo $full_path -m pip install $as_user_option -r requirements.txt"
    echo "Requirements installed."
fi
elif [$user_set_python == "s"]; then
    echo "Skipping python installation"
fi

############################
# Run setup.py
echo ""
echo ""

# call the python setup script to create the user.yaml file.
eval $full_path ./setup.py