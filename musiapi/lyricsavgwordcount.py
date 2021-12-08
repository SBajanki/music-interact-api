import argparse
from http import HTTPStatus
import re
import requests
import time
import urllib



class musicLyrics():


    def get_artist_id(self, artist_name:str):
        '''
                Returns artist_id ,
                :param name: artist_name:str
                :return: artist_id:str
        '''
		'''
		 This function doesn't return any value when more than one artist with the same name and score=100 exists.
		 Couldn't work on this condition due to time constraint
		'''
        print(f'Getting the artist id ...')

        artist_name = urllib.parse.quote(artist_name, safe='')
        url = f'https://musicbrainz.org/ws/2/artist/?query={artist_name}&fmt=json'

        requests.get(url)
        response = requests.get(url)
        artist_id_name_dict = {}
        if response.status_code == HTTPStatus.OK:
            try:
                artist_dict = response.json()['artists']
                for artist in artist_dict:
                    score = artist['score']
                    if score == 100:
                        artist_id = artist['id']
                        artist_id_name_dict[artist_id]= artist['name']

                if len(artist_id_name_dict)>1:
                    print('Sorry , There are more than one artists with this name.')
                    for key, val in artist_id_name_dict.items():
                        print(f'artist_name:{key} and artist_id:{val}')
                    exit()
                elif len(artist_id_name_dict) == 0:
                    print("Sorry, artist name doesn't exist")
                    exit()
                else:
                    return (artist_id)
            except Exception as e:

                print(f"Error: {e}")
                exit()
        else:
            print("Error:API cannot be connected")
            exit()

    def get_songs_list(self, artist_id:str):
        '''
                Returns songs set,
                :param name: artist_id
                :return: songs_set
        '''

        print('Collecting all the songs list for the artist ...')


        # set initialisation
        url = f'https://musicbrainz.org/ws/2/recording?artist={artist_id}&fmt=json'
        songs_set = set()
        response = requests.get(url)
        #recordings = response.json()['recordings']
        if response.status_code == HTTPStatus.OK:
            recording_data = response.json()
            total_records = recording_data['recording-count']
            print(f'Total recordings for this artist:{total_records}')
            limit = 100
            offset = 0

        else:
            print("Sorry, no songs exist for this artist")
            exit()
        for i in range(0, total_records, 100):  # Check the status code of the url
            print(f'Collecting recording data from musicbrainz url with offset = {offset} and limit = {limit}')

            url = f'https://musicbrainz.org/ws/2/recording?artist={artist_id}&offset={offset}&limit={limit}&fmt=json'
            requests.get(url)
            response = requests.get(url)
           # print(response.status_code)
            if response:
                recordings = response.json()['recordings']
                for rec in recordings:
                    songs_set.add(rec['title'])
                time.sleep(2)
            offset += limit
        return songs_set


    def get_lyrics_word_count_list(self, artist_name:str, songs_set:set):
        '''
            Returns word count list,
            :param name: songs_set
            :return: word_count_list
        '''
        print('Calculating word count for the lyrics ...')

        word_count_list = []  #initialise the word_count_lsit
        for song_name in songs_set:
            try:
                #print(song_name)
                #logging.debug(f'{song_name}')
                print(f'calculating lyrics word count for {song_name}')

                #song_name = urllib.parse.quote(song_name, safe='')

                lyrics_dict = requests.get(f'https://api.lyrics.ovh/v1/{artist_name}/{song_name}').json()

                word_count = self.get_wordcount(lyrics_dict)  #call the function get_wordcount
                if word_count != 0:
                    word_count_list.append(word_count) #prepare a list of wordcounts

            except Exception as e:

                pass

        if int(sum(word_count_list)) == 0:
           print("lyrics doesn't exist for this artist")
           exit()
        else:

            return word_count_list


    def avg_words(self, word_count_list:list):
        '''
            Returns average words for the lyrics,
            :param name: word_count_list
            :return: avg_words_per_lyrics
         '''

        print('Calculating average word count for all lyrics ...')
        avg_words_per_lyrics = sum(word_count_list)/len(word_count_list)
        avg_words_per_lyrics = round(avg_words_per_lyrics,2)
        return avg_words_per_lyrics

    def get_wordcount(self, lyrics_dict:dict):
        '''
            Returns  word count in the lyrics,
            :param name: lyrics_dict:dict
            :return: word_count:int
        '''

        lyrics = lyrics_dict.get('lyrics')
        if lyrics == '':
            word_count = 0
        else:
            lyrics = lyrics_dict.get('lyrics')
            lyrics = re.sub(r'[^\w\s]','', lyrics.replace('\n', " "))
            lyrics_word_list = lyrics.split(" ")    #create list of words
            word_count = len(lyrics_word_list)      # calculate the length of the list

        return word_count

    def main(self, artist_id):
        arid = self.get_artist_id(artist_id)
        songs_list = self.get_songs_list(arid)



if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("artist_name",  help="Display the average words in the artist lyrics")
    args = parser.parse_args()
    if args.artist_name:
        mp = musicLyrics()
        arid = mp.get_artist_id(args.artist_name)
        songs_list = mp.get_songs_list(arid)
        word_count_list = mp.get_lyrics_word_count_list(args.artist_name, songs_list)
        avg_words_per_lyrics = mp.avg_words(word_count_list)
        print(f'Average words in the {args.artist_name} lyrics are {avg_words_per_lyrics}')


