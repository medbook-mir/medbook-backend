FROM node:18-alpine
WORKDIR /app

RUN npx create-next-app@latest . --ts false --yes

RUN npm install
COPY --chown=node:node . .

CMD ["npm", "run", "dev"]