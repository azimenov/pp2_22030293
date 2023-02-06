def high_score(movie):
    return movie["imdb"] > 5.5
        

print(high_score({"name": "We Two","imdb": 4.2,"category": "Romance"}))