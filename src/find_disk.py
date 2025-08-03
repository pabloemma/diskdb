import psutil

def list_external_drives_psutil():
    external_drives = []
    for partition in psutil.disk_partitions():
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
    return external_drives

if __name__ == "__main__":
    drives = list_external_drives_psutil()
    if drives:
        print("External drives detected:")
        for drive in drives:
            print(f"- {drive}")
    else:
        print("No external drives found.")