document.addEventListener("DOMContentLoaded", () => {
    const new_session_button = document.getElementById("new_session_button");

    new_session_button.addEventListener("click", () => {
        // Disable the button
        new_session_button.disabled = true;

        // Create the popup window
        const popup = document.createElement("div");
        popup.classList.add("popup");
        popup.innerHTML = `
            <div class="popup-content">
                <input type="text" id="session_id_input" placeholder="Enter session ID" />
                <button id="send_session" class="btn btn-primary">Send</button>
                <button id="cancel_session" class="btn btn-secondary">Cancel</button>
                <div id="error_message" class="error-message" style="display: none;"></div>
            </div>
        `;
        document.body.appendChild(popup);

        const sendButton = document.getElementById("send_session");
        const cancelButton = document.getElementById("cancel_session");
        const sessionIdInput = document.getElementById("session_id_input");
        const errorMessage = document.getElementById("error_message");

        cancelButton.addEventListener("click", () => {
            // Close the popup
            document.body.removeChild(popup);
            new_session_button.disabled = false;
        });

        sendButton.addEventListener("click", () => {
            const session_id = sessionIdInput.value;

            // Make the request to /new_session
            fetch('/new_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Show error in the popup
                    errorMessage.textContent = data.error;
                    errorMessage.style.display = 'block';
                    sessionIdInput.value = ''; // Clear input
                } else {
                    // Process successful response
                    const newSessionId = data.content;
                    // Close the popup
                    document.body.removeChild(popup);
                    new_session_button.disabled = false;

                    // Add the new session button to the list
                    const sessionList = document.getElementById("sessions_list");
                    const newListItem = document.createElement("li");
                    newListItem.classList.add("list-group-item");
                    newListItem.innerHTML = `
                        <button data-session-id="${newSessionId}" class="btn btn-primary w-100" onclick="edit_session('${newSessionId}')">
                            ${newSessionId}
                        </button>
                    `;
                    sessionList.insertBefore(newListItem, sessionList.lastElementChild); // Add before the last item
                }
            })
            .catch(err => {
                console.error("Error:", err);
                errorMessage.textContent = "An error occurred. Please try again.";
                errorMessage.style.display = 'block';
                sessionIdInput.value = ''; // Clear input
            });
        });
    });
});

function edit_session(session_id) {
    // Make the request to /edit_session/<session_id> to load the edit page
    window.location.href = `/edit_session/${session_id}`;
}
