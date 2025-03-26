-- Création des tables de base

CREATE TABLE players (
    id_player SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    last_online TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parties (
    id_party SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rows INT NOT NULL CHECK (rows BETWEEN 5 AND 100),
    cols INT NOT NULL CHECK (cols BETWEEN 5 AND 100),
    max_players INT NOT NULL CHECK (max_players BETWEEN 2 AND 50),
    max_turns INT NOT NULL CHECK (max_turns BETWEEN 10 AND 200),
    turn_duration INT NOT NULL CHECK (turn_duration BETWEEN 10 AND 300),
    nb_obstacles INT NOT NULL CHECK (nb_obstacles >= 0),
    nb_wolves INT NOT NULL CHECK (nb_wolves >= 1),
    nb_villagers INT NOT NULL CHECK (nb_villagers >= 1),
    started BOOLEAN DEFAULT FALSE,
    finished BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CHECK (nb_wolves + nb_villagers <= max_players)
);

CREATE TABLE player_party (
    id_player_party SERIAL PRIMARY KEY,
    id_player INT REFERENCES players(id_player),
    id_party INT REFERENCES parties(id_party),
    role VARCHAR(10) CHECK (role IN ('wolf', 'villager')),
    is_npc BOOLEAN DEFAULT FALSE,
    is_alive BOOLEAN DEFAULT TRUE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_player, id_party)
);

CREATE TABLE obstacles (
    id_obstacle SERIAL PRIMARY KEY,
    id_party INT REFERENCES parties(id_party),
    row INT NOT NULL,
    col INT NOT NULL,
    UNIQUE(id_party, row, col)
);

CREATE TABLE turns (
    id_turn SERIAL PRIMARY KEY,
    id_party INT REFERENCES parties(id_party),
    turn_number INT NOT NULL,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    UNIQUE(id_party, turn_number)
);

CREATE TABLE positions (
    id_position SERIAL PRIMARY KEY,
    id_player_party INT REFERENCES player_party(id_player_party),
    id_turn INT REFERENCES turns(id_turn),
    row INT NOT NULL,
    col INT NOT NULL,
    UNIQUE(id_player_party, id_turn)
);

CREATE TABLE moves (
    id_move SERIAL PRIMARY KEY,
    id_player_party INT REFERENCES player_party(id_player_party),
    id_turn INT REFERENCES turns(id_turn),
    row_delta INT NOT NULL CHECK (row_delta BETWEEN -1 AND 1),
    col_delta INT NOT NULL CHECK (col_delta BETWEEN -1 AND 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_player_party, id_turn)
);
