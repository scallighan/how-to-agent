
# 2025ignite.json sourced from https://api-v2.ignite.microsoft.com/api/session/all/en-US

# I want to take the 2025ignite.json file and convert each session into a json file with the following format:
# {
#    "id": "sessionCode",
#    "title": "title",
#    "link": "https://ignite.microsoft.com/en-US/sessions/{sessionCode}",
#    "speakers": "speakerNames",
#    "description": "description",
#    "transcription": "aiDescription"
# }
import json
import os

def convert_sessions_to_json(input_file, output_folder):
    with open(input_file, 'r') as f:
        data = json.load(f)

    sessions = data
    
    for session in sessions:
        session_code = session.get('sessionCode', '')
        title = session.get('title', '')
        link = f"https://ignite.microsoft.com/en-US/sessions/{session_code}"
        speakers = session.get('speakerNames', '')
        description = session.get('description', '')
        ai_description = session.get('aiDescription', '')
        onDemand = session.get('onDemand', '')

        session_data = {
            "id": session_code,
            "title": title,
            "link": link,
            "speakers": speakers,
            "description": description,
            "transcription": ai_description,
            "onDemand": onDemand
        }

        output_file = os.path.join(output_folder, f"{session_code}.json")
        with open(output_file, 'w') as out_f:
            json.dump(session_data, out_f, indent=4)


# upload the sessions_json to an Azure Storage Account container called "search" in the directory "2025-Ignite"
from azure.storage.blob import BlobServiceClient
import os
from azure.identity import DefaultAzureCredential

def upload_sessions_to_blob_storage(container_name, local_folder):
    STORAGE_ACCOUNT_NAME = "sahowtolghosarxwus3"
    blob_service_client = BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=DefaultAzureCredential())

    container_client = blob_service_client.get_container_client(container_name)

    for filename in os.listdir(local_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(local_folder, filename)
            blob_name = f"2025-Ignite/{filename}"
            with open(file_path, 'rb') as data:
                container_client.upload_blob(name=blob_name, data=data, overwrite=True)
                print(f"Uploaded {filename} to blob storage as {blob_name}")

if __name__ == "__main__":
    input_file = 'data/2025ignite.json'  # Path to the input JSON file
    output_folder = 'sessions_json'  # Folder to save the output JSON files

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    convert_sessions_to_json(input_file, output_folder)
    upload_sessions_to_blob_storage('search', output_folder)


