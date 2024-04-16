import os
import shutil
import json
import psutil
from datetime import datetime
from slack_sdk import WebClient  # Uncomment if you have slack_sdk installed


def send_slack_message(channel_id, message, slack_token):
    client = WebClient(token=slack_token)
    client.chat_postMessage(channel=channel_id, text=message)


def get_disk_usage(path):
    usage = psutil.disk_usage(path)
    total_space = usage.total
    used_space = usage.used
    free_space = usage.free
    return total_space, used_space, free_space


def get_sorted_date_folders(path):
    """Return a list of folders sorted by date from oldest to newest."""
    all_folders = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    date_folders = [d for d in all_folders if is_valid_date(os.path.basename(d))]
    
    # Print all folders and date folders for debugging
    # print(f"All folders in {path}: {all_folders}")
    # print(f"Date folders in {path}: {date_folders}")

    date_folders.sort(key=lambda date: datetime.strptime(os.path.basename(date), '%Y%m%d').strftime('%Y-%m-%d'), reverse=True)
    return date_folders


def is_valid_date(path):
    """Check if a string is a valid date in the format YYYY-MM-DD."""
    date_string = os.path.basename(path)  # Extracting folder name from the full path
    try:
        datetime.strptime(date_string, '%Y%m%d').strftime('%Y-%m-%d')
        return True
    except ValueError:
        return False


def cleanup_folder(folder_path):
    """Cleanup the folder structure."""
    print(f"Initiating cleanup for: {folder_path}")
    for client_folder in os.listdir(folder_path):
        client_path = os.path.join(folder_path, client_folder)
        if not os.path.isdir(client_path):
            continue  # skip if not a directory
        for camera_folder in os.listdir(client_path):
            camera_path = os.path.join(client_path, camera_folder)
            if not os.path.isdir(camera_path):
                continue  # skip if not a directory
            date_folders = get_sorted_date_folders(camera_path)

            if len(date_folders) <= 3:  # If there are 3 or fewer folders, skip deletion
                print(f"Skipped: {camera_path} as it has {len(date_folders)} date folders.")
                continue
            
            # Keep latest 3 folders, delete the rest
            for old_folder in date_folders[3:]:
                path_to_delete = os.path.join(camera_path, old_folder)
                try:
                    shutil.rmtree(path_to_delete)
                    print(f"Deleted: {path_to_delete}")
                except Exception as e:
                    print(f"Failed to delete {path_to_delete}. Error: {e}")


def check_disk_space(drive_path, threshold, slack_channel_id, slack_token, folders_to_clean):
    total, used, free = get_disk_usage(drive_path)
    free_gb = free / (1024 ** 3)  # Convert bytes to gigabyte
    print(f"Free space: {free_gb:.2f} GB")

    if free_gb <= threshold:
        print("Free space below threshold. Initiating cleanup...")
        # Cleanup folders
        for folder in folders_to_clean:
            cleanup_folder(folder)

        # Send a Slack notification after data cleanup
        message = "Congratulations! Your hard drive is free."
        send_slack_message(slack_channel_id, message, slack_token)
        print(message)


def main():
    # Load variables from the JSON file
    with open('config.json') as json_file:
        config = json.load(json_file)

    drive_path = config['drive_path']
    threshold_gb = config['threshold_gb']
    slack_channel_id = config['slack_channel_id']
    slack_token = config['slack_token']
   
    folders_to_clean = [os.path.join(drive_path, folder) for folder in config['folders_to_clean']]

    check_disk_space(drive_path, threshold_gb, slack_channel_id, slack_token, folders_to_clean)


if __name__ == "__main__":
    main()
