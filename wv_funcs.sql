-- Fonction pour obtenir position aléatoire qui n'a jamais été choisie dans une partie donnée
CREATE OR REPLACE FUNCTION random_position(party_id INT) RETURNS TABLE(row INT, col INT) AS $$
DECLARE
    grid_size INT;
    chosen_row INT;
    chosen_col INT;
BEGIN
    -- Récupérer taille grille
    SELECT p.grid_size INTO grid_size FROM parties p WHERE p.id_party = party_id;

    -- Trouver une position non occupée aléatoirement
    LOOP
        chosen_row := FLOOR(RANDOM() * grid_size);
        chosen_col := FLOOR(RANDOM() * grid_size);

        -- Vérif si position est déjà prise
        IF NOT EXISTS (
            SELECT 1 FROM players_in_parties 
            WHERE id_party = party_id 
            AND current_row = chosen_row 
            AND current_col = chosen_col
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