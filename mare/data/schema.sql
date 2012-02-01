CREATE TABLE stats (
        uid INTEGER NOT NULL,
        user_uid INTEGER,
        video_id INTEGER,
        watched INTEGER,
        status INTEGER,
        PRIMARY KEY (uid),
        FOREIGN KEY(user_uid) REFERENCES user (uid),
        FOREIGN KEY(video_id) REFERENCES video (id)
);
CREATE TABLE user (
        uid INTEGER NOT NULL,
        name VARCHAR,
        email VARCHAR,
        password VARCHAR,
        brokernum INTEGER,
        PRIMARY KEY (uid)
);
CREATE TABLE video (
        id INTEGER NOT NULL,
        module VARCHAR(250),
        duration INTEGER,
        title VARCHAR(250),
        PRIMARY KEY (id)
);
