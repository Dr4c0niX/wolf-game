-- Appeler COMPLETE_TOUR lorsque le tour est marqué terminé
CREATE OR REPLACE FUNCTION call_complete_tour()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM COMPLETE_TOUR(NEW.id_turn, NEW.id_party);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_complete_tour
AFTER UPDATE ON turns
FOR EACH ROW
WHEN (OLD.end_time IS NULL AND NEW.end_time IS NOT NULL)
EXECUTE FUNCTION call_complete_tour();


-- Appeler USERNAME_TO_LOWER lorsqu'un joueur s'inscrit
CREATE OR REPLACE FUNCTION call_username_to_lower()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM USERNAME_TO_LOWER();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_username_to_lower
AFTER INSERT ON players
FOR EACH ROW
EXECUTE FUNCTION call_username_to_lower();