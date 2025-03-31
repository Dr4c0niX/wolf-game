-- Insérer des données de test dans une partie donnée
CREATE OR REPLACE PROCEDURE SEED_DATA(NB_PLAYERS INT, PARTY_ID INT) AS $$
DECLARE
    i INT;
    new_player_id INT;
    new_role_id INT;
    new_row INT;
    new_col INT;
BEGIN
    FOR i IN 1..NB_PLAYERS LOOP
        -- Insert joueur fictif
        INSERT INTO players (pseudo) 
        VALUES ('player_' || i) 
        RETURNING id_player INTO new_player_id;

        -- Assigner rôle aléatoire
        SELECT random_role(PARTY_ID) INTO new_role_id;

        -- Trouver une position libre
        SELECT * INTO new_row, new_col FROM random_position(PARTY_ID);

        -- Insérer le joueur dans la partie
        INSERT INTO players_in_parties (id_party, id_player, id_role, current_row, current_col) 
        VALUES (PARTY_ID, new_player_id, new_role_id, new_row, new_col);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Compléter un tour en appliquant les demandes de déplacement
CREATE OR REPLACE PROCEDURE COMPLETE_TOUR(TOUR_ID INT, PARTY_ID INT) AS $$
DECLARE
    rec RECORD;
    existing_player INT;
BEGIN
    FOR rec IN (
        SELECT pp.id_player, pp.origin_position_row, pp.origin_position_col, 
               pp.target_position_row, pp.target_position_col
        FROM players_play pp
        WHERE pp.id_turn = TOUR_ID AND pp.id_party = PARTY_ID
        ORDER BY pp.start_time
    ) LOOP
        IF EXISTS (
            SELECT 1 
            FROM obstacles o 
            WHERE o.id_party = PARTY_ID 
              AND o.row = rec.target_position_row 
              AND o.col = rec.target_position_col
        ) THEN
            RAISE NOTICE 'Déplacement impossible : obstacle à la position (% ,%)', rec.target_position_row, rec.target_position_col;
        ELSE
            SELECT id_player INTO existing_player
            FROM players_in_parties
            WHERE id_party = PARTY_ID AND current_row = rec.target_position_row AND current_col = rec.target_position_col;
            IF existing_player IS NULL THEN
                UPDATE players_in_parties
                SET current_row = rec.target_position_row, current_col = rec.target_position_col
                WHERE id_party = PARTY_ID AND id_player = rec.id_player;
            ELSE
                DELETE FROM players_in_parties
                WHERE id_party = PARTY_ID AND id_player = existing_player;
            END IF;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Pseudos en minuscules
CREATE OR REPLACE PROCEDURE USERNAME_TO_LOWER() AS $$
BEGIN
    UPDATE players SET pseudo = LOWER(pseudo);
END;
$$ LANGUAGE plpgsql;