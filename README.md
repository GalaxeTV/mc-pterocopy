# mcserver-ftp-sync

Syncs Minecraft servers with staging and production

## Prerequisites

* wget (for downloading from the FTP server)
  * This is already installed on most Linux distributions
  * On Windows, you can install it with [chocolatey](https://chocolatey.org/) by running `choco install wget`
* Python 3.8+
* API Credentials to access the FTP server and the Pterodactyl Panel
  * Specific permissions needed are all files permissions and the ability to stop and start the server

## How to use

1. Clone repository
2. `cp .env.example .env` to create the `.env` file
3. Modify `.env` to your specified settings
4. `pip install -r requirements.txt` to install the required Python dependencies
5. `python3 sync.py` to run the sync script

The sync script will automatically detect if the server is running or not and will stop it if it is running.

> **Note**
> Depending on the size of the server, it may take a while to sync.

## Example configuration

```env
# Production server related settings
PRODUCTION_SERVER="" # The IP address of the server without the ftp:// prefix
PRODUCTION_USERNAME="" # The username to access the FTP server
PRODUCTION_PASSWORD="" # The password to access the FTP server

# Staging server related settings
STAGING_SERVER="" # The panel URL
STAGING_API_KEY="" # The API key to access the Pterodactyl Panel
```
