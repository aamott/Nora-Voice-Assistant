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
while ($full_path -eq $false -or $null -eq $full_path) {
    
    # Get python executable
    $PYTHON_PATH = Read-Host "Path to python executable (enter to use default)"
    if ($PYTHON_PATH -eq "") {
        $PYTHON_PATH = "python"
    }

    try {
        $full_path = (Get-Command $PYTHON_PATH).Path
        Write-Output "Full path to python is '${full_path}'"
    }
    catch {
        Write-Output "Could not find python at '${PYTHON_PATH}'"
        $full_path = "python"
    }
}


############################
# Requirements install
if ($full_path) {

    Write-Output ""
    Write-Output ""

    # check if user is admin. Only install for the user if they are not admin.
    $is_admin = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
    $as_user = "--user"
    if ($is_admin -eq $false) {
        $as_user = ""
    }

    Write-Output "Installing requirements..."
    & $full_path -m pip install -r requirements.txt $as_user

    Write-Output "Requirements installed."
}
else {
    Write-Output "Warning: Not installing requirements.txt. To install, run 'pip install -r requirements.txt'"
    Write-Output "or '<python path> -m pip install -r requirements.txt'"
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