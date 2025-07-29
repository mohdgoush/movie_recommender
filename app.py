from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity_matrix.pkl', 'rb'))

def recommend(movie):
    movie = movie.strip().lower()  # Strip spaces and lowercase for match
    match = movies[movies['Movie Name'].str.lower() == movie]
    
    if match.empty:
        raise ValueError("Movie not found")
    
    movie_index = match.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]]['Movie Name'] for i in movie_list]
    return recommended_movies


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_route():
    movie = request.form['movie']
    try:
        recommended = recommend(movie)
        return render_template('index.html', recommended=recommended, selected_movie=movie)
    except:
        return render_template('index.html', error="Movie not found")

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q', '').lower()
    suggestions = [movie for movie in movies['Movie Name'].values if search in movie.lower()]
    return jsonify(suggestions[:10])  # Limit to 10 suggestions

if __name__ == '__main__':
    app.run(debug=True)
