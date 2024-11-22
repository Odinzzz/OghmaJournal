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
    

    // Event listener for auto-save on input
    entries_container.addEventListener('input', (event) => {
        const textarea = event.target;

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
        
        if (container) {
            const textarea = container.querySelector('.description-field')
            
             
            
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

        if (event.target.classList.contains("del-btn")) {
            deleteEntry(entryId).then(response => {
                if (response.ok) {
                    event.target.closest('.entry').remove();
                    updateIndices();
                } else {
                    console.error("Error deleting entry");
                }
            });
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

// Fetch entries and render them
function fetchEntries(session_id, entries_container) {
    fetch(`/get_entries/${session_id}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.locations) {
                entries_container.innerHTML = "";
                Object.values(data.locations).forEach(location => {
                    const locationHeader = document.createElement('h3');
                    locationHeader.textContent = location.location_name;
                    entries_container.appendChild(locationHeader);

                    location.entries.forEach(entry => {
                        const entryHTML = entry_container(entry);
                        const entryElement = document.createElement('div');
                        entryElement.innerHTML = entryHTML;
                        entries_container.appendChild(entryElement);
                    });
                });
            } else {
                console.error(`Error: ${data.error}`);
            }
        })
        .catch(err => {
            console.error("Error fetching sessions:", err);
            entries_container.innerHTML = `<p class="text-danger">Failed to load entries. Please try again later.</p>`;
        });
}

// Update indices after deletion
function updateIndices() {
    const entries = document.querySelectorAll('.entry');
    entries.forEach((entry, index) => {
        entry.dataset.entryIndex = index;
        entry.querySelector('textarea').id = `description_field_${index}`;
    });
}

// Backend interaction functions
function tagEntry(entryId) {
    return fetch(`/tool/ai/tag_description/${entryId}`, { method: 'PATCH' }).then(response => response.json());
}

function correctString(string) {
    return fetch(`/tool/ai/correct_string`, { method: 'POST',headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({ 'string': string })  }).then(response => response.json());
}

function deleteEntry(entryId) {
    return fetch(`/db/delete_entry/${entryId}`, { method: 'DELETE' });
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
    document.getElementById('process_journal_button').disabled = disabled;    
    
}
// Entry container function
function entry_container(entry) {
    return `
        <div class="entry shadow-lg border rounded p-2 my-1" data-entry-id="${entry.entry_id }" data-entry-index="${entry.entry_index}">
            <div class="row justify-content-start">
            <div class="col-4 mb-3">
            <label for="title_field_${entry.entry_id}" class="form-label"><strong>Title</strong></label>
                <input type="text" class="form-control" id="title_field_${entry.entry_id}" placeholder="Title" value="${entry.title || "" } ">           
            </div>
            </div>
            <div class="mb-3">
                <label for="description_field_${entry.entry_id}" class="form-label"><strong>Description</strong>

                <button class="btn cor-btn fs-6 m-0 mb-1 p-0" aria-label="correct" data-entry-id="${entry.entry_id}">📖</button>
                </label>                
                <textarea class="form-control description-field m-0" id="description_field_${entry.entry_id}" rows="3">${entry.entry_description || ''}</textarea>
                <div class="row justify-content-between">
                <div class="col-auto">
                <button class="btn  tag-btn fs-6  m-0 mb-1 p-0"  aria-label="tag" data-entry-id="${entry.entry_id}">🏷️</button>
                </div>
                <div class="col-10 p-0 m-0" >
                    <small class="text-body-secondary" class="tag_description_holder" id="tagged_description_holder_${entry.entry_id}">With faded secondary text</small>
                </div>
                <div class="col-1 position-relative">
                    <button class="btn del-btn fs-6 m-0 p-0 position-absolute top-0 end-0" style="right: 20px !important;" aria-label="delete" data-entry-id="${entry.entry_id}">🗑️</button>
                </div>
                </div>
            </div>
            
            
            <div class="row justify-content-end">
                <div class="col-auto">
                <small class="text-body-secondary">ID: ${entry.entry_id} INDEX: ${entry.entry_index}</small>
                </div>
            </div>
        </div>`
    ;
}
