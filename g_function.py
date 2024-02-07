from google.oauth2 import service_account
from googleapiclient import discovery


def get_gcloud_client(c_path):
    credentials = service_account.Credentials.from_service_account_file(
        c_path,  # 替换成您的服务帐户密钥文件路径
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    return discovery.build("compute", "v1", credentials=credentials)


def create_instance(client, project_id, name, zone, email):
    request_body = {
        "name": name,
        "machineType": f"projects/{project_id}/zones/{zone}/machineTypes/e2-micro",
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": "projects/debian-cloud/global/images/debian-12-bookworm-v20240110",
                    "diskSizeGb": "10",
                    "diskType": f"projects/{project_id}/zones/{zone}/diskTypes/pd-balanced",
                },
            }
        ],
        "networkInterfaces": [
            {
                "network": f"projects/{project_id}/global/networks/default",
                "accessConfigs": [{"name": "External NAT", "type": "ONE_TO_ONE_NAT"}],
                "networkTier": "PREMIUM",
                "stackType": "IPV4_ONLY",
                "subnet": f"projects/{project_id}/regions/{zone.split('-')[0]}/subnetworks/default",
            }
        ],
        "noRestartOnFailure": True,
        "maintenancePolicy": "TERMINATE",
        "provisioningModel": "SPOT",
        "instanceTerminationAction": "STOP",
        "serviceAccounts": [
            {
                "email": email,
                "scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/trace.append",
                ],
            }
        ],
        "labels": {"goog-ec-src": "vm_add-gcloud"},
        "reservationAffinity": {"consumeReservationType": "ANY_RESERVATION"},
        "shieldedInstanceConfig": {
            "enableSecureBoot": False,
            "enableVtpm": True,
            "enableIntegrityMonitoring": True,
        },
    }

    client.instances().insert(
        project=project_id, zone=zone, body=request_body
    ).execute()


def get_instances(client, project_id, zone):
    return client.instances().list(project=project_id, zone=zone).execute()
