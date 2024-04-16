## Disk Space Monitoring and Cleanup

This script monitors the disk space of a specified drive and cleans up specified folders by deleting the oldest files if the free space falls below a certain threshold. It also sends a notification to a specified Slack channel once the cleanup is done.

### How It Works

1. The script first checks the free space of the specified drive.
2. If the free space is below the specified threshold, it initiates the cleanup process.
3. It goes through each specified folder and deletes all but the three most recent date folders. The date folders should be in the format 'YYYYMMDD'.
4. After the cleanup, it sends a notification to the specified Slack channel.

### Configuration

You need to configure the script by providing the necessary details in a `config.json` file.

Here's the structure of the `config.json` file:

- `drive_path`: The path of the drive you want to monitor. E.g., "C:/".
- `threshold_gb`: The free space threshold in gigabytes. If the free space falls below this number, the script will initiate cleanup.
- `slack_channel_id`: The Slack channel ID where you want to send the notification after cleanup.
- `slack_token`: Your Slack API token.
- `folders_to_clean`: A list of folders (inside the `drive_path`) you want to clean up.

Make sure to update the `config.json` file with the appropriate values before running the script.

### Dependencies

- os
- shutil
- json
- psutil
- datetime
- slack_sdk

### Usage

1. Install the required dependencies.
2. Configure the `config.json` file.
3. Run the script.
