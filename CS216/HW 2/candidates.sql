SELECT vote
FROM person_votes
WHERE vote_id = 'h581-114.2015'
    AND NOT vote = 'Not Voting'
GROUP BY vote;