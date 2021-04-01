if ($args.Length -eq 1) {
    $machine = $args[0]
    $vm_ip_info = $(VBoxManage guestproperty get "$machine" '/VirtualBox/GuestInfo/Net/0/V4/IP')
    echo $vm_ip_info
    $final_addr_info =  $([int]$vm_ip_info.split(".")[-1] -1)
    echo "VM : 10.10.10.$final_addr_info" >> './VM_Shared/ips.txt'
}