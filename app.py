import uuid
import re



from flask import Flask, jsonify,render_template, request, abort
from cs50.sql import SQL



from config.config import config
from scripts.quill_processing import quill_processing
from ai import ai_check


app = Flask(__name__)

db = SQL(config.SQLALCHEMY_DATABASE_URI)



@app.route("/get_sessions", methods=['POST'])
def get_sessions():
    sessions = db.execute('SELECT id FROM sessions')
    print(sessions)

    return jsonify({"sessions": sessions})


@app.route("/get_html", methods=['POST'])
def get_html() -> dict:
    """retrieve the draft text

    Returns:
        dict: {'success': bool, 'html_content': html}
    """

    data = request.json

    html = db.execute('SELECT html FROM sessions WHERE id = ?;', data['session_id'])

    print(html)

    return jsonify({'success': True, 'html_content': html[0]['html'] })


@app.route("/save_draft", methods=['POST'])
def save_draft():
    data = request.json

    print(data['html'])

    db.execute("UPDATE sessions SET html = ? WHERE id = ?", data['html'], data['session_id'])

    return {"success": "success"}


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/new_session", methods=["POST"])
def new_session():

    data = request.json

    session_id = data['session_id']

    try:
        int(session_id)
    except ValueError as e:
        return {'error': f'{e} session id must be in format yyyymmdd'}
    
    if len(session_id) != 8:
        return {'error': f'{session_id} {len(session_id)} session id must be in format yyyymmdd'}
    
    if db.execute('INSERT INTO sessions (id) VALUES (?);', session_id):
        return {"content": session_id}
    else:
        return {'error': 'session already exist'}
    

@app.route("/edit_session/<session_id>")
def edit_session(session_id):
    dnd_session = db.execute("SELECT * FROM sessions WHERE id=?",session_id)

    

    if dnd_session:

        if dnd_session[0]['session_state'] == 0:
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
        return jsonify({"error": "Bad request: content or session_id cannot be null"})

    # check if session id exist
    check_id = db.execute("SELECT id FROM sessions WHERE id = ?", session_id )
    if not check_id:
        return jsonify({"error": f"Bad request: no session with id :{session_id}"}) 
    
    try:
        process_content = quill_processing(content)
    except ValueError as e:
        return jsonify({"error": f"{e}"}) # order list not use or empty
    
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

    

    for location in process_content:

        for location_index, location_name in enumerate(location):
            location_id = location_dict.get(location_name)

            if not location_id: # check with ai if there is a typo or not

                
                try:
                    check = ai_check(location_name, location_dict)
                except:
                    return jsonify({"error": 'Unknow error from openAi'}), 500


                if check['exist'] == False: # No Typo new entry

                    tag_id = str(uuid.uuid4())
                    tag = db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);",tag_id, check["foundry_tag"], 'location')
                    location_id = str(uuid.uuid4())
                    location_db = db.execute("INSERT INTO locations (id, name, tag_id) VALUES (?, ?, ?);", location_id, check["name"], tag_id  )
                    location_dict[check['name']] = {"id": location_id, 'tag': check["foundry_tag"]} 

                    if location_db:

                        print(f'DEBUG: New location created into database location_name: {check["name"]} with id: {location_id}')

                    else:

                        return jsonify({"error": "fail to create new database entry"})
                    
                else: # Typo already exist in the database
                    check_name: str = check.get('name')
                    if not check_name:
                        return jsonify({'error': 'ai messed up'})                   
                    location_id = db.execute("SELECT id FROM locations WHERE name = ?", check_name )
                    if not location_id:
                        return jsonify({"error": "fail to retrieve database entry"})
                    location_id = location_id['0']['id'] # make sure that location id is a string
            else:

                location_id = location_id['id'] # make sure that location id is a string 


            db.execute("INSERT INTO sessionlocations (session_id, location_id, crono_index) VALUES (?, ?, ?);", session_id, location_id , int(location_index))


            for event_index, event in enumerate(location[location_name]):

                entry_id = str(uuid.uuid4())
                db.execute("INSERT INTO entries (id, description, session_id, location_id, entry_index ) VALUES (?,?,?,?,?);", entry_id, event, session_id, location_id, int(event_index))
                print(f'DEBUG: Entry created with id: {entry_id} at index: {event_index} content:{event}')


    db.execute("UPDATE sessions SET session_state = 1 WHERE id = ?;", session_id)
            


    return jsonify({"session": session_id})

    
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
        return jsonify({'error': 'Fail to create character: Name and Tag cannot be Null'})
    
    pattern = r'@JournalEntry\[[^\[\]{}]+\]\{[^\[\]{}]+\}'
    tag_check = re.fullmatch(pattern, tag)

    if not tag_check:
        return jsonify({'error': 'Fail to create character: Tag must be formated like @JournalEntry[foundry_name]{alias}'})

    if not classe:
        classe = ""
    if not char_type:
        char_type = ""

    tag_check = db.execute('SELECT * FROM tags WHERE tag = ?;', tag)
    if tag_check:
        return jsonify({'error': 'Fail to create character: Tag already exist'})
    
    character_check = db.execute('SELECT * FROM characters WHERE name = ?;', name)
    if character_check:
        return jsonify({'error': 'Fail to create character: Character already exist'})
    
    # dataBase entry creation
    character_id = str(uuid.uuid4())
    tag_id = str(uuid.uuid4())
    
    db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);", tag_id, data['tag'], 'character'  )
    db.execute("INSERT INTO characters (id, name, classe, type, tag_id) VALUE (?, ?, ?, ?, ?);", character_id, name, classe, char_type, tag_id)

    return jsonify({
        'id': character_id,
        'name': name,
        'classe': classe,
        'char_type': char_type,
        'tag': tag,
        'tag_id': tag_id
        })


@app.route("/db/add_tag", methods=["POST"])
def db_add_tag():
    """
    data = {
        tag: NN must be @JournalEntry[foundry_name]{alias}
        tag_type: NN location, character, faction, item, ...
    }
    """
    data: dict = request.json

    tag = data.get('tag')
    tag_type = data.get('tag_type')

    if not tag_type or not tag:
        return jsonify({'error': 'Fail to create Tag: {tag_type} and {tag} cannot be Null'})
    
    pattern = r'@JournalEntry\[[^\[\]{}]+\]\{[^\[\]{}]+\}'
    tag_check = re.fullmatch(pattern, tag)

    if not tag_check:
        return jsonify({'error': 'Fail to create Tag: {tag} must be formated like @JournalEntry[foundry_name]{alias}'})
    
    tag_id = str(uuid.uuid4())
    db.execute("INSERT INTO tags (id, tag, tag_type) VALUES (?, ?, ?);", tag_id, data['tag'], 'character'  )

    return jsonify({
        'id': tag_id,
        'tag': tag,
        'tag_type': tag_type
    })
