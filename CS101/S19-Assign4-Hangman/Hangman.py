'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: YourName    YourNetID
'''




def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    
    #Your Code Here
    pass 




def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words that is of length length.
    '''
    
    #Your Code Here
    pass 




def createDisplayString(lettersGuessed, misses, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    
    #Your Code Here
    pass 




def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    
    #Your Code Here
    pass 




def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''
    
    #Your Code Here
    pass 




def processUserGuess(guessedLetter, secretWord, hangmanWord, misses):
    '''
    Uses the information in the parameters to update the user's progress in the hangman game.
    '''
    
    #Your Code Here
    pass 




def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''
    
    #Your Code Here
    pass 



if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    runGame('lowerwords.txt')
