-- Table des parties
CREATE TABLE parties (
    id_party SERIAL PRIMARY KEY,
    title_party VARCHAR(100) NOT NULL,
    grid_rows INT NOT NULL DEFAULT 10,          
    grid_cols INT NOT NULL DEFAULT 10,
    obstacles_count INT NOT NULL DEFAULT 0,  -- Ajouté cette ligne
    max_players INT NOT NULL DEFAULT 8,
    max_turns INT NOT NULL DEFAULT 30,
    turn_duration INT NOT NULL DEFAULT 60, -- en secondes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_started BOOLEAN DEFAULT FALSE,
    is_finished BOOLEAN DEFAULT FALSE
);

-- Table des rôles
CREATE TABLE roles (
    id_role SERIAL PRIMARY KEY,
    role_name VARCHAR(10) NOT NULL UNIQUE,
    description_role TEXT NOT NULL
);

-- Table des joueurs
CREATE TABLE players (
    id_player SERIAL PRIMARY KEY,
    pseudo VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_online TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison joueurs-parties
CREATE TABLE players_in_parties (
    id_party INT NOT NULL REFERENCES parties(id_party) ON DELETE CASCADE,
    id_player INT NOT NULL REFERENCES players(id_player) ON DELETE CASCADE,
    id_role INT NOT NULL REFERENCES roles(id_role),
    is_alive BOOLEAN DEFAULT TRUE,
    current_row INT,
    current_col INT,
    PRIMARY KEY (id_party, id_player)
);

-- Table des tours
CREATE TABLE turns (
    id_turn SERIAL PRIMARY KEY,
    id_party INT NOT NULL REFERENCES parties(id_party) ON DELETE CASCADE,
    turn_number INT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    UNIQUE (id_party, turn_number)
);

-- Table des obstacles
CREATE TABLE obstacles (
    id_obstacle SERIAL PRIMARY KEY,
    id_party INT NOT NULL REFERENCES parties(id_party) ON DELETE CASCADE,
    row INT NOT NULL,
    col INT NOT NULL,
    UNIQUE (id_party, row, col) 
);

-- Table des actions des joueurs
CREATE TABLE players_play (
    id SERIAL PRIMARY KEY,
    id_player INT NOT NULL,
    id_turn INT NOT NULL REFERENCES turns(id_turn) ON DELETE CASCADE,
    id_party INT NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('move', 'attack', 'pass')),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    origin_position_row INT NOT NULL,
    origin_position_col INT NOT NULL,
    target_position_row INT,
    target_position_col INT,
    FOREIGN KEY (id_party, id_player) REFERENCES players_in_parties(id_party, id_player)
);