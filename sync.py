from pydactyl import PterodactylClient
import ftplib
import os
import requests
import time
from dotenv import dotenv_values

# Load environment variables
env = dotenv_values(".env")

# Pterodactyl API
staging_server = env.get("STAGING_SERVER")
staging_api_key = env.get("STAGING_API_KEY")
api = PterodactylClient(staging_server, staging_api_key)
server = api.client.servers.list_servers()[0]['attributes']['identifier']

# FTP
# TODO: Validate FTP configuration to stop timeout errors and allow for file transfer
production_server = env.get("PRODUCTION_SERVER")
production_username = env.get("PRODUCTION_USERNAME")
production_password = env.get("PRODUCTION_PASSWORD")
ftp = ftplib.FTP(production_server, timeout=120)


# ftp.login(production_username, production_password)


def main():
    download_ftp_legacy()
    stop_server()
    upload_files()
    start_server()


def download_ftp():
    # Download files from production server recursively and save them to a folder
    local_path = "./files"
    os.makedirs(local_path, exist_ok=True)
    download_directory("/default", local_path)
    ftp.quit()


def download_ftp_legacy():
    # Download files from production server recursively and save them to a folder
    # This is a legacy version of the download_ftp function, assuming that you are running a Linux server with wget installed
    print("Downloading files from production server")
    print("WARNING: THIS FUNCTION IS CONSIDERED LEGACY AND WILL BE REMOVED IN A FUTURE UPDATE")
    print("Resuming in 5 seconds...")
    time.sleep(5)
    # create files directory if it doesn't exist
    if not os.path.exists("./files"):
        os.makedirs("./files")
    # check if wget is installed
    if os.system("which wget") != 0:
        print("wget is not installed! Please install wget to continue.")
        exit(1)
    os.system("wget -r -nH ftp://" + production_server + "/default -P ./files --user " +
              production_username + " --password " + production_password)


def download_file(file_name, local_path):
    # Download a file from the production server
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    with open(local_path + '/' + file_name, 'wb') as f:
        ftp.retrbinary('RETR ' + file_name, f.write, 1024)


def download_directory(path, local_path):
    # Download a directory from the production server
    ftp.cwd(path)
    files = ftp.nlst()
    for file_name in files:
        if "." in file_name:
            print("Downloading file: " + file_name)
            download_file(file_name, local_path)
        else:
            os.makedirs(local_path + '/' + file_name, exist_ok=True)
            print("Entering directory: " + file_name)
            download_directory(path + '/' + file_name,
                               local_path + '/' + file_name)
            ftp.cwd("..")


def upload_files():
    # Upload a file to the staging server using the Pterodactyl API
    for root, dirs, files in os.walk("./files/default"):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, "./files/default")
            if file.endswith(".zip"):
                print("Skipping file: " + rel_path)
                continue
            print("Uploading file: " + rel_path)
            file_upload_url = api.client.servers.files.get_upload_file_url(server)
            file_upload_request = requests.post(
                file_upload_url,
                files={'files': open('./files/default/' + rel_path, 'rb')})
            if file_upload_request.status_code == 200:
                print("File uploaded: " + file)
            else:
                print("File upload failed: " + file)
                print(file_upload_request.text)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            rel_path = os.path.relpath(dir_path, "./files/default")
            print("Creating folder: " + rel_path)
            api.client.servers.files.create_folder(server, rel_path, os.path.realpath(dir))
            print("Created folder: " + rel_path)


def stop_server():
    # Stops the staging server,to prevent any issues with the files being overwritten
    api.client.servers.send_power_action(server, "stop")
    print("Server stopped")


def start_server():
    # Starts the staging server
    api.client.servers.send_power_action(server, "start")
    print("Server started")


if __name__ == "__main__":
    main()
