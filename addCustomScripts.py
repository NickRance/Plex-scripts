import os
import random
import PyInstaller.__main__
from pathlib import Path
from crontab import CronTab, CronSlices
HERE = Path(__file__).parent.absolute()

PATHS_TO_SCRIPTS = [
    str(HERE / "media_management" /"remove_bad_songs.py"),
    str(HERE / "playlist_collection" / "create_mix_playlists.py"),
]

def install():
    for path in PATHS_TO_SCRIPTS:
        PyInstaller.__main__.run([
            path,
            '--onefile',
        ])

def add_to_crontab(command:str,time_string:str):
    cron = CronTab(user=True)
    existing_jobs = list(cron)
    new_job = cron.new(command=command)
    new_job.setall(time_string)
    already_exists = False
    for job in existing_jobs:
        # print(cron)
        # print(job.command)
        if job == new_job:
        # if job.command == command and job.comment == time_string:
            print("Job already exists")
            already_exists = True
            break
    if not already_exists:
        cron.write()

def addToCron() :
    binaryDirectory = str(Path(__file__).parent.joinpath('dist'))
    binaryPaths = map(lambda x: Path(binaryDirectory).joinpath(x),[os.path.basename(x).split(".")[0] for x in PATHS_TO_SCRIPTS])
    #add each script to cron 
    for ndx,path in enumerate(binaryPaths):
        print(f"Adding {path} to cron")
        add_to_crontab(str(path), f"0 {12 + ndx} * * 1")
        # add_to_crontab(str(path), f"{random.randint(0,59)} {random.randint} * * *")
        # os.system(f"echo '0 0 * * * {path}' | crontab -")

if __name__ == "__main__":
    # validation_filesexist = map(lambda x: os.path.exists(x), PATHS_TO_SCRIPTS)
    # assert(all(validation_filesexist)), "Not all script paths exist"
    # install()
    addToCron()
