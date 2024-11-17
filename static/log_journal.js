function update_visited_locations() {
const visited_locations = document.getElementById("visited_locations_list")

for (const visited_location in window.journal.locations) {
    if (Object.prototype.hasOwnProperty.call(window.journal.locations, visited_location)) {
        const element = window.journal.locations[visited_location];
        const new_li = document.createElement("li")

        new_li.textContent = element.name

        visited_locations.appendChild(new_li)
        
    }
}
}

function update_heroes() {
    const heros_list = document.getElementById("heros_list")


    for (const hero in journal.heroes_involved) {
        if (Object.prototype.hasOwnProperty.call(journal.heroes_involved, hero)) {
            const element = journal.heroes_involved[hero];
            const new_li = document.createElement("li");
            new_li.textContent = element.name;

            heros_list.appendChild(new_li);           
        }
    }
    
}

function update_encounters() {
    const encouters_locations_list = document.getElementById("encouters_locations_list")

    encouters_locations_list.innerHTML = ""


    for (const location of window.journal.encounters) {

        const location_li = document.createElement("li")
        location_li.innerHTML = `<h2>${location.location}</h2>`

        const individuals_list = createElement("ul")

        encouters_locations_list.appendChild(location_li)
        location_li.appendChild(individuals_list)

        for (const individual of location.individuals) {

            const individual_li = document.createElement('li')
            individual_li.textContent = individual.name

            individuals_list.appendChild(individual_li)
            
        }
        
    }
}

function update_events() {
    const locations_list = document.getElementById("locations_list")

    for (const location of journal.chronology_of_events) {

        const location_li = document.createElement('li')
        location_li.innerHTML = `<h2>${location.location}</h2>`

        locations_list.appendChild(location_li)
        
        const location_events_list = document.createElement("ul")
        
        location_li.appendChild(location_events_list)


        locations_list.appendChild(location_events_list)


        for (const event of location.events) {

            const new_li = document.createElement("li")
            new_li.textContent = event.description

            location_events_list.appendChild(new_li)
            
        }
        
    }
}



document.addEventListener("DOMContentLoaded", async ()=>{

    const response = await fetch("/get_journal");
    const journal = await response.json();

    window.journal = journal;

    update_visited_locations()
    update_heroes()
    update_encounters()
    update_events()
});