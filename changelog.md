### Changelog: 00.00.03.00 – Location Management & Session Enhancements 🌍

#### **Database Updates**
- **Added**: Fake data to test the database for better debugging.  
- **Updated**: `Schema.sql` to reflect new database changes.  
- **Updated**: `sessionLocations` now uses unique IDs for better handling in the UI.  
- **Updated**: `entries` to reference the new `sessionLocations.ID`.  
- **Added**: UUID to `encounter` and `key_event` tables.  
- **Updated**: `relatedEvent` now refers to `entry_id` instead of `key_event`.  
- **Added**: A `bddiagram` file and updated `schema.pdf` to document these changes.

#### **Backend Routes**
- **Added**: `/db/add_location`  
  Add a new location to the database.  
- **Added**: `/db/add_session_location`  
  Associate a location with a session.  
- **Added**: `/db/new_entry`  
  Moved functionality to a more appropriate place in the code space.  
- **Added**: `/db/remove_session_location`  
  Remove a location from a session.  
- **Added**: `/get_session_heroes`  
  Retrieve all heroes in a specific session.  
- **Added**: `/view_session/<session_id>`  
  Render a session in its HTML form.  
- **Updated**: Logic for `/db/get_entries` extracted to a reusable function.

#### **Web App**
- **Added**: A dropdown UI element to select locations, along with a modal to add non-existent locations.  
- **Updated**: The `save-session-btn` in `edit_session.html` now redirects to `view_session.html`.  
- **Added**: A primitive `view_session.html` to display session details.  
- **Improved**: Logic for rendering sessions using Jinja.  
- **Updated**: `get_sessions.js` to support viewing instead of direct editing.

#### **JavaScript**
- **Added**: `LocationContainerTemplate` for reusable location components.  
- **Added**: `locationDropdownTemplate` for the dropdown UI element.  
- **Updated**: `fetchEntries` now considers the new dropdown for session locations.  
- **Implemented**: Button functionality for the new location management system.

#### **Python**
- **Added**: Functions to validate a session ID.  
- **Added**: `get_session_encounters` to retrieve session-specific encounters.  
- **Enhanced**: Reusable logic extracted from `/get_entries` for better maintainability.  

#### **AI Integration**
- **Updated**: Translation prompt to improve accuracy.

#### **Testing & Documentation**
- **Added**: Foundry macro for testing future features.  
- **Updated**: All related documentation to reflect new features and changes.

Enjoy the improved location management system, enhanced session views, and a streamlined experience! 🚀


---

### Changelog: 00.00.02.00 – Hero Features & Tags Expansion 🌟

#### **Backend Routes**
- **Added**: `/get_characters`  
  Retrieve all characters from the database. 
- **Added**: `/get_heros/<session_id>`  
  Retrieve all heroes for a specific session.
- **Added**: `/tool/ai/generate_title/<entry_id>`  
  AI-powered service to generate a title for an entry.
- **Added**: `/db/add_hero`  
  Add a new hero to the session.
- **Added**: `/db/remove_hero`  
  Remove a hero from the session.

#### **Functions**
- **Added**: `get_tags`  
  Function to retrieve tags for a specific entry.

#### **Scripts**
- **Added**: `get_all_tags.js`  
  Script to retrieve all tags from the Foundry game.

#### **Web App**
- **Added**: Ability to add a hero to a session.  
- **Added**: UI element (button) for future use (currently inactive).

#### **Changes**
- **Updated**: API documentation to reflect new routes and features.
- **Updated**: CSS for a cleaner and more modern layout.
- **Updated**: UI for a more streamlined user experience.

Enjoy the new hero management features and cleaner interface! 🚀

---

### Hotfix: 00.00.01.1 - tagged_string

#### **Web App**
- **fix**: a bug where tag tagged string doen show up when edit_entry is loaded

---


### Changelog: 00.00.01.0 – The Emoji Update 🎉✨

#### **Database Updates**
- **Added**: Column `title` to the `entries` table in the database.

#### **API Enhancements**
- **Added**: `/get_entries/<int:session_id>`  
  Retrieve all entries for a specific session. 
- **Added**: `/db/update_entry/<field>`  
  Generic API endpoint to edit an entry. 
- **Added**: `/db/delete_entry/<entry_id>`  
  Delete an entry by its ID. 
- **Added**: `/tool/ai/tag_description/<entry_id>`  
  AI-powered tagging for entry descriptions. 
- **Added**: `/tool/ai/correct_string`  
  AI service for correcting and translating strings to `config.LANG`.

#### **User Interface**
- **Updated**: UI elements now include beautiful and relevant emojis 🎨.

#### **Testing**
- **Added**: Various tests to ensure robustness of new and existing features.

#### **Codebase Improvements**
- **Refactored**: All code to handle errors gracefully and return a consistent response structure:  
  ```json
  {
    "success": bool,
    "error": string|null,
    "content": object|string|null
  }
  ```

#### **Documentation**
- **Updated**: Wiki to reflect the new API routes and features.

Enjoy the expressive power of emojis and enhanced functionality in this update! 🎈🎉
