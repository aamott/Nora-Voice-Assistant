#################################
# setup.ps1
# 1. Installs requirements
# 2. Creates needed config files
#################################

#################################
# Get user specified Python executable or use default 
# Required for installation and python script to create configs
Write-Output ""
Write-Output ""

$full_path = $null
$PYTHON_PATH = $null
while ($false -eq $full_path -or $null -eq $full_path) {
    
    # Ask the user for python executable to use
    $PYTHON_PATH = Read-Host "Path to python executable (enter to use 'python')"
    if ($PYTHON_PATH -eq "") {
        $PYTHON_PATH = "python"
    }

    # confirm that the Python path is valid
    try {
        $full_path = (Get-Command $PYTHON_PATH).Path
        Write-Output "Python path is: '${full_path}'"

        # get the python version
        $python_version = (& python --version)
    }
    catch {
        Write-Output "Could not find python at '${PYTHON_PATH}'"
        $full_path = $null
    }
}


Write-Output ""
Write-Output ""

# check if user is admin. Only install requirements for the user if they are not admin.
$is_admin = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
$as_user = "--user"
if ($is_admin -eq $false) {
    $as_user = ""
}

Write-Output "Installing requirements..."
& $full_path -m pip install -r requirements.txt $as_user

Write-Output "Requirements installed."

# DeepSpeech was only released for Python 3.5-3.9
if ($python_version.StartsWith("Python 3.9") -or $python_version.StartsWith("Python 3.8") -or
                $python_version.StartsWith("Python 3.7") ) {
    $answer = Read-Host "Would you like to install the DeepSpeech offline speech-to-text engine? (Y/n)"

    if ( $answer.StartsWith("y") -or $answer.StartsWith("Y") ) {
        & $full_path -m pip install deepspeech $as_user
    }
}


############################
# Run setup.py
Write-Output ""
Write-Output ""

# run the python script to create the user.yaml file.
& $full_path ./setup.py

############################
# Finished
Write-Output ""
Write-Output ""
Write-Output "Finished Setup"