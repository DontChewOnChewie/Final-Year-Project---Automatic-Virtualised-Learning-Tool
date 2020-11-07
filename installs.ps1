$VBOX_SAVE_PATH = "installers/vbox-install.exe"
$VBOX_URI = "https://download.virtualbox.org/virtualbox/6.1.14/VirtualBox-6.1.14-140239-Win.exe"
$VBOX_ARGS = $args[0].Split("-")

$DOCKER_SAVE_PATH = "installers/docker-install.exe"
$DOCKER_URI = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
$DOCKER_ARGS = $args[1].Split("-")

New-Item -ItemType Directory -Force -Path installers

if ($VBOX_ARGS[0] -eq "1") {
    echo "Retrieving VirtualBox."
    Invoke-WebRequest -URI $VBOX_URI -OutFile $VBOX_SAVE_PATH -UseBasicParsing
    echo "VirtualBox installer downloaded."
    if ($VBOX_ARGS[1] -eq "1") { .\installers\vbox-install.exe }
}

if ($DOCKER_ARGS[0] -eq "1") {
    echo "Retrieving Docker."
    Invoke-WebRequest -URI $DOCKER_URI -OutFile $DOCKER_SAVE_PATH -UseBasicParsing
    echo "Docker installer downloaded."
    if ($DOCKER_ARGS[1] -eq "1") { .\installers\docker-install.exe }
}
