import os
import csv

import pandas as pd

folder_path = "./csvFile/"


def parse_files_csv():
	csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
	for file in csv_files:
		file_path = os.path.join(folder_path, file)
		with open(file_path, 'r', newline='') as csvfile:
			csv_reader = csv.reader(csvfile)
			data = list(csv_reader)
			label_name = data[0][0].split(" ")[1].split("(")[0]
			data = data[2:]
			for row in data:
				row[:] = [row[6]]
				row.insert(1, label_name)
		
		with open(file_path, 'w', newline='') as csvfile:
			csv_writer = csv.writer(csvfile)
			csv_writer.writerows(data)
	print('文件格式化完成 ...')
	

def data_file_deduplication():
	file_list = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
	for file in file_list:
		file_path = os.path.join(folder_path, file)
		# 读取CSV文件
		df = pd.read_csv(file_path)
		# 去重
		df = df.drop_duplicates()
		# 将去重后的数据写回CSV文件
		df.to_csv(file_path, index=False)
		print(f"{file} 去重完成")
	

if __name__ == '__main__':
	parse_files_csv()
	data_file_deduplication()
