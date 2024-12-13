// Function to download an image and return a Blob
async function getBlob(imageUrl) {
    try {
        const response = await fetch(imageUrl);
        const blob = await response.blob();
        return blob;
    } catch (error) {
        console.error('Error fetching image:', error);
        throw error; // Re-throw the error to be caught in the calling function
    }
}

// Function to download and save the image to IndexedDB
async function downloadAndSaveImageToIndexedDB(imageUrl, fileName) {
    try {
        // Fetch the image as a Blob
        const blob = await getBlob(imageUrl);

        // Prepare file data to store in IndexedDB
        const fileData = {
            name: fileName,
            blob: blob,
            createdAt: new Date(),
        };

        // Open IndexedDB
        const request = indexedDB.open('myDatabase', 1);

        request.onsuccess = (event) => {
            const db = event.target.result;
            // Create a transaction
            const transaction = db.transaction(['filesStore'], 'readwrite');
            const objectStore = transaction.objectStore('filesStore');

            // Add the file data to the object store
            const addRequest = objectStore.add(fileData);

            // Handle success/failure of adding data
            addRequest.onsuccess = () => {
                console.log('Image saved to IndexedDB!');
            };

            addRequest.onerror = (event) => {
                console.error('Error saving image:', event);
            };

            // Ensure transaction does not complete until the image is added
            transaction.oncomplete = () => {
                console.log('Transaction complete');
            };

            transaction.onerror = (event) => {
                console.error('Transaction failed:', event);
            };
        };

        // Handle database upgrade (create object store if not exists)
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            const objectStore = db.createObjectStore('filesStore', { keyPath: 'id', autoIncrement: true });
            objectStore.createIndex('name', 'name', { unique: false });
        };

        request.onerror = (event) => {
            console.error('Error opening IndexedDB:', event);
        };
    } catch (error) {
        console.error('Error downloading or saving image:', error);
    }
}

    
    






// Example usage (download and save image to IndexedDB)
downloadAndSaveImageToIndexedDB('Tokens/DALL%C2%B7E%202024-08-01%2017.14.20%20-%20A%20professional-quality%20photography%20image%20of%20an%20evil%20orc%20warrior%20dressed%20in%20full%20plate%20armor%2C%20more%20muscular%20and%20fearsome%2C%20and%20armed%20with%20a%20long%20spear%2C%20.webp', 'downloaded_image.jpg');



// ##########################################################################################################################################################


function retrieveBlobAndDownload(id, fileName) {
    const request = indexedDB.open('myDatabase', 1);

    request.onerror = (event) => {
        console.error('Error opening IndexedDB:', event);
    };

    request.onsuccess = (event) => {
        const db = event.target.result;
        const transaction = db.transaction(['filesStore'], 'readonly');
        const objectStore = transaction.objectStore('filesStore');

        const getRequest = objectStore.get(id);
        getRequest.onsuccess = (event) => {
            const fileData = event.target.result;

            if (fileData) {
                // Create a Blob URL from the retrieved Blob
                const blobUrl = URL.createObjectURL(fileData.blob);

                // Create a temporary anchor element
                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = fileName;  // Set the file name
                document.body.appendChild(a);  // Append to the DOM
                a.click();  // Trigger the download

                // Clean up
                document.body.removeChild(a);
                URL.revokeObjectURL(blobUrl);  // Release memory
                console.log('Image downloaded to PC!');
            } else {
                console.log('No image found with this ID');
            }
        };
        getRequest.onerror = (event) => {
            console.error('Error retrieving image from IndexedDB:', event);
        };
    };
}

// Example usage (retrieve image from IndexedDB and save to file)
retrieveBlobAndDownload(1, 'downloaded_image_from_db.jpg');








// ############################################################################################################

function exportDataToFile(data, fileName) {
    // Sample data to export
    
  
    // Convert data to JSON string
    const jsonString = JSON.stringify(data);
  
    // Create a Blob and download link
    const blob = new Blob([jsonString], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName; // File name
    link.click();
    link.remove()
  }


function getBlob(imageUrl, fileName) {
    
    fetch(imageUrl)
    .then(response => response.blob())
    .then(blob => {

        const fileData = {
            name: fileName,
            blob: blob,
            createdAt: new Date(),
        }

        exportDataToFile(fileData)

    })
}




getBlob('Tokens/DALL%C2%B7E%202024-08-01%2017.14.20%20-%20A%20professional-quality%20photography%20image%20of%20an%20evil%20orc%20warrior%20dressed%20in%20full%20plate%20armor%2C%20more%20muscular%20and%20fearsome%2C%20and%20armed%20with%20a%20long%20spear%2C%20.webp', 'downloaded_image.json');


// ####################################################################--WORKING--##################################################################

// Function to export an image Blob as a file
function downloadImage(blob, fileName) {
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob); // Create a URL for the Blob
    link.href = url;
    link.download = fileName; // Set the file name for the download
    link.click(); // Trigger the download
    URL.revokeObjectURL(url); // Clean up the object URL after download
}

// Function to fetch image and download it
function getBlob(imageUrl, fileName) {
    fetch(imageUrl)
        .then(response => response.blob()) // Fetch the image as a Blob
        .then(blob => {
            // Download the image as a file
            downloadImage(blob, fileName); // Use the Blob to download the image
        })
        .catch(error => {
            console.error('Error fetching image:', error);
        });
}

// Usage example: Fetch the image and download it
getBlob('Tokens/DALL%C2%B7E%202024-08-01%2017.14.20%20-%20A%20professional-quality%20photography%20image%20of%20an%20evil%20orc%20warrior%20dressed%20in%20full%20plate%20armor%2C%20more%20muscular%20and%20fearsome%2C%20and%20armed%20with%20a%20long%20spear%2C%20.webp', 'downloaded_image.webp');



// ####################################################################################################################################################

async function saveFileToCustomLocation(blob, fileName) {
    try {
        // Request the user to pick a location to save the file
        const handle = await window.showSaveFilePicker({
            suggestedName: fileName, // Default file name
            types: [
                {
                    description: 'Image Files',
                    accept: { 'image/*': ['.jpg', '.png', '.webp'] },
                },
            ],
        });

        // Create a writable stream to write the Blob to the file
        const writable = await handle.createWritable();
        await writable.write(blob); // Write the Blob data to the file
        await writable.close(); // Close the stream after writing
        console.log('File saved successfully');
    } catch (error) {
        console.error('Error saving file:', error);
    }
}

// Function to fetch the image and save it to a custom location
function getBlob(imageUrl, fileName) {
    fetch(imageUrl)
        .then(response => response.blob())
        .then(blob => {
            // Call the save function to allow the user to choose where to save
            saveFileToCustomLocation(blob, fileName);
        })
        .catch(error => {
            console.error('Error fetching image:', error);
        });
}

// Usage example
getBlob('Tokens/DALL%C2%B7E%202024-08-01%2017.14.20%20-%20A%20professional-quality%20photography%20image%20of%20an%20evil%20orc%20warrior%20dressed%20in%20full%20plate%20armor%2C%20more%20muscular%20and%20fearsome%2C%20and%20armed%20with%20a%20long%20spear%2C%20.webp', 'downloaded_image.webp');
