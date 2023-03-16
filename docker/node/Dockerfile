FROM node:19-alpine

RUN corepack enable

WORKDIR /var/ciby

COPY . .

RUN yarn install && yarn run webpack --config webpack.dev.js
