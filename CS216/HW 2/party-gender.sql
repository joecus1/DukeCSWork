SELECT party, gender, COUNT(*)
FROM cur_members
GROUP BY party, gender;
