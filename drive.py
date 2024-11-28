import os, shlex
from copy import copy
from googleapiclient.errors import HttpError
from gdstorage.storage import GoogleDriveStorage as gds
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


class DriveManager:
    def __init__(self):
        self.s = gds()._drive_service
        self.context = []
    
    def curr_folder_id(self, context = None):
        if context is None:
            context = self.context
        return context[-1][1] if context else "root"
    
    def curr_path(self):
        return "/" + "/".join([name for name, _ in self.context])
    
    def is_directory(self, file):
        return file.get("mimeType") == gds._GOOGLE_DRIVE_FOLDER_MIMETYPE_
    
    def ls(self):
        res = self.s.files().list(q=f"'{self.curr_folder_id()}' in parents").execute()
        for file in res["files"]:
            name = file["name"]
            if self.is_directory(file):
                name += "/"
            print(name)

    def cd(self, file, context = None):
        if not file:
            return
        if context is None:
            context = self.context
        file = file.rstrip("/")
        if file.startswith("/"):
            new_context = []
            file = file.lstrip("/")
        else:
            new_context = copy(self.context)
        error = False
        if not file:
            return
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
                    res = self.s.files().list(q=f"name = '{name}' and mimeType = '{gds._GOOGLE_DRIVE_FOLDER_MIMETYPE_}' and '{self.curr_folder_id(new_context)}' in parents").execute()
                    if len(res["files"]) == 0:
                        error = True
                        break
                    new_context.append((name, res["files"][0]["id"]))
        if error:
            print(f"No such directory: {name}")
        else:
            context.clear()
            context.extend(new_context)
        return not error

    def rm(self, files):
        for file in files:
            split_name = file.rstrip("/").rsplit("/", 1)
            match len(split_name):
                case 1:
                    dirname, filename = ".", split_name[-1]
                case 2:
                    dirname, filename = split_name
                case _:
                    return
            context = copy(self.context)
            if not self.cd(dirname, context):
                return
            res = self.s.files().list(q=f"name = '{filename}' and '{self.curr_folder_id(context)}' in parents").execute()
            if len(res["files"]) == 0:
                print(f"No such file: {filename}")
                return
            file_data = res["files"][0]
            if self.is_directory(file_data):
                while True:
                    decision = input(f"{filename} is a directory. Confirm delete? y/N: ")
                    match decision:
                        case "Y" | "y" | "yes":
                            remove = True
                            break
                        case "N" | "n" | "no" | "":
                            remove = False
                            break
            else:
                remove = True
            if remove:
                self.s.files().delete(fileId=file_data["id"]).execute()


def main():
    dm = DriveManager()
    print("Available commands: ls, cd, rm <file> <file> ..")
    while True:
        try:
            line = input(f"{bcolors.OKBLUE}{dm.curr_path()}{bcolors.ENDC}$ ")
            if not line:
                continue
            arr = shlex.split(line)
            try:
                match arr[0]:
                    case "ls":
                        dm.ls()
                    case "cd":
                        if len(arr) > 1:
                            dm.cd(arr[1])
                    case "rm":
                        if len(arr) > 1:
                            dm.rm(arr[1:])
            except HttpError as e:
                print(e.reason)
        except EOFError:
            print()
            break
        

if __name__ == "__main__":
    main()