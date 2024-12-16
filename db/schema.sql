-- Table: sessions
CREATE TABLE sessions (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    draft TEXT,
    session_state INTEGER DEFAULT 0, -- Default state is 0
    title TEXT,
    summary TEXT,
    html TEXT,
    discord TEXT
);

-- Table: characters
CREATE TABLE characters (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    name TEXT NOT NULL, -- Cannot be null
    classe TEXT,
    tag_id TEXT, -- References tags.id
    type TEXT,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE SET NULL
);

-- Table: locations
CREATE TABLE locations (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    name TEXT NOT NULL, -- Cannot be null
    region TEXT,
    tag_id TEXT, -- References tags.id
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE SET NULL
);

-- Table: heros
CREATE TABLE heros (
    session_id TEXT NOT NULL, -- Link to sessions.id
    character_id TEXT NOT NULL, -- Link to characters.id
    PRIMARY KEY (session_id, character_id), -- Composite primary key to avoid duplicate entries
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE,
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE
);

-- Table: encounters
CREATE TABLE encounters (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    session_id TEXT NOT NULL, -- Link to sessions.id
    character_id TEXT NOT NULL, -- Link to characters.id
    location_id TEXT NOT NULL, -- Link to locations.id
    PRIMARY KEY (session_id, character_id, location_id), -- Composite primary key
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE,
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE
);

-- Table: entries
CREATE TABLE entries (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    title TEXT,
    description TEXT,
    tagged_description TEXT,
    session_id TEXT NOT NULL, -- Link to sessions.id
    session_location_id TEXT NOT NULL, -- Link to sessionlocations.id
    entry_index INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE,
    FOREIGN KEY (session_location_id) REFERENCES sessionlocations (id) ON DELETE CASCADE
);


-- Table: key_events
CREATE TABLE key_events (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    title TEXT,
    impact TEXT,
    session_id TEXT NOT NULL, -- Link to sessions.id
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
);

-- Table: factions
CREATE TABLE factions (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    name TEXT NOT NULL, -- Name cannot be null
    description TEXT, -- Optional description
    tag_id TEXT, -- References tags.id
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE SET NULL
);

-- Table: members
CREATE TABLE members (
    character_id TEXT NOT NULL, -- Link to characters.id
    faction_id TEXT NOT NULL, -- Link to factions.id
    PRIMARY KEY (character_id, faction_id), -- Composite primary key to avoid duplicate entries
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE, -- Ensure referential integrity
    FOREIGN KEY (faction_id) REFERENCES factions (id) ON DELETE CASCADE -- Ensure referential integrity
);

-- Table: relatedevents
CREATE TABLE relatedevents (
    entry_id TEXT NOT NULL, -- Reference to an event (could refer to key_events or other future tables)
    character_id TEXT NOT NULL, -- Link to characters.id
    PRIMARY KEY (event_id, character_id), -- Composite primary key
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE -- Ensure referential integrity
    FOREIGN KEY (entry_id) REFERENCES entries (id) ON DELETE CASCADE -- Ensure referential integrity
);

-- Table: sessionlocations
CREATE TABLE sessionlocations (
    id TEXT PRIMARY KEY NOT NULL, -- Unique identifier for each visit to a location
    session_id TEXT NOT NULL, -- Link to sessions.id
    location_id TEXT NOT NULL, -- Link to locations.id
    crono_index INTEGER NOT NULL, -- Can be non-unique to allow flexibility for reordering
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE
);


-- Table: tags
CREATE TABLE tags (
    id TEXT PRIMARY KEY NOT NULL, -- Unique and cannot be null
    tag TEXT NOT NULL, -- Cannot be null
    tag_type TEXT NOT NULL -- Cannot be null (location, character, faction, item, ...)
);
