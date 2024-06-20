import random
import math

# ---------- GLOBAL VARIABLES ----------

ITEMS = [
    'MTI',           # Heal 1 health bar
    'Detector',      # Detects poison in the current sandwich
    'Synergist',     # If the current sandwich is poisoned the damage will be doubled, if the sandwich is normal nothing happens
    'Sleep pills',   # Skips the enemy players next turn
    'Milk',          # Skip the current sandwich
    'Reversor'       # Reverses the current sandwich, normal becomes poisoned and poisoned becomes normal.
]

INTRODUCTION = "You will take turns eating or passing sandwiches,\n be careful if you have eaten 5 poisoned sandwiches you will lose unless you have used healing items.\n Your turn can be extended by eating a normal sandwich or through the use of items,\n items can be very advantageous in this game use them wisely."

# ---------- GAME FUNCTIONS MODULE ----------

class Core:
    def getSandwiches(round):
        round += 1
        sandwiches = []
        total_poisoned_sandwiches = round
        total_normal_sandwiches = round
        total_random_sandwiches = round
        for poisoned_sandwiches in range(total_poisoned_sandwiches):
            sandwiches.append(1)
        for normal_sandwiches in range(total_normal_sandwiches):
            sandwiches.append(0)
        for random_sandwiches in range(total_random_sandwiches):
            sandwiches.append(random.randint(0, 1))
        random.shuffle(sandwiches)
        return sandwiches
    
    def getItems(round, item_list:list):
        round += 1
        items = []
        for i in range(round+1):
            choosen_item = random.choice(item_list)
            items.append(choosen_item)
        return items
    
    def coinflip():
        return random.randint(0, 1)

# for i in range(3):
#     print(f"[+] Round {i+1}: {Core.getSandwiches(i)}")
#     print(f"Items: {Core.getItems(i, ITEMS)}")
#     print("-" * 10)

PLAYER1 = input("Player one name:")

PLAYER2 = input("Player two name:")

coin_result = Core.coinflip()
if coin_result == 0:
    print(PLAYER1, "will have the first turn")
    for i in range(3):
        print(f"[+] Round {i+1}: {Core.getSandwiches(i)}")
        player1_items = Core.getItems(i, ITEMS)
        player2_items = Core.getItems(i, ITEMS)
        print(f"{PLAYER1}'s Items: {player1_items}")
        print(f"{PLAYER2}'s Items: {player2_items}")
        print("-" * 10)
else:
    print(PLAYER2, "will have the first turn")
    for i in range(3):
        print(f"[+] Round {i+1}: {Core.getSandwiches(i)}")
        player1_items = Core.getItems(i, ITEMS)
        player2_items = Core.getItems(i, ITEMS)
        print(f"{PLAYER1}'s Items: {player1_items}")
        print(f"{PLAYER2}'s Items: {player2_items}")
        print("-" * 10)

