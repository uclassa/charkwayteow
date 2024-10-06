import os, json
from gdstorage.storage import GoogleDriveStorage
os.environ["DJANGO_SETTINGS_MODULE"] = "charkwayteow.settings"

def main():
    s = GoogleDriveStorage()._drive_service
    print("Available commands: list, delete <id> <id> <id>...")
    while line := input():
        arr = line.split()
        if arr[0] == "list":
            try:
                print(json.dumps(s.files().list(q=f"'{arr[1]}' in parents").execute(), indent=4))
            except IndexError:
                print(json.dumps(s.files().list().execute(), indent=4))
        elif arr[0] == "delete":
            for item in arr[1:]:
                s.files().delete(fileId=item).execute()
            print(json.dumps(s.files().list().execute(), indent=4))

if __name__ == "__main__":
    main()