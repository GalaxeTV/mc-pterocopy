# mcptero-copy

Copies a production Minecraft server to a developer Minecraft serer

## Prerequisites

* A Minecraft server running on a hosted provider (e.g. Apex Hosting, etc.) [Production Server]
* A Minecraft server running on a Pterodactyl Panel [Staging Server]
* wget (for downloading from the FTP server)
  * This is already installed on most Linux distributions
  * On Windows, you can install it with [chocolatey](https://chocolatey.org/) by running `choco install wget`, *however it is untested*
* Python 3.8+
* API keys and FTP Credentials to access the FTP server and the Pterodactyl Panel
  * Specific permissions needed are all files permissions and the ability to stop and start the server

## Setting up an API access key

> **Note**
>
> This can be run as any user on the panel, but it is recommended to create a new subuser that only has full `power` and `file` permissions access for this purpose. **This is NOT the same as the Application API key.**

1. Log into the panel
2. Click on the user icon in the top right corner
3. Click on "API Credentials"
4. Click on "Create New API Key"
5. Give the key a name and click "Create Key"
6. Copy the key and save it to the `.env` file as the `STAGING_API_KEY` value (see [Example configuration](#example-configuration))

## How to use script

1. Clone repository
2. `cp .env.example .env` to create the `.env` file
3. Modify `.env` to your specified settings
4. `pip install -r requirements.txt` to install the required Python dependencies
5. `python3 .\sync.py` to run the sync script

The sync script will automatically detect if the server is running or not and will stop it if it is running.

> **Note**
>
> Depending on the size of the server, it may take a while to sync. The script will print out the progress of the sync. It will also **delete any files that are on the staging server** but NOT on the production server.

## Example configuration

```env
# Production server related settings
PRODUCTION_SERVER="" # The URL of the FTP server without the ftp:// prefix
PRODUCTION_USERNAME="" # The username to access the FTP server
PRODUCTION_PASSWORD="" # The password to access the FTP server

# Staging server related settings
STAGING_SERVER="" # The panel URL
STAGING_API_KEY="" # The API key to access the Pterodactyl Panel
```
