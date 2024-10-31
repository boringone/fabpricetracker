FROM node

WORKDIR /app

COPY yarn.lock package.json ./
RUN yarn install

COPY . .


EXPOSE 5173

CMD ["yarn", "dev"]