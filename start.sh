cd nuxt
docker build -t hasura-allow-list-manager-nuxt .
cd ../backend
docker build -t hasura-allow-list-manager-python .
cd ..
docker-compose up