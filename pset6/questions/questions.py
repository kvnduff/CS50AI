import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
import sys
import os
import string
import math
from operator import itemgetter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # Initialize files dictionary
    files = {}

    # Iterate through files in folder
    counter = 0
    file_names = []
    for file in os.listdir(directory):

        # Concatenate full path of directory and file
        path = os.path.join(directory, file)

        # Open file contents
        with open(path) as f:
            content = f.read()
            files[file] = content

        # Iterate counter
        counter += 1

        # Append filename
        file_names.append(file)

    # Return files dictionary
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # Initialize words list
    words = []

    # Tokenize input
    tokens = nltk.wordpunct_tokenize(document)

    # Iterate over tokens
    for token in tokens:

        # Convert to lower case
        token = token.lower()

        # Filter out punctuation
        punctuation = False
        for character in token:
            if character in string.punctuation:
                punctuation = True

        # Filter out stopwords
        if token in nltk.corpus.stopwords.words("english"):
            continue

        # Append remaining tokens to word list
        if punctuation is False:
            words.append(token)

    # Return words
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Create list of all tokens
    tokens = []
    for document, words in documents.items():
        for word in words:
            if word not in tokens:
                tokens.append(word)

    # Initialize idfs dictionary with tokens as keys and 0 as values
    idfs = {tokens: float(0) for tokens in tokens[:]}

    # Add token document counts to idfs
    for token in tokens:
        for document in documents.keys():
            if token in documents[document]:
                idfs[token] += 1

    # Compute idf for all tokens
    for token, idf in idfs.items():
        idfs[token] = math.log(len(documents)/idf)

    # Return idfs
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # Initialize tfidf dictionary with files as keys and 0 as values
    tfidfs = {file: 0 for file in files}

    # Iterate through files
    for file in files.keys():

        # Initialize tf dictionary with query words as keys and 0 as values
        tf = {word: 0 for word in query}

        # Iterate over words in query
        for word in query:

            # Iterate over tokens in file
            for token in files[file]:

                # Compute term frequency
                if token == word:
                    tf[word] += 1

            # Compute tfidf
            tfidfs[file] += tf[word] * idfs[word]

    # Rank files by tfidf
    top_files = sorted([file for file in files],
        key=lambda x: (tfidfs[x]), reverse=True)

    # Return n entries from top_files
    return top_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # Initialize sentence IDF dictionary
    info = {sentence: {
        "idf_score": float(0),
        "sentence_length": float(0),
        "query_words": float(0),
        "qtd_score": float(0)}
        for sentence in sentences}

    # Iterate through sentences
    for sentence, words in sentences.items():

        # Update sentence length
        info[sentence]["sentence_length"] = len(sentences[sentence])

        # Iterate through words in query
        for word in query:

            # If query word in sentence
            if word in sentences[sentence]:

                # Update idf_score
                info[sentence]["idf_score"] += idfs[word]

                # Update query words
                info[sentence]["query_words"] += \
                    sentences[sentence].count(word)

        # Update qtd_score
        info[sentence]["qtd_score"] = \
            info[sentence]["query_words"] / info[sentence]["sentence_length"]

    # Rank sentences, first by idf_score, second by qtf_score
    top_sentences = sorted([sentence for sentence in sentences],
        key=lambda x: (
        info[x]['idf_score'],
        info[x]['qtd_score']), reverse=True)

    return top_sentences[:n]


if __name__ == "__main__":
    main()
