from sre_constants import SUCCESS
import uuid
import re



from flask import Flask, jsonify,render_template, request, abort, session
from flask_cors import CORS

from cs50.sql import SQL




from config.config import config
from scripts import summary
from scripts.quill_processing import quill_processing
from scripts.event_title import get_title
from ai import ai_check, ai_corrector
from scripts.tag import tagging


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}) # enanble cross app



db = SQL(config.SQLALCHEMY_DATABASE_URI)

# Routes
@app.route("/test")
def test():

    return jsonify({"success": True, "content": "Hi from Back END"}),200


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/<int:session_id>")
def view_session(session_id):
    heros, _ = get_session_heros(session_id)
    # encouter, _ = get_session_encounter()
    payload = {
        'id': session_id,
        'heros': heros['content'],
        'encounters':[
            {'name': 'Othran', 'role': 'Paladin'},
            {'name': 'Othran', 'role': 'Paladin'}
        ],
        'locations':[
            {'name': 'dynnegal', 'events':[
                {'title': '1', 'description': '1'},
                {'title': '2', 'description': '2'}
            ]}
        ]
    }
    return render_template('view_session.html', dnd_session=payload)  


@app.route("/get_sessions", methods=['POST'])
def get_sessions():
    try:
        sessions = db.execute('SELECT id FROM sessions')
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500

    return jsonify({"sessions": sessions}),200


@app.route("/get_entries/<int:session_id>")
def get_entries(session_id):


    try:
    # get all he location for a session

        session_locations = db.execute('SELECT * FROM sessionlocations WHERE session_id = ? ORDER BY crono_index;', session_id)
        response = {
            "session_id": session_id,
            "session_title": "",
            "locations":{}
            } 

        

        for session_location in session_locations:

            location_data:dict = db.execute('SELECT * FROm locations WHERE id= ?;', session_location['location_id'])

            location_entries = db.execute('SELECT * FROM entries WHERE session_id = ? and session_location_id = ? ORDER BY entry_index;', session_id, session_location.get('id'))

            
            

            crono_index = str(session_location['crono_index'])  # Convert to string

            response['locations'][crono_index] = {
                'location_name': location_data[0].get('name'),
                'session_location_id': session_location.get('id'),
                'location_id': location_data[0].get('id'),
                "entries":[]
            }
            for location_entry in location_entries:
                

                response['locations'][crono_index]['entries'].append({
                    "entry_id": location_entry.get('id'),
                    "entry_index": location_entry.get('entry_index'),
                    "entry_title": location_entry.get('title'),
                    "entry_description": location_entry.get('description'),
                    "entry_tagged": location_entry.get('tagged_description')
                    
                })
        
       
        
    except Exception as e:
        print(f'MYEXEPTION: {e}')
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    

    return jsonify(response), 200
    

@app.route("/get_entries_old/<int:session_id>")
def get_entries_old(session_id):



    try:
        db_data = db.execute("""
            SELECT 
                sessions.title AS session_title,
                sessions.summary AS session_summary,
                locations.name AS location_name,
                locations.id AS location_id,             
                sessionlocations.crono_index AS location_index,
                tags.tag AS location_tag,
                tags.id AS tag_id,
                entries.id AS entry_id,
                entries.title AS entry_title,
                entries.entry_index,
                entries.description AS entry_description,
                entries.tagged_description AS entry_tagged
            FROM 
                sessions
            LEFT JOIN 
                entries ON sessions.id = entries.session_id
            LEFT JOIN 
                locations ON entries.location_id = locations.id
            LEFT JOIN 
                tags ON locations.tag_id = tags.id
            LEFT JOIN 
                sessionlocations ON sessions.id = sessionlocations.session_id AND locations.id = sessionlocations.location_id
            WHERE 
                sessions.id = ?;
            """, session_id)
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    if not db_data:
        return jsonify({"success": False, "error": 'session do not exist'})
    
    session_data= {"session_id": session_id}
    session_data["session_title"] = db_data[0].get('session_title')
    session_data['locations'] = {}

    for data in db_data:
        if data['location_index'] not in session_data['locations']:
            session_data['locations'][data['location_index']] = {'location_name': data['location_name'], 'location_id': data['location_id'], 'location_index': data['location_index'], "entries": []}
        
        session_data['locations'][data['location_index']]['entries'].append({
            "entry_id": data['entry_id'],
            'entry_index': data['entry_index'],
            'entry_title': data['entry_title'],
            "entry_description": data["entry_description"],
            "entry_tagged": data["entry_tagged"]
        })

    return jsonify(session_data), 200
    

@app.route("/get_characters")
def get_characters():

    try:
        characters = db.execute("SELECT * FROM characters;")
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    if not characters:
        return jsonify({"success": False, "error": f"character found"}), 400
    
    return jsonify({"success": True, "content": characters}), 200


@app.route("/get_locations")
def get_locations():

    try:
        locations = db.execute("SELECT * FROM locations;")
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    if not locations:
        return jsonify({"success": False, "error": f"character found"}), 400
    
    return jsonify({"success": True, "content": locations}), 200


@app.route("/get_heros/<session_id>")
def get_heros(session_id):
    try:
        int(session_id)
    except Exception as e:
        return jsonify({"success": False, 'error': f'{session_id = } must be an integer'})
    
    try:
        heros = db.execute("""
            SELECT characters.id as character_id,
            characters.name as character_name
            FROM heros
            JOIN characters ON heros.character_id = characters.id
            WHERE heros.session_id = ?;""", session_id)
    except Exception as e:
        return jsonify({'success': False, 'error': 'Database error', 'details': str(e)}), 500
    

    return jsonify({'success': True, 'content': heros})


@app.route("/get_html", methods=['POST'])
def get_html() -> dict:
    """Retrieve the draft text.

    Returns:
        dict: {'success': bool, 'html_content': html}
    """
    try:
        # Ensure 'session_id' exists in the request body
        data = request.json

        session_id = data.get('session_id')
        if not session_id:
            return jsonify({'success': False, 'error': 'Missing session_id'}), 400

        # Query the database for the html content
        html = db.execute('SELECT html FROM sessions WHERE id = ?;', session_id)

        if not html:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        # If the query is successful, return the HTML content
        return jsonify({'success': True, 'html_content': html[0]['html']})

    except KeyError as e:
        return jsonify({'success': False, 'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'An unexpected error occurred', 'details': str(e)}), 500


@app.route("/save_draft", methods=['POST'])
def save_draft():
    
    data:dict = request.json

    html = data.get("html")
    session_id = data.get("session_id")

    if not html or not session_id:
        return jsonify({'success': False, 'error': f'Missing data: html: {html} session_id: {session_id}'}), 400

    try:
        db.execute("UPDATE sessions SET html = ? WHERE id = ?", data['html'], data['session_id'])
        return jsonify({'success': True, 'html_content': html}), 202
    except Exception as e:
        return jsonify({'success': False, 'error': 'Database error', 'details': str(e)}), 500
        

@app.route("/new_session", methods=["POST"])
def new_session():

    data = request.json

    session_id = data['session_id']

    try:
        int(session_id)
    except ValueError as e:
        return jsonify({"success": False, 'error': f'{e} session id must be in format yyyymmdd'}), 400
    
    if len(session_id) != 8:
        return jsonify({"success": False, 'error': f'{session_id} {len(session_id)} session id must be in format yyyymmdd'}), 400
    
    if db.execute('INSERT INTO sessions (id) VALUES (?);', session_id):
        return jsonify({"success": True, "content": session_id}), 201
    else:
        return jsonify({"success": False,'error': 'session already exist'}), 400
    

@app.route("/edit_session/<session_id>")
def edit_session(session_id):
    dnd_session = db.execute("SELECT * FROM sessions WHERE id=?",session_id)

    

    if dnd_session:

        if dnd_session[0]['session_state'] == 100: # refractor this to remove draft
            return render_template("draft.html",dnd_session=dnd_session[0])
        else:
            return render_template("edit_session.html", dnd_session=dnd_session[0])
    else:
        abort(400, 'Record not found')


@app.route("/process_draft", methods=["POST"])  # Use methods argument for HTTP methods
def process_draft():

    # Access JSON data sent in the request body
    data: dict = request.json

    # Extract specific fields from the JSON payload and check there is content in it
    session_id = data.get('session_id')
    content = data.get('html')

    
    if session_id is None or content is None:
        return jsonify({"success": False, "error": "Bad request: content or session_id cannot be null"}), 400

    # check if session id exist
    check_id = db.execute("SELECT id FROM sessions WHERE id = ?", session_id )
    if not check_id:
        return jsonify({"success": False, "error": f"Bad request: no session with id :{session_id}"}), 400
    
    try:
        process_content = quill_processing(content)
        
    except ValueError as e:
        return jsonify({"success": False, "error": f"{e}"}), 400 # order list not use or empty
    
    # Preload all locations with their tags
    all_locations = db.execute("""
        SELECT 
            locations.id AS location_id, 
            locations.name AS location_name, 
            tags.tag AS tag_name
        FROM 
            locations
        LEFT JOIN 
            tags 
        ON 
            locations.tag_id = tags.id;
    """)

    # Build a dictionary for quick lookups
    location_dict = {loc['location_name']: {'id': loc['location_id'], 'tag': loc['tag_name']} for loc in all_locations}

    

    for location_index, location in enumerate(process_content):

        for location_name in location:
            location_id = location_dict.get(location_name)

            print(location_id)

            if not location_id: # check with ai if there is a typo or not

                
                try:
                    check = ai_check(location_name, location_dict)
                except:
                    return jsonify({"success": False, "error": 'Unknow error from openAi'}), 500


                if check['exist'] == False: # No Typo new entry

                    tag_id = str(uuid.uuid4())
                    tag = db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);",tag_id, check["foundry_tag"], 'location')
                    location_id = str(uuid.uuid4())
                    location_db = db.execute("INSERT INTO locations (id, name, tag_id) VALUES (?, ?, ?);", location_id, check["name"], tag_id  )
                    location_dict[check['name']] = {"id": location_id, 'tag': check["foundry_tag"]} 

                    if location_db:

                        print(f'DEBUG: New location created into database location_name: {check["name"]} with id: {location_id}')

                    else:

                        return jsonify({"success": False, "error": "fail to create new database entry"}), 500
                    
                else: # Typo already exist in the database
                    check_name: str = check.get('name')
                    if not check_name:
                        return jsonify({"success": False, 'error': 'ai messed up'}), 500                   
                    location_id = db.execute("SELECT id FROM locations WHERE name = ?", check_name )
                    if not location_id:
                        return jsonify({"success": False, "error": "fail to retrieve database entry"}), 500
                    location_id = location_id[0]['id'] # make sure that location id is a string
            else:

                location_id = location_id['id'] # make sure that location id is a string 

                print(f'{session_id = } {location_id = } {location_index = }')
            db.execute("INSERT INTO sessionlocations (session_id, location_id, crono_index) VALUES (?, ?, ?);", session_id, location_id , int(location_index))


            for event_index, event in enumerate(location[location_name]):

                entry_id = str(uuid.uuid4())
                db.execute("INSERT INTO entries (id, description, session_id, location_id, entry_index ) VALUES (?,?,?,?,?);", entry_id, event, session_id, location_id, int(event_index))
                print(f'DEBUG: Entry created with id: {entry_id} at index: {event_index} content:{event}')


    db.execute("UPDATE sessions SET session_state = 1 WHERE id = ?;", session_id)
            


    return jsonify({"success": True, "session": session_id}), 201

################################################################################
#                                    TOOLS                                     #
################################################################################


@app.route("/tool/ai/tag_description/<entry_id>", methods=["PATCH"])
def tag_description(entry_id):
    entry = db.execute("SELECT description FROM entries WHERE id= ?;", entry_id)

    if not entry:
        return jsonify({"success": False, "error": f"No entry with ID: {entry_id}"}), 400
    
    try:
        print( f'({entry[0]}) is of type {type(entry[0])}')
        tagged_description = tagging(entry[0]['description'])
    except Exception as e:
        return jsonify({"success": False, "error": f"OpenAI Error: {e}"}), 500
    
    response, code = update_entry("tagged_description", tagged_description['tagged_string'], entry_id)
    return jsonify(response), code


@app.route ("/tool/ai/generate_title/<entry_id>", methods=['PATCH'] )
def generate_title(entry_id):
    entry = db.execute("SELECT description FROM entries WHERE id= ?;", entry_id)

    if not entry:
        return jsonify({"success": False, "error": f"No entry with ID: {entry_id}"}), 400
    
    try:
        print( f'({entry[0]}) is of type {type(entry[0])}')
        generated_title = get_title(event=entry[0]['description'])
    except Exception as e:
        return jsonify({"success": False, "error": f"OpenAI Error: {e}"}), 500

    print(f'{generated_title}: {type(generated_title)}')
    response, code = update_entry("title", generated_title, entry_id)
    return jsonify(response), code


@app.route("/tool/ai/correct_string", methods=['POST'])
def tool_correct_string():

    data = request.json
    string = data.get('string')

    response, code = correct_string(string)
    return jsonify(response), code


################################################################################
#                                    DATABASE                                  #
################################################################################

@app.route("/db/add_hero", methods=['POST'])
def add_hero():
    data: dict = request.json
    print(request)
    session_id = data.get('session_id')
    character_id = data.get('character_id')
    character_name = data.get('character_name')

    print(f'{session_id = } {character_id = } {character_name = }')

    if not session_id or not character_id or not character_name:
        return jsonify({'success': False, 'error': f'No session_id: {session_id} or character_id: {character_id} or character_name: {character_name} provided '}),400
    try:
        new_hero = db.execute("INSERT INTO heros (session_id, character_id) VALUES (?, ?);", session_id, character_id)
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    if new_hero:
        return {'success': True, 'content': {
            'session_id': session_id,
            'character_id': character_id,
            'character_name': character_name
        }}

    return jsonify({"success": False, "error": 'Something went wrong'}), 500


@app.route("/db/remove_hero", methods=['DELETE'])
def remove_hero():
    data:dict = request.json
    session_id = data.get('session_id')
    character_id = data.get('character_id')

    if not character_id or not session_id:
        return jsonify({'success': False, 'error': f'{session_id = } and {character_id = } cannot be null'})
    
    try:
        removed_hero = db.execute('DELETE FROM heros WHERE character_id = ? AND session_id = ?;', character_id, session_id)
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    
    if removed_hero:
        return {'success': True, 'content': {
            'session_id': session_id,
            'character_id': character_id,
        }}

    return jsonify({"success": False, "error": 'Something went wrong'}), 500


@app.route("/db/add_character", methods=["POST"])
def db_add_character():
    """
    data = {
        name: NN foundry_name Case sensitive
        classe:
        char_type:
        tag: NN must be @JournalEntry[foundry_name]{alias}
    }
    """
    # parse the data for easier validation
    data:dict =  request.json
    name = data.get('name')
    classe = data.get('classe')
    char_type = data.get('type')
    tag = data.get('tag')

    # data validation
    if not name or not tag:
        return jsonify({"success": False, 'error': 'Fail to create character: Name and Tag cannot be Null'}), 400
    
    pattern = r'@JournalEntry\[[^\[\]{}]+\]\{[^\[\]{}]+\}'
    tag_check = re.fullmatch(pattern, tag)

    if not tag_check:
        return jsonify({"success": False, 'error': 'Fail to create character: Tag must be formated like @JournalEntry[foundry_name]{alias}'}), 400

    if not classe:
        classe = ""
    if not char_type:
        char_type = ""

    tag_check = db.execute('SELECT * FROM tags WHERE tag = ?;', tag)
    if tag_check:
        return jsonify({"success": False, 'error': 'Fail to create character: Tag already exist'}), 400
    
    character_check = db.execute('SELECT * FROM characters WHERE name = ?;', name)
    if character_check:
        return jsonify({"success": False, 'error': 'Fail to create character: Character already exist'}), 400
    
    # dataBase entry creation
    character_id = str(uuid.uuid4())
    tag_id = str(uuid.uuid4())
    
    try:
        db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);", tag_id, data['tag'], 'character'  )
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500
    try:
        db.execute("INSERT INTO characters (id, name, classe, type, tag_id) VALUE (?, ?, ?, ?, ?);", character_id, name, classe, char_type, tag_id)
    except Exception as e:
        return jsonify({"success": False, "error": f"DataBaseError: {e}"}), 500

    return jsonify({
        "success": True,
        'id': character_id,
        'name': name,
        'classe': classe,
        'char_type': char_type,
        'tag': tag,
        'tag_id': tag_id
        })


@app.route("/db/add_tag", methods=["POST"])
def db_add_tag():
    data = request.json
    response, code = add_tag(data.get('tag'), data.get('tag_type'))
    return jsonify(response), code


@app.route("/db/update_entry/<field>/", methods=['POST'])
def db_update_entry(field):
    data:dict  = request.json
    value = data.get('new_value')
    entry_id = data.get('entry_id')

    response, code = update_entry(field, value, entry_id)
    return jsonify(response), code

    
@app.route("/db/delete_entry/<entry_id>", methods=['DELETE'])
def db_delete_entry(entry_id):
    deleted = db.execute('DELETE FROM entries WHERE id = ?;', entry_id)

    if deleted > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, 'error': 'Deletion fail'})


@app.route('/db/add_location', methods=['POST'])
def db_add_location():

    try:
        # Extract data from the request JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Missing JSON payload"}), 400

        name = data.get('name')
        region = data.get('region', "")  # Optional parameter, defaults to an empty string

        # Validate input
        if not name or not isinstance(name, str):
            return jsonify({"success": False, "error": "Invalid 'name' parameter"}), 400

        # Call the add_location function
        result, status_code = add_location(name=name, region=region)
        return jsonify(result), status_code

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"success": False, "error": f"Internal Server Error: {e}"}), 500


@app.route('/db/add_session_location', methods=['POST'])
def db_add_session_location():
    data:dict = request.json

    location_id = data.get('locationId')
    session_id = data.get('sessionId')
    index = data.get('index')
    result, status_code = add_session_location(location_id=location_id,session_id=session_id,index=index)
    return jsonify(result), status_code


@app.route('/db/new_entry', methods=['POST'])
def db_new_entry():
    print(request)
    data: dict = request.json
    session_id = data.get("session_id")
    session_location_id = data.get("session_location_id")
    title = data.get("title", "")
    description = data.get("description", "")
    tagged_description = data.get("tagged_description", "")
    entry_index = int(data.get("entry_index", 0))

    if config.DEBUG : print(f'{config.DM} Calling new_entry({session_id = }, {session_location_id = }, {title = }, {description = }, {tagged_description = }, {entry_index = })')

    result, status_code = new_entry(
        session_id=session_id,
        session_location_id=session_location_id,
        title=title, description=description, 
        tagged_description=tagged_description,
        entry_index=entry_index
    )

    if config.DEBUG: print(f'{config.DM} new_entry() -> {result = }, {status_code = }')

    return jsonify(result), status_code


@app.route('/db/remove_session_location', methods=['DELETE'])
def db_remove_session_location():

    data:dict = request.json

    session_location_id = data.get('session_location_id', '')

    
    result, status_code = remove_session_location(session_location_id=session_location_id)
    return jsonify(result), status_code


################################################################################
#                                   FUNCTIONS                                 #
################################################################################


def get_session_heros(session_id) -> tuple[dict, int]:

    if not is_valid_session(session_id):
        return {'success': False, 'error': f'Unable to retrive session_hero\n{session_id = }, is an invalid id format please provide a 8 digit long id'}, 404
    
    try:
        heros = db.execute(f'''
            SELECT characters.id, characters.name, characters.classe, characters.tag_id, characters.type 
            FROM heros
            JOIN characters ON heros.character_id = characters.id
            WHERE heros.session_id = ?;
            ''',session_id
            )
        return {"success": True, "content": heros}, 200
    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}, 500


def add_tag(tag: str, tag_type: str) -> tuple[dict, int]:
    """
    Create a new tag in the database.

    Args:
        tag (str): The tag string to be added.
        tag_type (str): The type of the tag.

    Returns:
        tuple: A JSON-style response with a status code.
    """
    if not tag.strip() or not tag_type.strip():
        return {"success": False, 'error': 'Tag and tag_type cannot be empty'}, 400

    # Validate tag format
    pattern = r'@JournalEntry\[[^\[\]{}]+\]\{[^\[\]{}]+\}'
    if not re.fullmatch(pattern, tag):
        return {"success": False, 'error': 'Invalid tag format'}, 400

    try:
        if db.execute('SELECT 1 FROM tags WHERE tag = ?;', tag):
            return {"success": False, 'error': f"Tag '{tag}' already exists"}, 400

        # Insert tag
        tag_id = str(uuid.uuid4())
        db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);", tag_id, tag, tag_type)
        return {
            'success': True,
            'content': {
                'id': tag_id,
                'tag': tag,
                'tag_type': tag_type
            }
        }, 200
    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}, 500


def add_location(name: str, region: str = "") -> tuple[dict, int]:
    """
    Add a new location to the database.

    Args:
        name (str): The name of the location.
        region (str, optional): The region of the location. Defaults to "".

    Returns:
        tuple: A JSON-style response with a status code.
    """
    if not name.strip():
        return {'success': False, "error": "Location name cannot be empty"}, 400

    try:
        if db.execute("SELECT 1 FROM locations WHERE name = ?;", name):
            return {'success': False, 'error': f"Location '{name}' already exists in the database"}, 400

        # Create a tag for the location
        tag_name = f"@JournalEntry[{name}]{{{name}}}"
        new_tag, code = add_tag(tag_name, 'location')

        if not new_tag['success']:
            return new_tag, code

        new_tag_data = new_tag.get('content')
        if not new_tag_data:
            return {"success": False, "error": "Unexpected error during tag creation"}, 500

        location_id = str(uuid.uuid4())
        db.execute(
            'INSERT INTO locations (id, name, region, tag_id) VALUES (?, ?, ?, ?);',
            location_id, name, region, new_tag_data['id']
        )
        return {
            'success': True,
            'content': {
                'location_id': location_id,
                'location_name': name,
                'location_region': region,
                'tag_id': new_tag_data['id']
            }
        }, 200

    except Exception as e:
        # Cleanup created tag if location creation fails
        try:
            if new_tag_data and new_tag_data.get('id'):
                db.execute('DELETE FROM tags WHERE id = ?;', new_tag_data['id'])
        except Exception as cleanup_error:
            return {
                "success": False,
                "error": f"Failed to create location and encountered error during cleanup: {cleanup_error}"
            }, 500
        return {"success": False, "error": f"Database error: {e}"}, 500


def add_session_location(location_id: str, session_id: str, index: int) -> tuple[dict, int]:

    if not location_id or not session_id :
        response = {'succes': False, 'error': f'{location_id = }, {session_id = } and {index = } cannot be none' }
        if config.DEBUG : print(f'{config.DM} add_session_location() -> {response} ')
        return response , 500
    

    
    try:

        int_index = int(index)
        new_id = str(uuid.uuid4())
        db.execute('INSERT INTO sessionlocations (id, session_id, location_id, crono_index) VALUES (?, ? , ?, ?);',new_id, session_id, location_id, int_index)

        response = {
            'success': True,
            'content':{ 
                'session_location_id': new_id,       
                'session_id': session_id,
                'location_id': location_id,
                'location_index': int_index,
            }
        }

        if config.DEBUG : print(f'{config.DM} add_session_location() -> {response} ')
        return response, 200
    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}, 500


def remove_session_location(session_location_id: str):
    try:
        db.execute('DELETE FROM sessionlocations WHERE id = ?;', session_location_id)
        return {'success': True, 'content': f'{session_location_id = }'}, 200
    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}, 500


def new_entry(session_id: str = "", session_location_id: str = "", title: str = "", description: str = "", tagged_description: str = "", entry_index: int = 0) -> tuple[dict, int]:

    if not session_id or not session_location_id:
        return {'success': False, 'error': f'Unable to create new entry ({session_id = }) and ({session_location_id = }) cannot be null'}, 400
    
    try:
        new_entry_id = str(uuid.uuid4())
        _ = db.execute(
            'INSERT INTO entries (id, session_id, session_location_id, title, description, tagged_description, entry_index) VALUES (?,?,?,?,?,?,?);',
            new_entry_id, session_id, session_location_id, title, description, tagged_description, entry_index    
        )

        if _:
            return {"success": True, 'content':{
                'entry_id': new_entry_id,
                'session_location_id': session_location_id,
                'session_id': session_id,  
                'entry_title': title,
                'entry_description': description, 
                'entry_tagged': tagged_description, 
                'entry_index': entry_index 
            }}, 200

    except Exception as e:
        return {"success": False, "error": f'DataBaseError: {e}'}, 500 


def update_entry(field: str, value: str, entry_id: str):

    if field == "entry_index":
        try:
            value = int(value)
        except ValueError as e:
            return {"success": False, "error": f"{value} is not an interger"}
    
    try:
        db.execute("""
            UPDATE entries
            SET ? = ?
            WHERE id = ?;

        """,field, value, entry_id )
    except Exception as e:
        return {"success": False, "error": f'DataBaseError: {e}'}, 500

    print(f'DEBUG: Entry {entry_id} as updated {field} to the value: {value}')

    return {"success": True, "content": value, "field": field}, 200


def correct_string(string):

    if not string:
        return {"success": False, 'error': 'no string provided'}, 400
    
    try:
        correction = ai_corrector(string)
    except Exception as e:
        return {"success": False, 'error': f'OpenAI ERROR: {e}'}, 500
    
    if not correction['success']:
        return {"success": False, 'error': 'unable to correct the string'}, 400
    
    if correction[config.LANG] == "":
        return {"success": False, "error": "Unexpected error OpenAi return an empty string"}
    return {'success': correction['success'], 'content': correction[config.LANG]}, 200


def get_tags(type='all'):

    if type == 'all':
        
        try:
            tags = db.execute("SELECT * FROM tags;")            
        except Exception as e:
            return {"success": False, "error": f'DataBaseError: {e}'}, 500
        
    return {'success': True, 'content': tags}, 200


def is_valid_session(session_id) -> bool:

    try:
        int(session_id)
    except ValueError as e:
        return False
    
    pattern = r'^\d{8}$'

    return bool(re.match(pattern, str(session_id)))
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=(int('3000')), debug=True)