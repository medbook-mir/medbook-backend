FROM node:18-alpine
WORKDIR /app

COPY package.json ./

RUN npm install
COPY --chown=node:node . .

CMD ["npm", "run", "dev"]