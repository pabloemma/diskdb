# Info on disk for disk db

import os
import sys
import platform
import psutil as PS
import shutil as SH


class disk_info(object):
    def __init__(self):
        super().__init__()

    
    def GetSize(self,disk_path= None,unit = None):
        """Gets size of disk, unit =G gives gigabyte, T = Terrabyte"""
        unit = 'G'
        div = 1.e9

        if unit == 'T':
            div = 1.e12

        size = tuple(map(lambda x: x /div, SH.disk_usage(disk_path)))
        print('total size',size[0],unit)
        print('used size',size[1],unit)
        print('free size',size[2],unit)

        return size
    
    def find_all_dirs(self,path=None,max_depth = 2):
        """recursively find all the directories in a tree down to max_depth"""
        dir_list = []


        for root, dirs, files in os.walk(path):
        # Calculate current depth relative to the start_path
            current_depth = root.count(os.sep) - path.count(os.sep)
            dir_list.append(root)
        
            if current_depth <= max_depth:
                print(f"Current directory (level {current_depth}): {root}")
                for file in files:
                    print(f"  File: {file}")
            else:
        # If we exceed the max_depth, prevent further recursion into subdirectories
        # by clearing the 'dirs' list. This only works if topdown=True (default).
                dirs[:] = []




 #       for root, dirs, files in os.walk(path):
 #           dir_list.append(root)
        return root,dir_list,files
            




    def find_drives(self):
        external_drives = []
        for partition in PS.disk_partitions():
        # Heuristics for identifying external drives:
        # - Check for 'removable' option in mount options (Linux/macOS)
        # - Check for specific device paths (e.g., /dev/sdX, /Volumes/...)
        # - Exclude common internal system partitions
            if 'removable' in partition.opts or (
                partition.mountpoint.startswith('/Volumes/') or  # macOS
                partition.device.startswith('/dev/sd') # Linux, often external
            ) and not (
                partition.mountpoint.startswith('/boot') or
                partition.mountpoint.startswith('/sys') or
                partition.mountpoint.startswith('/proc') or
                partition.mountpoint == '/' # Root partition
            ):
                external_drives.append(partition.mountpoint)
                print(partition.fstype, partition.mountpoint)

        for drives in external_drives:
            print(f"-{drives}")
        self.external_drives = external_drives 
        return      

    def get_dir_entries(self,path=None):
        ''' returns directories in secelcted path'''
        
        return [item for item in os.listdir(path) if os.path.isdir(path+item)]
    
    def get_file_listing(self,path=None):
        """lists all the files in path"""

        return [item for item in os.listdir(path) if os.path.isfile(path+'/'+item)]



if __name__ == "__main__":
    path = '/Volumes/samsung2/Backups.backupdb'
    #path = '/Users/klein'
    DI = disk_info()
    DI.find_drives()
    DI.GetSize(path)
 #   print(DI.get_dir_entries(path=path))
    #print(DI.get_file_listing(path=path))
    #print(DI.find_all_dirs(path=path,max_depth = 1))

