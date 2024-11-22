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
