FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install @kangc/v-md-editor@next

RUN npm install vue-diff

COPY . .

EXPOSE 7070

CMD ["npm", "run", "serve"]