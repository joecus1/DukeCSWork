WITH votes_compare(vote_id, vote1, vote2) AS
(SELECT v1.vote_id, v1.vote, v2.vote
 FROM votes v, persons p1, persons p2, person_votes v1, person_votes v2
 WHERE v.chamber = 'h' AND (v.session = 2015 or v.session = 2016)
   AND p1.last_name = 'Butterfield' AND p2.last_name = 'Pelosi'
   AND v1.person_id = p1.id AND v2.person_id = p2.id
   AND v1.vote_id = v2.vote_id AND v.id = v1.vote_id)
SELECT COUNT(*) AS agree,
       (SELECT COUNT(*) FROM votes_compare) AS total,
       COUNT(*)*100.00 / (SELECT COUNT(*) FROM votes_compare) AS percent
FROM votes_compare
WHERE vote1 = vote2;
