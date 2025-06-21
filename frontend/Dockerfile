FROM node:18-alpine
WORKDIR /app

COPY package.json ./

# Commented this command. 
# since it did not include package.json 
# and threw certain packages not found err
# RUN npx create-next-app@latest . --ts false --yes

RUN npm install
COPY --chown=node:node . .

CMD ["npm", "run", "dev"]