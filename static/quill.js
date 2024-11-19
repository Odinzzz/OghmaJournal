document.addEventListener("DOMContentLoaded", () => {
    const quill = new Quill('#editor', {
        theme: 'snow'
    });

    const sessionId = document.querySelector('#editor').getAttribute('data-session-id');

    // Fetch HTML from the backend when the page loads
    fetch('/get_html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ session_id: sessionId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.html_content) {
            // If content is returned, load it into Quill
            quill.root.innerHTML = data.html_content;
        } else {
            console.error("Error loading HTML content:", data.error);
        }
    })
    .catch(error => {
        console.error("Error fetching HTML:", error);
    });



    const saveButton = document.getElementById("save_btn");
    const processButton = document.getElementById("process_btn");
    const saveWidget = document.getElementById("save_widget");

    let typingTimeout = null;
    

    // Change the widget to red when editing
    quill.on('text-change', function() {
        saveButton.classList.remove("btn-success");
        saveButton.classList.add("btn-danger");
        saveButton.textContent = "Not Saved";

        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            saveDraft();
        }, 2000); // Save after 2 seconds of inactivity
    });

    // Save draft content
    function saveDraft() {
        const editorContent = quill.root.innerHTML;

        // Send the editor content to backend via POST request
        fetch('/save_draft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                html: editorContent
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Change the widget to green after saving
                saveButton.classList.remove("btn-danger");
                saveButton.classList.add("btn-success");
                saveButton.textContent = "Saved";
            } else {
                // Handle error
                alert("Failed to save draft.");
            }
        })
        .catch(error => {
            console.error("Error saving draft:", error);
            alert("Failed to save draft.");
        });
    }

    // Process button - sends the content for further processing
    processButton.addEventListener("click", () => {
        processButton.disabled = true;
        processButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...`;

        const editorContent = quill.getSemanticHTML();

        fetch('/process_draft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                html: editorContent
            })
        })
        .then(response => response.json())
        .then(data => {
            processButton.disabled = false;
            processButton.innerHTML = "Process";

            if (data.error) {
                // Display error below the editor
                const errorMessage = document.createElement("div");
                errorMessage.classList.add("alert", "alert-danger");
                errorMessage.textContent = "Error: " + data.error;
                document.querySelector("#editor").after(errorMessage);
            } else {
                // Redirect to the route returned by backend
                window.location.href = data.redirect_url || '/';
            }
        })
        .catch(error => {
            console.error("Error processing draft:", error);
            processButton.disabled = false;
            processButton.innerHTML = "Process";
        });
    });
});
