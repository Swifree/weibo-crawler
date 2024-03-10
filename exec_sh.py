import subprocess


def exec_sh(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)  # ignore_security_alert
    out, err = process.communicate()

    if process.returncode == 0:
        print('Command successfully executed!\n')
        res = out.decode('UTF-8')
        print('Output: ' + res)
        return res
    else:
        print('Command failed. Return code :', process.returncode)
        print('Error: ' + err.decode('UTF-8'))
        return None
