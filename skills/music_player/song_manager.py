############################
# Song Database Class
# This class is used to store and manage the songs in the database
#
# Code adapted from a previous project:
# https://github.com/aamott/Offline-Playback-Skill/blob/19.08/song_database_manager.py
############################
import re
from lingua_franca.parse import match_one, fuzzy_match
from pathlib import Path
import os.path
from tinytag import TinyTag
import random

######################################
# Song Database Class
# This class is used to store and manage songs and playlists
######################################
class SongDatabase:

    def __init__(self,
                 music_dir: str = str(Path.home()) + "/Music",
                 music_extensions=('.mp3', '.aac', '.cda', '.flac', '.ogg',
                                   '.opus', '.wma', '.zab', 'm4a', '.wav'),
                 playlist_extensions=('.asx', '.xspf', '.b4s', '.m3u',
                                      'm3u8')):
        """Initializes the song database.

            Parameters:
                music_dir    (the directory to search for music)
        """
        self.songs = {} # {'song title': {'title': str, 'artist': str, 'album': str, ... }, ...}
        self.artists = {}  # {'artist name': [songs], ...}
        self.albums = {} # {'album name': [songs], ...}
        self.genres = {} # {'genre name': [songs], ...}

        # each playlist is a dict with a filepath and songs list
        self.playlists = {}  # {'playlist name': {'filepath': str, 'songs': [str, str, ...]}, ...}

        # for keeping song of playback
        self.previous_songs = [] # [song, song, ...]

        self.load_database(directory=music_dir,
                           music_extensions=music_extensions,
                           playlist_extensions=playlist_extensions)


    #########################
    # Random Functions
    #########################
    def get_random_song(self) -> str:
        """Returns a random song from the database

        Returns:
            dict: (a dictionary of song metadata)
                song metadata: {'filepath': str, 'title': str, 'artist': str, 'album': str, ...}
        """
        song = random.choice(list(self.songs.values()))
        return song


    #########################
    # Misc Functions
    #########################
    def standardize_title(self, title):
        """ Removes all non-alphanumeric characters and replaces underscores and hyphens with spaces
            and converts to lowercase 

            Parameters:
                title:str (title to standardize)
            Returns:
                standardized_title:str (standardized title)"""
        title = re.sub(r'[^\w\s]', '', title)
        title = title.replace("_", " ")
        title = title.replace("-", " ")
        title = title.lower()
        return title


    def read_playlist(self, filepath:str) -> list[str]:
        """Parses a playlist file and returns a list of songs.
        Supports m3u, m3u8, pls, xspf, wpl, and plain text with one song per line

        Parameters:
            filepath:str (the path to the playlist file)
        Returns:
            song_list:list[str] (a list of song filepaths)
        """
        # TODO: load each song's metadata and return a list of those instead of just the filepath
        with open(filepath, 'r') as file:
            playlist = []
            line = file.readline().strip()

            # m3u or m3u8 playlist
            if line == '#EXTM3U':
                for line in file:
                    # remove comments
                    if line.strip()[0] != '#':
                        playlist.append(line.strip())

            # pls playlist
            elif line == '[playlist]':
                for line in file:
                    # only get file paths
                    if line.startswith('File'):
                        path = line.split('=')[1].strip()
                        if os.path.exists(path):
                            playlist.append(path)

            # xspf playlist
            elif line == '<?xml version="1.0" encoding="UTF-8"?>':
                for line in file:
                    # only get file paths
                    if line.startswith('<location>'):
                        path = line.split('>')[1].split('<')[0].strip()
                        if os.path.exists(path):
                            playlist.append(path)

            # wpl playlist
            elif line.startswith('<?wpl'):
                for line in file:
                    # only get file paths
                    if line.startswith('<media'):
                        path = line.split('src="')[1].split('"')[0]
                        if os.path.exists(path):
                            playlist.append(path)

            # if the playlist is not one of the above, assume it is a simple list of songs
            else:
                for line in file:
                    if os.path.exists(line.strip()):
                        playlist.append(line.strip())

            return playlist


    def load_database(self,
                      directory=str(Path.home()) + "/Music",
                      music_extensions:tuple=('.mp3', '.aac', '.cda', '.flac', '.ogg',
                                       '.opus', '.wma', '.zab', 'm4a', '.wav'),
                      playlist_extensions:tuple=('.asx', '.xspf', '.b4s', '.m3u',
                                          'm3u8')):
        """ Loads the database of songs from a directory 

            Parameters:
                directory:str (directory to load songs from)
                music_extension:tuple (extensions of music files)
                playlist_extension:tuple (extensions of playlist files)
        """
        directory = Path(directory)
        if not directory.exists():
            print("Directory does not exist")
            raise Exception("Directory does not exist")

        # convert music_extensions and playlist_extensions to tuples
        music_extensions = tuple(music_extensions)
        playlist_extensions = tuple(playlist_extensions)

        for root, subfolder, files in os.walk(directory):
            for filename in files:
                item_path = os.path.join(root, filename)
                # MUSIC FILES
                if music_extensions and filename.lower().endswith(music_extensions):
                    tags = TinyTag.get(item_path)

                    song_data = tags.as_dict()
                    song_data['filepath'] = item_path

                    # SONG
                    if tags.title:
                        title = tags.title
                    else:
                        title = Path(item_path).stem
                        title = self.standardize_title(title)
                        tags.title = title
                        song_data["title"] = title
                    self.songs[title] = song_data

                    # ARTIST: creates a list of songs under each artist
                    if (tags.artist is
                            None) and root != directory and directory != Path(
                                root).parent and directory != Path(
                                    root).parent.parent:
                        # If no artist tag, then use the name of the folder two levels up
                        artist_name = Path(item_path).parent.parent.name
                        tags.artist = self.standardize_title(artist_name)
                    # else, tags.artist is None
                    if tags.artist in self.artists:
                        # if the artist already exists, add the song to the list
                        self.artists[tags.artist].append(song_data)
                    else:
                        # otherwise, create a new list for the artist
                        self.artists[tags.artist] = [song_data]

                    # ALBUM: adds a list of songs to each album
                    if tags.album is None and root != directory and directory != Path(
                            root).parent:
                        # if the album name is None, then it is the name of the parent folder
                        album = Path(root).parent.name
                        tags.album = self.standardize_title(album)
                    if tags.album in self.albums:
                        self.albums[tags.album].append(song_data)
                    else:
                        self.albums[tags.album] = [song_data]

                    # GENRE: adds a list of songs to each genre
                    if tags.genre in self.genres:
                        self.genres[tags.genre].append(song_data)
                    else:
                        self.genres[tags.genre] = [song_data]

                # PLAYLIST FILES
                elif playlist_extensions and filename.lower().endswith(
                        playlist_extensions):
                    playlist_title = Path(item_path).stem
                    playlist_title = self.standardize_title(playlist_title)

                    songs = self.read_playlist(item_path)
                    playlist_data = {
                        'filepath': item_path,
                        'title': playlist_title,
                        'songs': songs
                    }

                    # add the playlist data to the dict of playlists
                    self.playlists[playlist_title] = playlist_data

        # clear out any None values
        if None in self.albums:
            del self.albums[None]
        if None in self.genres:
            del self.genres[None]
        if None in self.artists:
            del self.artists[None]


    #########################
    # Search Functions
    #########################
    # TODO: Should queries be case insensitive and remove accents? Stripped of spaces? Special characters removed?

    def search(self,
               query: str,
               type: str = 'all',
               confidence_threshold: float = 0.8) -> list[tuple[dict, float]]:
        """ Searches the database for a query

            Parameters:
                query:str  - the query to search for
                type:str  - 'album', 'artist', 'genre', 'song', or 'playlist' or 'all'
            Returns:
                matches: 
                    list[tuple[album: dict{'title': str, 'song': data about song}, confidence: float]] (an ordered list of tuples of the form (album/artist/song data, confidence)) 
                    OR None (if no matches found) 
        """
        results:list[tuple[dict, float]] = []
        if type == 'album' or type == 'all':
            result = self.search_albums(query, confidence_threshold=confidence_threshold)
            if result:
                results += result
        if type == 'artist' or type == 'all':
            result = self.search_artists(query, confidence_threshold=confidence_threshold)
            if result:
                results += result
        if type == 'genre' or type == 'all':
            result = self.search_genres(query, confidence_threshold=confidence_threshold)
            if result:
                results += result
        if type == 'playlist' or type == 'all':
            result = self.search_playlists(query, confidence_threshold=confidence_threshold)
            if result:
                results += result
        if type == 'song' or type == 'all':
            # get songs, but make them the same format as albums, artists, etc.
            songs = self.search_songs(query, confidence_threshold=confidence_threshold)
            for song_data, confidence in songs:
                song_data = {
                    'title': song_data['title'],
                    'song': song_data
                }
                results.append((song_data, confidence))


        # sort the results by confidence
        results.sort(key=lambda x: x[1], reverse=True)

        return results


    def search_albums(
            self,
            query: str,
            artist_name: str = None,
            confidence_threshold: float = 0.5) -> list[tuple[dict, float]]:
        """ Searches for albums by name and optionally artist.

            Parameters:   
                query:str  (album to search)
                artist name:str (artist name to search for)
                confidence_threshold:float (0.0 to 1.0) (the minimum confidence to return a match)
            Returns:
                matches: 
                    list[(album: dict{'title': str, 'song': data about song}, confidence: float)] (an ordered list of tuples of the form (album/artist/song data, confidence))
                    list[tuple[album: dict, confidence: float]] (a list of songs in the album) 
                    OR None (if no matches found) 
        """
        # Do a fuzzy match of each album name
        # matching_albums will look like this: [(album_name:str, confidence:float), (album_name:str, confidence:float), ...]
        matching_albums = []

        for album_name in self.albums.keys():
            confidence = fuzzy_match(query, album_name)
            if confidence > confidence_threshold:
                album_contents = self.albums[album_name]
                album_data = {
                    'title': album_name,
                    'songs': album_contents
                }

                # if the artist name is not None, then check if the album is by the artist
                if artist_name is not None:
                    # fuzzy match the artist name
                    artist_confidence = fuzzy_match(artist_name, album_data['songs'][0]['artist'])
                    if artist_confidence < confidence_threshold:
                        continue

                    # average the confidence of the artist name and the album name
                    confidence = (confidence + artist_confidence) / 2

                matching_albums.append((album_data, confidence))

        # Sort the matching albums by confidence, max to min
        matching_albums.sort(key=lambda x: x[1], reverse=True)

        # Return the list of matching albums
        return matching_albums


    def search_genres(self, query:str, confidence_threshold: float = 0.8) -> list[tuple[dict, float]]:
        """ Searches for genres by name.

            Parameters:   
                query:str  (genre to search)
                confidence_threshold:float (0.0 to 1.0) (the minimum confidence to return a match)
            Returns:
                matches:
                    list[tuple[genre: dict, confidence: float]] (a list of songs in the genre)
        """
        # Do a fuzzy match of each genre name
        # matching_genres will look like this: [(genre_name:str, confidence:float), (genre_name:str, confidence:float), ...]
        matching_genres = []

        for genre_name in self.genres.keys():
            confidence = fuzzy_match(query, genre_name)
            if confidence > confidence_threshold:
                genre_contents = self.genres[genre_name]
                genre_data = {
                    'title': genre_name,
                    'songs': genre_contents
                }
                matching_genres.append((genre_data, confidence))

        # Sort the matching genres by confidence, max to min
        matching_genres.sort(key=lambda x: x[1], reverse=True)

        # Return the list of matching genres
        return matching_genres


    def search_playlists(self, query:str, confidence_threshold: float = 0.8) -> list[tuple[dict, float]]:
        """ Searches for playlists by name.

            Parameters:   
                query:str  (playlist to search)
                confidence_threshold:float (0.0 to 1.0) (the minimum confidence to return a match)
            Returns:
                matches:
                    list[tuple[playlist: dict, confidence: float]] (a list of songs in the playlist)
        """
        # Do a fuzzy match of each playlist name
        # matching_playlists will look like this: [(playlist_name:str, confidence:float), (playlist_name:str, confidence:float), ...]
        matching_playlists = []

        for playlist_name in self.playlists.keys():
            confidence = fuzzy_match(query, playlist_name)
            if confidence > confidence_threshold:
                playlist_contents = self.playlists[playlist_name]
                playlist_data = {
                    'title': playlist_name,
                    'songs': playlist_contents
                }
                matching_playlists.append((playlist_data, confidence))

        # Sort the matching playlists by confidence, max to min
        matching_playlists.sort(key=lambda x: x[1], reverse=True)

        # Return the list of matching playlists
        return matching_playlists


    def search_artists(self, query:str, confidence_threshold:float=0.8) -> list[tuple[dict, float]]:
        """ Searches for artists by name.

            Parameters:   
                query:str  (artist to search)
                confidence_threshold:float (0.0 to 1.0) (the minimum confidence to return a match)
            Returns:
                matches:
                    list[tuple[artist: dict, confidence: float]] (a list of songs in the artist)
        """
        # Do a fuzzy match of each artist name
        # matching_artists will look like this: [(artist_name:str, confidence:float), (artist_name:str, confidence:float), ...]
        matching_artists = []

        query = query.lower()

        for artist_name in self.artists.keys():
            confidence = fuzzy_match(query, artist_name.lower())
            if confidence > confidence_threshold:
                artist_contents = self.artists[artist_name]
                artist_data = {
                    'title': artist_name,
                    'songs': artist_contents
                }
                matching_artists.append((artist_data, confidence))

        # Sort the matching artists by confidence, max to min
        matching_artists.sort(key=lambda x: x[1], reverse=True)

        # Return the list of matching artists
        return matching_artists


    def search_songs(self, query:str, artist_name=None, confidence_threshold:float=0.8) -> list[tuple[dict, float]]:
        """ Searches for songs by name.

            Parameters: 
                query:str  (song to search)
                artist_name:str (artist of the song) (optional)
                confidence_threshold:float (0.0 to 1.0) (the minimum confidence to return a match)
            Returns:
                matches:
                    list[tuple[song: dict, confidence: float]] (a list of songs in the song)
        """
        # Do a fuzzy match of each song name
        # matching_songs will look like this: [(song_name:str, confidence:float), (song_name:str, confidence:float), ...]
        matching_songs = []

        query = query.lower()

        for song_name in self.songs.keys():
            confidence = fuzzy_match(query, song_name.lower())
            if confidence > confidence_threshold:
                song_data = self.songs[song_name]

                # If artist name is specified, only return songs by that artist
                if artist_name:
                    # fuzzy match the artist name
                    artist_confidence = fuzzy_match(artist_name, song_data['artist'])
                    # If the artist name doesn't match, skip this song
                    if artist_confidence < confidence_threshold:
                        continue

                    # average the confidence of the artist name and the song name
                    confidence = (confidence + artist_confidence) / 2

                matching_songs.append((song_data, confidence))


        # Sort the matching songs by confidence, max to min
        matching_songs.sort(key=lambda x: x[1], reverse=True)

        # Return the list of matching songs
        return matching_songs



def test():
    print()

    player = SongDatabase(music_dir="D:/Music")

    print("----------------------------------------------------")
    print("----------- Testing search_albums() ----------------")
    print("----------------------------------------------------")
    print()

    query = "Lamar Holley"
    print(f'Searching for "{query}" in albums:')
    albums = player.search_albums(query)
    if albums:
        album_data, confidence = albums[0]
        print(f'Match: "{album_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()

    print('Searching for "Lamar Holley" in albums by "Lamar Holley":')
    albums = player.search_albums("Lamar Holley", "Lamar Holley")
    if albums:
        album_data, confidence = albums[0]
        print(f'Match: "{album_data["title"]}" by "{album_data["songs"][0]["artist"]}" with confidence {confidence}')
    else:
        print("No matches found")


    print()
    print("----------------------------------------------------")
    print("----------- Testing search_genres() ----------------")
    print("----------------------------------------------------")
    print()

    query = "Rockk"
    print(f'Searching for "{query}" in genres:')
    genres = player.search_genres(query)
    if genres:
        genre_data, confidence = genres[0]
        print(f'Match: "{genre_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()


    print("----------------------------------------------------")
    print("----------- Testing search_playlists() ------------")
    print("----------------------------------------------------")
    print()

    playlist_query = "Workout"
    print(f'Searching for "{playlist_query}" in playlists:')
    playlists = player.search_playlists(playlist_query)
    if playlists:
        playlist_data, confidence = playlists[0]
        print(f'Match: "{playlist_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()


    print("----------------------------------------------------")
    print("----------- Testing search_artists() --------------")
    print("----------------------------------------------------")
    print()

    artist_query = "Lamar Hollyn" # "Lamar Holley"
    print(f'Searching for "{artist_query}" in artists:')
    artists = player.search_artists(artist_query)
    if artists:
        artist_data, confidence = artists[0]
        print(f'Match: "{artist_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()


    print("----------------------------------------------------")
    print("----------- Testing search_songs() --------------")
    print("----------------------------------------------------")
    print()

    song_query = "Amotto"
    print(f'Searching for "{song_query}" in songs:')
    songs = player.search_songs(song_query, confidence_threshold=0.5)
    if songs:
        song_data, confidence = songs[0]
        print(f'Match: "{song_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()

    print(f'Searching for "{song_query}" in songs by "Lamar Holley":')
    songs = player.search_songs(song_query, "Lamar Holley", confidence_threshold=0.5)
    if songs:
        song_data, confidence = songs[0]
        print(f'Match: "{song_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")
    print()

    print("----------------------------------------------------")
    print("--------------- Testing search() ------------------")
    print("----------------------------------------------------")
    print()

    print(f'Searching for "{song_query}" in all categories:')
    songs = player.search(song_query, confidence_threshold=0.5)
    if songs:
        song_data, confidence = songs[0]
        print(f'Match: "{song_data["title"]}" with confidence {confidence}')
    else:
        print("No matches found")

    print()


if __name__ == "__main__":
    test()