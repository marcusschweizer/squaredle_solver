

from pickle import TRUE
import nltk
from nltk.corpus import words



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



def find_words(board, all_words, word):
    #print("find_words for ", word)

    #get a list of all words from all available adjacent letters
    adj_words = get_adj(board, word)

    #startswith = lambda x : x in 

    #print(len(adj_words))
    return_words = []

    for adj_word in adj_words:
        the_word = adj_word.word
        
        possible_words = [x for x in all_words if x.startswith(the_word)]
        #print("Number of possible words ", len(possible_words))
        if len(possible_words) == 0:
            print("n_", the_word)

        if len(possible_words) == 1 and the_word == possible_words[0]:# and len(word.word) >= min_len:
            print("FOUND a ", adj_word)
            return_words.append(adj_word)

        if len(possible_words) > 1:
            if the_word in possible_words:
                print("FOUND b ", adj_word)
                return_words.append(adj_word)

            if len(possible_words) > 0:

                return_words.extend(find_words(board, possible_words, adj_word))
                #if len(more_words) > 0:
                #    return_words.extend(more_words)
                
            

    return return_words

    

    



if __name__=="__main__":
    print("\nWelcome to squaredle solver")

    #print(board)
    board_dict = {}
    for r in range(0,len(board)):
        for c in range(0,len(board[r])):
            pos = (r,c)
            board_dict[pos] =  board[r][c]
    print(board_dict)

    min_length = 4
    

    
    #get all words 
    #with open('/usr/share/dict/words') as f:
    #    all_words = [line.strip() for line in f if len(line.strip()) >= min_length]

    all_words = [word for word in words.words() if len(word) >= min_length]
    

    print('Loaded %dx%d board' % (len(board), len(board[0])) )
    print('Loaded %d words' % (len(all_words)))


    if True:
        words = []
        for pos in board_dict:
            word = Word(board_dict[pos], [pos])
            print("\n\n", word)
            words.extend(find_words(board_dict, all_words, word))
            print("FINALLY ", len(words))

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


    if True:
        print(all_words[:20])
  
        print(len(all_words))

    if "cats" in all_words:
        print("YES")
