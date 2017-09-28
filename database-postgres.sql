CREATE TABLE faq (
    broadcaster VARCHAR NOT NULL PRIMARY KEY,
    faq VARCHAR NOT NULL 
);

CREATE TABLE faq_game (
    broadcaster VARCHAR NOT NULL,
    twitchGame VARCHAR NOT NULL,
    faq VARCHAR NOT NULL,
    PRIMARY KEY (broadcaster, twitchGame)
);

CREATE TABLE highlight_marker (
    id SERIAL NOT NULL PRIMARY KEY,
    broadcaster VARCHAR NOT NULL,
    broadcastId BIGINT NOT NULL,
    broadcastTime TIMESTAMP NOT NULL,
    markedTime TIMESTAMP NOT NULL,
    reason VARCHAR NULL
);
CREATE INDEX highlight_broadcaster ON highlight_marker (broadcaster);

CREATE TABLE quotes (
    quoteId SERIAL NOT NULL PRIMARY KEY,
    broadcaster VARCHAR NOT NULL,
    quote VARCHAR NOT NULL
);
CREATE INDEX quotes_broadcaster ON quotes (broadcaster);

CREATE TABLE auto_purge (
    broadcaster VARCHAR NOT NULL,
    twitchUser VARCHAR NOT NULL,
    stopcommands BOOLEAN NOT NULL,
    PRIMARY KEY (broadcaster, twitchUser)
);

CREATE TABLE auto_ban_words (
    broadcaster VARCHAR NOT NULL,
    word VARCHAR NOT NULL,
    PRIMARY KEY (broadcaster, word)
);

CREATE TABLE url_whitelist (
    broadcaster VARCHAR NOT NULL,
    urlMatch VARCHAR NOT NULL,
    PRIMARY KEY (broadcaster, urlMatch)
);

CREATE TABLE quotes_tags (
    quoteId INTEGER NOT NULL,
    tag VARCHAR NOT NULL,
    PRIMARY KEY (quoteId, tag),
    FOREIGN KEY (quoteId) REFERENCES quotes(quoteId)
        ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX quotes_tags_id ON quotes_tags (quoteId);

CREATE TABLE quotes_history (
    id SERIAL NOT NULL PRIMARY KEY,
    quoteId INTEGER NOT NULL,
    createdTime TIMESTAMP NOT NULL,
    broadcaster VARCHAR NOT NULL,
    quote VARCHAR NOT NULL,
    editor VARCHAR NOT NULL
);
CREATE INDEX quotes_history_broadcaster ON quotes_history (broadcaster);

CREATE TABLE warp_world (
    broadcaster VARCHAR NOT NULL PRIMARY KEY,
    secretkey VARCHAR
);
