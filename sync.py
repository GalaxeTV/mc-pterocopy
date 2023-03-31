"""_summary_ Sync files from production server to staging server using FTP and the Pterodactyl API
"""

import os
import sys
import time
import requests
from dotenv import dotenv_values
from pydactyl import PterodactylClient

# Load environment variables
env = dotenv_values(".env")

# Pterodactyl API
staging_server = env.get("STAGING_SERVER")
staging_api_key = env.get("STAGING_API_KEY")
api = PterodactylClient(staging_server, staging_api_key)
server = api.client.servers.list_servers()[0]['attributes']['identifier']

# FTP
production_server = env.get("PRODUCTION_SERVER")
production_username = env.get("PRODUCTION_USERNAME")
production_password = env.get("PRODUCTION_PASSWORD")


def main():
    """_summary_ Main function to run the script
    """
    download_ftp()
    stop_server()
    upload_files()
    start_server()


def download_ftp():
    """_summary_ Download files from production server recursively and save them to a folder
    """
    print("Downloading files from production server")
    time.sleep(5)
    # create files directory if it doesn't exist
    if not os.path.exists("./files"):
        os.makedirs("./files")
    # check if wget is installed
    if os.system("which wget") != 0:
        print("wget is not installed! Please install wget to continue.")
        sys.exit(1)
    os.system(
        f"wget -r -nH ftp://{production_server}/default -P ./files" +
        "--user {production_username} --password {production_password}")


def upload_files():
    """_summary_ Upload files to staging server recursively using the Pterodactyl API
    """
    for root, dirs, files in os.walk("./files/default"):
        for file in files:
            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, "./files/default")
            if file.endswith(".zip"):
                print("Skipping file: " + rel_file_path)
                continue
            print("Uploading file: " + rel_file_path)
            file_upload_url = api.client.servers.files.get_upload_file_url(
                server)
            file_upload_request = requests.post(
                file_upload_url + "&directory=/" +
                os.path.dirname(rel_file_path),
                files={'files': open('./files/default/' +
                                     rel_file_path, 'rb')},
                timeout=60)
            if file_upload_request.status_code == 200:
                print("File uploaded: " + rel_file_path)
            else:
                print("File upload failed: " + rel_file_path)
                print(file_upload_request.text)
        for directory in dirs:
            sub_dir = os.path.join(root, directory)
            rel_sub_dir = os.path.relpath(
                sub_dir, "./files/default").replace("\\", "/")
            print("Creating directory: " + rel_sub_dir)
            api.client.servers.files.create_folder(
                server, rel_sub_dir, "/")
            print("Directory created: " + rel_sub_dir)


def stop_server():
    """_summary_ Stops the staging server to prevent any issues with the files being overwritten
    """
    api.client.servers.send_power_action(server, "stop")
    print("Server stopped")


def start_server():
    """_summary_ Starts the staging server
    """
    api.client.servers.send_power_action(server, "start")
    print("Server started")


if __name__ == "__main__":
    main()
