import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialize probability distribution dictionary
    pd = {}

    # Declare variable of number of pages in corpus
    num_pages = len(corpus)

    # Declare dictionary of number of links on pages
    num_links = {}
    for webpage in corpus:
        if len(corpus[page]) > 0:
            num_links[webpage] = len(corpus[webpage])
        else:
            num_links[webpage] = 0

    # If page has no outgoing links then assign equal probability to all pages
    if num_links[page] == 0:
        for webpage in corpus:
            pd[webpage] = (1 / num_pages)

    # Otherwise assign probability based on page and link probability
    else:
        for webpage in corpus:
            # Page probability
            pd[webpage] = ((1 - damping_factor) / num_pages)
            # Link probability
            if webpage in corpus[page]:
                pd[webpage] += (damping_factor / (num_links[page]))
    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize page rank dictionary and sample list
    rank = {}
    sample = []

    # Randomly choose a page from corpus and add to sample
    selected = random.choice(list(corpus))
    sample.append(selected)

    # Use transition model to determine probability distribution
    pd = transition_model(corpus, selected, damping_factor)

    # Declare a list of corpus pages (i.e. choices for selection)
    choices = list(corpus.keys())

    # Select n - 1 pages using probability distribution and add to sample
    for _ in range(n - 1):
        # Create weights for choosing next selection
        weights = [pd[page] for page in corpus]
        # Select next page
        selected = random.choices(choices, weights).pop()
        # Add selection to sample
        sample.append(selected)
        # Determine next probability distribution
        pd = transition_model(corpus, selected, damping_factor)

    # Determine page rank for each page and assign to rank
    for page in corpus:
        rank[page] = sample.count(page) / n
    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize dictionaries for page rank (new and old) and page rank change
    rank_new = {}
    rank_old = {}
    change = {}

    # Declare base values for page rank and page rank change
    for page in corpus:
        rank_new[page] = 1 / len(corpus)
        change[page] = 1

    # If page has no links than add all links
    for page in corpus:
        if not corpus[page]:
            corpus[page] = set(page for page in corpus)

    # Create dictionary to store links to pages (i.e. incoming links)
    links = dict()
    for page_outer in corpus:
        for page_inner in corpus:
            if page_inner in corpus[page_outer]:
                if page_inner in links:
                    links[page_inner] = links[page_inner].union([page_outer])
                else:
                    links[page_inner] = set([page_outer])

    # Iteratively update page rank until page rank change <= 0.001
    counter = 0

    while any(value > 0.001 for value in change.values()):
        counter += 1

        # Store page rank before update for calculating page rank change
        rank_old = rank_new.copy()

        # Iterate over pages
        for page_outer in corpus:

            # Determine page component of iterative formula
            rank_page = (1 - damping_factor) / len(corpus)

            # Determine link component of iterative formula
            rank_link = 0
            for page_inner in links[page_outer]:
                num_pages = len(corpus[page_inner])
                val = rank_old[page_inner] / num_pages
                rank_link += val
            rank_link = rank_link * damping_factor

            # Calculate new page rank by adding component parts
            rank_new[page_outer] = rank_page + rank_link

            # Calculate page rank change
            change[page_outer] = abs(rank_old[page_outer] - rank_new[page_outer])

    return rank_new


if __name__ == "__main__":
    main()
