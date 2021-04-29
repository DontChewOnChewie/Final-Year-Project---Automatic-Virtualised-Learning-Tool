# Self-elevate the script if required (https://blog.expta.com/2017/03/how-to-self-elevate-powershell-script.html)
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
 if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
  $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
  Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine
  Exit
 }
}

# --- Network Setup --- #

[System.Collections.ArrayList]$orig_connections = @()
$kali_machine_name = $($(cat config.json) | ConvertFrom-Json).default_machine
$nat_network = $($(cat config.json) | ConvertFrom-Json).nat_network_name
$added_connection = ""

# https://stackoverflow.com/questions/10042354/how-to-get-local-area-connection-name-with-batch-script-in-windows-7
$original_connections_data = $(wmic nic where "netconnectionid like '%'" get netconnectionid)

# Start at 1 to skip header.
for ($i = 1; $i -lt $original_connections_data.Count; $i++) {
    if ($original_connections_data[$i] -ne "") {
        $orig_connections.Add($original_connections_data[$i].Trim()) | Out-Null
    } 
}

VBoxManage hostonlyif create
$created_interface = $(VBoxManage list hostonlyifs).Split("`n")[0].Split(":")[1].Trim()
VBoxManage hostonlyif ipconfig "$created_interface" --ip 172.100.100.1
VBoxManage dhcpserver add --interface "$created_interface" --lowerip 172.100.100.2 --upperip 172.100.100.254 --server-ip 172.100.100.100 --netmask 255.255.255.0
VBoxManage dhcpserver modify --ifname "$created_interface" --enable

$final_connections_data = $(wmic nic where "netconnectionid like '%'" get netconnectionid)

for ($i = 1; $i -lt $final_connections_data.Count; $i++) {
    if ($final_connections_data[$i] -ne "") {
        if ($final_connections_data[$i].Trim() -in $orig_connections) {continue}
            
        $added_connection = $final_connections_data[$i].Trim()
        break
    }
}

# https://techdiip.com/how-to-disable-lan-connection/
netsh interface set interface name="$added_connection" admin=DISABLED
netsh interface set interface name="$added_connection" admin=ENABLED


# Create NAT Network
VBoxManage natnetwork add --netname $nat_network --network "10.10.10.0/24" --dhcp on --enable

# Setup bundled Kali machine.
VBoxManage modifyvm $kali_machine_name --nic1 hostonly
VBoxManage modifyvm $kali_machine_name --hostonlyadapter1 "$added_connection"
VBoxManage modifyvm $kali_machine_name --nic2 natnetwork
VBoxManage modifyvm $kali_machine_name --nat-network2 $nat_network





