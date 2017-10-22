FROM node

COPY . /app

WORKDIR /app

CMD ['node','indexjs']


FROM node:boron

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package.json .
COPY package.json package-lock.json ./

RUN npm install

# Bundle app source
COPY . .
ENV PLEX_USERNAME
ENV PLEX_PASSWORD

CMD [ "npm", "start" ]
