# hasura-allow-list-manager

This project is meant to make it easier to maintain an allow list on the community edition of hasura

# How to use?

This project currently is nothing more than a POC, but it should work if your deployment meets a few needs.

Requirements:

- Every query name has to be unique
- The queries that are saved to hasura have to be called as they are called in your code
    - Why? If they are called differently it is pretty hard to detect changed queries
    - If you have queries with the same name for different roles prepend them with the name for that role
- You have to run hasura in docker
- You probably have to use linux

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

Important: Before you can add queries you have to add a collection the default name for the allow list is called "
allowed-queries".

**Caveats:**

- All collections you add to hasura are not automatically part of the allow list if you want to add a collection to the
  allow list you have to click the button
- I haven't yet taking care of proper refetching of the data (it's a POC) so sometimes (often) you have to press F5 to
  see changes
- If you want to see the hasura response open the dev console (modal component already added but haven't integrated it
  everywhere yet)

# How does it work?

We are listening to the hasura docker container logs where all the queries that are requested are logged.

Details can be seen in: `./python/main.py` - it's pretty simple
