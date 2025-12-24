import sys
import subprocess
import glob
import os

def uploadFile(file_name):
    global serial_port
    print("Uploading file ", file_name)
    try :
        result = subprocess.run(["ampy", "--port", serial_port, "put", file_name])
        if result.stdout != None:
            print("STDOUT:", result.stdout)
        if  result.stderr != None:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print("ERROR\n")
        return (result.returncode == 0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("Error output:", e.stderr)
    return False
    
def uploadProject(proj_folder, cmn_folder, temp_folder, wifi_name, wifi_passwd, pw_ip, exclude_boot):
    global serial_port
    files_to_upload = glob.glob(cmn_folder + "/*.py")
    for f in files_to_upload:
        if not uploadFile(f):
            return False
    
    files_to_upload = glob.glob(proj_folder + "/*.py")
    boot_file = None
    for f in files_to_upload:
        if exclude_boot and f.endswith("/boot.py"):
            boot_file = f
            continue
        if not uploadFile(f):
            return False

    if not uploadFile(proj_folder + "/settings.txt"):
        return False
    
    configFileTemplate = proj_folder + "/config.txt"
    configFile = temp_folder + "/config.txt"
    content = ""
    try:
        with open(configFileTemplate, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{configFileTemplate}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for file '{configFileTemplate}'.")

    content = content.replace("<wifi>", wifi_name)
    content = content.replace("<wifi password>", wifi_passwd)
    content = content.replace("<pw_ip>", pw_ip)

    os.makedirs(temp_folder, exist_ok=True)
    f = open(configFile, 'w')
    if f == None:
        print(f"Error: Can't write to file '{configFile}'.")
        return False
    f.write(content)
    f.close()

    if not uploadFile(configFile):
        return False

    if boot_file != None:
        print("command to run board is: ampy --port " + serial_port + " run " + boot_file)     

    return True

param_count = len(sys.argv)
if param_count != 8 and param_count != 9 or param_count == 9 and sys.argv[8] != "exclude_boot":
    print("upload_proj.py <project folder> <common folder> <serial port> <temp folder> <wifi name> <wifi password> <PW IP> [exclude_boot]")
    exit(1)


serial_port = sys.argv[3]

uploadProject(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5], sys.argv[6], param_count == 8)




