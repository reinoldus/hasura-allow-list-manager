FROM node:12-alpine
# create destination directory
RUN mkdir -p /usr/src/nuxt-app/
WORKDIR /usr/src/nuxt-app

# copy the app, note .dockerignore
COPY ./package.json /usr/src/nuxt-app/
COPY ./yarn.lock /usr/src/nuxt-app/
RUN yarn

COPY . /usr/src/nuxt-app/

# build necessary, even if no static files are needed,
# since it builds the server as well
ENV NUXT_HOST=0.0.0.0 \
    NUXT_PORT=3011
RUN yarn run build

# expose 5000 on container
EXPOSE 3011
# start the app
CMD ["yarn", "nuxt", "start" ]
