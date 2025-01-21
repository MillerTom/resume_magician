import os
import sys
import logging
import socket
import subprocess
import platform
import threading
import requests

# THIS IS INTENDED SOLELY FOR RUNNING IN DEV ENVIRONMENT
# This script is designed to help set up the development environment by:
# - Checking for conflicts with the default ports used by React (3000) and Django (8000).
# - Setting up virtual environments, building React app, running Django migrations, and starting both apps.
# Ensure that you are running this script in a development environment only.

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Directories for the project
base_dir = os.getcwd()
venv_dir = os.path.join(base_dir, 'server', 'venv')
start_react_dir = os.path.join(base_dir, 'client', 'build')
start_django_dir = os.path.join(base_dir, 'server', 'manage.py')

# Default ports for React and Django
REACT_PORT = 3000
DJANGO_PORT = 8000

def check_port_in_use(port):
    """Check if a given port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            return result == 0
        except socket.error as e:
            logging.error(f"Error checking port {port}: {e}")
            return False

def find_free_port(start_port):
    """Find a free port by incrementing the port number."""
    port = start_port
    while check_port_in_use(port):
        logging.log(logging.CRITICAL, f"Port {port} is already in use. Trying the next available port.")
        port += 1
        if port > 65000:
            logging.critical(f"ERROR: Unable to find a free port after trying many. Please check port usage or your environment.")
            sys.exit(1)
    logging.info(f"Found a free port: {port}")
    return port

def run_subprocess(command, check=True):
    """Run a subprocess command."""
    logging.debug(f"Running command: {command}")
    try:
        command_list = command.split()
        subprocess.run(command_list, check=check)
    except subprocess.CalledProcessError as e:
        logging.critical(f"ERROR: Command failed: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logging.critical(f"ERROR: Command not found: {e}")
        sys.exit(1)

def run_subprocess_async(command):
    """Run a subprocess command asynchronously."""
    def run_command(command):
        logging.debug(f"Running command asynchronously: {command}")
        try:
            command_list = command.split()
            subprocess.Popen(command_list)
        except Exception as e:
            logging.error(f"Error starting command asynchronously: {e}")

    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()

def build_react_app():
    """Build the React app"""
    logging.info("Building React app...")

    # Define the directory for React app build
    react_dir = os.path.join(base_dir, 'client')

    # Check platform and adjust command accordingly
    system_info = platform.system()

    if system_info == 'Windows':
        # For Windows, use PowerShell to run the commands
        try:
            # Run 'npm install' and 'npm run build' using PowerShell
            run_subprocess(f'powershell -Command "cd {react_dir} && npm install"')  # Ensure dependencies are installed
            run_subprocess(f'powershell -Command "cd {react_dir} && npm run build"')  # Build the app
        except Exception as e:
            logging.critical(f"ERROR: React build failed on Windows: {e}")
            sys.exit(1)
    else:
        # For other platforms (Linux/macOS), run directly in the terminal
        try:
            # Run 'npm install' and 'npm run build' in the React directory directly
            run_subprocess(f'cd {react_dir} && npm install')  # Ensure dependencies are installed
            run_subprocess(f'cd {react_dir} && npm run build')  # Build the app
        except Exception as e:
            logging.critical(f"ERROR: React build failed on {system_info}: {e}")
            sys.exit(1)

    logging.info("React build completed.")

# Example call to the function (assuming base_dir is set)
base_dir = os.getcwd()  # Make sure to define your base directory
build_react_app()
def setup_virtualenv():
    """Set up the Python virtual environment."""
    logging.info("Setting up Python virtual environment...")
    if not os.path.exists(venv_dir):
        python_executable = sys.executable
        try:
            run_subprocess(f'{python_executable} -m venv server/venv')
        except Exception as e:
            logging.critical(f"ERROR: Failed to create virtual environment: {e}")
            sys.exit(1)
    else:
        logging.info("Virtual environment already exists. Skipping setup.")

def run_django_migrations():
    """Run Django database migrations."""
    logging.info("Running Django migrations...")
    system_info = platform.system()
    python_command = os.path.join(venv_dir, 'Scripts' if system_info == 'Windows' else 'bin', 'python')
    try:
        run_subprocess(f'python manage.py migrate')
    except Exception as e:
        logging.critical(f"ERROR: Django migrations failed: {e}")
        sys.exit(1)

def start_react_app(free_port):
    """Start the React app."""
    logging.info(f"Starting React app on port {free_port}...")
    react_start_command = f'npm start --port {free_port}'  # You may want to adjust this command if needed
    try:
        run_subprocess(f'cd {base_dir}/client && {react_start_command}')
    except Exception as e:
        logging.critical(f"ERROR: React app failed to start: {e}")
        sys.exit(1)

def start_django_app():
    """Start the Django application."""
    logging.info("Starting Django app...")
    system_info = platform.system()
    python_command = os.path.join(venv_dir, 'Scripts' if system_info == 'Windows' else 'bin', 'python')
    try:
        run_subprocess(f'python runserver')
    except Exception as e:
        logging.critical(f"ERROR: Django app failed to start: {e}")
        sys.exit(1)

def test_servers(free_port):
    """Test if the servers are running by making HTTP requests."""
    logging.info(f"Testing React app on port {free_port}...")
    try:
        react_test_url = f'http://127.0.0.1:{free_port}'
        response = requests.get(react_test_url)
        if response.status_code == 200:
            logging.info(f"React app is successfully running at {react_test_url}")
        else:
            logging.warning(f"React app returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        logging.critical(f"ERROR: React app is not running. Could not connect to {react_test_url}. Exception: {e}")
    
    logging.info("Testing Django app on port 8000...")
    try:
        django_test_url = 'http://127.0.0.1:8000'
        response = requests.get(django_test_url)
        if response.status_code == 200:
            logging.info(f"Django app is successfully running at {django_test_url}")
        else:
            logging.warning(f"Django app returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        logging.critical(f"ERROR: Django app is not running. Could not connect to {django_test_url}. Exception: {e}")

def main():
    """Main setup function to orchestrate the entire setup process."""
    # Console warning that this is for dev environment
    logging.info("THIS IS INTENDED SOLELY FOR RUNNING IN DEV ENVIRONMENT")
    print("\n** THIS IS INTENDED SOLELY FOR RUNNING IN DEV ENVIRONMENT **\n")
    
    logging.info("Starting setup process...")

    # Check if React or Django ports are in use before starting the servers
    if check_port_in_use(REACT_PORT):
        logging.critical(f"ERROR: Port {REACT_PORT} (React app) is already in use. Please resolve the issue.")
        logging.critical("To fix this, either stop the service using port 3000, or modify the port used by React in your 'package.json'.")
        sys.exit(1)

    if check_port_in_use(DJANGO_PORT):
        logging.critical(f"ERROR: Port {DJANGO_PORT} (Django app) is already in use. Please resolve the issue.")
        logging.critical("To fix this, either stop the service using port 8000, or modify the port used by Django in your settings.py.")
        sys.exit(1)

    # Setup virtual environment (if not already done)
    setup_virtualenv()

    # Build React app
    build_react_app()

    # Run Django migrations
    run_django_migrations()

    # Find a free port for React app (but only if the default port is in use)
    react_port = find_free_port(REACT_PORT)  # React uses port 3000 by default
    django_port = DJANGO_PORT  # Django uses port 8000 by default

    # Start React app and Django app in parallel
    thread_react = threading.Thread(target=start_react_app, args=(react_port,))
    thread_django = threading.Thread(target=start_django_app)
    
    thread_react.start()
    thread_django.start()

    # Test the servers after starting them
    test_servers(react_port)

    # Instructions to user on how to verify setup
    logging.info(f"Setup is complete. To verify the setup:")
    logging.info(f"1. Open a browser and navigate to http://127.0.0.1:{react_port}. You should see your React app running.")
    logging.info(f"2. Open a browser and navigate to http://127.0.0.1:{django_port}. You should see your Django app running.")
    logging.info("If both apps are running and you see the expected pages, everything is set up correctly.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Setup interrupted by user. Terminating...")
        sys
