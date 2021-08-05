cd nuxt
docker build -t hasura-allow-list-manager-nuxt .
cd ../python
docker build -t hasura-allow-list-manager-python .
cd ..
docker-compose up