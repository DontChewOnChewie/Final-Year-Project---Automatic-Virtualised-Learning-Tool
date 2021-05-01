# Self-elevate the script if required (https://blog.expta.com/2017/03/how-to-self-elevate-powershell-script.html)
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
 if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
  $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
  Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine
  Exit
 }
}

function Add_VBoxManage_To_PATH() {
    $registry_path_base = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    $registry_PATH = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\Path"

    if ((Test-Path $registry_path_base)) {
        $current_path_value = (Get-ItemProperty -Path $registry_path_base -Name path).path
        $new_path = $current_path_value + ";C:\Program Files\Oracle\VirtualBox"
        New-ItemProperty -Path $registry_path_base -Name path -Value $new_path -PropertyType ExpandString -Force | Out-Null
    } else {
        echo "Path route does not exist!"
    }
}

$VBOX_SAVE_PATH = "installers\vbox-install.exe"
$VBOX_URI = "https://download.virtualbox.org/virtualbox/6.1.14/VirtualBox-6.1.14-140239-Win.exe"

$DOCKER_SAVE_PATH = "installers\docker-install.exe"
$DOCKER_URI = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"

$WSL_SAVE_PATH = "installers\wsl.msi"
$WSL_URI = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"

cd $env:USERPROFILE

New-Item -ItemType Directory -Force -Path installers

if ($args[0] -eq "1") {
    echo "Retrieving VirtualBox..."
    Invoke-WebRequest -URI $VBOX_URI -OutFile $VBOX_SAVE_PATH -UseBasicParsing
    echo "VirtualBox installer downloaded."
    echo "Installing VirtualBox..."
    .\installers\vbox-install.exe --silent --ignore-reboot
    echo "Installation of VirtualBox complete."

    Start-Sleep -Seconds 5
    Add_VBoxManage_To_PATH
}

if ($args[1] -eq "1") {
    echo "Retrieving Docker..."
    Invoke-WebRequest -URI $DOCKER_URI -OutFile $DOCKER_SAVE_PATH -UseBasicParsing
    echo "Docker installer downloaded."
    echo "Installing Docker..."
    .\installers\docker-install.exe install --quiet
    echo "Installation of Docker complete."

    #echo "Retrieving WSL (Docker dependancy)..."
    Invoke-WebRequest -URI $WSL_URI -OutFile $WSL_SAVE_PATH -UseBasicParsing
    #echo "WSL (Docker dependancy) installer downloaded."
    #echo "Installing WSL (Docker dependancy)..."
    .\installers\wsl.msi /quiet
    #echo "Installation of WSL (Docker dependancy) complete."

    netsh advfirewall firewall set rule group="Network Discovery" new enable=Yes
}

$config_path = $args[2]
node "$config_path\installer.js"

echo "Y" > "$config_path\installed.dat"

echo "Installations Complete - We Reccommend a Re-Start of your System."
