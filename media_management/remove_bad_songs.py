#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
The use case of this script is the following:
	Delete all the tracks rated as one star or fewer.
Setup:
	Fill the variables below firstly, then run the script with -h to see the arguments that you need to give.
"""
#TODO: July 30, 2024: Placeholder -- need to loop back to this script and finish it

plex_ip = ''
plex_port = ''
plex_api_token = ''

import pprint
import sys
from os import getenv
from typing import List

# Environmental Variables
plex_ip = getenv('PLEX_IP', plex_ip)
plex_port = getenv('PLEX_PORT', plex_port)
plex_api_token = getenv('PLEX_API_KEY', plex_api_token)
base_url = f"http://{plex_ip}:{plex_port}"

# Target Playlist
DELETION_PLAYLIST = 'Deletion_Queue'

from plexapi.server import PlexServer

plex = PlexServer(base_url, plex_api_token)
# https://www.reddit.com/r/PleX/comments/bmxcya/going_mad_with_plexapi_filenames_from_playlist/
tmp_lst = []
def clear_deletion_queue(playlist_name:str):
	count = 0
	deletedFiles = []
	for media_list in [x for x in plex.playlist(playlist_name).items()]:
		for media in media_list:
			filepath = "".join([x.file for x in media_list.iterParts()])
			print(f"Deleting {media.title}")
			media.delete()
			count += 1
			deletedFiles.append(filepath)
	print(f"Deleted {count} items from {playlist_name}")
	return count, deletedFiles

if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser(description="Delete all tracks rated as one star or fewer")
	parser.add_argument('-p', '--playlist', help='Playlist name to delete tracks from', default=DELETION_PLAYLIST)
	args=parser.parse_args()
	clear_deletion_queue(args.playlist)
