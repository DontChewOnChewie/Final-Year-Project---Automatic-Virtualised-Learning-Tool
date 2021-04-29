$nat_network = $($(cat config.json) | ConvertFrom-Json).nat_network_name

function ISO_Setup ($img_file, $vm_name) {
    VBoxManage createvm --name $vm_name --ostype "Other_64" --register

    VBoxManage storagectl $vm_name --name "IDE Controller" --add ide --controller PIIX4       
    VBoxManage storageattach $vm_name --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium $img_file      
    VBoxManage modifyvm $vm_name --boot1 dvd --boot2 disk --boot3 none --boot4 none 
    VBoxManage modifyvm $vm_name --nic1 natnetwork
    VBoxManage modifyvm $vm_name --nat-network1 $nat_network
}

function VDI_Setup($img_file, $vm_name) {
    VBoxManage createvm --name $vm_name --ostype "Other_64" --register

    VBoxManage storagectl $vm_name --name "SATA Controller" --add sata --controller IntelAHCI
    VBoxManage storageattach $vm_name --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium $img_file
    VBoxManage modifyvm $vm_name --nic1 natnetwork
    VBoxManage modifyvm $vm_name --nat-network1 $nat_network
}

function VMKD_Setup($img_file, $vm_name) {
    $challenge_id = $vm_name.Split(" ")[0]
    $vdi_name = $vm_name.Split(" ")[1]
    VBoxManage createvm --name $vm_name --ostype "Other_64" --register

    VBoxManage clonehd --format VDI $img_file ".\Downloads\$challenge_id\$vdi_name.vdi"
    VBoxManage storagectl $vm_name --name "SATA Controller" --add sata --controller IntelAHCI
    VBoxManage storageattach $vm_name --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium ".\Downloads\$challenge_id\$vdi_name.vdi"
    VBoxManage modifyvm $vm_name --nic1 natnetwork
    VBoxManage modifyvm $vm_name --nat-network1 $nat_network
}

echo $args
if ($args.Length -eq 2) {
    $img = $args[0]
    $vm_name = $args[1]
    $extension = ($img.Split(".")[$img.Split(".").Count - 1])
    
    switch ($extension) {
        'vmdk' {
            VMKD_Setup $img $vm_name; break;
        }
        'vdi' {
            VDI_Setup $img $vm_name; break;
        }
        'iso' {
            ISO_Setup $img $vm_name; break;
        }
        default {
            "Unsupported file type ($extension)."; break;
        }
    }

} else {
    echo "Image file not given."
}

#VBoxManage createhd --filename "C:\Users\Oliver\VirtualBox VMs\TEST\$vm.vdi" --size 16384 --format vdi
