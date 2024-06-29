from flask import Flask, render_template, request, jsonify
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

CLIENT_ID = "777a383125c843a085958fa7c1903f30"
CLIENT_SECRET = "0b13c011985742ef88e4168ecbb29cfc"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters
@app.route('/')
def home():
    return render_template('new2.html')

@app.route('/new')
def new():
    return render_template('new.html')
@app.route('/music')
def music():
    return render_template('music.html')
    
@app.route('/indexo')
def indexo():
    return render_template('index 1.html')

@app.route('/index1')
def index():
    music_list = music['song'].values
    return render_template('index 1.html', music_list=music_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    song = request.form['song']
    recommended_music_names, recommended_music_posters = recommend(song)
    return jsonify(names=recommended_music_names, posters=recommended_music_posters)

if __name__ == '__main__':
    app.run(debug=True)
