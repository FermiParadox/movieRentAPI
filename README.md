# Endpoints 

![image](https://user-images.githubusercontent.com/10809024/173878887-0264c668-729e-4c0e-a53b-f5499a89820d.png)


The user can search, rent, return movies and gets charged for it.
All requirements defined as Use Cases in the Assignment have been implemented. 

Instead of passing movie titles to endpoints when looking for a movie, I’m passing the movie_id to avoid issues with non-english letters. 

Searching for a movie by categories A, B returns all moves that are either A or B. 

User is charged for each day he rent’s a movie. Renting the moving for less than a day counts as 1 day (otherwise he’d be charged too little).

Additionally
    • I added a /login, which provides a JWT 
    • I applied middleware, which checks for the presence and validity of the aforementioned JWT in the request headers, before granting access to: 
        ◦ rent 
        ◦ return 
        ◦ see cost

# DB + ODM

MongoDB was used with the mongoengine ODM. 
I could have created a collection that contains only movie title+ID to make calls cheaper. Additionally, this DB is perhaps more suitable than an SQL DB, since there aren’t updates  simultaneously in different collections. Plus it can scale horizontally.
Also, I’ve never used a relational DB, so I couldn’t risk trying to learn+apply the basics in a couple of days. 

As for the actual movie files, I don’t know if MongoDB would be the best option. (I didn’t implement a movie download, since it wasn’t present in the Use Cases.)

# SOLID principles 
I’d normally break all functions/methods into tiny pieces in compliance with the Single Responsibility Principle, but didn’t do so due to lack of time. 

Likewise I could have used much more often dependency injection and dependency inversion, which would improve the code by reducing strong coupling and make it more testable. 

# Testing
Code coverage is about 96%. Of course there’s much more that could be tested. Despite the seemingly large coverage, the number of implemented tests are a fraction of what was really needed.

# Bugs
Individually running `test_main.py` works fine. When running all tests, tests of `test_main.py` fail with: 
	"mongoengine.connection.ConnectionFailure: You have not defined a default connection". 

It might be mongoengine related.
