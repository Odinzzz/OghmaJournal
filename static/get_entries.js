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
    document.getElementById('heroDropdownSearch').addEventListener('input', function () {
        const filter = this.value.toLowerCase();
        const listItems = document.querySelectorAll('#heroDropdownList .dropdown-item');
        updateDropdown(filter, listItems);
    });

    document.getElementById('locationDropdownSearch').addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    const listItems = document.querySelectorAll('#locationDropdownList .dropdown-item');
    updateDropdown(filter, listItems);
    });

    // Handle form submission
    document.getElementById("addLocationForm").addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent form submission
    
        // Get form data
        const name = document.getElementById("locationName").value;
        const region = document.getElementById("locationRegion").value;
    
        // Prepare the data for the API call
        const locationData = { name, region };
    
        // Call the /db/add_location endpoint via POST
        fetch('/db/add_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(locationData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Create the location object as required by the dropdown function
                const location = {
                    id: data.content.location_id,
                    name: data.content.location_name,
                    region: data.content.location_region
                };
    
                // Add the new location to the dropdown
                const locationItem = locationDropdown(location);
                document.getElementById("locationDropdownList").insertAdjacentHTML('beforeend', locationItem);
    
                // Optionally, close the modal after successful submission
                const addLocationModal = bootstrap.Modal.getInstance(document.getElementById("addLocationModal"));
                addLocationModal.hide();
    
                // Clear form inputs after submission
                this.reset();
            } else {
                // Handle the error from the backend
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => {
            // Handle network or server errors
            console.error('There was an error!', error);
            alert('An unexpected error occurred. Please try again later.');
        });
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
                    const listItems = document.querySelectorAll('#heroDropdownList .dropdown-item');
                    updateDropdown("", listItems)



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

        // Check if the clicked button has the specified class
        if (event.target.classList.contains("add_location_to_database")) {
            // Show the Bootstrap modal
            const addLocationModal = new bootstrap.Modal(document.getElementById("addLocationModal"));
            addLocationModal.show();
        }

        if (event.target.classList.contains('add-location-btn')) {
            const locationId = event.target.dataset.locationId
            const sessionId = document.getElementById('session_id').dataset.sessionId
            const entriesContainer = document.getElementById('entries_container');
            const liCount = Array.from(entriesContainer.children).filter(child => child.tagName === 'LI').length;

            

            const payload = {
                locationId: locationId,
                sessionId: sessionId,
                index: liCount,
            }

            console.log('Calling /db/add_session_location with payload:');
            console.log(payload);
            
            

            fetch('/db/add_session_location', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    console.log('/db/add_session_location -> :');
                    console.log(data.content);
                    
                    
                    const locationName = event.target.dataset.locationName;

                    const location = {
                        session_location_id: data.content.session_location_id,
                        location_name: locationName,
                        location_id: locationId,
                        location_index: liCount,
                    };
                    const [newLocation, _] = locationContainer(location, sessionId);
                    const buttonContainer = document.getElementById('locationDropDownContainer');

                    entriesContainer.insertBefore(newLocation, buttonContainer)
                }else{
                    console.error(data.error);

                    
                }                    
            })
            .catch(err =>{
                // Handle network or unexpected errors
                console.error("Request Failed:", err.message);
                alert(`An error occurred: ${err.message}`);
            });
        }

        if (event.target.classList.contains('add-entry-btn')) {
            
            const sessionId = document.getElementById('session_id').dataset.sessionId
            const locationContainer = event.target.closest('li')
            const sessionLocationId = locationContainer.dataset.sessionLocationId
            const locationEntriesList = locationContainer.querySelector(".entries-container")
            const liCount = Array.from(locationEntriesList.children).filter(child => child.tagName === 'LI').length;

            const payload = {
                session_location_id: sessionLocationId,
                session_id: sessionId,
                entry_index: liCount,
            }

            console.log(payload);
            
            fetch('/db/new_entry',{
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            })
            .then(responce => responce.json())
            .then(data => {
                if (data.success) {
                    const entryData = data.content
                    const newEntryHTML = entry_container(entryData)
                    const entryElement = document.createElement('li');
                    entryElement.classList.add("entry") // added this for the transition animation when delete an
                    entryElement.setAttribute('data-entry-id', entryData.entry_id)
                    entryElement.innerHTML = newEntryHTML;
                    locationEntriesList.appendChild(entryElement);
                    


                }else{
                    console.error(data.error);                    
                }

            })
            .catch(err => {
                alert(err)
                console.error(err);
                
            })
            
        }

        if (event.target.classList.contains('delete_location_btn')) {
            const sessionLocationId = event.target.dataset.sessionLocationId
            const payload = {
                session_location_id: sessionLocationId,
            }
            console.log('DELETE to /db/remove_session_location with payload:');
            console.log(payload);   
            
            fetch('/db/remove_session_location',{
                method: 'DELETE',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            })
            .then(responce => responce.json())
            .then(data => {
                if (data.success) {
                    const locationContainer = event.target.closest('li')
                    console.log(locationContainer);
                    
                    locationContainer.remove()

                
                }else{
                    console.error(data.error);                    
                }
            })
            .catch(err => {
                alert(err)
                console.error(err); 
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


function updateDropdown(filter, listItems) {
    

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
            if (data.locations) { // [0] is to make sure there something in the list  
                addLocationButton = document.getElementById('locationDropDownContainer')
                console.log('im here');
                console.log(data);
                
                
                
                const createdDiv = []; // for updating text area later down the code
                
                // SECTION WHERE ALL THE LOCATION AND ENTRIES IS CREATED
                Object.values(data.locations).forEach(location => {  
                    console.log(location);
                                     
                    
                    const [locationListItem, entriesList] = locationContainer(location, session_id)

                    entries_container.insertBefore(locationListItem, addLocationButton)
                    

                    location.entries.forEach(entry => {
                        const entryHTML = entry_container(entry);
                        const entryElement = document.createElement('li');
                        entryElement.classList.add("entry") // added this for the transition animation when delete an
                        entryElement.setAttribute('data-entry-id', entry.entry_id)
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
        
    fetch("/get_locations", {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        if (data.success){
            const locationDropdownList = document.getElementById("locationDropdownList");

            data.content.forEach(location => {
                
                const listItem = document.createElement('li');
                listItem.innerHTML = locationDropdown(location);
                locationDropdownList.appendChild(listItem)

                
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

function locationContainer(location, sessionId) {

    // Create the main list item
    const listItem = document.createElement('li');
    listItem.id = `${sessionId}_${location.location_id}_${location.location_index}`;
    listItem.setAttribute('data-location-name', location.location_name);
    listItem.setAttribute('data-location-id', location.location_id);
    listItem.setAttribute('data-session-location-id', location.session_location_id);
    listItem.setAttribute('data-chrono-index', location.location_index);

    // Create the heading
    const headingDiv = document.createElement('div')
    headingDiv.classList.add('row', 'justify-content-between')
    const deleteBtn = document.createElement('button')
    deleteBtn.classList.add('btn', 'col-auto','p-0', 'mx-2', 'delete_location_btn')
    deleteBtn.setAttribute('data-session-location-id', location.session_location_id)
    const heading = document.createElement('h3');
    heading.classList.add('col-auto')
    headingDiv.appendChild(heading)
    headingDiv.appendChild(deleteBtn)
    deleteBtn.textContent = '🗑️'
    heading.textContent = location.location_name;
    listItem.appendChild(headingDiv);


    // Create the inner unordered list
    const entriesContainer = document.createElement('ul');
    entriesContainer.className = 'entries-container';
    entriesContainer.id = `entriesContainer_${location.location_name}_${location.location_index}`;
    listItem.appendChild(entriesContainer);

    // Create the new button
    const addEntryButton = document.createElement('button')
    addEntryButton.classList.add('btn', 'btn-primary','mb-2' , 'add-entry-btn')
    addEntryButton.innerHTML = 'New entry'
    listItem.appendChild(addEntryButton)

    return [listItem, entriesContainer];
}

function characterDropdown(character) {

    return `<li><button class="dropdown-item add-hero-btn" data-character-id="${character.id}" data-character-name="${character.name}" >${character.name}</button></li>`
    
}

function locationDropdown(location) {
    
    return `<li><button class="dropdown-item add-location-btn" data-location-id="${location.id}" data-location-name="${location.name}" >${location.name}</button></li>`
}

function heroBadge(character) {
    return`
    
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button data-character-id="${character.character_id}" type="button" class="btn btn-primary no-hover">${character.character_name}</button>
                            <button type="button" data-character-id="${character.character_id}" class="btn text-center remove-hero-btn btn-primary">❌</button>                    
                        </div>
                    
    `
}