# hasura-allow-list-manager

This project is meant to make it easier to maintain an allow list on the community edition of hasura

# How to use?

This project currently is nothing more than a POC but it should work if your deployment meets a few needs. In order to test if it works with your setup do the following:

Clone this repo:
```
git clone https://github.com/reinoldus/hasura-allow-list-manager.git
```

Go into the cloned folder and create a file called: `env_hasura_python` with the following content:
```
HASURA_ADMIN_SECRET=[your hasura secret]
HASURA_CONTAINER_NAME="name-of-your-hasura-container"
HASURA_URL="http://localhost:8080"
```

Then run `./start.sh`

Important: Before you can add queries you have to add one query via the hasura console to the allow list.

This will add the "allowed-queries" collection to hasura which is required. Hasura allows to create collections to better
manage queries but that is not supported so far:

If you do not know what to add: `query { test {id name}}` just paste this here:
![image](https://user-images.githubusercontent.com/2091290/128465477-86d13136-1b66-4ed4-a8c7-82cb27ac120c.png)

All you have to do know is execute a bunch of queries through your frontend or whatever you are using and the queries should appear in the frontend.

# How does it work?

We are listening to the hasura docker container logs where all the queries that are requested are logged. (Your hasura instance has to enable "query-log".)

Every time you reload the frontend we'll fetch the most recent metadata from hasura and take out the queries from there which are already in the allow-list.

The queries from both sources are hashed in the same way to make it easier to compare them, this should be fine because hasura is pretty strict with it's allow list, if you change the order of the attributes in your query, it's considered a different query.

And that is pretty much it nothing more to it. 

Details can be seen in: `./python/main.py` - it's pretty simple

# How does it look:

Incredibly ugly:

![Screenshot 2021-08-06 at 09-24-17 hasura-allow-list-manager](https://user-images.githubusercontent.com/2091290/128466412-130867c6-6370-469e-ae15-b7607354a1a8.jpg)

