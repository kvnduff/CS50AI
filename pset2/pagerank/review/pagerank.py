import os
import random
import re
import sys
# import libraries

DAMPING = 0.85
# set constant DAMPING to 0.85, this is the damping factor
SAMPLES = 10000
# set constant SAMPLES to 10000, this is the number of samples taken


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # requires command line argument indicating directory of web pages
    corpus = crawl(sys.argv[1])
    # crawl helper function (see below), returns dictionary with page as keys
    # and links to other web pages as set of values
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # sample_pagerank helper function (see below), using Markov sampling
    # method, returns dictionary with page as keys and estimated PageRank as
    # values (number between 0 and 1)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    # prints Markov sampling PageRank results for all web pages
    ranks = iterate_pagerank(corpus, DAMPING)
    # iterate_pagerank helper function (see below), using iterative method,
    # returns dictionary with page as keys and estimated PageRank as values
    # (number between 0 and 1)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    # prints iterative PageRank sampling results for all web pages


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()
    # create empty pages dictionary

    # extract all links from HTML files
    for filename in os.listdir(directory):
    # iterate over all filenames in the web page directory
        if not filename.endswith(".html"):
        # skip files without html extension
            continue
        with open(os.path.join(directory, filename)) as f:
        # open html file
            contents = f.read()
            # read html file contents
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # use regex to find all links
            pages[filename] = set(links) - {filename}
            # pages dictionary, set key to filename and value to a set of
            # links

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    # only include links to other pages (not to same page)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
