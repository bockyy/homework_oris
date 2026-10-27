class Playlist:
    def __init__(self):
        self.songs = []

    def __len__(self):
        return len(self.songs)

    def __str__(self):
        if self.songs:
            track_list = "\n".join(f"{song['name']} ({song['duration']} сек)" for song in self.songs)
            return f"Плейлист:\n{track_list}"
        else:
            return 'Плейлист пуст'

    def add_song(self, name, duration):
        self.songs.append({
            'name': name,
            'duration': duration,
        })

    def remove_song(self, name):
        for song in self.songs:
            if song['name'] == name:
                self.songs.remove(song)
                return
        print('song not found')

    def total_duration(self):
        return sum(x['duration'] for x in self.songs)



#1
playlist = Playlist()
playlist.add_song("Song 1", 200)
playlist.add_song("Song 2", 300)
playlist.add_song("Song 3", 400)
print(playlist.total_duration())
print(len(playlist))
playlist.remove_song("Song 4")
print(len(playlist))
playlist.remove_song("Song 1")
print(len(playlist))

playlist2 = Playlist()
print(playlist2.total_duration())

print(playlist)
print(playlist2)