document.addEventListener("DOMContentLoaded", () => {
    const sessions_list = document.getElementById("sessions_list");

    // Send a POST request to fetch sessions from the server
    fetch('/get_sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.sessions) {
            // Loop through the sessions and create a button for each session
            data.sessions.forEach(session => {
                const newListItem = document.createElement("li");
                newListItem.classList.add("nav-item");

                newListItem.innerHTML = `
                    <button data-session-id="${session.id}" class="nav-link" onclick="edit_session('${session.id}')">
                        ${session.id}
                    </button>
                `;

                // Append the new button before the "Add New Session" button
                sessions_list.insertBefore(newListItem, sessions_list.querySelector("#new_session_button").parentElement);
            });
        }
    })
    .catch(err => {
        console.error("Error fetching sessions:", err);
    });
});

function edit_session(session_id) {
    // Redirect to the edit session page
    window.location.href = `/edit_session/${session_id}`;
}
