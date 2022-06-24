import csv
import sys
# import full libraries

from util import Node, StackFrontier, QueueFrontier
# import specific functions from util library (these are originally from
# maze.py)

# Maps names to a set of corresponding person_ids
names = {}
# declare names dictionary, names is a dictionary with names as keys and values
# being sets of ids (because each name could have multiple ids)

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}
# declare people dictionary, people is a dictionary of keys that are ids and
# values that are dictionaries with name, birth and movie keys with
# corresponding values of name, birth and movies (the movies value is a set of
# movie ids)

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
# declare movies dictionary, movies is a dictionary of keys that are ids and
# values that are dictionaries with title, year and stars keys with
# corresponding values of title, year and stars (the stars value is a set of
# people ids)


def load_data(directory):
# define load_data function that takes directory as an argument
    """
    Load data from CSV files into memory.
    """
    # Load people
    # with open(f"{directory}/people.csv", encoding="utf-8") as f:
    with open(f"/home/kevin/Documents/education/CompSci/ai_ml/CS50AI/projects/project0/degrees/small/people.csv", encoding="utf-8") as f:
    # open people.csv as f in read mode (default) using utf-8 encoding, changed
    # directory to small so can more easily run this within neovim without
    # needing to specify small files
        reader = csv.DictReader(f)
        # use DictReader method to read f as an iterator object, note, when
        # using DictReader, the iterator object can't simply be printed (if so
        # then it will return the memory location) needs to be iterated over as
        # follows
        for row in reader:
        # iterate over each row in reader, each row is a dictionary with
        # key/value pairs
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # populate people dictionary where the id is the key and the value
            # is another dictionary that includes key of name with name values,
            # key of birth with birth values and key of movies with value being
            # an empty set
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
                # if the name is not in names dictionary then add key of name
                # with value that is a set of ids
            else:
                names[row["name"].lower()].add(row["id"])
                # if the name is already in the names dictionary then use the
                # set add method to add the id to the id set

    # Load movies
    # with open(f"{directory}/movies.csv", encoding="utf-8") as f:
    with open(f"/home/kevin/Documents/education/CompSci/ai_ml/CS50AI/projects/project0/degrees/small/movies.csv", encoding="utf-8") as f:
    # open movies.csv as f in read mode (default) using utf-8 encoding, changed
    # directory to small so can more easily run this within neovim without
    # needing to specify small files
        reader = csv.DictReader(f)
        # use DictReader method to read f as an iterator object, note, when
        # using DictReader, the iterator object can't simply be printed (if so
        # then it will return the memory location) needs to be iterated over as
        # follows
        for row in reader:
        # iterate over each row in reader, each row is a dictionary with
        # key/value pairs
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
            # populate movies dictionary where the id is the key and the value
            # is another dictionary that includes key of title with title
            # values, key of year with year values and key of starts with
            # value being an empty set

    # Load stars
    # with open(f"{directory}/stars.csv", encoding="utf-8") as f:
    with open(f"/home/kevin/Documents/edjkucation/CompSci/ai_ml/CS50AI/projects/project0/degrees/small/stars.csv", encoding="utf-8") as f:
    # open stars.csv as f in read mode (default) using utf-8 encoding, changed
    # directory to small so can more easily run this within neovim without
    # needing to specify small files
        reader = csv.DictReader(f)
        # use DictReader method to read f as an iterator object, note, when
        # using DictReader, the iterator object can't simply be printed (if so
        # then it will return the memory location) needs to be iterated over as
        # follows
        for row in reader:
        # iterate over each row in reader, each row is a dictionary with
        # key/value pairs
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                # using set add method, add movie_id to people if not present
                movies[row["movie_id"]]["stars"].add(row["person_id"])
                # using set add method, add person_id to movies if not present
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
    # if incorrect number of command line arguments...
        sys.exit("Usage: python degrees.py [directory]")
        # ... specify correct command line usage
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    # save directory inputted in command line to directory, if none entered then
    # use large

    # Load data from files into memory
    print("Loading data...")
    # print "Loading data..." while data loading
    load_data(directory)
    # load data into memory using load_data function
    print("Data loaded.")
    # print "Data loaded." when data loaded

    source = person_id_for_name(input("Name: "))
    # ask user for source name and assign to source using person_id_for_name
    # function
    if source is None:
        sys.exit("Person not found.")
        # if source name None (doesn't match a name in database) then exit and
        # print message "Person not found."
    target = person_id_for_name(input("Name: "))
    # ask user for target name and assign to target using person_id_for_name
    # function
    if target is None:
        sys.exit("Person not found.")
        # if target name None (doesn't match a name in database) then exit and
        # print message "Person not found."

    path = shortest_path(source, target)
    # determine shortest path using shortext_path function with arguments source
    # and target and assign to path

    if path is None:
        print("Not connected.")
        # if path is None (there is no path) then print "Not connected."
    else:
        # if there is a path/connection then ...
        degrees = len(path)
        # determine the length of path and assign to degrees
        print(f"{degrees} degrees of separation.")
        # print the  degrees of separation with fstring
        path = [(None, source)] + path
        # assign the entire path sequence to path including the original source
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            # print the source/target persons and the movie for each degree


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Notes
    # path is a list of tuples in the form (movie_id, person_id)
    # source should be the first movie_id
    # target should be the last person_id

    # TODO
    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    # use the dictionary get method to retrieve the id associated with a name
    # specified as an argument from the names dictionary, use the lower method
    # to convert to lowercase so no case errors, if person_ids is empty then
    # return the default value which is an empty set
    if len(person_ids) == 0:
        return None
        # return None if the length of person_ids is 0, meaning that no names
        # were retrieved, None is what is returned when the get method doesn't
        # find any matches)
    elif len(person_ids) > 1:
        # if more than one match...
        print(f"Which '{name}'?")
        # prompt user to specify which name was intended by listing the names
        # and birth dates
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
            # print the ID, name and birth for each possible match
        try:
            person_id = input("Intended Person ID: ")
            # prompt user to specify intended person by inputting person id
            if person_id in person_ids:
                return person_id
                # if the inputted id was one of the possible matches then return
                # the id
        except ValueError:
            pass
            # if the inputted id wasn't one of the possible matches then pass
            # (the pass keyword avoids you getting an error when empty code is
            # not allowed), on next line None will be returned
        return None
    else:
        return person_ids[0]
        # if the name specified only has one person id then return it


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    # assign all movie ids to movie_ids for the person_id specified as argument
    neighbors = set()
    # declare neighbors as empty set
    for movie_id in movie_ids:
    # for each of the movie ids
        for person_id in movies[movie_id]["stars"]:
        # for each of the person_ids in movie
            neighbors.add((movie_id, person_id))
            # add the movie id and person id to neighbors
    return neighbors
    # return neighbors


if __name__ == "__main__":
# above __name__ is a built in attribute on what is a called a dunder attribute
# (Double UNDERscore), __name__ is automatically set to __main__ when you run
# your code as a script, however, if you import your code from elsewhere as a 
# library, then __name__ will be replaced by the name of the file (in this
# case degrees.py), therefore, this here calls main() if __name__ == "__main__"
# or in other words, if degrees.py is run as a script and not imported as a
# library
    main()
