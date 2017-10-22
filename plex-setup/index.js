var PlexAPI = require("plex-api");
const querystring = require('querystring');

var client = new PlexAPI({
    "hostname":"plex_server",
    "username":process.env.PLEX_USERNAME,
    "password":process.env.PLEX_PASSWORD
});

var movie_section={
    "scanner":"Plex Movie Scanner",
    "language":"en",
    "type":"movie",
    "agent":"com.plexapp.agents.imdb",
    "location":"/movies",
    "name":"Movies"
};

var music_section={
    "scanner":"Plex Music Scanner",
    "language":"en",
    "type":"artist",
    "agent":"com.plexapp.agents.lastfm",
    "location":"/music",
    "name":"Music"
};

var tv_section={
    "scanner":"Plex Series Scanner",
    "language":"en",
    "type":"show",
    "agent":"com.plexapp.agents.thetvdb",
    "location":"/tv",
    "name":"TV Shows"
};

var photo_section={
    "scanner":"Plex Photo Scanner",
    "language":"en",
    "type":"photo",
    "agent":"com.plexapp.agents.none",
    "location":"/photos",
    "name":"Photos"
};

client.postQuery("/library/sections?" + querystring.stringify(movie_section)).then(result => {
	console.log(result._children);
},function (err) {
	console.error("Could not connect to server", err);
})