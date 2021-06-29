"""This script sets up the local and RPI0 enivroments.

To run this script, issue the command:

python3 ./workspace_setup.py <network drive>

"""
import sys 
import os
import subprocess
import json 
import sysconfig


curdir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def main():
    if len(sys.argv) != 2:
        print('Must provide network drive as argument')
        sys.exit(-1)

    network_drive = sys.argv[1]
    network_drive = network_drive.replace('\\', '/')
    if network_drive.endswith('/'):
        network_drive = network_drive[:-1]

    # Install dirsync into the local environment
    # https://pypi.org/project/dirsync/
    # We use this to sync the local workspace with the RPI0 workspace
    install_pip_package('dirsync')

    # List the network drive to ensure it is readable
    try:
        os.listdir(network_drive)
    except Exception as e:
        print(f'Failed to read network drive: {network_drive}, err: {e}')
        sys.exit(-1)

    # Update the tasks.json
    # with the given network drive
    tasks_path = f'{curdir}/.vscode/tasks.json'
    with open(tasks_path, 'r') as fp:
        tasks = json.load(fp)

    for task in tasks['tasks']:
        if task['label'] == 'sync-workspace':
            task['args'][1] = f'{network_drive}/home/pi/rpi0_tflite_picamera'
            print(f'Updating {tasks_path} with network drive: {network_drive}')
            with open(tasks_path, 'w') as fp:
                json.dump(tasks, fp, indent=2)
            break

    # Ensure the "plink" command is locally available
    try:
        issue_shell_command('plink', '-V')
    except Exception as e:
        print(f'"plink" command not found. Ensure it is installed locally')
        sys.exit(-1)

    # Run the setup script on the RPI0
    issue_shell_command(
        'plink', '-batch', 
        '-pw', 'raspberry', 'pi@raspberrypi.local', 
        '-m',f'{curdir}/setup_rpi0.sh'
    )

    # Create the file rpi0_tflite_camera.pth:
    # In the local site-packages directory
    # This file contains paths to the RPI0 Python packages
    # This allows the local Python indexer to find packages
    # on the RPI0
    # More details about the .pth file here:
    # https://docs.python.org/3/library/site.html
    site_packages_dir = sysconfig.get_paths()['purelib'].replace('\\', '/')

    rpi0_tflite_camera_pth_path = f'{site_packages_dir}/rpi0_tflite_camera.pth'
    print(f'Creating {rpi0_tflite_camera_pth_path}')
    with open(rpi0_tflite_camera_pth_path, 'w') as fp:
        fp.write(f'{network_drive}/home/pi/.local/lib/python3.7/site-packages\n')
        fp.write(f'{network_drive}/usr/lib/python3/dist-packages')







def install_pip_package(package):
    issue_shell_command(sys.executable, "-m", "pip", "install", package)


def issue_shell_command(*args):
    print(' '.join(args))
    p = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)
    retval = p.wait()
    if retval != 0:
        sys.exit(retval)

if __name__ == '__main__':
    main()