let personnagesEntries = [];
let lieuxEntries = [];

const data = {
    characters: [],
    places: [],
};

// Get the entries from relevant folder
game.journal.contents.forEach(entry => {

    let folder_name;

    try {        
        folder_name = entry.folder.name;
    } catch (error) {
        console.log(error);        
    }

    if (folder_name === 'Personnages' ){
        personnagesEntries.push(entry);
    } else if (folder_name === 'Lieux'){
        lieuxEntries.push(entry);
    }
    
});

console.log('DEBUG: step one complete'); 
console.log('DEBUG: Pesonnages');
console.log(personnagesEntries);
console.log('DEBUG: Lieux');
console.log(lieuxEntries);

 
const personnagesContents = [];

personnagesEntries.forEach(entry => {
    personnagesContents.push(entry.pages.contents[0].text.content);
});

const lieuxContents = [];

lieuxEntries.forEach(entry => {
    lieuxContents.push(entry.pages.contents[0].text.content);
});


let regex = /@JournalEntry\[[^\]]+\]\{[^\}]+\}/g;

let alltag = [];
let journalJson = {};

// Extract and process the JournalEntry tags
personnagesContents.forEach(content => {
    let matches = content.match(regex);

    console.log(matches);
    
    
    if (matches) {
        matches.forEach(match => {
            let journalMatch = match.match(/@JournalEntry\[(.+?)\]\{(.+?)\}/);
            if (journalMatch) {
                              
                
                data.characters.push({
                    name: journalMatch[1],
                    tag: match,
                })
                
            }
        });
    } else {
        console.warn(`No matches found in content: ${content}`);
    }
});

lieuxContents.forEach(content => {
    let matches = content.match(regex);

    console.log(matches);
    
    
    if (matches) {
        matches.forEach(match => {
            let journalMatch = match.match(/@JournalEntry\[(.+?)\]\{(.+?)\}/);
            if (journalMatch) {
                              
                
                data.places.push({
                    name: journalMatch[1],
                    tag: match,
                })
                
            }
        });
    } else {
        console.warn(`No matches found in content: ${content}`);
    }
});

// Log the JSON result
console.log(data);

console.log(JSON.stringify(data))

function exportDataToFile(data) {
    // Sample data to export
    
  
    // Convert data to JSON string
    const jsonString = JSON.stringify(data);
  
    // Create a Blob and download link
    const blob = new Blob([jsonString], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'all_tags.json'; // File name
    link.click();
  }
  
  exportDataToFile(data);
  