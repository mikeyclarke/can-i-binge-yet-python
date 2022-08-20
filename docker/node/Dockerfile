FROM node:18-alpine

RUN corepack enable

WORKDIR /var/bingeable

COPY . .

RUN yarn install && yarn run webpack --config webpack.dev.js
