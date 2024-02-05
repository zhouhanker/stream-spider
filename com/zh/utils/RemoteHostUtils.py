import paramiko

from com.zh.label.config import config


class RemoteHostUtils:
	
	@staticmethod
	def inspect_remote_file(remote_host, dir_path):
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		try:
			
			ssh_client.connect(remote_host, port=22, username=config.remote_user_name, password=config.remote_user_password)
			sftp_client = ssh_client.open_sftp()
			directory_items = sftp_client.listdir(dir_path)
			
			return directory_items
		
		finally:
			ssh_client.close()
