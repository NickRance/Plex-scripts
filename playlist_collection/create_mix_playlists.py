from os import getenv
from pathlib import Path
from plexapi.server import PlexServer
import audioread
from tqdm import tqdm

plex_ip = ""
plex_port = ""
plex_api_token = ""
target_playlist = ""

#Config

all_music_playlist = "All Music"
recently_added_playlist = "Recently Added"

# Environmental Variables
plex_ip = getenv("plex_ip", plex_ip)
plex_port = getenv("plex_port", plex_port)
plex_api_token = getenv("plex_api_token", plex_api_token)
target_playlist = getenv("target_playlist", target_playlist)
base_url = f"http://{plex_ip}:{plex_port}"


length_threshold = 20  # in minutes


def get_duration(file_path: Path) -> int:
    if not file_path.exists():
        print(f"Skipping {file_path}, files does not exist")
        return -1
    try:
        with audioread.audio_open(str(file_path)) as f:
            length = f.duration
            # print("Duration obtained!")
            return int(length)
        # audio = WAVE(str(file_path))
        # # contains all the metadata about the wavpack file
        # audio_info = audio.info
        # length = int(audio_info.length)
        # return length
    except Exception as e:
        print(f"Skipping {file_path}, {e}")
        return -1


def isTrackAMixCompilation(duration: int) -> bool:
    #    duration = get_duration_ffmpeg(file_path)
    return duration > length_threshold * 60


def getTargetPlaylist(plex: PlexServer, target_playlist: str):
    playlists = plex.playlists(title=target_playlist)
    if len(playlists) == 1:
        return playlists[0]
    else:
        print(f"Either no playlist named {target_playlist} or multiple playlists with this name")
        return False
    
def duration_detector(length: int | float): 
    hours = length // 3600  # calculate in hours 
    length %= 3600
    mins = length // 60  # calculate in minutes 
    length %= 60
    seconds = length  # calculate in seconds 

    return hours, mins, seconds 
def driver(complete: bool):
    if complete:
        search_playlist_title = all_music_playlist
    else:
        search_playlist_title = recently_added_playlist
    plex = PlexServer(base_url, plex_api_token)
    search_playlist = getTargetPlaylist(plex, search_playlist_title)
    destination_playlist = getTargetPlaylist(plex, target_playlist)
    desination_playlist_contents = []
    if destination_playlist:
        print(f"Fetching contents of {target_playlist}")
        desination_playlist_contents = destination_playlist.items()
        print(f"Found {len(desination_playlist_contents)} items in the playlist")
    uncheckedTracks = list(
        filter(lambda x: x not in desination_playlist_contents, search_playlist.items())
    )
    longTracks = list(
        filter(
            lambda x: isTrackAMixCompilation(get_duration(Path(x.locations[0]))),
        tqdm(uncheckedTracks, desc="Analyzing track durations"),
        )
    )
    print(f"Found {len(longTracks)} long tracks")
    ## Create playlist if it does not exist
    if not destination_playlist:
        print(f"Creating playlist {target_playlist}")
        destination_playlist = plex.createPlaylist(
            title=target_playlist,section="Music", items=[x for x in longTracks]
        )
    else:
        ## Add the tracks to the playlist
        print(f"Adding {len(longTracks)} tracks to the {destination_playlist.title} playlist")
        destination_playlist.addItems([x for x in longTracks])

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete","-c", nargs="?", default=False, const=True)
    args = parser.parse_args()
    driver(args.complete)
