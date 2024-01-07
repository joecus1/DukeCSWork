CREATE TABLE states (
  id CHAR(2) NOT NULL PRIMARY KEY
);
CREATE TABLE persons (
  id CHAR(10) NOT NULL PRIMARY KEY, -- bioguide id
  id_govtrack INTEGER NOT NULL UNIQUE, -- govtrack id; useful just in case
  id_lis CHAR(4), -- senate LIS id; useful just in case
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50),
  last_name VARCHAR(50) NOT NULL,
  birthday DATE,
  gender CHAR(1) CHECK (gender IS NULL OR gender IN ('F', 'M')),
  religion VARCHAR(50)
);
CREATE TABLE person_roles (
  person_id CHAR(10) NOT NULL REFERENCES persons(id),
  type CHAR(3) NOT NULL CHECK (type IN ('rep', 'sen')),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  state CHAR(2) NOT NULL REFERENCES states(id),
  district INTEGER
    CHECK ((type = 'rep' AND district IS NOT NULL) OR (type = 'sen')),
  party VARCHAR(50)
  -- Recent values are one of 'Democrat', 'Republican', and
  -- 'Independent', but there has been many partiies historically.
);
CREATE TABLE votes (
  id CHAR(20) NOT NULL PRIMARY KEY,
  category VARCHAR(50) NOT NULL,
  chamber CHAR(1) NOT NULL CHECK (chamber IN ('h', 's')),
  session INTEGER NOT NULL,
  date DATE NOT NULL,
  number INTEGER NOT NULL,
  question TEXT NOT NULL,
  subject TEXT,
  type TEXT NOT NULL,
  result TEXT NOT NULL,
  UNIQUE (chamber, session, number)
);
CREATE TABLE bills (
  id CHAR(20) NOT NULL PRIMARY KEY,
  session INTEGER NOT NULL,
  type VARCHAR(10) NOT NULL,
  number INTEGER NOT NULL,
  status TEXT NOT NULL,
  status_at TIMESTAMP WITH TIME ZONE NOT NULL,
  official_title TEXT NOT NULL,
  popular_title TEXT,
  short_title TEXT,
  UNIQUE (session, type, number)
);
CREATE TABLE votes_re_bills (
  vote_id CHAR(20) NOT NULL PRIMARY KEY REFERENCES votes(id),
  bill_id CHAR(20) NOT NULL REFERENCES bills(id)
);
CREATE TABLE votes_re_amendments (
  vote_id CHAR(20) NOT NULL PRIMARY KEY REFERENCES votes(id),
  -- Uncomment below if we load the amendments data:
  amendment_id CHAR(20) NOT NULL -- REFERENCES amendments(id)
);
CREATE TABLE votes_re_nominations (
  vote_id CHAR(20) NOT NULL PRIMARY KEY REFERENCES votes(id),
  nomination_number INTEGER NOT NULL,
  nomination_title TEXT NOT NULL
);
CREATE TABLE person_votes (
  vote_id CHAR(20) NOT NULL REFERENCES votes(id),
  person_id CHAR(10) NOT NULL REFERENCES persons(id),
  vote VARCHAR(50) NOT NULL,
  -- Most of the time votes are one of Yea(Aye), Nay(No), Present, and Not Voting
  -- (https://www.govtrack.us/blog/2009/11/18/aye-versus-yea-whats-the-difference/).
  -- However, occasionally we also have other kind of votes, e.g., the
  -- "leadership" vote of 2013/h2 that elected Boehner as the Speaker.
  PRIMARY KEY (vote_id, person_id)
);
CREATE VIEW cur_members AS
SELECT p.id, p.first_name, p.last_name, p.gender, p.birthday, p.religion,
       r.type, r.party, r.state
FROM persons p, person_roles r
WHERE p.id = r.person_id
AND r.start_date <= DATE('2019-01-01')
AND DATE('2019-01-01') <= r.end_date;


.separator "|"
.mode column
.headers on
.import load/states.dat states
.import load/persons.dat persons
.import load/person_roles.dat person_roles
.import load/votes.dat votes
.import load/bills.dat bills
.import load/votes_re_bills.dat votes_re_bills
.import load/votes_re_amendments.dat votes_re_amendments
.import load/votes_re_nominations.dat votes_re_nominations
.import load/person_votes.dat person_votes
