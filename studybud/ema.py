import random

# List of sentences
sentences = [
    "Ema pusi igoru",
    "igor jede guzu",
    "ema masira igora sa stopalima",
    "igor ljubi emi vrat",
    "ema masira igoru leđa",
    "igor cicla bradavice"
]

# Function to roll the dice and select a random sentence
def roll_dice_and_select_sentence():
    # Roll the dice (generate a random number between 1 and 6)
    dice_roll = random.randint(1, 6)
    # Select the sentence corresponding to the dice roll
    selected_sentence = sentences[dice_roll - 1]  # Adjusting for 0-based indexing
    return selected_sentence

# Main function

print("Welcome to the Random Sentence Dice Game!")
input("Press Enter to roll the dice and get a sentence...")
print(roll_dice_and_select_sentence())
# Roll the dice and 


