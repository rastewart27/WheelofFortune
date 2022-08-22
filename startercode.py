from config import dictionaryloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import finalprize


import random
from datetime import datetime
import math
import time

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    wordSelection = open(dictionaryloc, "r")
    for word in wordSelection:
        dictionary.append(word.strip().lower())
    wordSelection.close()

        
def readFinalRoundTxtFile(playerNum):  
    #read in turn intial turn status "message" from file
    print(f"Congratulations, {players[playerNum]['name']} you get to play in the bonus round!")
    print("You get the letters R,S,T,L,N,E for free.")
    print("Just give us 3 consonants and a vowel, and then you will have 5 seconds to guess the puzzle.")


def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    wheelCreation = open(wheeltextloc, "r")
    for wheelSlice in wheelCreation:
        wheellist.append(wheelSlice.strip())
    wheelCreation.close() 
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    for key in players:
        print(f"Please enter the name of player {key + 1}: ")
        players[key]["name"] = input()

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readWheelTxtFile()
    getPlayerInfo()
    
def getWord():
    global dictionary
    global roundWord
    global blankWord
    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.

    random.shuffle(dictionary)
    roundWord = dictionary.pop()
    #print(roundWord)      ####################################### Specifically left here for grading ease if needed ###############

    #reset the blankword list.
    blankWord = []
    for letter in range(0,len(roundWord)):
        blankWord.append('_')



def wofRoundSetup():
    global players
    # Set round total for each player = 0
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)

    for key in players:
        players[key]["roundtotal"] = 0

    #seed the random to get closer to true random
    random.seed(datetime.now())
    initPlayer = math.floor(random.random() * len(players))
    #edge case catching:
    if initPlayer == 3: initPlayer = 2

    getWord()
    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.
    spinResult = random.choice(wheellist)
    goodGuess = False
    if (spinResult == 'bankrupt'):
        print("Unfortunate, you laneded on the bankrupt.")
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
    elif (spinResult == 'loseturn'):
        print("It happens to the best of us, you landed on lose a turn.")
        stillinTurn = False
    else:
        spinResult = int(spinResult)
        print(f"Your spin landed on {spinResult}, please guess a letter: ")
        letter = input().strip().lower()[0]
        if letter in vowels:
            print("Please choose a consonant (last chance): ")
            letter = input().strip().lower()[0]
            if letter in vowels:
                return False
        goodGuess, count = guessletter(letter)

    if goodGuess:
        players[playerNum]['roundtotal'] += spinResult * count
        stillinTurn = True
    elif not goodGuess: #not totally necessary, but makes things a little easier to read.
        stillinTurn = False
    
    return stillinTurn


def guessletter(letter): 
    global players
    global blankWord
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    
    #some quick checks, being kind to the players.    
    if letter in blankWord:
        print("This letter has already been found in the puzzle.")
        return False, 0
    
    count = 0
    if letter in roundWord:
        for index in range(0, len(roundWord)):
            if roundWord[index] == letter:
                blankWord[index] = letter
                count += 1
        goodGuess = True
    elif letter not in roundWord:
        goodGuess = False
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    players[playerNum]['roundtotal'] -= vowelcost
    print("Enter a vowel you wish to buy, not including 'y': ")
    letter = input().strip().lower()[0]
    if letter in blankWord:
        print("This letter has already been found in the puzzle.")
        return False

    if letter in roundWord:
        for index in range(0, len(roundWord)):
            if roundWord[index] == letter:
                blankWord[index] = letter
        goodGuess = True
    elif letter not in roundWord:
        goodGuess = False

    return goodGuess      
        
def guessWord():
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  
    print("Please enter your guess, no spaces: ")
    wordguess = input().strip().lower()
    if wordguess == roundWord:
        for letter in range(0,len(roundWord)):
            blankWord[letter] = roundWord[letter]
        return True #because we check if there are no _ in the blankword each round, we return true instead of false.
    else:
        return False

def printRoundState():
    print(blankWord)
    print("\nPlayer 1 \t Player 2 \t Player 3")
    print(f"{players[0]['roundtotal']} \t\t {players[1]['roundtotal']} \t\t {players[2]['roundtotal']}\n")


def printGameState():
    print(blankWord)
    print("Total Scores: ")
    print("\nPlayer 1 \t Player 2 \t Player 3")
    print(f"{players[0]['gametotal']} \t\t {players[1]['gametotal']} \t\t {players[2]['gametotal']}")
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinTurn = True
    while stillinTurn:
        printRoundState()
        if '_' not in blankWord:
            return True
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        print(f"It is Player {playerNum + 1}'s turn.\n Please input either, S to spin the wheel, B to buy a vowel, or G to solve the puzzle.")
        choice = input()                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B" and players[playerNum]["roundtotal"] >= 250):
            stillinTurn = buyVowel(playerNum)
        elif(choice.strip().upper() == "B"):
            print("You need 250$ to buy a vowel, please choose again.")
        elif(choice.upper() == "G"):
            stillinTurn = guessWord()
        else:
            print("Not a correct option") 
     

    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    currentPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    puzzleSolved = False
    while not puzzleSolved:
        puzzleSolved = wofTurn(currentPlayer)

        if puzzleSolved:
            players[currentPlayer]['gametotal'] += players[currentPlayer]['roundtotal']

        if currentPlayer == (len(players) - 1):
            currentPlayer = 0
        else:
            currentPlayer += 1

    printGameState()

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    finalRoundLetters = ['r','s','t','l','n','e']
    userLetters = []
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won 

    if players[0]['gametotal'] > players[1]['gametotal']:
        if players[0]['gametotal'] > players[2]['gametotal']:
            #player 0 plays
            readFinalRoundTxtFile(0)
            winplayer = 0
        else:
            #player 2 plays
            readFinalRoundTxtFile(2)
            winplayer = 2
    elif players[1]['gametotal'] > players[2]['gametotal']:
        #player 1 plays
        readFinalRoundTxtFile(1)
        winplayer = 1
    else:
        #player 2 plays
        readFinalRoundTxtFile(2)
        winplayer = 2


    getWord()
    for lastletter in finalRoundLetters:
        guessletter(lastletter)

    printGameState()

    arbitraryCounter = 0
    while arbitraryCounter < 3:
        print("Please enter a consonant: ")
        probablyVowel = input().strip().lower()[0]
        if probablyVowel in vowels:
            print("Do you know what a consonant is?  It's not a vowel.\n Try again.") #if the user does this, I give up.
        else:
            arbitraryCounter += 1
            userLetters.append(probablyVowel)
    
    arbitraryCounter = 0
    while arbitraryCounter != 1:
        print("Please enter a singular vowel: ")
        definitelyVowel = input().strip().lower()[0]
        if definitelyVowel not in vowels:
            print("Why. Just, why?")
        else:
            arbitraryCounter += 1
            userLetters.append(definitelyVowel)

    for choices in userLetters:
        guessletter(choices)

    printGameState()
    print("You have 5 seconds to guess the word.")
    start = time.time()
    guess = input().strip().lower()
    end = time.time()
    if end - start > 5:
        print("Sorry you took to long.")
    else:
        if guess == roundWord:
            print("Congrats you win the bonus prize!!")
            players[winplayer]['gametotal'] += finalprize
        else:
            print("Good try.")

    #fill out the blanks.
    for letter in range(0,len(roundWord)):
            blankWord[letter] = roundWord[letter]

    #end the game.
    printGameState()
    print("Thanks for playing!")

def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
            time.sleep(2)
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
