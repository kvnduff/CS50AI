import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP NP | NP VP NP Conj NP VP
S -> NP VP Conj VP NP | NP VP NP NP Conj VP NP | NP VP NP Conj NP VP NP VP
NP -> N | Det N | Det Adj NP | NP P NP | Adj NP | P NP
VP -> V | VP P | Adv VP | VP Adv | VP Adv | Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Initialize word list
    words = []

    # Tokenize input
    tokens = nltk.wordpunct_tokenize(sentence)

    # Iterate over tokens
    for token in tokens:

        # Flag for alpha characters
        alpha = False

        # Convert to lower case
        token = token.lower()

        # Iterate over characters in token
        for character in token:

            # Flag token if character is alpha
            if character.isalpha():
                alpha = True

        # Append token to words list if alpha character
        if alpha:
            words.append(token)

    # Return words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Initialize chunks list
    chunks = []

    # Iterate through subtrees
    for subtree in tree:

        # Retrieve subtree label
        label = subtree.label()

        # If label is NP then search for children with NP label
        if label == "NP":

            # If no children have NP label then terminal leaf and can append
            if search(subtree) is False:
                chunks.append(subtree)

            # If children have NP label then continue recursively
            else:
                subsubtree = np_chunk(subtree)
                for leaf in subsubtree:
                    chunks.append(leaf)

    # Return chunks
    return chunks


def search(subtree):
    """
    Returns True if any children of subtree has NP label.
    """

    # Search children
    for subsubtree in subtree:

        # If child label is NP then return True
        if subsubtree.label() == "NP":
            return True

        # If child is not terminal then recursively search children
        if len(subsubtree) > 1:
            search(subsubtree)

    # Otherwise return False
    return False


if __name__ == "__main__":
    main()
