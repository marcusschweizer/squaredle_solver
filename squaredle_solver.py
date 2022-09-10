

from xml.etree.ElementPath import find
from nltk.corpus import words
from nltk.corpus import wordnet


board = [["a", "b", "x"],
         ["c", "a", "t"],
         ["a", "b", "s"]]


class Word:
    def __init__(self, word, positions):
        self.word = word
        self.positions = positions
        pass

    def __str__(self):
        return '%s - %s' % (self.word, self.positions)


def get_adj(board, word):
    
    #adj_words = []

    # row and column of last pos 
    r = word.positions[-1][0]
    c = word.positions[-1][1]

    # create the 3x3 matrix with all adjacent position tuples
    adj_pos = [[(r+y,c+x) for x in range(-1,2)] for y in range(-1,2)]

    # flatten the matrix to a list and
    # filter for exists on board (deals with nulls or board edges) and is not an alread used positions
    available = lambda x : x in board and x not in word.positions
    adj_pos = [val for sublist in adj_pos for val in filter(available, sublist) ] 
    #adj_pos = [val for sublist in adj_pos for val in sublist if val in board and val not in word.positions ] 

    #create a list of adjacent words based with new letter appended and new position appended to position list
    adj_words = [(Word(word.word + board[newPos], word.positions + [newPos])) for newPos in adj_pos ]        
            
    return adj_words



def find_words(board, word, min_length):
    #print("find_words for ", word)

    adj_words = []
    if word == []:
        #get starting positions
        for pos in board_dict:
            adj_words.append(Word(board_dict[pos], [pos]))
    else:
        #get a list of all words from all available adjacent letters
        adj_words = get_adj(board, word)



    #print(len(adj_words))
    return_words = []

    for adj_word in adj_words:
        the_word = adj_word.word
        
        if len(the_word) >= min_length and wordnet.synsets(the_word) and adj_word not in return_words:
            print("FOUND c ", adj_word)
            return_words.append(adj_word)

        return_words.extend(find_words(board, adj_word, min_length))
        
    return return_words

    

    



if __name__=="__main__":
    print("\nWelcome to squaredle solver")

    #print(board)
    board_dict = {}
    for r in range(0,len(board)):
        for c in range(0,len(board[r])):
            pos = (r,c)
            board_dict[pos] =  board[r][c]

    print('Loaded %dx%d board' % (len(board), len(board[0])) )
    print(board)
    min_length = 4

    if True:
        words = []
        words = find_words(board_dict, [], min_length)
        
        print("\n\n")
        for x in words:
            print(x)


    if False:
        #adjacent tester
        pos = (1,2)
        word = Word(board_dict[pos],[pos])
        print(word)
        adj_words = get_adj(board_dict,word)
        for aword in adj_words:
            print(aword)


