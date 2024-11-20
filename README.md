## Overview

The Journal Session Manager is a comprehensive application for organizing and tracking narrative-driven events, characters, locations, and factions. It is tailored for role-playing games (RPGs), collaborative storytelling, or campaign management. Users can dynamically edit, manage, and process sessions, leveraging a structured database to link characters, locations, key events, and factions seamlessly.

---

## Features

- **Session Management**  
  - Create, view, and edit journal sessions with metadata such as title, summary, and state tracking.  
  - Support for draft management and rich HTML content editing.  
  - Attach key events, encounters, and hero information to sessions for better context.

- **Character & Faction Integration**  
  - Define characters with attributes such as name, class, and type.  
  - Associate characters with factions and track their involvement in sessions, locations, or specific events.

- **Location & Encounter Tracking**  
  - Add and manage locations with regions and tags for contextual storytelling.  
  - Link characters and events to specific locations, allowing detailed encounter tracking.

- **Dynamic Tags**  
  - Tag characters, locations, factions, and key events to enable fast retrieval and better categorization.  
  - Tags are dynamically managed and AI-assisted for typo correction and consistency.

- **Narrative Tools**  
  - Record key events with titles and impact descriptions.  
  - Maintain chronological order of session locations and their related events for detailed storytelling.

- **Relational Integrity**  
  - All entities (sessions, characters, locations, factions) are interconnected, ensuring comprehensive relationships for narratives.  
  - Database constraints enforce data consistency and integrity across all modules.

--- 

## Installation

### Prerequisites
- Python 3.8 or above
- A database system `SQLite`
- `OpenAI` Api key

### Steps
1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
     
4. **Setup the dataBase**
   ```bash
   Get-Content .\db\schema.sql | sqlite3 .\db\journal.db  
   ```
  
5. **Run the Application**  
   ```bash
   flask --debug run
   ```

   The application will be available at `http://127.0.0.1:5000`.

---

## Usage

### **Routes and APIs**

1. **Main Routes**
   - `/`  
     Redirects to the journal logging page.
   - `/log_journal`  
     Displays the main page for managing journal sessions.

2. **Session Management**
   - `/new_session` (`POST`)  
     Create a new journal session.  
     **Payload Example:**  
     ```json
     { "session_id": "20241119" }
     ```
   - `/edit_session/<session_id>` (`GET`)  
     Edit a specific session based on its ID.

3. **Draft Management**
   - `/get_html` (`POST`)  
     Fetch saved HTML content for a session.  
     **Payload Example:**  
     ```json
     { "session_id": "20241119" }
     ```
   - `/save_draft` (`POST`)  
     Save or update draft content for a session.  
     **Payload Example:**  
     ```json
     { "session_id": "20241119", "html": "<p>Example content</p>" }
     ```

4. **Processing**
   - `/process_draft` (`POST`)  
     Processes the draft using AI tools for typo detection and location tagging.

---

### **Frontend Functionality**

#### Quill.js Editor
- Embedded for editing journal entries with live draft-saving capabilities.
- Integrated with `/get_html` and `/save_draft` for data persistence.

#### Session List
- Dynamically loads existing sessions using `/get_sessions`.
- Provides buttons for creating new sessions or editing existing ones.

---

## Project Structure

```
├── config/               # Configuration files
│   ├── config.py         # Application configuration
├── db/                   # Database related files
│   ├── constructdb.txt   # command to make the DB
│   ├── schema.pdf        # visual rep of the database
│   ├── schema.sql        # cli prompt to make the database
├── templates/            # HTML templates
│   ├── log_journal.html  # Journal logging page
│   ├── draft.html        # Draft editor page
│   ├── edit_session.html # Edit session page
│   ├── layout.html       # layout blueprint page  
├── static/               # Static assets
│   ├── get_session.js # Session list functionality
│   ├── new_session.js # Session creation functionality
│   ├── quill.js       # Draft editor functionality
├── scripts/              # Custom scripts
│   ├── quill_processing.py # Content processing logic
│   ├── ...               # old script to manualy make the journal (depricated)
├── add_event_to_journal.py # old script to manualy make the journal (depricated)
├── ai.py                 # OpenAi tools
├── app.py                # Main application logic
├── audio_to_text_dev.py  # old script to manualy make the journal (depricated)
├── decorator.py          # old script to manualy make the journal (depricated)
├── makefile.py           # old script to manualy make the journal (depricated)
├── proccessJournal.py    # Main application logic
├── requirements.txt      # Python dependencies
```

---

## Planned Features

- **Session Editing & Foundry Tagging**  
  Enhance session management by allowing detailed session editing with easy tagging for integration with Foundry VTT. Users will be able to organize, edit, and tag sessions with Foundry-compatible metadata for seamless interaction with the platform.

- **Automated Posting of Resumes to Social Apps**  
  Automate the posting of session summaries and key events to social platforms like Discord, Slack, and other communication tools, allowing for live updates and discussions among players or stakeholders. This feature will enhance the sharing of game progress and session summaries in real-time.

- **Full Integration of Foundry Module OghmaScribe**  
  Integrate the OghmaScribe module into the system for Foundry Virtual Tabletop (VTT) for a smoother campaign management experience. This will allow for automatic export of session details into Foundry and enable detailed logging and tracking of events and characters directly in the VTT.

- **Communication Between Foundry VTT App and the API**  
  Enable bi-directional communication between the Foundry VTT app and the Journal Session Manager API. This feature will allow for automatic updates from the VTT to the database and vice versa, creating a seamless workflow for players and game masters.

- **Character & Event Visualization**  
  Introduce a visual dashboard to view character interactions, events, and locations in a graph or map format. This will allow users to visualize complex relationships and event chains for better planning and storytelling.

- **Dynamic AI-Assisted Event Generation**  
  Implement AI-powered event suggestion tools to automatically generate session entries based on current campaign context. These events can include encounters, NPC dialogues, and more, helping game masters to create rich content quickly.

- **Customizable Templates for Session Logs**  
  Allow users to create and use custom templates for session logs and key event summaries, improving session documentation and enabling personalized journaling experiences.

- **Cross-Platform Syncing**  
  Sync session data across different devices and platforms to ensure users can manage their sessions from anywhere. This includes cloud syncing with mobile applications for on-the-go session updates.

- **Advanced Search & Filtering**  
  Implement advanced search and filtering functionality for quick access to sessions, characters, events, and locations based on custom criteria, making it easier to retrieve and work with large amounts of session data.

--- 

## Notes

### Error Handling
The application includes comprehensive error handling for common issues, including:
- Missing or invalid session IDs.
- Database errors during insert/update operations.
- AI-related errors (e.g., API failures).

### AI Integration
AI-powered typo detection and tagging are implemented using `openai`. Ensure you configure API keys in a secure manner before deployment.

---

## Contribution

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit and push your changes.
4. Submit a pull request with a clear description.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

For further assistance, contact the development team.
