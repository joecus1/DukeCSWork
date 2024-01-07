WITH temp_table(id, date, result, vote_count) AS
(SELECT v.id, v.date, v.result, COUNT(p_vote.person_id)
 FROM votes v, person_votes p_vote
 WHERE v.question = 'Election of the Speaker' AND v.id = p_vote.vote_id
GROUP BY v.id)
SELECT id, date, result, vote_count
FROM temp_table
ORDER BY date DESC LIMIT 1;