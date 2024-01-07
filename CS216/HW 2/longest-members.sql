SELECT id, first_name, last_name, birthday,
       (SELECT SUM(end_date - start_date)
        FROM person_roles r
        WHERE r.person_id = p.id) AS duration
FROM persons p
ORDER BY duration DESC LIMIT 10;
