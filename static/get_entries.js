document.addEventListener("DOMContentLoaded", () => {
    const entries_container = document.getElementById('entries_container');
    const session_id = document.getElementById('session_id').innerText;

    console.log(session_id);

    // Fetch entries
    fetchEntries(session_id, entries_container);

    // Auto-save handler state
    const autoSaveTimers = new Map();

    textareas = entries_container.querySelectorAll("textarea.description-field")

    console.log(textareas);
    
    // HERO DROP DOWN
    document.getElementById('dropdownSearch').addEventListener('input', function () {
        const filter = this.value.toLowerCase();
        updateDropdown(filter);
      });
    
      

    // Event listener for auto-save on input
    entries_container.addEventListener('input', (event) => {
        const textarea = event.target;

        resizeTextArea(textarea);

        if (textarea.classList.contains('description-field')) {
            const textarea_parent = textarea.closest('.entry');
            
            const entryId = textarea_parent.dataset.entryId;
            const newDescription = textarea.value;

            // Add visual feedback for editing
            textarea.classList.add('border-danger');
            disabled_btn(textarea_parent, true)

            // Clear existing timer, if any
            if (autoSaveTimers.has(entryId)) {
                clearTimeout(autoSaveTimers.get(entryId));
            }

            // Set a new timer for auto-save
            const timer = setTimeout(() => {
                update_entry(entryId,'description', newDescription, textarea);
            }, 2000);

            autoSaveTimers.set(entryId, timer);
        }   
    });

    // Event listener for buttons
    document.addEventListener("click", (event) => {
        const entryId = event.target.dataset.entryId;
        const container = event.target.closest('.entry')

        
        
        if (event.target.classList.contains("title-btn")) {
            event.target.disabled = true;
            generateTitle(entryId).then(data => {
                if (data.success) {

                    const title_field = document.querySelector(`#title_field_${entryId}`);

                    title_field.value = data.content;
                    event.target.disabled = false;                    
                }else{
                    console.log(`Error generating title ${data.error}`);
                    event.target.disabled = false;                    
                }
            });     
        }


        if (event.target.classList.contains("lock-btn")) {
            console.log('🔒');
            
            if (event.target.innerHTML === "🔓"){
                event.target.innerHTML = "🔒";
                //TODO: add logic to lock the entry
            }else{
                event.target.innerHTML = "🔓";
                //TODO: add logic to unlock the entry
            }
        }


        if (event.target.classList.contains("tag-btn")) {

            event.target.disabled = true;

            tagEntry(entryId).then(data => {
                if (data.success) {                
                    
                    const tag_holder = document.querySelector(`#tagged_description_holder_${entryId}`);
                    
                    tag_holder.innerHTML = data.content;
                    event.target.disabled = false;
                } else {
                    console.error(`Error tagging entry ${data.error}`);
                    event.target.disabled = false;
                }
            });
        }

        if (event.target.classList.contains("cor-btn")) {
            event.target.disabled = true;
            const container = event.target.closest('.entry')
            const textarea = container.querySelector('.description-field')
            correctString(textarea.value).then(data => {
                if (data.success) {
                    
                    textarea.value = data.content;
                    update_entry(entryId,'description', textarea.value, textarea)
                    event.target.disabled = false;
                } else {
                    console.error(`Error correcting entry ${data.error}`);
                    event.target.disabled = false;
                }
            });
        }

        // TODO: Make this great again (the delete dont check if it work in the back end)
        if (event.target.classList.contains("del-btn")) {
            deleteEntry(entryId).then(response => {
                if (response.ok) {
                    const location = event.target.closest('ul');
                    console.log(location);
                    const item = event.target.closest('li');
                    removeItem(item)
                    updateIndices(location);
                } else {
                    console.error("Error deleting entry");
                }
            });
        }

        if (event.target.classList.contains("add-hero-btn")) {
            const characterId = event.target.dataset.characterId
            const characterName = event.target.dataset.characterName
            const sessionId = document.getElementById("session_id").dataset.sessionId
            console.log(`${sessionId} ${characterId} ${characterName} `);
            
            addHero(sessionId, characterId, characterName).then(data => {
                if (data.success) {
                    const heroDropDownContainer = document.getElementById("heroDropDownContainer")
                    const heroContainer = document.getElementById('heroContainer')
                    const dropdownSearch = document.getElementById('dropdownSearch')
                    const newHeroBadge = document.createElement('div')
                    newHeroBadge.classList.add('col-auto', 'mb-1', 'badge-container')
                    newHeroBadge.innerHTML = heroBadge(data.content)
                    heroContainer.insertBefore(newHeroBadge, heroDropDownContainer);
                    dropdownSearch.value = ""
                    updateDropdown("")



                } else {
                    console.error(`Error deleting entry ${data.error}`);
                }
            });
        }

        if (event.target.classList.contains("remove-hero-btn")) {
            const characterId = event.target.dataset.characterId
            const sessionId = document.getElementById("session_id").dataset.sessionId
            event.target.disabled = true;
            removeHero(sessionId, characterId).then(data =>{
                if (data.success){
                    const badge = event.target.closest(".badge-container")

                    if (badge){

                        
                        badge.remove()
                    }else{
                        console.error(badge);

                        event.target.disabled = false;
                    }
                }else{
                    console.error(data.error);
                    event.target.disabled = false;

                    
                }
            })
        }


    });

    // Function to tag all descriptions in one go
    document.getElementById('tagall').addEventListener('click', () => {
        const entries = document.querySelectorAll('.entry');
        entries.forEach(entry => {
            const entryId = entry.dataset.entryId;
            const tagButton = entry.querySelector('.tag-btn');
            if (!tagButton.disabled) {
                tagButton.disabled = true;
                tagEntry(entryId).then(data => {
                    if (data.success) {
                        
                        const tag_holder = document.querySelector(`#tagged_description_holder_${entryId}`);
                        
                        tag_holder.innerHTML = data.content;
                        tagButton.disabled = false;
                    } else {
                        console.error(`Error tagging entry ${data.error}`);
                        tagButton.disabled = false;
                    }
                });
            }
        });
    });

});


function updateDropdown(filter) {
    const listItems = document.querySelectorAll('#heroDropdownList .dropdown-item');

    listItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(filter)) {
            item.style.display = ''; // Show item
        } else {
            item.style.display = 'none';
        }
    });
}

function resizeTextArea(textArea) {
    if (textArea.tagName === 'TEXTAREA') {
        // Reset the height to allow shrinking before measuring content height
        textArea.style.height = 'auto';
        
        // Set the height based on the scrollHeight (content height)
        textArea.style.height = `${textArea.scrollHeight + 2}px`;
    }
}

// Fetch entries and render them
function fetchEntries(session_id, entries_container) {
    fetch(`/get_entries/${session_id}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.locations[0]) { // [0] is to make sure there something in the list  
                entries_container.innerHTML = "";
                
                const createdDiv = []; // Collect created divs
                
                Object.values(data.locations).forEach(location => {
                    const locationListItem = document.createElement('li')
                    const locationHeader = document.createElement('h3');
                    const entriesList = document.createElement('ul')
                    locationListItem.appendChild(locationHeader)
                    locationListItem.appendChild(entriesList)
                    locationHeader.textContent = location.location_name;
                    entries_container.appendChild(locationListItem);

                    location.entries.forEach(entry => {
                        const entryHTML = entry_container(entry);
                        const entryElement = document.createElement('li');
                        entryElement.classList.add("entry") // added this for the transition animation when delete an
                        entryElement.innerHTML = entryHTML;
                        entriesList.appendChild(entryElement);

                        createdDiv.push(entryElement); // Push created entry div
                    });
                });

                // Ensure textareas are resized after all elements are added to the DOM
                setTimeout(() => {
                    for (const div of createdDiv) {
                        const textArea = div.querySelector('.description-field');
                        if (textArea) {
                            resizeTextArea(textArea);
                            console.log(`Textarea in ${div} has been resized.`);
                        }
                    }
                }, 0);
            } else {
                console.log(data);
                
                console.error(`Error: ${data.error}`);
            }
        })
        .catch(err => {
            console.error("Error fetching sessions:", err);
            entries_container.innerHTML = `<p class="text-danger">Failed to load entries. Please try again later.</p>`;
        });

    fetch(`/get_heros/${session_id}`, {method: 'GET'})
        .then(response => response.json())
        .then(data =>{
            if (data.success) {
                heroContainer = document.getElementById('heroContainer')
                data.content.forEach(character => {

                    const newHeroBadge = document.createElement('div')
                    newHeroBadge.classList.add('col-auto', 'mb-1', 'badge-container')
                    newHeroBadge.innerHTML = heroBadge(character)
                    heroContainer.insertBefore(newHeroBadge, heroDropDownContainer);

                })
                
            } else {

                console.error(data.error);
                
            }
        })
        .catch(err => { 
            
        })
        
    
    fetch("/get_characters", {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const heroDropdownList = document.getElementById("heroDropdownList");

                data.content.forEach(character => {
                    console.log(character);
                    const listItem = document.createElement('li');
                    listItem.innerHTML = characterDropdown(character);
                    heroDropdownList.appendChild(listItem)

                    
                })


            }else{
                console.error(data.error);
                
            }
        })
        .catch(err => {
            console.error("Error Fetching Character: ", err);
            
        });    

}


// Update indices after deletion
function updateIndices(location) {
    const entries = location.querySelectorAll('.entry');
    entries.forEach((entry, index) => {
        const entryId = entry.dataset.entryId
        fetch(`/db/update_entry/entry_index`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ entry_id: entryId, 'new_value': index }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`DEBUG: entry id:${entryId} set to index ${index}`);
                
            } else {
                console.log(data.error);
                
            }
        })
        
    });
}

// Backend interaction functions
function tagEntry(entryId) {
    return fetch(`/tool/ai/tag_description/${entryId}`, { method: 'PATCH' }).then(response => response.json());
}

function addHero(sessionId, characterId, characterName) {
    const payload = {
        session_id: sessionId,
        character_id: characterId,
        character_name: characterName,
    }
    
    
    return fetch("/db/add_hero", { 
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(payload)  
    }).then(response => response.json());
    
}

function removeHero(sessionId, characterId) {
    const payload = {
        session_id: sessionId,
        character_id: characterId,
    }

    return fetch("/db/remove_hero", {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(payload)  
    }).then(response => response.json());
    
}

function correctString(string) {
    return fetch(`/tool/ai/correct_string`, { method: 'POST',headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({ 'string': string })  }).then(response => response.json());
}

function generateTitle(entryId) {
    return fetch(`/tool/ai/generate_title/${entryId}`, { method: 'PATCH'}).then(response => response.json())
}

function deleteEntry(entryId) {
    return fetch(`/db/delete_entry/${entryId}`, { method: 'DELETE' });
}

function removeItem(item) {
    if (item) {
      // Add fade-out class
      item.classList.add('fade-out');
      // Use transitionend to ensure removal happens after animation
      item.addEventListener('transitionend', () => {
        item.remove();
      });
    }
  }
  

// Save description to backend
function update_entry(entryId,field, description, textarea) {
    container = textarea.closest('.entry');
    disabled_btn(container, false)
    fetch(`/db/update_entry/${field}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entry_id: entryId, 'new_value': description }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI after saving
                textarea.classList.remove('border-danger');
                textarea.classList.add('border-success');
                disabled_btn(container, false);
            } else {
                console.error(`Error saving description ${data.error}`);
                disabled_btn(container, false);
            }
        })
        .catch(err => {
            console.error("Error during save:", err);
        });
}

// enable or disable button 
function disabled_btn(container, disabled= true) {
    
    container.querySelector('.tag-btn').disabled = disabled;
    container.querySelector('.del-btn').disabled = disabled;
    container.querySelector('.cor-btn').disabled = disabled;
    container.querySelector('.title-btn').disabled = disabled;
    document.getElementById('process_journal_button').disabled = disabled;    
    
}
// Entry container function
function entry_container(entry) {
    return `
    
        <div class="shadow-lg border rounded position-relative p-2 my-2" data-entry-id="${entry.entry_id }" data-entry-index="${entry.entry_index}">
            <div class=" position-absolute top-0 end-0">
            <button class="btn down-btn fs-6 m-0 p-0 " aria-label="down" data-entry-id="${entry.entry_id}">⬇️</button>
            <button class="btn up-btn fs-6 m-0 p-0 " aria-label="Up" data-entry-id="${entry.entry_id}">⬆️</button>
            <button class="btn lock-btn fs-6 m-0 p-0 " aria-label="lock" data-entry-id="${entry.entry_id}">🔓</button>
            </div>
            <div class="row justify-content-start">
            <div class="col-4 mb-3">
            <label for="title_field_${entry.entry_id}" class="form-label"><strong>Title</strong><button class="btn title-btn fs-6  m-0 mb-1 p-0"  aria-label="tag" data-entry-id="${entry.entry_id}">🔄️</button></label>
                <input type="text" class="form-control" id="title_field_${entry.entry_id}" placeholder="Title" value="${entry.entry_title || "" } ">           
            </div>
            </div>
            <div class="mb-3">
                <label for="description_field_${entry.entry_id}" class="form-label"><strong>Description</strong>

                    <button class="btn cor-btn fs-6 m-0 mb-1 p-0" aria-label="correct" data-entry-id="${entry.entry_id}">📖</button>
                    <button class="btn  tag-btn fs-6  m-0 mb-1 p-0"  aria-label="tag" data-entry-id="${entry.entry_id}">🏷️</button>
                </label>                
                <textarea class="form-control description-field m-0" style="resize: none;" id="description_field_${entry.entry_id}" rows="3">${entry.entry_description || ''}</textarea>
                <div class="row justify-content-between">
                
                <div class="col-10  mx-3" >
                    <small class="text-body-secondary" class="tag_description_holder" id="tagged_description_holder_${entry.entry_id}">${entry.entry_tagged || ''}</small>
                </div>
                <div class="col-1 mb-2 position-relative">
                    <button class="btn del-btn fs-6 m-0 p-0 position-absolute top-0 end-0" style="right: 20px !important;" aria-label="delete" data-entry-id="${entry.entry_id}">🗑️</button>
                </div>
                </div>
            </div>
            
            
            <div hidden class="row justify-content-start">
                <div class="col-auto">
                <small class="text-body-secondary">ID: ${entry.entry_id} INDEX: ${entry.entry_index}</small>
                </div>
            </div>
        </div>
    `
    ;
}

function characterDropdown(character) {

    return `<li><button class="dropdown-item add-hero-btn" data-character-id="${character.id}" data-character-name="${character.name}" >${character.name}</button></li>`
    
}

function heroBadge(character) {
    return`
    
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button data-character-id="${character.character_id}" type="button" class="btn btn-primary no-hover">${character.character_name}</button>
                            <button type="button" data-character-id="${character.character_id}" class="btn text-center remove-hero-btn btn-primary">❌</button>                    
                        </div>
                    
    `
}