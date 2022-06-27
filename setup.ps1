##############################
# setup.ps1
##############################

############################
# Python executable
Write-Output ""
Write-Output ""

# show the user the full path to the python executable.
$full_path = $null
$PYTHON_PATH = $null
while (($full_path -eq $false -or $null -eq $full_path) -and $PYTHON_PATH -cne "s") {
    
    # Get python executable
    $PYTHON_PATH = Read-Host "Path to python executable (enter to use default. 's' to skip)"
    if ($PYTHON_PATH -eq "") {
        $PYTHON_PATH = "python"
    }

    try {
        if ($PYTHON_PATH -cne "s") {
            $full_path = (Get-Command $PYTHON_PATH).Path
            Write-Output "Full path to python is '${full_path}'"
        }
    }
    catch {
        Write-Output "Could not find python at '${PYTHON_PATH}'"
        $full_path = $false
    }
}


############################
# Requirements install
if ($full_path) {

    Write-Output ""
    Write-Output ""

    # run 'python -m pip install -r requirements.txt'
    Write-Output "Installing requirements..."
    $install_result = Invoke-Expression -Command "& '${full_path}' -m pip install -r requirements.txt"

    Write-Output "Requirements installed."
}
else {
    Write-Output "Warning: Not installing requirements.txt. To install, run 'pip install -r requirements.txt'"
    Write-Output "or '<python path> -m pip install -r requirements.txt'"
}



############################
# Set up settings.yaml
Write-Output ""
Write-Output ""

# check if settings.yaml exists. Only create if it doesn't or user wants to overwrite.
$settings_file = "settings.yaml"
$overwrite = $false
if (Test-Path $settings_file) {
    $overwrite = Read-Host "Would you like to overwrite '${settings_file}? (y/N)'"
    if ($overwrite -eq "y") {
        Write-Output "Overwriting '${settings_file}'"
        $overwrite = $true
    }
    else {
        Write-Output "Skipping settings file creation"
        exit 1
    }
}

if ($overwrite -eq $true) {

    ############################
    # Wakeword config
    Write-Output ""
    Write-Output ""

    Write-Output "Please go to the following URL to obtain an access key"
    Write-Output "https://console.picovoice.ai/"

    Write-Output ""

    do {
        $access_key = Read-Host "Once you have set it up, enter your Access Key ('s' to skip)"
    } until ($access_key -ne "" -and $access_key -cne "s")
    if ($access_key -eq 's') {
        $access_key = "<your access key>"
    }
    
    
    ############################
    # Write the file
    $settings_string = @"
wakeword:
    picovoice:
        key: ${access_key}
        keywords:
        - computer
        model_path: null
        sensitivities: null
"@
    Write-Output "Creating '${settings_file}'"
    $settings_string | Out-File -FilePath $settings_file
}