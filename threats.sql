-- Table definition
CREATE TABLE threats (
  reply_id    TEXT PRIMARY KEY,
  content     TEXT NOT NULL,
  severity    INTEGER,
  color       TEXT
);

-- Anonymized data inserts
INSERT INTO threats (reply_id, content, severity, color) VALUES
('1937098791514996831',
 'Expressed that warnings were ignored and advocated destruction of a capital city, predicting significant political fallout.',
 5, 'Red'),
('1938383368623657473',
 'Shared a link to external content without additional comment.',
 1, 'Blue'),
('1937490987737358681',
 'Commented on the ongoing conflict and desire for resolution.',
 1, 'Blue'),
('1937399612333257119',
 'Noted that objectives were unmet and predicted prolonged conflict.',
 1, 'Blue'),
('1937390674103664676',
 'Questioned previous military interventions in another region.',
 1, 'Blue'),
('1937390287149560140',
 'Suggested redeployment of personnel from allied regions to support ongoing operations.',
 1, 'Blue'),
('1937386333502374311',
 'Urged for increased provision of air defense capabilities to an ally.',
 1, 'Blue'),
('1937385413380853977',
 'Demanded immediate arms supply to an ally.',
 1, 'Blue'),
('1937105613550395823',
 'Criticized a political leader’s competence and motives regarding military leadership.',
 1, 'Blue'),
('1937062204026818873',
 'Advised service members from minority backgrounds to use protective measures and warned of unidentified hostile actors, emphasizing self-defense.',
 1, 'Blue'),
('1936603821389890019',
 'Shared a link claiming to reveal alleged intelligence agency experiments, urging belief in its authenticity.',
 1, 'Blue');
