-- Vérif que le nombre de joueurs est supérieur à 0
ALTER TABLE parties
ADD CONSTRAINT check_max_players CHECK (max_players > 0);

-- Vérif que la durée du tour est positive (en secondes)
ALTER TABLE parties
ADD CONSTRAINT check_turn_duration CHECK (turn_duration > 0);

-- Vérif que last_online est avant la date actuelle
ALTER TABLE players
ADD CONSTRAINT check_last_online CHECK (last_online <= CURRENT_TIMESTAMP);

-- Parties
CREATE INDEX idx_parties_status ON parties(is_started, is_finished);
CREATE INDEX idx_parties_created ON parties(created_at);
CREATE INDEX idx_parties_rows_cols ON parties(grid_rows, grid_cols);
CREATE INDEX idx_parties_players ON parties(max_players);

-- Roles
CREATE INDEX idx_roles_name ON roles(role_name);

-- Players
CREATE INDEX idx_players_pseudo ON players(pseudo);
CREATE INDEX idx_players_activity ON players(last_online);
CREATE INDEX idx_players_created ON players(created_at);

-- players_in_parties
CREATE INDEX idx_pip_party ON players_in_parties(id_party);
CREATE INDEX idx_pip_player ON players_in_parties(id_player);
CREATE INDEX idx_pip_role ON players_in_parties(id_role);
CREATE INDEX idx_pip_alive ON players_in_parties(is_alive) WHERE is_alive = TRUE;
CREATE INDEX idx_pip_position ON players_in_parties(current_row, current_col);
CREATE INDEX idx_pip_party_role ON players_in_parties(id_party, id_role);
CREATE INDEX idx_pip_party_player ON players_in_parties(id_party, id_player);

-- Turns
CREATE INDEX idx_turns_party ON turns(id_party);
CREATE INDEX idx_turns_number ON turns(turn_number);
CREATE INDEX idx_turns_time_range ON turns(start_time, end_time);
CREATE INDEX idx_turns_party_number ON turns(id_party, turn_number);

-- players_play
CREATE INDEX idx_pp_turn ON players_play(id_turn);
CREATE INDEX idx_pp_player ON players_play(id_player);
CREATE INDEX idx_pp_party ON players_play(id_party);
CREATE INDEX idx_pp_action_type ON players_play(action);
CREATE INDEX idx_pp_timing ON players_play(start_time, end_time);
CREATE INDEX idx_pp_origin_pos ON players_play(origin_position_row, origin_position_col);
CREATE INDEX idx_pp_target_pos ON players_play(target_position_row, target_position_col);
CREATE INDEX idx_pp_player_turn ON players_play(id_player, id_turn);
CREATE INDEX idx_pp_party_turn ON players_play(id_party, id_turn);

-- Obstacles
CREATE INDEX idx_obstacles_position ON obstacles(id_party, position_row, position_col);
CREATE INDEX idx_obstacles_party ON obstacles(id_party);

-- Requêtes fréquentes
CREATE INDEX idx_pp_action_positions ON players_play(
    action, 
    origin_position_row, 
    origin_position_col, 
    target_position_row, 
    target_position_col
);

-- Actions de mouvement
CREATE INDEX idx_pp_move_actions ON players_play(id_party, id_player)
WHERE action = 'move';

-- Actions d'attaque
CREATE INDEX idx_pp_attack_actions ON players_play(id_party, id_player)
WHERE action = 'attack';

-- Requêtes de vérification de position
CREATE INDEX idx_position_verification ON players_in_parties(
    id_party, 
    current_row, 
    current_col, 
    is_alive
);