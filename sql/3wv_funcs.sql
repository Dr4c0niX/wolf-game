CREATE OR REPLACE FUNCTION random_position(party_id INT) 
RETURNS SETOF RECORD AS $$
DECLARE
    grid_size INT;
    chosen_row INT;
    chosen_col INT;
BEGIN
    -- Récupérer la taille de la grille
    SELECT p.grid_size INTO grid_size 
    FROM parties p 
    WHERE p.id_party = party_id;

    -- Trouver une position non occupée aléatoirement
    LOOP
        chosen_row := FLOOR(RANDOM() * grid_size);
        chosen_col := FLOOR(RANDOM() * grid_size);

        -- Vérifier position est déjà prise par un joueur / obstacle
        IF NOT EXISTS (
            SELECT 1 
            FROM players_in_parties 
            WHERE id_party = party_id 
            AND current_row = chosen_row 
            AND current_col = chosen_col
        ) 
        AND NOT EXISTS (
            SELECT 1
            FROM obstacles o
            WHERE o.id_party = party_id 
            AND o.row = chosen_row 
            AND o.col = chosen_col
        ) THEN
            EXIT;
        END IF;
    END LOOP;

    RETURN QUERY SELECT chosen_row, chosen_col;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour attribuer rôle random en respectant l'équilibre loup/villageois
CREATE OR REPLACE FUNCTION random_role(party_id INT) RETURNS INT AS $$
DECLARE
    total_players INT;
    total_wolves INT;
    total_villagers INT;
    role_id INT;
BEGIN
    -- Compter les joueurs déjà inscrits
    SELECT COUNT(*) INTO total_players FROM players_in_parties WHERE id_party = party_id;

    -- Nb loups + villageois dans la partie
    SELECT 
        COUNT(CASE WHEN r.role_name = 'loup' THEN 1 END), 
        COUNT(CASE WHEN r.role_name = 'villageois' THEN 1 END)
    INTO total_wolves, total_villagers
    FROM players_in_parties pip
    JOIN roles r ON pip.id_role = r.id_role
    WHERE pip.id_party = party_id;

    -- Répartition équilibrée (exemple : 25% loups, 75% villageois)
    IF total_wolves < total_players / 4 THEN
        SELECT id_role INTO role_id FROM roles WHERE role_name = 'loup';
    ELSE
        SELECT id_role INTO role_id FROM roles WHERE role_name = 'villageois';
    END IF;

    RETURN role_id;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour récup les infos du vainqueur d'une partie donnée
CREATE OR REPLACE FUNCTION get_the_winner(party_id INT) RETURNS TABLE(
    player_name VARCHAR,
    role_name VARCHAR,
    party_name VARCHAR,
    turns_played INT,
    total_turns INT,
    avg_decision_time INTERVAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.pseudo AS player_name,
        r.role_name AS role_name,
        pa.title_party AS party_name,
        COUNT(DISTINCT t.id_turn) AS turns_played,
        pa.max_turns AS total_turns,
        AVG(pp.end_time - pp.start_time) AS avg_decision_time
    FROM players_in_parties pip
    JOIN players p ON pip.id_player = p.id_player
    JOIN roles r ON pip.id_role = r.id_role
    JOIN parties pa ON pip.id_party = pa.id_party
    JOIN players_play pp ON pip.id_player = pp.id_player AND pip.id_party = pp.id_party
    JOIN turns t ON pp.id_turn = t.id_turn
    WHERE pip.id_party = party_id
    AND pip.is_alive = TRUE
    GROUP BY p.pseudo, r.role_name, pa.title_party, pa.max_turns
    ORDER BY turns_played DESC, avg_decision_time ASC
    LIMIT 1;  -- Sélectionne le joueur le plus performant
END;
$$ LANGUAGE plpgsql;