Table sessions {
  id TEXT [primary key, not null]
  draft TEXT
  session_state INTEGER [default: 0]
  title TEXT
  summary TEXT
  html TEXT
  discord TEXT
}

Table characters {
  id TEXT [primary key, not null]
  name TEXT [not null]
  classe TEXT
  tag_id TEXT
  type TEXT
}

Table locations {
  id TEXT [primary key, not null]
  name TEXT [not null]
  region TEXT
  tag_id TEXT
}

Table heros {
  session_id TEXT [not null]
  character_id TEXT [not null]
  primary key (session_id, character_id)
}

Table encounters {
  id TEXT [primary key, not null]
  session_id TEXT [not null]
  character_id TEXT [not null]
  location_id TEXT [not null]
  primary key (session_id, character_id, location_id)
}

Table entries {
  id TEXT [primary key, not null]
  title TEXT
  description TEXT
  tagged_description TEXT
  session_id TEXT [not null]
  session_location_id TEXT [not null]
  entry_index INTEGER
}

Table key_events {
  id TEXT [primary key, not null]
  title TEXT
  impact TEXT
  session_id TEXT [not null]
}

Table factions {
  id TEXT [primary key, not null]
  name TEXT [not null]
  description TEXT
  tag_id TEXT
}

Table members {
  character_id TEXT [not null]
  faction_id TEXT [not null]
  primary key (character_id, faction_id)
}

Table relatedevents {
  entry_id TEXT [not null]
  character_id TEXT [not null]
  primary key (entry_id, character_id)
}

Table sessionlocations {
  id TEXT [primary key, not null]
  session_id TEXT [not null]
  location_id TEXT [not null]
  crono_index INTEGER [not null]
}

Table tags {
  id TEXT [primary key, not null]
  tag TEXT [not null]
  tag_type TEXT [not null]
}

Ref: characters.tag_id > tags.id
Ref: locations.tag_id > tags.id
Ref: heros.session_id > sessions.id
Ref: heros.character_id > characters.id
Ref: encounters.session_id > sessions.id
Ref: encounters.character_id > characters.id
Ref: encounters.location_id > locations.id
Ref: entries.session_id > sessions.id
Ref: entries.session_location_id > sessionlocations.id
Ref: key_events.session_id > sessions.id
Ref: factions.tag_id > tags.id
Ref: members.character_id > characters.id
Ref: members.faction_id > factions.id
Ref: relatedevents.entry_id > entries.id
Ref: relatedevents.character_id > characters.id
Ref: sessionlocations.session_id > sessions.id
Ref: sessionlocations.location_id > locations.id
