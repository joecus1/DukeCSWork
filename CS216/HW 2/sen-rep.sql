WITH temp_table(person_id, first_name, last_name, type_count, state) AS
(SELECT p.id, p.first_name, p.last_name, COUNT(DISTINCT pr.type), pr.state
 FROM persons p, person_roles pr
 WHERE pr.state = 'NC'
    AND pr.person_id = p.id
 GROUP BY p.id)
SELECT person_id, first_name, last_name
FROM temp_table
WHERE type_count > 1;