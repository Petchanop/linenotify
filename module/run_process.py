import os
import sys
import subprocess

if __name__ == "__main__":

    try:
        token = sys.argv[1]
        path = sys.argv[2]
        splitPath = path.split("/")
        if len(splitPath) > 1:
            joinPath = '@'.join([splitPath[-2], splitPath[-1]])
        else:
            joinPath = '@'.join(splitPath)
        name = sys.argv[3] + joinPath
    except Exception as err:
        print(err)
        
    workdir = os.getcwd()
    workdir = workdir + "\\module"
    subprocess.run("powershell Write-output Y | powershell.exe Set-ExecutionPolicy -ExecutionPolicy RemoteSigned")
    subprocess.run("powershell Unblock-File -Path .\\AutoConfig.ps1")
    subprocess.run(f"powershell .\\AutoConfig.ps1 {name} {token} {path} {workdir} &", shell=True) 