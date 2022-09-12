from nltk.corpus import words
from nltk.corpus import wordnet
import bisect
import time
import os


board_first = [["a", "b", "x"],
         ["c", "a", "t"],
         ["a", "", "s"]]

board_tutorial = [["", "l", "a",""],
         ["t", "r", "i", ""],
         ["o", "u", "", ""],
         ["", "", "t", ""]]

board_base = [
["", "", "", "", ""],
["", "", "", "", ""],
["", "", "", "", ""],
["", "", "", "", ""],
["", "", "", "", ""]
]

board_sept_ten = [
["p", "a", "u", "s", "e"],
["d", "t", "a", "b", "a"],
["e", "o", "" , "c", "i"],
["m", "r", "c", "z", "n"],
["h", "s", "i", "p", "t"]
]

board_sept_eleven = [
["a", "r", "b", "h", ""],
["n", "c", "o", "t", ""],
["a", "d", "n", "y", ""],
["a", "s", "p", "s", ""],
["", "", "", "", ""]
]

board_sept_twelve = [
["t", "h", "h", "o", "m"],
["r", "f", "a", "l", "e"],
["p", "m", "y", "o", "v"],
["p", "i", "l", "i", "t"],
["c", "j", "e", "s", "o"]
]

board_special_reddit = [
["b", "p", "h", "e", "r"],
["l", "a", "s", "m", "e"],
["c", "o", "h", "a", "y"],
["n", "a", "t", "w", "l"],
["s", "f", "r", "t", "s"]
]


debug = False


class Word:
    """Represents a possible word with list of positions
    """

    def __init__(self, word, positions):
        self.word = word
        self.positions = positions
        pass

    def __str__(self):
        return '%s - %s' % (self.word, self.positions)

    def __lt__(self, other):
        return self.word < other.word


def get_adj(board, input_word):
    """gets all adjacent letters and finds all possible combinations to extend input_word

    Arguments:
        board {dict} -- board dictionary
        input_word {Word} -- initial word

    Returns:
        adj_words -- all possible word combinations
    """

    # row and column of last pos     
    word = input_word.word
    positions = input_word.positions

    r = positions[-1][0]
    c = positions[-1][1]

    # create the 3x3 matrix with all adjacent position tuples
    adj_pos = [[(r+y,c+x) for x in range(-1,2)] for y in range(-1,2)]

    # flatten the matrix to a list and
    # filter for exists on board (deals with nulls or board edges) and is not an alread used positions
    available = lambda x : x in board and x not in positions
    adj_pos = [val for sublist in adj_pos for val in filter(available, sublist) ] 

    
    #create a list of adjacent words based with new letter appended and new position appended to position list
    adj_words = [(Word(word + board[newPos], positions + [newPos])) for newPos in adj_pos ]        

    return adj_words



def find_words(board, all_possible_words, word, min_length):
    """recursive method to find all words on a board
    Uses nltk wordnet synsets test to establish if word exists
    Note squardle uses mariams dictionary so results may very

    Arguments:
        board {dict} -- board dictionary
        word {list} -- word to extend and search, blank list - [] - to start
        min_length {int} -- minimum word length to be using.

    Returns:
        adj_words -- all possible word combinations
    """

    adj_words = []
    if word == []:
        #get starting positions
        for pos in board:
            # need to have the unique starting position with otherwise similar letters are overwritten
            new_word = Word(board[pos], [pos]) 
            adj_words.append(new_word)
    
    else:
        #get a list of all words from all available adjacent letters
        adj_words = get_adj(board, word)


    #loop through all possible words that are adjacent extensions of incoming word
    return_words = []
    for word_item in adj_words:
        
        the_word = word_item.word
        the_positions = word_item.positions

        if len(the_word) == 1:
             debug and print(the_word)

        # if the word is a real word, is long enough, and isn't already in the list, add it, you found a word!
        # xxx should use same dictionary as Squardle!
        # xxx found a couple of words in squardle not in wordnet, like carb or synth!
        if len(the_word) >= min_length and the_word in all_possible_words and the_word not in [w.word for w in return_words]:
            # yay!
            debug and print(word_item)
            bisect.insort(return_words, word_item)
            #return_words.append(word_item)
        
        possible_words = [x for x in all_possible_words if x.startswith(the_word)]
        
        # if there is a word that starts with this combination of letters, continue - save time if not   
        if len(possible_words) > 0:
            
            # recursively call function on all extended words
            next_words = find_words(board, possible_words, word_item , min_length)
        
            #append next words whilst checking that it doesn't exist in words    
            [bisect.insort(return_words,n) for n in next_words if n.word not in [w.word for w in return_words]]
    
        
    return return_words


def solve(board, min_length):

    board_dict = {}
    #read in board to a board dict
    for r in range(0,len(board)):
        for c in range(0,len(board[r])):
            pos = (r,c)
            letter = board[r][c]
            #handle blank spots
            if letter != "":
                board_dict[pos] =  letter

    #read the word list
    scrabble_file = "words/Collins Scrabble Words (2019).txt"

    with open(os.path.join(os.path.dirname(__file__), scrabble_file)) as f:
        all_words = [line.strip().lower() for line in f.readlines()[1:] if len(line.strip()) >= min_length]

    print('Loaded %d words from %s' %(len(all_words), scrabble_file))

    print('Loaded %dx%d board' % (len(board), len(board[0])) )
    for b in board:
        print(b)
    
    print("solving...")
    tic = time.perf_counter()
    results = find_words(board_dict, all_words, [], min_length)
    toc = time.perf_counter()
    print(f"solved in {toc - tic:0.4f} seconds")

    return results





if __name__=="__main__":
    print("\nWelcome to squaredle solver")

    min_length = 4
    board = board_special_reddit
    
    results = solve(board, min_length)

    print('\nResults, found %d words: \nfirst position - word' % (len(results)))
    for w in results:
        print('%s - %s' % (w.positions[0], w.word))




