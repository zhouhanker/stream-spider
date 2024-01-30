import math
import os.path
import random
import time
import timeit

import requests
import re
import csv
import pandas as pd
from colorama import Fore
from lxml import html
from pyspark.python.pyspark.shell import sc

from com.zh.label.config import config
from com.zh.utils.FileUtils import get_user_agent
from datetime import datetime
from pyspark.sql import session, SparkSession
from com.zh.utils.SeleniumUtils import seleniumUtils

s = 'https://bscscan.com/accounts/label/bitcoin-pegged'
limit_page = math.ceil(727 / 100)
print(limit_page)
limit = 100
for i in range(1, limit_page + 1):
	new_url = s+f'?subcatid=undefined&size={limit}&start=0&col=1&order=asc'
	print(new_url)
	limit += 100


