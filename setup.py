import subprocess
import platform
import sys
import os
import threading

args = sys.argv
run_type = None
if(len(args) >  1):
    if args[1] == 'local':
        run_type = args[1]
        sys.argv.pop(1)

python_executable = sys.executable
system_info = platform.system()
base_dir = os.getcwd()
venv_dir = os.path.join(base_dir, 'server', 'venv')
print(python_executable)
print(system_info)
print(base_dir)

def run_subprocess(command):
    command_list = command.split()
    subprocess.run(command_list, check=True)

def run_subprocess_async(command):
    def run_command(command):
        command_list = command.split()
        subprocess.Popen(command_list)
    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()

# Setup virtualenv
run_subprocess(f'{python_executable} -m venv server/venv')

# Install packages
if system_info == 'Windows':
    pip_command = os.path.join(venv_dir, 'Scripts', 'pip')
else:
    pip_command = os.path.join(venv_dir, 'bin', 'pip')
run_subprocess(f'{pip_command} install -r server/requirements.txt')

if system_info == 'Windows':
    python_command = os.path.join(venv_dir, 'Scripts', 'python')
else:
    python_command = os.path.join(venv_dir, 'bin', 'python')

# DB migrations
if system_info == 'Windows':
    python_command = os.path.join(venv_dir, 'Scripts', 'python')
else:
    python_command = os.path.join(venv_dir, 'bin', 'python')
start_django_dir = os.path.join(base_dir, 'server', 'manage.py')
if run_type != None:
    run_subprocess(f'{python_command} {start_django_dir} migrate {run_type}')
else:
    run_subprocess(f'{python_command} {start_django_dir} migrate')

# Start React app
start_react_dir = os.path.join(base_dir, 'client', 'build')
sudo_prefix = ''
if system_info != 'Windows': sudo_prefix = 'sudo '
run_subprocess_async(f'{sudo_prefix}{python_command} -m http.server 80 --directory {start_react_dir}')

# Start Django
start_django_dir = os.path.join(base_dir, 'server', 'manage.py')
if run_type != None:
    run_subprocess(f'{python_command} {start_django_dir} runserver {run_type}')
else:
    run_subprocess(f'{python_command} {start_django_dir} runserver')