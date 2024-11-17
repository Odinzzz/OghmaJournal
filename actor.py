import json
import os



inventory_path = os.path.join("inventory")

with open("vampireActor.json", "r", encoding="utf-8") as vampire_file:
    vampire = json.load(vampire_file)

inventory = {}

for item in vampire["items"]:
    if item["type"] not in inventory:
        inventory[item["type"]] = []
    inventory[item["type"]].append(item)

for loot in inventory["loot"]:
    print(loot["name"])
    with open(f'inventory/{loot["name"]}.json', "w") as item_file:
        json.dump(loot, item_file, indent=4, ensure_ascii=False)

for weapon in inventory["weapon"]:
    print(f'| {weapon["name"]}')
    with open(f'inventory/{weapon["name"]}.json', "w") as item_file:
        json.dump(weapon, item_file, indent=4, ensure_ascii=False)

for equipment in inventory["equipment"]:
    with open(f'inventory/{equipment["name"]}.json', "w") as item_file:
        json.dump(equipment, item_file, indent=4, ensure_ascii=False)
    print(f'| {equipment}')