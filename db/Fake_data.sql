-- Insert fake data for tags
INSERT INTO tags (id, tag, tag_type) VALUES
('1', '@JournalEntry[Forest]{Forest}', 'location'),
('2', '@JournalEntry[Dungeon]{Dungeon}', 'location'),
('3', '@JournalEntry[Aragon]{Aragon}', 'character'),
('4', '@JournalEntry[Gandalf]{Gandalf}', 'character'),
('5', '@JournalEntry[Dark Guild]{Dark Guild}', 'faction'),
('6', '@JournalEntry[Light Guild]{Light Guild}', 'faction')
('7', '@JournalEntry[Misty Mountain]{Misty Mountain}', 'location'),
('8', '@JournalEntry[Enchanted Forest]{Enchanted Forest}', 'location'),
('9', '@JournalEntry[Legolas]{Legolas}', 'character'),
('10', '@JournalEntry[Thranduil]{Thranduil}', 'character'),
('11', '@JournalEntry[Shadow Coven]{Shadow Coven}', 'faction'),
('12', '@JournalEntry[Knights of the Sun]{Knights of the Sun}', 'faction'),
('13', '@JournalEntry[Elven Kingdom]{Elven Kingdom}', 'location'),
('14', '@JournalEntry[Orc Camp]{Orc Camp}', 'location'),
('15', '@JournalEntry[Elrond]{Elrond}', 'character'),
('16', '@JournalEntry[Sauron]{Sauron}', 'character'),
('17', '@JournalEntry[The Fallen Order]{The Fallen Order}', 'faction'),
('18', '@JournalEntry[The Holy Alliance]{The Holy Alliance}', 'faction'),
('19', '@JournalEntry[Lake Town]{Lake Town}', 'location'),
('20', '@JournalEntry[Dragons Keep]{Dragons Keep}', 'location');

-- Insert fake data for sessions
INSERT INTO sessions (id, draft, session_state, title, summary, html, discord) VALUES
('20201011', NULL, 0, 'The Journey Begins', 'A group of adventurers embarks on their first quest.', NULL, NULL),
('20201012', NULL, 0, 'Darkness Rising', 'The heroes face a mysterious enemy.', NULL, NULL),
('20201013', NULL, 0, 'The Final Battle', 'The adventurers confront their ultimate foe.', NULL, NULL);


-- Insert fake data for characters
INSERT INTO characters (id, name, classe, tag_id, type) VALUES
('1', 'Aragon', 'Ranger', '3', 'hero'),
('2', 'Gandalf', 'Wizard', '4', 'mentor'),
('3', 'Legolas', 'Archer', '9', 'hero'),
('4', 'Thranduil', 'King', '10', 'ally'),
('5', 'Elrond', 'Scholar', '15', 'ally'),
('6', 'Sauron', 'Dark Lord', '16', 'villain');


-- Insert fake data for locations
INSERT INTO locations (id, name, region, tag_id) VALUES
('1', 'Forest', 'Greenwood Region', '1'),
('2', 'Dungeon', 'Shadowlands', '2'),
('3', 'Misty Mountain', 'Northern Peaks', '7'),
('4', 'Enchanted Forest', 'Feywild', '8'),
('5', 'Elven Kingdom', 'Lorien', '13'),
('6', 'Orc Camp', 'Wastelands', '14'),
('7', 'Lake Town', 'Rivermist Valley', '19'),
('8', 'Dragons Keep', 'Flame Mountains', '20');


-- Insert fake data for heros
INSERT INTO heros (session_id, character_id) VALUES
('20201011', '1'), -- Aragon in The Journey Begins
('20201011', '3'), -- Legolas in The Journey Begins
('20201012', '2'), -- Gandalf in Darkness Rising
('20201012', '4'), -- Thranduil in Darkness Rising
('20201013', '1'), -- Aragon in The Final Battle
('20201013', '6'); -- Sauron in The Final Battle


-- Insert fake data for encounters
INSERT INTO encounters (session_id, character_id, location_id) VALUES
('20201011', '1', '1'), -- Aragon in Forest
('20201011', '3', '2'), -- Legolas in Dungeon
('20201012', '2', '3'), -- Gandalf in Misty Mountain
('20201012', '4', '4'), -- Thranduil in Enchanted Forest
('20201013', '1', '8'), -- Aragon in Dragon's Keep
('20201013', '6', '8'); -- Sauron in Dragon's Keep


INSERT INTO sessionlocations (id, session_id, location_id, crono_index) VALUES
('1','20201011', '1', 1), -- Forest in The Journey Begins
('2','20201011', '2', 2), -- Dungeon in The Journey Begins
('3','20201012', '3', 1), -- Misty Mountain in Darkness Rising
('4','20201012', '4', 2), -- Enchanted Forest in Darkness Rising
('5','20201013', '8', 1); -- Dragon's Keep in The Final Battle


-- Insert fake data for entries
INSERT INTO entries (id, title, description, tagged_description, session_id, session_location_id, entry_index) VALUES
('E1', 'Arrival at Forest', 'The heroes enter the dense woods.', '@JournalEntry[Forest]{Forest}', '20201011', '1', 1),
('E2', 'Dungeon Delve', 'They uncover secrets in the depths.', '@JournalEntry[Dungeon]{Dungeon}', '20201011', '2', 2),
('E3', 'Misty Peaks', 'An encounter with ancient beings.', '@JournalEntry[Misty Mountain]{Misty Mountain}', '20201012', '3', 1),
('E4', 'Enchanted Secrets', 'A mysterious power is unveiled.', '@JournalEntry[Enchanted Forest]{Enchanted Forest}', '20201012', '4', 2),
('E5', 'Final Confrontation', 'The battle against Sauron begins.', '@JournalEntry[Dragons Keep]{Dragons Keep}', '20201013', '5', 1);


-- Insert fake data for key_events
INSERT INTO key_events (title, impact, session_id) VALUES
('Heroic Encounter', 'The heroes bond while facing danger.', '20201011'),
('Dark Revelation', 'The enemy’s motives are uncovered.', '20201012'),
('Climactic Battle', 'The fate of the realm is decided.', '20201013');


-- Insert fake data for factions
INSERT INTO factions (id, name, description, tag_id) VALUES
('1', 'Dark Guild', 'A mysterious and malevolent group operating in the shadows.', '5'),
('2', 'Light Guild', 'A benevolent faction devoted to justice and order.', '6'),
('3', 'Shadow Coven', 'A cabal of dark magic users pursuing forbidden knowledge.', '11'),
('4', 'Knights of the Sun', 'An honorable order of warriors dedicated to protecting the realm.', '12'),
('5', 'The Fallen Order', 'A faction of exiled knights seeking revenge on the kingdom.', '17'),
('6', 'The Holy Alliance', 'A coalition of factions united under a common cause of peace.', '18');


-- Insert fake data for members
INSERT INTO members (character_id, faction_id) VALUES
('1', '2'), -- Aragon in Light Guild
('3', '2'), -- Legolas in Light Guild
('4', '2'), -- Thranduil in Light Guild
('6', '1'); -- Sauron in Dark Guild


-- Insert fake data for relatedevents
INSERT INTO relatedevents (event_id, character_id) VALUES
('E1', '1'), -- Aragon related to Arrival at Forest
('E2', '3'), -- Legolas related to Dungeon Delve
('E3', '2'), -- Gandalf related to Misty Peaks
('E4', '4'), -- Thranduil related to Enchanted Secrets
('E5', '6'); -- Sauron related to Final Confrontation


