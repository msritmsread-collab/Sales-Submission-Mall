import paramiko,os

class SFTPClient:
    def __init__(self, hostname, port, username, password):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.sftp_client = None

    def connect(self):
        try:
            self.ssh_client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            self.sftp_client = self.ssh_client.open_sftp()
            print("Connection Success")
        except Exception as e:
            print(f"Connection failed: {e}")

    def send_file(self, local_path, remote_path, file_name):
        try:
            local_file_path = os.path.join(local_path,file_name)
            remote_file_path = remote_path+'/'+file_name
            self.sftp_client.put(local_file_path, remote_file_path)
            # print(local_file_path,'\n',remote_file_path)
            print(f"File '{file_name}' sent successfully.")
        except Exception as e:
            print(f"Error sending file '{file_name}': {e}")

    def send_files(self, local_path, remote_path, file_list):
        try:
            for file_name in file_list:
                self.send_file(local_path, remote_path, file_name)
            print("All files sent successfully.")
        except Exception as e:
            print(f"Error sending files: {e}")

    def list_files(self, remote_path):
        try:
            files = self.sftp_client.listdir(remote_path)
            # print(f"Files in {remote_path}:")
            # for file_name in files:
            #     print(file_name)
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def close(self):
        if self.sftp_client:
            self.sftp_client.close()
        if self.ssh_client:
            self.ssh_client.close()