include .env
export $(shell sed 's/=.*//' .env)
playlist_uploader:
	python3 playlist_collection/m3u_to_playlist__with_search.py -l "$(plex_library_name)" -f "$(input_dir)"

subfolder_playlist:
		python3 playlist_collection/sub_folder_playlists.py -f "$(plex_library_name)"
