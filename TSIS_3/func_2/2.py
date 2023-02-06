def filter_high(movies):
    result = []
    for film in movies:
        if film["imdb"] > 5.5:
            result.append(film)
    return result

movies = [{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 5,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 3.0,
"category": "Adventure"
}]
print(filter_high(movies))