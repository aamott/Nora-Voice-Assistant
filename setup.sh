#!/bin/bash
##############################
# setup.ps1
##############################

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
    read -p "Path to python executable (Enter to use default. 's' to skip installing requirements): " user_set_python

    # default
    if [$user_set_python == ""]; then 
        # default python installation
        full_path = which python
        echo "Using default python executable: $full_path"
    fi
    
    
    # user chosen
    if [$user_set_python != "s"];
            if [ -f $user_set_python ]; then
                full_path = $user_set_python
            else
                echo "File not found"
            fi
    fi

    # skip - exit loop
    if [$user_set_python == "s"]; then
        echo "Skipping python installation"
        break
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
# Set up settings.yaml
echo ""
echo ""

# check if settings.yaml exists. Only create if it doesn't exist or user wants to overwrite it
create_settings_file = true
input = ""
if [-f $settings_file]; then
    read -p "Settings.yaml already exists. create_settings_file? (y/N): " input
    
    if [$input == "y"]; then
        echo "Overwriting settings.yaml'"
        $create_settings_file = true
    fi
    else
        echo "Skipping settings file creation"
        create_settings_file = false
    fi
fi



if [$create_settings_file == true]; then

    ############################
    # Wakeword config
    echo

    echo "Please go to the following URL to obtain an access key"
    echo "https://console.picovoice.ai/"

    while [$access_key == ""]
        $access_key = read -p "Access Key ('s' to skip)"
        if [$access_key == "s"]; then
            echo "Skipping access key"
            $access_key = "<your access key>"
            break
        fi
    done
    
    
    ############################
    # Write the file
    settings_string = "
wakeword:
    picovoice:
        key: ${access_key}
        keywords:
        - computer
        model_path: null
        sensitivities: null
"
    echo "Creating settings.yaml"
    echo $settings_string > settings.yaml
}