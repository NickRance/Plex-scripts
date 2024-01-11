from os import getenv
from pathlib import Path
from plexapi.server import PlexServer
import ffmpeg

plex_ip = ''
plex_port = ''
plex_api_token = ''
target_playlist = ''

# Environmental Variables
plex_ip = getenv("plex_ip", plex_ip)
plex_port = getenv("plex_port", plex_port)
plex_api_token = getenv("plex_api_token", plex_api_token)
target_playlist = getenv("target_playlist", target_playlist)
base_url = f"http://{plex_ip}:{plex_port}"

length_threshold = 20  # in minutes


def get_duration_ffmpeg(file_path:Path) -> int:
   if not file_path.exists():
      print(f"Skipping {file_path}, files does not exist")
      return -1
   probe = ffmpeg.probe(file_path)
   stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
   duration = int(stream['duration'])
   return duration

def isTrackAMixCompilation(duration:int) -> bool:
#    duration = get_duration_ffmpeg(file_path)
   return duration > length_threshold * 60

plex = PlexServer(base_url, plex_api_token)
playlists = plex.playlists(title="All Music")
assert len(playlists) == 1,"Either no playlist found or multiple playlists found"
playlist = playlists[0]
trackLocations = list(map(lambda x: Path(x.locations[0]), playlist.items()))
trackDurations = list(map(lambda x: get_duration_ffmpeg(x), trackLocations))
print(zip(trackLocations, trackDurations))
longTracks = list(filter(lambda x: isTrackAMixCompilation(x[1]), zip(trackLocations, trackDurations)))
print(longTracks)
# music = plex.library.section('Music')
# print(music.totalSize)
# print(music.totalStorage/ (1024*1024))
# allSongs =  music.search("*")
# print(len(allSongs))
# for song in music.search(''):
#     print(song.title)
#     break