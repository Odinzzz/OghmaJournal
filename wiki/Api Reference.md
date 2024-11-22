

# API Documentation

## Table of Contents
- [Retrieve All Session IDs](#retrieve-all-session-ids)
- [Retrieve Draft HTML](#retrieve-draft-html)
- [Save Draft HTML Content](#save-draft-html-content)
- [Create a New Session](#create-a-new-session)
- [Edit Session](#edit-session)
- [Process Draft](#process-draft)
- [Tag Entry Description](#tag-entry-description)
- [Correct String](#correct-string)
- [Add Character to Database](#add-character-to-database)
- [Add Tag to Database](#add-tag-to-database)
- [Get Entries for Session](#get-entries-for-session)
- [Update Entry Field](#update-entry-field)
- [Delete Entry](#delete-entry)

---

## Retrieve All Session IDs

### Endpoint
**Method**: `POST`  
**URL**: `/get_sessions`

### Description
This endpoint retrieves all session IDs from the database, providing a list of available sessions.

### Parameters
This endpoint does not require any path, query, or body parameters.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully retrieved a list of session IDs.
  - **Response Body**:
    ```json
    {
      "sessions": [
        {"id": 1},
        {"id": 2}
      ]
    }
    ```

#### Error Responses
- **Status Code**: `500` - Internal Server Error due to database querying issues.

---

## Retrieve Draft HTML

### Endpoint
**Method**: `POST`  
**URL**: `/get_html`

### Description
This endpoint retrieves the draft HTML content for a specified session ID.

### Parameters
#### Request Body Parameters
- **`session_id`** *(string, required)*: The session ID for which to retrieve draft HTML.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully retrieved the draft HTML.
  - **Response Body**:
    ```json
    {
      "success": True,
      "html_content": "<p>Sample HTML content</p>"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Missing `session_id` in the request.
- **Status Code**: `404` - Session not found.
- **Status Code**: `500` - Internal Server Error due to unexpected errors.

---

## Save Draft HTML Content

### Endpoint
**Method**: `POST`  
**URL**: `/save_draft`

### Description
Save draft HTML content associated with a specific session ID.

### Parameters
#### Request Body Parameters
- **`html`** *(string, required)*: The HTML content to save.
- **`session_id`** *(string, required)*: The session ID associated with the draft.

### Responses
#### Success Response
- **Status Code**: `202` - HTML content successfully saved.
  - **Response Body**:
    ```json
    {
      "success": True,
      "html_content": "<p>Sample HTML content</p>"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Missing `html` or `session_id`.
- **Status Code**: `500` - Database error when trying to save.

---

## Create a New Session

### Endpoint
**Method**: `POST`  
**URL**: `/new_session`

### Description
Create a new session by providing a unique session ID in `yyyymmdd` format.

### Parameters
#### Request Body Parameters
- **`session_id`** *(string, required)*: The session ID to create.

### Responses
#### Success Response
- **Status Code**: `201` - Session successfully created.
  - **Response Body**:
    ```json
    {
      "success": True,
      "content": "20230101"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Improper session ID format or session ID already exists.
- **Status Code**: `400` - Invalid length for the session ID.

---

## Edit Session

### Endpoint
**Method**: `GET`  
**URL**: `/edit_session/<session_id>`

### Description
Retrieve session details to edit based on session ID. Renders appropriate HTML based on session state.

### Parameters
#### Path Parameters
- **`session_id`** *(string)*: The session ID to retrieve and edit.

### Responses
#### Success Responses
- **Status Code**: `200` - Renders the draft or edit session HTML page.
  - **Response**: HTML content.

#### Error Responses
- **Status Code**: `400` - Record not found.

---

## Process Draft

### Endpoint
**Method**: `POST`  
**URL**: `/process_draft`

### Description
Processes and saves draft content by checking and inserting locations and entries into the database.

### Parameters
#### Request Body Parameters
- **`session_id`** *(string, required)*: The session ID to associate with the draft.
- **`html`** *(string, required)*: The draft content to process.

### Responses
#### Success Response
- **Status Code**: `201` - Successfully processed and stored draft content.
  - **Response Body**:
    ```json
    {
      "success": True,
      "session": "20230101"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Missing or incorrect parameters.
- **Status Code**: `500` - Processing error or unknown AI error.

---

## Tag Entry Description

### Endpoint
**Method**: `PATCH`  
**URL**: `/tool/ai/tag_description/<entry_id>`

### Description
Adds AI-generated tags to a specific entry's description.

### Parameters
#### Path Parameters
- **`entry_id`** *(string)*: The unique identifier for the entry.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully tagged the entry description.
  - **Response Body**:
    ```json
    {
      "success": True
    }
    ```

#### Error Responses
- **Status Code**: `400` - No entry found with the provided ID.
- **Status Code**: `500` - AI processing error.

---

## Correct String

### Endpoint
**Method**: `POST`  
**URL**: `/tool/ai/correct_string`

### Description
Corrects and validates a given string through AI processing.

### Parameters
#### Request Body Parameters
- **`string`** *(string, required)*: The string to be corrected.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully corrected the string.
  - **Response Body**:
    ```json
    {
      "success": True,
      "content": "Corrected string content"
    }
    ```

#### Error Responses
- **Status Code**: `400` - No string provided for correction.
- **Status Code**: `500` - Error during string correction.

---

## Add Character to Database

### Endpoint
**Method**: `POST`  
**URL**: `/db/add_character`

### Description
Adds a fictional character entry to the database with relevant details.

### Parameters
#### Request Body Parameters
- **`name`** *(string, required)*: Character's name.
- **`classe`** *(string, optional)*: Character's class.
- **`type`** *(string, optional)*: Character's type.
- **`tag`** *(string, required)*: Tag identifier in format `@JournalEntry[foundry_name]{alias}`.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully added character to the database.
  - **Response Body**:
    ```json
    {
      "success": True,
      "id": "character_uuid",
      "name": "Character Name",
      "classe": "",
      "char_type": "",
      "tag": "Tag",
      "tag_id": "tag_uuid"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Missing or invalid tag format or name.
- **Status Code**: `500` - Database error during insertion.

---

## Add Tag to Database

### Endpoint
**Method**: `POST`  
**URL**: `/db/add_tag`

### Description
Add a new tag to the database, ensuring it adheres to the required format and uniqueness.

### Parameters
#### Request Body Parameters
- **`tag`** *(string, required)*: The tag to be added.
- **`tag_type`** *(string, required)*: The type of tag being added.

### Responses
#### Success Response
- **Status Code**: `200` - Tag successfully created and stored in the database.
  - **Response Body**:
    ```json
    {
      "id": "tag_uuid",
      "tag": "@JournalEntry[Example]{Alias}",
      "tag_type": "character"
    }
    ```

#### Error Responses
- **Status Code**: `400` - Tag format is invalid or the tag already exists.
- **Status Code**: `400` - Missing tag or tag type.

---

## Get Entries for Session

### Endpoint
**Method**: `GET`  
**URL**: `/get_entries/<int:session_id>`

### Description
Retrieve session entries, including locations and associated data, for a specified session ID.

### Parameters
#### Path Parameters
- **`session_id`** *(integer)*: The session ID to retrieve entries for.

### Responses
#### Success Response
- **Status Code**: `200` - Successfully retrieved session entries.
 
  - **Response Body**:
    ```json
    {
      "session_id": 12345678,
      "session_title": "Session Title",
      "locations": {
        "1": {
          "location_name": "Location Name",
          "entries": [
            {
              "entry_id": "entry_uuid",
              "entry_index": 0,
              "entry_title": "Entry Title",
              "entry_description": "Description of the entry",
              "entry_tagged": "Tagged description"
            }
          ]
        }
      }
    }
    ```

### Error Responses
- **Status Code**: `500` - Internal Server Error due to database querying issues.
- **Status Code**: `404` - The specified session ID does not exist.

---

## Update Entry Field

### Endpoint
**Method**: `POST`  
**URL**: `/db/update_entry/<field>/`

### Description
Updates a specific field of an entry in the database.

### Parameters
#### Path Parameters
- **`field`** *(string)*: The name of the field to update.

#### Request Body Parameters
- **`new_value`** *(string, required)*: The new value to assign to the field.
- **`entry_id`** *(string, required)*: The unique identifier for the entry to update.

### Responses
#### Success Response
- **Status Code**: `200` - Entry field successfully updated.
  - **Response Body**:
    ```json
    {
      "success": True,
      "content": "Updated value",
      "field": "field_name"
    }
    ```

#### Error Responses
- **Status Code**: `500` - Internal Server Error during the update operation.

---

## Delete Entry

### Endpoint
**Method**: `DELETE`  
**URL**: `/db/delete_entry/<entry_id>`

### Description
Deletes an entry from the database using the specified entry ID.

### Parameters
#### Path Parameters
- **`entry_id`** *(string)*: The unique identifier for the entry to be deleted.

### Responses
#### Success Response
- **Status Code**: `200` - Entry successfully deleted.
  - **Response Body**:
    ```json
    {
      "success": True
    }
    ```

#### Error Responses
- **Status Code**: `400` - Deletion failed, possibly due to the entry not existing.
  - **Response Body**:
    ```json
    {
      "success": False,
      "error": "Deletion failed"
    }
    ```
