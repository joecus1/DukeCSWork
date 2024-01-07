SELECT p.first_name, p.last_name, p.birthday, MIN(pr.start_date) AS start_date,
    MAX(pr.end_date) AS end_date
FROM persons p, person_roles pr
WHERE pr.party = 'Democrat'
    AND pr.person_id = p.id
    AND pr.state = 'NC'
    AND pr.type = 'sen'
GROUP BY pr.person_id
ORDER BY start_date DESC;