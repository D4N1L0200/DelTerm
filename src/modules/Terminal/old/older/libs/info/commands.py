import os
from datetime import datetime
from json_handler import Data, JSONObj
from rich import print as rprint

import platform
import re
import socket
import subprocess
import uuid

import cpuinfo
import psutil
import pyspeedtest
from screeninfo import get_monitors


def index():
    return ["info"]


def get_size(bytes_: int, suffix="B") -> str:
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_ < factor:
            return f"{bytes_:.2f}{unit}{suffix}"
        bytes_ /= factor


def get_info(data: Data, fast: bool) -> Data:
    print("Getting system data...")
    uname = platform.uname()
    shell_version = subprocess.check_output("pwsh --version", shell=True, text=True)
    data.system = {
        "name": uname.system,
        "node_name": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": [
            uname.processor,
            cpuinfo.get_cpu_info()["brand_raw"],
        ],
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac_address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
        "python_version": platform.python_version(),
        "shell_version": shell_version.split()[1],
    }

    print("Getting monitor data...")
    for monitor in get_monitors():
        data.monitors[monitor.name[4:]] = {
            "x": monitor.x,
            "y": monitor.y,
            "width": monitor.width,
            "height": monitor.height,
            "primary": monitor.is_primary,
        }

    print("Getting boot time...")
    data.boot_timestamp = psutil.boot_time()

    print("Getting cpu data...")
    cpufreq = psutil.cpu_freq()
    cores = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores.update({f"core_{i}": percentage})
    cpu = data.system["processor"][1].split()
    data.cpu = {
        "fabricator": cpu[2],
        "gen": cpu[0],
        "version": cpu[4],
        "speed": cpu[6],
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": cpufreq.max,
        "min_frequency": cpufreq.min,
        "current_frequency": cpufreq.current,
        "cores_usage": cores,
        "usage": psutil.cpu_percent(),
    }

    print("Getting memory data...")
    svmem = psutil.virtual_memory()
    data.memory = {
        "total": svmem.total,
        "avaliable": svmem.available,
        "used": svmem.used,
        "percentage": svmem.percent,
    }

    print("Getting swap data...")
    swap = psutil.swap_memory()
    data.swap = {
        "total": swap.total,
        "avaliable": swap.free,
        "used": swap.used,
        "percentage": swap.percent,
    }

    print("Getting disk data...")
    disks = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disks.update(
            {
                partition.device[:1]: {
                    "file_system_type": partition.fstype,
                    "total": partition_usage.total,
                    "avaliable": partition_usage.free,
                    "used": partition_usage.used,
                    "percentage": partition_usage.percent,
                }
            }
        )
    disk_io = psutil.disk_io_counters()
    data.disk = {
        "drives": disks,
        "io_since_boot": {
            "total_read": disk_io.read_bytes,
            "total_write": disk_io.write_bytes,
        },
    }

    print("Getting network data...")
    if_addrs = psutil.net_if_addrs()
    interfaces = {}
    for interface_name, interface_addresses in if_addrs.items():
        interfaces.update({f"{interface_name}": interface_addresses})
    net_io = psutil.net_io_counters()
    if not fast:
        test = pyspeedtest.SpeedTest()
        # print("Measuring ping...")
        # ping = test.ping()
        print("Measuring download speed...")
        download = test.download() / (1024**2)
        print("Measuring upload speed...")
        upload = test.upload() / (1024**2)
    else:
        print("Skipping speed test...")
        download = 0
        upload = 0
    data.network = {
        "interfaces": interfaces,
        "sent": net_io.bytes_sent,
        "recieved": net_io.bytes_recv,
        "download": download,
        "upload": upload,
    }

    return data


def info(lib, mode: str = None):
    settings: JSONObj = JSONObj(
        "C:\\Users\\danil\\Documents\\Coding\\Os\\data\\settings.json"
    )
    data: Data = Data(settings.data_path, "info.json")
    match mode:
        case "update":
            data = get_info(data, False)
        case "fast":
            data = get_info(data, True)
        case "+":
            rprint(data)
            return

    username = data.system["node_name"]
    system_name = data.system["name"]
    system_machine = data.system["machine"]
    system_version = data.system["version"]
    bt = datetime.fromtimestamp(data.boot_timestamp)
    boot_timestamp = f"{bt.hour}:{bt.minute}:{bt.second} {bt.day}/{bt.month}/{bt.year}"
    python_version = data.system["python_version"]
    shell_version = data.system["shell_version"]
    width = data.monitors["DISPLAY1"]["width"]
    height = data.monitors["DISPLAY1"]["height"]
    mem_used = get_size(data.memory["used"])
    mem_total = get_size(data.memory["total"])
    mem_perc = get_size(data.memory["percentage"])
    swap_used = get_size(data.swap["used"])
    swap_total = get_size(data.swap["total"])
    swap_perc = get_size(data.swap["percentage"])
    disk_used = get_size(data.disk["drives"]["C"]["used"])
    disk_total = get_size(data.disk["drives"]["C"]["total"])
    disk_perc = get_size(data.disk["drives"]["C"]["percentage"])
    download_speed = data.network["download"]
    upload_speed = data.network["upload"]
    cpu = f'{data.cpu["gen"]} Gen {data.cpu["fabricator"]} {data.cpu["version"]}'
    cpu_cores = data.cpu["total_cores"]
    cpu_speed = data.cpu["speed"]

    os.system("cls" if os.name == "nt" else "clear")
    print(
        f"""
                  -`                   {username}
                 .o+`                  -----------------
                `ooo/                  OS: {system_name} {system_machine}
               `+oooo:                 Version: {system_version}
              `+oooooo:                Boot Time: {boot_timestamp}
              -+oooooo+:               Python: {python_version}
            `/:-:++oooo+:              PowerShell: {shell_version}
           `/++++/+++++++:             Resolution: {width}x{height}
          `/++++++++++++++:            CPU: {cpu}
         `/+++ooooooooooooo/`          CPU: {cpu_cores} Cores @ {cpu_speed}
        ./ooosssso++osssssso+`         GPU: No
       .oossssso-````/ossssss+`        Memory: {mem_used} / {mem_total} ({mem_perc}%)
      -osssssso.      :ssssssso.       SWAP: {swap_used} / {swap_total} ({swap_perc}%)
     :osssssss/        osssso+++.      Disk: {disk_used} / {disk_total} ({disk_perc}%)
    /ossssssss/        +ssssooo/-      Download: {download_speed:.2f}Mb/s
  `/ossssso+/:-        -:/+osssso+-    Upload: {upload_speed:.2f}Mb/s
 `+sso+:-`                 `.-/+oso: 
`++:.                           `-/+/
.`                                 `/"""
    )
