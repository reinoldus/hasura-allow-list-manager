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


# How does it work?

We are listening to the hasura docker container logs where all the queries that are requested are logged.

Details can be seen in: `./python/main.py` - it's pretty simple
