function Setup-VBOX($vbox_file, $challenge_id, $filename) {
    .\setup_vbox.ps1 ".\Downloads\$challenge_id\$vbox_file" "$challenge_id $filename"
}

function Setup-Docker($docker_zip) {

}

if ($args.Length -eq 2) {
    $download_link = $args[0]
    $challenge_id = $args[1]

    Invoke-WebRequest -URI http://localhost:5000$download_link -OutFile ./Downloads/$challenge_id.zip -UseBasicParsing -UseDefaultCredential
    
    $file_parts = "./Downloads/$challenge_id.zip"
    $extension = $file_parts[$file_parts.Length -1]
    $temp_path = "$challenge_id"+"_temp"

    Expand-Archive "./Downloads/$challenge_id.zip" -DestinationPath "./Downloads/$temp_path"
    mv "./Downloads/$temp_path/static/Challenges/$challenge_id/build" "./Downloads/$challenge_id"
    Remove-Item "./Downloads/$temp_path" -Recurse
    rm "./Downloads/$challenge_id.zip"

    $files = dir "./Downloads/$challenge_id"
    $files = $files -replace '\s+'
    $files = $files.Split("`n")

    echo $files
    echo $files.Count

    for ($i = 0; $i -lt $files.Count; $i++) {
        $temp_ext = $files[$i].Split(".")[$files[$i].Split(".").Count - 1]

        if ($temp_ext -eq "vdi" -Or $temp_ext -eq "vmdk" -Or $temp_ext -eq "iso") {
            Setup-VBOX $files[$i] $challenge_id $files[$i].Split(".")[0]
        }
    }
}