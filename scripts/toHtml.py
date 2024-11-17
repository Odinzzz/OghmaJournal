import json
import os






def toHtml(journal):



    locations = ''

    for location in journal['locations']:

        locations += f"<li><p><strong>{location['tag']}</strong><br><em>{location['note']}</em></p></li>"

    personages = ''

    for personage in journal['heroes_involved']:

        personages += f"<li><strong>{personage['tag']}</strong> - <em>{personage['role']}</em></li>"

    encounters = ''

    if len(journal['encounters']) == 0:
        encounters = "<p><em>(This section would detail any significant individuals or creatures encountered during the mission. As it stands, no such information is recorded for this day.)</em></p>"
    else:

        for encounter in journal['encounters']:
            location = encounter['tag']
            for individual in encounter["individuals"]: 

                encounters += f"<li><p><strong>{individual['tag']}</strong> - <em>{individual['title']} - {individual['role']}</em><br><em>(Encountered at {location})</em></p></li>"
    events = ''

    for location in journal["chronology_of_events"]:
        events += f"<h5><strong>{location['tag']}</strong></h5><ol>"
        for event in location['events']:

            events += f"<li><p><strong>{event['event_title']}</strong><br>{event['tagged_description']}</p></li>"


        events += '</ol>'
    
    template = f'''
    
    <hr>
    <h2>Report Date: {journal["report_date"]}</h2>
    <hr>
    <h4><strong>Location:</strong></h4>
    <ul>
        {locations}
    </ul>
    <hr>
    <h4><strong>Heroes Involved:</strong></h4>
    <ul>
        {personages}
    </ul>
    <hr>
    <h4><strong>Encounters of the Day:</strong></h4>
    <ul>
        {encounters}
    </ul>
    <hr>
    <h4><strong>Chronology of Events:</strong></h4>
        {events}
    <hr>
    <h2><strong>Conclusion:</strong></h2>
        {journal['conclusion']['summary']}

    '''

    return template















if __name__ == "__main__":
    id = input("session id: ")
    file = 'journalFinal.json'

    file_path = os.path.join("sessions",id, file)
    try:
        with open(file_path, 'r') as jrnl:

            journal = json.load(jrnl)

            print(type(journal))
    except FileNotFoundError:
        print('unable to load json')
    with open('journalHtml.html','w') as journalhtml:
        
        journalhtml.write(toHtml(journal))