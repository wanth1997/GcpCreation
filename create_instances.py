from google.oauth2 import service_account
from googleapiclient import discovery
from g_function import *
from zones import all_zone_list, zone_list
from time import sleep


# 定义实例的配置
project_id = "poetic-brace-413612"
image = "projects/debian-cloud/global/images/debian-12-bookworm-v20240110"
client = get_gcloud_client("credentials/poetic-brace-413612-a5d7805d8a92.json")
email = "783400911269-compute@developer.gserviceaccount.com"

for zone in zone_list:
    print(zone)
    instances = get_instances(client, project_id, zone)
    if "items" not in instances:
        count = 1
    else:
        count = len(instances["items"]) + 1
    if count > 3:
        print("Too many, skip")

    while count <= 3:
        name = f"{zone}-{count}"

        resp = create_instance(
            client,
            project_id,
            name,
            zone,
            email,
        )
        print(resp)
        count += 1
        sleep(1)
