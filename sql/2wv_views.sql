-- Vues pour chaque table

-- Vue pour la table parties
CREATE VIEW v_parties AS
SELECT * FROM parties;

-- Vue pour la table roles
CREATE VIEW v_roles AS
SELECT * FROM roles;

-- Vue pour la table players
CREATE VIEW v_players AS
SELECT * FROM players;

-- Vue pour la table players_in_parties
CREATE VIEW v_players_in_parties AS
SELECT * FROM players_in_parties;

-- Vue pour la table turns
CREATE VIEW v_turns AS
SELECT * FROM turns;

-- Vue pour la table players_play
CREATE VIEW v_players_play AS
SELECT * FROM players_play;


-- Vues supplémentaires demandées

-- Vue ALL_PLAYERS
CREATE VIEW ALL_PLAYERS AS
SELECT 
    p.pseudo AS player_name,
    COUNT(DISTINCT pip.id_party) AS number_of_games_played,
    COUNT(DISTINCT pp.id_turn) AS number_of_turns_played,
    MIN(p.created_at) AS first_participation_date,
    MAX(pp.start_time) AS last_action_date
FROM players p
JOIN players_in_parties pip ON pip.id_player = p.id_player
JOIN players_play pp ON pp.id_player = p.id_player
GROUP BY p.pseudo
ORDER BY number_of_games_played DESC, first_participation_date ASC, last_action_date DESC, player_name ASC;

-- Vue ALL_PLAYERS_ELAPSED_GAME
CREATE VIEW ALL_PLAYERS_ELAPSED_GAME AS
SELECT
    p.pseudo AS player_name,
    pa.title_party AS party_name,
    COUNT(DISTINCT pip.id_player) AS number_of_participants,
    MIN(pp.start_time) AS first_action_time,
    MAX(pp.end_time) AS last_action_time,
    EXTRACT(EPOCH FROM (MAX(pp.end_time) - MIN(pp.start_time))) AS elapsed_seconds
FROM players p
JOIN players_in_parties pip ON pip.id_player = p.id_player
JOIN parties pa ON pa.id_party = pip.id_party
JOIN players_play pp ON pp.id_player = p.id_player AND pp.id_party = pa.id_party
GROUP BY p.pseudo, pa.title_party
ORDER BY player_name ASC, party_name ASC;

-- Vue ALL_PLAYERS_ELAPSED_TOUR
CREATE VIEW ALL_PLAYERS_ELAPSED_TOUR AS
SELECT 
    p.pseudo AS player_name,
    pa.title_party AS party_name,
    t.turn_number AS turn_number,
    t.start_time AS turn_start_time,
    pp.start_time AS decision_time,
    EXTRACT(EPOCH FROM (pp.start_time - t.start_time)) AS decision_time_seconds
FROM players p
JOIN players_in_parties pip ON pip.id_player = p.id_player
JOIN parties pa ON pa.id_party = pip.id_party
JOIN turns t ON t.id_party = pa.id_party
JOIN players_play pp ON pp.id_player = p.id_player AND pp.id_turn = t.id_turn AND pp.id_party = pa.id_party
ORDER BY player_name ASC, party_name ASC, turn_number ASC;

CREATE VIEW ALL_PLAYERS_STATS AS
WITH party_turns AS (
    SELECT 
        pa.id_party,
        COUNT(DISTINCT t.turn_number) AS total_turns
    FROM parties pa
    LEFT JOIN turns t ON t.id_party = pa.id_party
    GROUP BY pa.id_party
)
SELECT
    p.pseudo AS player_name,
    r.role_name AS player_role,
    pa.title_party AS party_name,
    COUNT(DISTINCT t.turn_number) AS number_of_turns_played,
    pt.total_turns AS total_turns_in_party,
    CASE
        WHEN pa.is_finished AND r.role_name = 'loup' THEN 'Loup gagnant'
        WHEN pa.is_finished AND r.role_name = 'villageois' THEN 'Villageois gagnant'
        ELSE 'En cours'
    END AS winner,
    AVG(EXTRACT(EPOCH FROM (pp.start_time - t.start_time))) AS avg_decision_time_seconds
FROM players p
JOIN players_in_parties pip ON pip.id_player = p.id_player
JOIN roles r ON r.id_role = pip.id_role
JOIN parties pa ON pa.id_party = pip.id_party
JOIN turns t ON t.id_party = pa.id_party
JOIN players_play pp ON pp.id_player = p.id_player AND pp.id_turn = t.id_turn AND pp.id_party = pa.id_party
JOIN party_turns pt ON pt.id_party = pa.id_party
GROUP BY p.pseudo, r.role_name, pa.title_party, pa.is_finished, pt.total_turns
ORDER BY player_name ASC, party_name ASC, number_of_turns_played DESC;