import random


def get_user_agent(path):
	uas = []
	with open(path, 'rb') as uaf:
		for ua in uaf.readlines():
			if ua:
				uas.append(ua.strip()[:-1])
	random.shuffle(uas)
	ua = random.choice(uas)
	return ua.decode('utf-8')[1:].strip()


if __name__ == '__main__':
	pass
