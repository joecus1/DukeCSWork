
SELECT first_name, last_name, birthday, gender
    FROM persons
    WHERE gender = 'F'
    AND birthday >= '1970-01-01'
    AND birthday < '1980-01-01'
