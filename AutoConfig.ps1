param ([string]$name = $argvs[0], [string]$token = $args[1], [string]$path = $args[2], [string]$workDir=$args[3])
[string]$pythonPath =  Get-Command -Name "pythonw" | Select-Object -ExpandProperty Source
$setting = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0
[string]$taskPath = $workdir.Substring(2)

Write-Host "Build task Scheduled in" $taskPath
Write-Host "Task Name:" $name
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "file_monitoring.py $token $path" -WorkingDirectory "$workDir"
Write-Debug $action
$trigger = New-ScheduledTaskTrigger -AtLogon
Write-Debug $trigger
Register-ScheduledTask -Action $action -Trigger $trigger -TaskPath "$taskPath" -TaskName "$name" -Settings $setting
Start-ScheduledTask -TaskPath $taskPath -TaskName "$name"
Get-ScheduledTask -TaskPath "$taskPath\"