if ($args.Count -eq 1) {
    $challenge_id = $args[0]
    $vms = $(VBoxManage list vms)
    $vm = $($vms -match "`"$challenge_id")
    $vm_name = $($vm -match "`"(.*)`"" | Out-Null; $Matches[1])
    VBoxManage unregistervm "$vm_name" -delete
}