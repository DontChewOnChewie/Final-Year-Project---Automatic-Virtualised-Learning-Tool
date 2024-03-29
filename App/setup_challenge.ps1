$has_docker_been_pruned = 0
$has_docker_files = 0

function Setup-VBOX($vbox_file, $challenge_id, $filename) {
    .\setup_vbox.ps1 ".\Downloads\$challenge_id\build\$vbox_file" "$challenge_id $filename"
    # Setup Start/Stop files.
    echo "VBoxManage startvm '$challenge_id $filename' --type headless" >> ".\Downloads\$challenge_id\start.ps1"
    echo "Start-Sleep -Seconds 5" >> ".\Downloads\$challenge_id\start.ps1"
    echo "VBoxManage controlvm '$challenge_id $filename' poweroff --type headless" >> ".\Downloads\$challenge_id\stop.ps1"
}

function Get-Docker-Port($dockerfile) {
    $docker_first_line = Get-Content $dockerfile | select -First 1
    $docker_first_line_parts = $docker_first_line.Split("=")
    if ($docker_first_line_parts.Count -gt 1) {
        if ($docker_first_line_parts[1] -match "^\d+$") {
            return $docker_first_line_parts[1]
        }
    }
    return 6789
}

function Setup-Docker($docker_zip, $challenge_id, $filename) {
    Expand-Archive "./Downloads/$challenge_id/build/$docker_zip" -DestinationPath "./Downloads/$challenge_id/$challenge_id $filename"
    rm "./Downloads/$challenge_id/build/$docker_zip"
    mv "./Downloads/$challenge_id/$challenge_id $filename/*" "./Downloads/$challenge_id/$filename"
    rmdir "./Downloads/$challenge_id/$challenge_id $filename"

    docker build -t "$challenge_id-$filename" "./Downloads/$challenge_id/$filename/"

    # Setup Start/Stop files.
    if ($has_docker_been_pruned -eq 0) {
        echo "docker system prune -f" >> ".\Downloads\$challenge_id\start.ps1"
        $has_docker_been_pruned = 1
        $has_docker_files = 1
    }

    $dockerfile_port = Get-Docker-Port "./Downloads/$challenge_id/$filename/Dockerfile"
    echo "Start-Job -ScriptBlock { docker run --name '$challenge_id-$filename' -p $dockerfile_port`:$dockerfile_port '$challenge_id-$filename' }" >> ".\Downloads\$challenge_id\start.ps1"
    echo "echo 'Docker `: 172.100.100.1`:$dockerfile_port' >> './VM_Shared/ips.txt'" >> ".\Downloads\$challenge_id\start.ps1"

    echo "docker stop '$challenge_id-$filename'" >> ".\Downloads\$challenge_id\stop.ps1"
}

function Setup-Attackers-Machine() {
    # Get users selected machine, can be same as default.
    $selected_machine = $($(cat config.json) | ConvertFrom-Json).selected_machine
    echo "VBoxManage startvm '$selected_machine'" >> ".\Downloads\$challenge_id\start.ps1"
    echo "Start-Sleep -Seconds 5" >> ".\Downloads\$challenge_id\start.ps1"
    echo "VBoxManage sharedfolder add '$selected_machine' --name 'Program_Shared' --hostpath './VM_Shared' --transient --automount" >> ".\Downloads\$challenge_id\start.ps1"
    echo "VBoxManage controlvm '$selected_machine' poweroff" >> ".\Downloads\$challenge_id\stop.ps1"
}

if ($args.Length -eq 2) {
    $download_link = $args[0]
    $challenge_id = $args[1]

    Invoke-WebRequest -URI http://localhost:5000$download_link -OutFile ./Downloads/$challenge_id.zip -UseBasicParsing -UseDefaultCredential
    
    $file_parts = "./Downloads/$challenge_id.zip"
    $extension = $file_parts[$file_parts.Length -1]
    $temp_path = "$challenge_id"+"_temp"

    Expand-Archive "./Downloads/$challenge_id.zip" -DestinationPath "./Downloads/$temp_path"
    mv "./Downloads/$temp_path/static/Challenges/$challenge_id" "./Downloads/$challenge_id"
    Remove-Item "./Downloads/$temp_path" -Recurse
    rm "./Downloads/$challenge_id.zip"

    $files = dir "./Downloads/$challenge_id/build"
    $files = $files -replace '\s+'
    $files = $files.Split("`n")

    # Create new start and stop files, output IP reset file and reset lesson file.
    New-Item -Path ".\Downloads\$challenge_id\start.ps1" -ItemType File
    echo "New-Item -Path '$($pwd.Path)\VM_Shared\ips.txt' -ItemType File -Force" >> ".\Downloads\$challenge_id\start.ps1"
    echo "if (Test-Path '.\VM_Shared\lesson.json') { rm '.\VM_Shared\lesson.json'}" >> ".\Downloads\$challenge_id\start.ps1"
    echo "if (Test-Path '.\Downloads\$challenge_id\lesson.json') { cp '.\Downloads\$challenge_id\lesson.json' '.\VM_Shared\lesson.json' }" >> ".\Downloads\$challenge_id\start.ps1"
    New-Item -Path ".\Downloads\$challenge_id\stop.ps1" -ItemType File

    for ($i = 0; $i -lt $files.Count; $i++) {
        $temp_ext = $files[$i].Split(".")[$files[$i].Split(".").Count - 1]

        if ($temp_ext -eq "vdi" -Or $temp_ext -eq "vmdk" -Or $temp_ext -eq "iso") {
            Setup-VBOX $files[$i] $challenge_id $files[$i].Split(".")[0]
        } elseif ($temp_ext -eq "zip") {
            Setup-Docker $files[$i] $challenge_id $files[$i].Split(".")[0]
        }
    }

    Setup-Attackers-Machine

    # Check this is working
    if ($has_docker_files -eq 1) {
        echo 'Remove-Job -State "Completed"' >> ".\Downloads\$challenge_id\stop.ps1"
    }

    rmdir "./Downloads/$challenge_id/build"
}