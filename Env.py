import subprocess


def install_py_lib():
	try:
		result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True, check=True)
		print(result.stdout)
		print('Installation completed successfully ....')
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}")
		print(e.stdout)


if __name__ == '__main__':
	
	install_py_lib()
	