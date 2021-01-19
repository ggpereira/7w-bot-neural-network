import json 
import sys
import network 
import time 
import save_statistics

# actions 
BUILD = 1
BUILD_WONDER = 2 
DISCARD = 3 


def match(value, array):
    for item in array:
        if item == value:
            return True 
    return False 


def is_valid_label(label, playerstatus):
    action = int(label/100)
    card_id = label % 100
    is_playable = False 

    if action == BUILD:
        playable_cards = playerstatus["cards_playable_id"]
        is_playable = match(card_id, playable_cards)        
        return is_playable

    if action == BUILD_WONDER:
        hand = playerstatus["cards_hand_id"]
        is_playable = match(card_id, hand)
        is_playable = playerstatus["can_build_wonder"]
        return is_playable

    if action == DISCARD: 
        hand = playerstatus["cards_hand_id"]
        is_playable = match(card_id, hand)
        return is_playable

    return is_playable 


def get_valid_label(sorted_labels, playerstatus):
    label_index = 0

    for i in range(len(sorted_labels)):
        if is_valid_label(sorted_labels[i], playerstatus):
            label_index = i 
            break 
    
    return sorted_labels[label_index]


def get_command(v):
    if v == BUILD:
        return "build_structure"

    if v == BUILD_WONDER:
        return "build_wonder"

    if v == DISCARD:
        return "discard"


def get_card_name(card_id, playerstatus):
    idx = 0
    hand = playerstatus["cards_hand_id"]
    # find index
    for i in range(len(hand)):
        if card_id == hand[i]:
            idx = i 
            break 
    return playerstatus["cards_hand"][idx]       


def write_json(label, bot_id, playerstatus):
    path = sys.argv[1] + "/player_" + str(bot_id +  1) + ".json"
    action = int(label/100)
    card_id = label % 100 

    command = get_command(action)
    cardname = get_card_name(card_id, playerstatus)

    command_dict = {"command": {"subcommand": command, "argument": cardname, "extra": ""}}

    print(command_dict)

    with open(path, "w") as write_file:
        json.dump(command_dict, write_file)

    file_ready = open(sys.argv[1] + "/ready.txt", "a")
    file_ready.write("ready\n")
    file_ready.close()


# def check_finish(gamestatus):
#     if (gamestatus["game"]["era"] >= 4 & gamestatus["game"]["turn"] >= 21):
#         return True 
#     return False 

def save_log(gamestatus, id):
    playerstate = gamestatus["players"][str(id)]
    winner = gamestatus["game"]["winner_id"] == id 
    
    save_statistics.save_match_log({
        "amount": playerstate["amount"],
        "wonder_id": playerstate["wonder_id"],
        "wonder_stage": playerstate["wonder_stage"],
        "resources": playerstate["resources"],
        "points": playerstate["points"],
        "winner": winner,
    })


def check_finish(gamestatus, id):
    if(gamestatus["game"]["era"] > 3):
        save_log(gamestatus, id)
        return True 
    return False 


def play(bot_id, gamestatus):
    if check_finish(gamestatus, bot_id):
        return 

    start_time = time.time()
    playerstatus = gamestatus["players"][str(bot_id)]
    inputs = network.transform_input(playerstatus, gamestatus["game"]["era"])
    sorted_labels = network.run(inputs, gamestatus["game"]["era"])
    label = get_valid_label(sorted_labels, playerstatus)
    write_json(label, bot_id, playerstatus)
    end_time = time.time()

    save_statistics.save_plays_log({
        "hand": playerstatus['cards_hand'],
        "action": label,
        "amount": playerstatus["amount"],
        "wonder_id": playerstatus["wonder_id"],
        "wonder_stage": playerstatus["wonder_stage"],
        "resources": playerstatus["resources"],
        "turn": gamestatus["game"]["turn"],
        "era": gamestatus["game"]["era"],
        "time": end_time - start_time 
    })


