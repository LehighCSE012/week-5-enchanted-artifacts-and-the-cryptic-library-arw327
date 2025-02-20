""" this module implements an adventure game"""
import random

inventory = []
              
def discover_artifact(player_stats, artifacts, artifact_name):
    artifact = artifacts.get(artifact_name)
    if artifact:
        print(f"You found the {artifact_name}!")
        print(artifact["description"])

        if artifact['effect'] == "increases health":
            player_stats['health'] = min(player_stats['health'] + artifact['power'],100)
            print("Your health increases!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print("Your attack enhances!")

    else:
        print("You found nothing of interest.")

    return player_stats, artifacts #return updated dictionaries

def acquire_item(current_inventory, item):
    """this will aquire item for the inventory"""
    current_inventory.append(item)
    print(f"You acquired a {item}!")
    return current_inventory
#this is still not working and displaying wrong on test 7, should it be a item?

def display_inventory(current_inventory):
    """this will display the user the inventory"""
    if len(current_inventory) == 0:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(current_inventory):
            print(f"{i + 1}. {item}")

def display_player_status(player_health):
    """ this will display the user the current health"""
    print(f'Your current health: {player_health}')

def handle_path_choice(player_health):
    """this sees where the player where go and how it affects player health, NO imput from user"""
    chosen_path = random.choice(["left", "right"])
    if chosen_path == "left":
        player_health = min(player_health + 10, 100)
        print("You encounter a friendly gnome who heals you for 10 health points.")

    elif chosen_path == "right":
        player_health -= 15
        print("You fall into a pit and lose 15 health points.")
        if player_health <= 0:
            player_health = 0
            print("You are barely alive!")
    return player_health

def player_attack(monster_health, player_stats):
    """this should update the current health of the monster, and it will simulat player's attack"""
    monster_health -= player_stats["attack"]
    print(f"You strike the monster for {player_stats['attack']} damage!")
    return monster_health, player_stats

def monster_attack(player_stats):
    """update the player health after monster has striken and return back the player health"""
    critical_hit = random.random()
    if critical_hit < 0.5:
        player_stats["health"] -= 20
        print("The monster lands a critical hit for 20 damage!")
    else:
        player_stats["health"] -= 10
        print("The monster hits you for 10 damage!")
    return player_stats

def combat_encounter(monster_health, has_treasure, player_stats):
    """there is a combat encounter that has attacks/change the health monster & player in loop"""
    while player_stats["health"] > 0 and monster_health > 0:
        display_player_status(player_stats["health"])
        monster_health = player_attack(monster_health, player_stats)
        if monster_health <= 0:
            print("You defeated the monster!")
            return True, has_treasure
        player_stats = monster_attack(player_stats)
        if player_stats["health"] <= 0:
            print("Game Over!")
            return False, has_treasure
    return False, player_stats

def check_for_treasure(has_treasure):
    """this code will check if the monster will have treasure, then tell the user through a bool"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def handle_challenge(challenge_type, current_inventory, challenge_outcome, player_health):
    """this code split up the enter dungeon region so less if with puzzle and trap"""
    if current_inventory is None:
        current_inventory = []
    if not isinstance(current_inventory, list):
        current_inventory = []
    if challenge_type == "puzzle":
        print("You encounter a puzzle!")
        choice = input("Solve or skip?: ")
        if choice.lower().strip() == 'solve':
            success_chance = 0.7
        else:
            success_chance = 0.3
        success = random.random() < success_chance

        if success:
            print(challenge_outcome[0])
            player_health += challenge_outcome[2]
            if player_health < 0:
                player_health = 0
                print("You are barely alive!")
        else:
            print(challenge_outcome[1])
            player_health += challenge_outcome[2]
            if player_health < 0:
                player_health = 0
                print("You are barely alive!")
        display_inventory(current_inventory)

    elif challenge_type == "trap":
        print("You see a potential trap!")
        choice = input("Disarm or bypass?: ")
        success = random.choice([True, False])
        if success:
            print(challenge_outcome[0])
            player_health += challenge_outcome[2]
            if player_health < 0:
                player_health = 0
                print("You are barely alive!")
        else:
            print(challenge_outcome[1])
            player_health += challenge_outcome[2]
            if player_health < 0:
                player_health = 0
                print("You are barely alive!")
    display_inventory(current_inventory)
    return player_health, current_inventory

def enter_dungeon(player_health, current_inventory, dungeon_rooms, clues):
    """this is for the player to enter the dungeon and start the items"""
    def find_clue(clues, new_clue):
        if new_clue not in clues:
            clues.add(new_clue)
            print(f"You discovered a new clue: {new_clue}")
        else:
            print("You already know this clue.")
    return clues

    for room in dungeon_rooms:
        room_description = room[0]
        item = room[1]
        challenge_type = room[2]
        challenge_outcome = room[3]
        print(room_description)
        if item:
            current_inventory = acquire_item(current_inventory, item)
            print(f"You found a {item} in the room.")
        if challenge_type != "none":
            player_health, current_inventory = handle_challenge(
                challenge_type,
                current_inventory,
                challenge_outcome,
                player_health
            )
            display_inventory(current_inventory)
        else:
            print("There doesn't seem to be a challenge in this room. You move on.")
        elif challenge_type == "library":
            print(room_description)
            possible_clues = []
            selected_clues = random.sample(possible_clues, 2)
            for clues in selected_clues:
                clues = find_clue(clues, clue)
    return player_health, current_inventory, clues

def main():
    """this code will initialize and set values to variables"""
    player_health_initial = 100
    monster_health_initial = 70
    has_treasure = False
clues = set()
    has_treasure = random.choice([True, False])
    player_health_initial = handle_path_choice(player_health_initial)

    treasure_obtained_in_combat = combat_encounter(
        player_health_initial,
        monster_health_initial,
        has_treasure
    )
    if player_health_initial > 0 and treasure_obtained_in_combat:
        check_for_treasure(treasure_obtained_in_combat)
    else:
        print("Game Over!")
    dungeon_rooms = []
    dungeon_rooms.append((
        "Spooky entrance hall",
        None,
        "trap",
        ("You cleverly disarm the trap!",
         "You triggered the trap!",
         -15)
    ))
    player_stats = {'health': 100, 'attack': 5}
    artifacts = {
        "amulet_of_liveliness": {
    """This will also increase healh by 15"""
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "bracelet_of_power": {
    """This will boost attack damage by 10"""
            "description": "A powerful bracelet that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "sword_of_truth": {
    """this will solve puzzles and add power by 5"""
            "description": "A sword imbued with ancient truth.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    artifact_name = None

    if random.random() < 0.3:
        artifact_name = random.choice(list(artifacts.keys()))
        if artifact_name:
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            print(f"Your current health is: {player_stats['health']}")
            print(f"Your current attack is: {player_stats['attack']}")
    else:
        print("No artifact was found at this time.")

    dungeon_rooms.append((
        "Caves with crystals",
        "Crystal Ball",
        "puzzle",
        ("You cracked the code!",
         "The chest remains stubbornly locked.",
         -5)
    ))
    dungeon_rooms.append((
        "Jail cell with dripping water",
        "Oxygen tank",
        "none",
        None
    ))
    dungeon_rooms.append((
        "The Cryptic Library",
        None,
        "library",
        None
    ))

    current_inventory = []
    if player_health_initial > 0:
        player_health_initial, current_inventory = enter_dungeon(
            player_health_initial,
            current_inventory,
            dungeon_rooms, clues
        )

if __name__ == "__main__":
    main()
