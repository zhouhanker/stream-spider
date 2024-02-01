import subprocess


def generate_env_file():
	try:
		result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True, check=True)
		print(result.stdout)
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}")
		print(e.stdout)


def install_py_lib():
	try:
		result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True, check=True)
		print(result.stdout)
		print('Installation completed successfully ....')
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}")
		print(e.stdout)


if __name__ == '__main__':
	# generate_env_file()
	install_py_lib()
	