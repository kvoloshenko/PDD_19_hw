CREATE TABLE hh_requests (
    id       INTEGER       PRIMARY KEY AUTOINCREMENT
                           NOT NULL
                           UNIQUE,
    keywords VARCHAR (256) NOT NULL
);

CREATE TABLE hh_responses (
    id            INTEGER      PRIMARY KEY AUTOINCREMENT
                               NOT NULL
                               UNIQUE,
    requests_id                REFERENCES hh_requests (id) 
                               NOT NULL,
    skill_name    VARCHAR (50) NOT NULL,
    skill_count   INTEGER      NOT NULL,
    skill_persent INTEGER      NOT NULL
);
