# Database Schema Documentation

This document provides a detailed overview of the database schema for managing sessions, characters, locations, and related entities. Each table is explained with its purpose, structure, relationships, and constraints.

---

## **Table: `sessions`**

**Purpose:** Stores information about individual sessions, including draft content and metadata.

**Columns:**
- `id`: Unique identifier for the session (Primary Key, Not Null).
- `draft`: Stores temporary draft text.
- `session_state`: Indicates the state of the session (default is 0 for drafts).
- `title`: Title of the session.
- `summary`: Summary or description of the session.
- `html`: Full HTML content for the session.
- `discord`: Optional field for storing Discord links or IDs.

---

## **Table: `characters`**

**Purpose:** Stores data about characters involved in the sessions.

**Columns:**
- `id`: Unique identifier for the character (Primary Key, Not Null).
- `name`: Name of the character (Not Null).
- `classe`: Class or type of character (e.g., Warrior, Mage).
- `tag_id`: References `tags.id` (nullable).
- `type`: Additional type information about the character.

**Relationships:**
- Foreign Key: `tag_id` references `tags.id` (on delete: set null).

---

## **Table: `locations`**

**Purpose:** Stores data about various locations mentioned or involved in sessions.

**Columns:**
- `id`: Unique identifier for the location (Primary Key, Not Null).
- `name`: Name of the location (Not Null).
- `region`: Optional field for specifying the region of the location.
- `tag_id`: References `tags.id` (nullable).

**Relationships:**
- Foreign Key: `tag_id` references `tags.id` (on delete: set null).

---

## **Table: `heros`**

**Purpose:** Links sessions with their associated characters, identifying the heroes in each session.

**Columns:**
- `session_id`: References `sessions.id` (Not Null).
- `character_id`: References `characters.id` (Not Null).

**Primary Key:**
- Composite: (`session_id`, `character_id`).

**Relationships:**
- Foreign Key: `session_id` references `sessions.id` (on delete: cascade).
- Foreign Key: `character_id` references `characters.id` (on delete: cascade).

---

## **Table: `encounters`**

**Purpose:** Links sessions, characters, and locations, representing encounters in the narrative.

**Columns:**
- `session_id`: References `sessions.id` (Not Null).
- `character_id`: References `characters.id` (Not Null).
- `location_id`: References `locations.id` (Not Null).

**Primary Key:**
- Composite: (`session_id`, `character_id`, `location_id`).

**Relationships:**
- Foreign Key: `session_id` references `sessions.id` (on delete: cascade).
- Foreign Key: `character_id` references `characters.id` (on delete: cascade).
- Foreign Key: `location_id` references `locations.id` (on delete: cascade).

---

## **Table: `entries`**

**Purpose:** Stores detailed entries for specific locations in a session.

**Columns:**
- `id`: Unique identifier for the entry (Primary Key, Not Null).
- `description`: Text description of the entry.
- `tagged_description`: Optionally stores processed/annotated text.
- `session_id`: References `sessions.id` (Not Null).
- `location_id`: References `locations.id` (Not Null).
- `entry_index`: Index position of the entry within the location.

**Relationships:**
- Foreign Key: `session_id` references `sessions.id` (on delete: cascade).
- Foreign Key: `location_id` references `locations.id` (on delete: cascade).

---

## **Table: `key_events`**

**Purpose:** Stores significant events tied to a session.

**Columns:**
- `title`: Title of the key event.
- `impact`: Description of the event's impact.
- `session_id`: References `sessions.id` (Not Null).

**Relationships:**
- Foreign Key: `session_id` references `sessions.id` (on delete: cascade).

---

## **Table: `factions`**

**Purpose:** Stores data about factions, which can be associated with characters.

**Columns:**
- `id`: Unique identifier for the faction (Primary Key, Not Null).
- `name`: Name of the faction (Not Null).
- `description`: Optional text description of the faction.
- `tag_id`: References `tags.id` (nullable).

**Relationships:**
- Foreign Key: `tag_id` references `tags.id` (on delete: set null).

---

## **Table: `members`**

**Purpose:** Links characters to factions, representing membership relationships.

**Columns:**
- `character_id`: References `characters.id` (Not Null).
- `faction_id`: References `factions.id` (Not Null).

**Primary Key:**
- Composite: (`character_id`, `faction_id`).

**Relationships:**
- Foreign Key: `character_id` references `characters.id` (on delete: cascade).
- Foreign Key: `faction_id` references `factions.id` (on delete: cascade).

---

## **Table: `relatedevents`**

**Purpose:** Links key events to characters.

**Columns:**
- `event_id`: Unique identifier for the event (Not Null).
- `character_id`: References `characters.id` (Not Null).

**Primary Key:**
- Composite: (`event_id`, `character_id`).

**Relationships:**
- Foreign Key: `character_id` references `characters.id` (on delete: cascade).

---

## **Table: `sessionlocations`**

**Purpose:** Links sessions to locations, tracking chronological or narrative order.

**Columns:**
- `session_id`: References `sessions.id` (Not Null).
- `location_id`: References `locations.id` (Not Null).
- `crono_index`: Index for ordering locations chronologically (Not Null).

**Primary Key:**
- Composite: (`session_id`, `location_id`).

**Relationships:**
- Foreign Key: `session_id` references `sessions.id` (on delete: cascade).
- Foreign Key: `location_id` references `locations.id` (on delete: cascade).

---

## **Table: `tags`**

**Purpose:** Stores tags that can be associated with various entities.

**Columns:**
- `id`: Unique identifier for the tag (Primary Key, Not Null).
- `tag`: Foundry journal tag @JournalEntry[foundry_name]{alias} (Not Null).
- `tag_type`: location, character, faction, item, ... (Not Null, Default location) .

---

## **Key Design Considerations**
1. **Referential Integrity:**
   - `ON DELETE CASCADE` ensures dependent records are removed when parent records are deleted.
   - `ON DELETE SET NULL` is used where relationships can be removed without deleting dependent entities.
   
2. **Composite Keys:**
   - Used in many-to-many relationships (e.g., `heros`, `encounters`, `members`).

3. **Tagging System:**
   - Tags provide a flexible way to classify and organize entities.

4. **Draft and State Management:**
   - `sessions` tracks draft content and session progression using `session_state`.

---

This schema supports a rich and interconnected system for managing RPG-like sessions and events, with robust relational data handling.