from g_function import get_gcloud_client
from zones import zone_list, all_zone_list
import paramiko

project_id = "clean-mason-413611"


target_instances = []
ip_list = []

if __name__ == "__main__":
    client = get_gcloud_client("credentials/clean-mason-413611-bf3888dd46a3.json")

    for zone in zone_list:
        print(zone)
        instances = client.instances().list(project=project_id, zone=zone).execute()
        if "items" not in instances:
            print("empty")
            continue
        for its in instances["items"]:
            if its["name"].startswith("instance"):
                print("skip")
                continue
            ip = its["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
            ip_list.append(ip)

    print(ip_list)
    port = 22
    username = "tinghsu"
    key_path = "/Users/tinghsu/.ssh/google_compute_engine"
    for ip in ip_list:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=key_path)
        ssh_client.connect(ip, port, username, pkey=private_key)

        local_script = "/Users/tinghsu/git/gcloud/run.sh"
        remote_script = "/home/tinghsu/run.sh"

        sftp = ssh_client.open_sftp()
        try:
            sftp.put(local_script, remote_script)
            print(f"File {local_script} successfully uploaded to {remote_script}")
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
        # sftp.put(local_script, remote_script)
        sftp.close()

        commands = [
            f"bash {remote_script}",
        ]

        # Execute the commands with a delay between each command
        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")
            print(f"Command: {command}\nOutput:\n{output}")

        ssh_client.close()
