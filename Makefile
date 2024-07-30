
current_dir := $(shell pwd)

include .env
export $(shell sed 's/=.*//' .env)
playlist_uploader:
	python3 playlist_collection/m3u_to_playlist__with_search.py -l "$(plex_library_name)" -f "$(input_dir)"

subfolder_playlist:
	python3 playlist_collection/sub_folder_playlists.py -f "$(plex_library_name)"

create_mix_playlists_complete:
	python3 $(current_dir)/playlist_collection/create_mix_playlists.py -c

create_mix_playlists_quick:
	python3 $(current_dir)/playlist_collection/create_mix_playlists.py

add_to_cron_monthly:
	(crontab -l ; echo "0 0 1 * * cd $(current_dir)/playlist_collection/ && make create_mix_playlists_complete") | sort - | uniq - | crontab -

add_to_cron_daily:
	(crontab -l ; echo "0 8 * * * ") && cd $(current_dir)/playlist_collection/ && make create_mix_playlists_complete" | sort - | uniq - | crontab -

create_crontab:
	sudo crontab -u $(USER)

delete_crontab:
	sudo crontab -u $(USER) -r