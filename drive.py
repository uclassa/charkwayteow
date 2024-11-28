import os, shlex
from copy import copy
from googleapiclient.errors import HttpError
from gdstorage.storage import GoogleDriveStorage
os.environ["DJANGO_SETTINGS_MODULE"] = "charkwayteow.settings"

"""
This is a simple tool to manage the service account drive connected to the project.
It starts you off in the root of the filesystem (basically "my drive").
Use the `ls` and `cd` commands to navigate the drive and `rm` to remove any unneeded files and directories.
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    s = GoogleDriveStorage()._drive_service
    print("Available commands: ls, cd, rm <file> <file> ..")
    print("Note: rm only supports files and directories in the current folder because Alex is lazy and hasn't implemented slash support yet")
    context = []
    while True:
        try:
            line = input(f"{bcolors.OKBLUE}/{"/".join(map(lambda tup: tup[0], context))}{bcolors.OKGREEN}$ {bcolors.ENDC}")
            if not line:
                continue
            arr = shlex.split(line)
            try:
                cmd = s.files()
                match arr[0]:
                    case "ls":
                        res = cmd.list(q=f"'{context[-1][1] if context else "root"}' in parents").execute()
                        for file in res["files"]:
                            name = file["name"]
                            if file["mimeType"] == "application/vnd.google-apps.folder":
                                name += "/"
                            print(name)
                    case "cd":
                        if len(arr) > 1:
                            arr[1] = arr[1].rstrip("/")
                            if arr[1].startswith("/"):
                                new_context = []
                                file = arr[1].lstrip("/")
                            else:
                                new_context = copy(context)
                                file = arr[1]
                            error = False
                            if file:
                                for name in file.split("/"):
                                    match name:
                                        case "..":
                                            if not new_context:
                                                error = True
                                                break
                                            new_context.pop()
                                        case ".":
                                            pass
                                        case _:
                                            res = cmd.list(q=f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and '{new_context[-1][1] if new_context else "root"}' in parents").execute()
                                            if len(res["files"]) == 0:
                                                error = True
                                                break
                                            new_context.append((name, res["files"][0]["id"]))
                            if error:
                                print(f"No such directory: {arr[1]}")
                            else:
                                context = new_context
                    case "rm":
                        for item in arr[1:]:
                            res = cmd.list(q=f"name = '{item.rstrip("/")}' and '{context[-1][1] if context else "root"}' in parents").execute()
                            if not res["files"]:
                                print(f"No such file: {item}")
                                break
                            file = res["files"][0]
                            if file["mimeType"] == "application/vnd.google-apps.folder":
                                while True:
                                    decision = input(f"{file["name"]} is a directory. Confirm delete? y/N: ")
                                    match decision:
                                        case "Y" | "y" | "yes":
                                            remove = True
                                            break
                                        case "N" | "n" | "no" | "":
                                            remove = False
                                            break
                            if remove:
                                cmd.delete(fileId=file["id"]).execute()
            except HttpError as e:
                print(e.reason)
        except EOFError:
            print()
            break
        

if __name__ == "__main__":
    main()