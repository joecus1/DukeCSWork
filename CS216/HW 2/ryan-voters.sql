WITH temp_table(person_id, state) AS
(SELECT pv.person_id, pr.state
FROM person_votes pv, person_roles pr
WHERE pv.vote_id = 'h581-114.2015'
    AND pv.person_id = pr.person_id
    AND pv.vote = 'Ryan (WI)')
SELECT state, COUNT(DISTINCT person_id)
FROM temp_table
GROUP BY state;