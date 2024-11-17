let targets = game.user.targets;
if (targets.size === 0) {
    ui.notifications.warn("No actor targeted.");
} else {
    targets.forEach(target => {
        let actor = target.actor;
        console.log(actor);
        
        if (actor) {
            let hp = actor.system.attributes.hp;
            let ac = actor.system.attributes.ac.normal;
            let touch = actor.system.attributes.ac.touch;
            let ct = actor.system.attributes.creatureType;
            let al = actor.system.details.alignment; 
            let re = actor.system.combinedResistances;
            let lvl = actor.system.details.level;

            let resistanceMessage = `|| Actor: ${actor.name}   \n\n`;
            resistanceMessage += `|| Current HP: ${hp.value} / ${hp.max} \n`;
            resistanceMessage += `|| Armor Class (AC): ${ac.total}   \n`;
            resistanceMessage += `|| Touch Armor Class: ${touch.total}   \n`;
            resistanceMessage += `|| Level: ${lvl.available} \n`;
            resistanceMessage += `|| Type: ${ct} \n`;
            resistanceMessage += `|| Alignment: ${al} \n`;
            resistanceMessage += "|| Resistances: \n";

            console.log(re);
            
            
            re.forEach(resistance => {
                
                if (resistance.immunity) {
                    resistanceMessage += `  Immune to: ${resistance.uid} \n`;
                }
                
                if (resistance.half) {
                    resistanceMessage += `  Resistant to: ${resistance.uid} \n`;
                }

                if (resistance.value > 0){

                    resistanceMessage += `${resistance.uid}: ${resistance.value}, \n`;
                }
                
            });

            

            ui.notifications.info(resistanceMessage);
        }
    });
}