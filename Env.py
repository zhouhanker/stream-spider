import subprocess

from tqdm import tqdm


def generate_env_file():
	result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
	with open('requirements.txt', 'w') as requirements_file, tqdm(total=len(result.stdout.splitlines()),
																  bar_format="{l_bar}{bar:40}{r_bar}", ncols=100,
																  desc='Generate req', ascii=True) as pbar:
		for line in result.stdout.splitlines():
			requirements_file.write(line + '\n')
			pbar.update(1)


def install_py_lib():
	try:
		result = subprocess.run(
			['pip', 'install', '-r', 'requirements.txt'],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			check=True,
			encoding='utf-8')
		for line in tqdm(result.stdout.splitlines(), desc='Installing', ncols=100, ascii=True):
			pass
		print('Installation completed successfully ....')
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}")
		print(e.stdout)


if __name__ == '__main__':
	# generate_env_file()
	install_py_lib()
	