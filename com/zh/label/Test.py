import time

import requests
import pandas as pd
from colorama import Fore
from tqdm import tqdm

custom_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"

li = tqdm(range(100), desc='test', ncols=100, ascii=True)

for i in li:
	time.sleep(0.3)
	li.set_postfix({'url': i})
	
# tqdm.write('当前i={}'.format(i))
