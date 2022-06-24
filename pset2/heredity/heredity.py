import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # Number of genes for each person
    genes_num = {}
    for person in people:
        if person in two_genes:
            genes_num[person] = 2
        elif person in one_gene:
            genes_num[person] = 1
        else:
            genes_num[person] = 0

    # Trait present for each person
    trait_has = {}
    for person in people:
        if person in have_trait:
            trait_has[person] = True
        else:
            trait_has[person] = False

    # Probability of genes and traits
    gene_pro = {}
    trait_pro = {}

    # Iterate over people
    for person in people:

        # Probabilty of gene if no parents
        if people[person]["mother"] is None:
            gene_pro[person] = PROBS["gene"][genes_num[person]]

        # Probabilty of gene if parents
        else:

            # Initialize variables to store probability for mother and father
            mother_pro = 0
            father_pro = 0

            # Probability gene from mother
            if genes_num[people[person]["mother"]] == 2:
                mother_pro = 1 - PROBS["mutation"]
            elif genes_num[people[person]["mother"]] == 1:
                mother_pro = 0.5
            else:
                mother_pro = PROBS["mutation"]

            # Probability gene from father
            if genes_num[people[person]["father"]] == 2:
                father_pro = 1 - PROBS["mutation"]
            elif genes_num[people[person]["father"]] == 1:
                father_pro = 0.5
            else:
                father_pro = PROBS["mutation"]

            # If person has two genes then probability is:
            # mother * father
            if genes_num[person] == 2:
                gene_pro[person] = mother_pro * father_pro

            # If person has one gene, then probability is:
            # (mother * not father) + (not mother * father)
            elif genes_num[person] == 1:
                gene_pro[person] = (
                    mother_pro * (1 - father_pro) +
                    ((1 - mother_pro) * father_pro))

            # If person has no genes, then probability is:
            # not mother * not father
            else:
                gene_pro[person] = (1 - mother_pro) * (1 - father_pro)

        # Probability of trait
        trait_pro[person] = PROBS["trait"][genes_num[person]][trait_has[person]]

    # Probability of gene/trait combination
    combined_pro = {}
    for person in people:
        combined_pro[person] = gene_pro[person] * trait_pro[person]

    # Joint probability
    joint_pro = 1
    for person in people:
        joint_pro = joint_pro * combined_pro[person]

    return joint_pro


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Iterate over probabalities
    for person in probabilities:

        # Update gene probabilities
        if person in two_genes:
            probabilities[person]["gene"][2] = \
                probabilities[person]["gene"][2] + p
        elif person in one_gene:
            probabilities[person]["gene"][1] = \
                probabilities[person]["gene"][1] + p
        else:
            probabilities[person]["gene"][0] = \
                probabilities[person]["gene"][0] + p

        # Update trait probabilities
        if person in have_trait:
            probabilities[person]["trait"][True] = \
                probabilities[person]["trait"][True] + p
        else:
            probabilities[person]["trait"][False] = \
                probabilities[person]["trait"][False] + p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # Iterate over probabilities
    for person in probabilities:

        # Normalize gene probabilities (gene probability / gene sum)
        gene_sum = (
            probabilities[person]["gene"][2] +
            probabilities[person]["gene"][1] +
            probabilities[person]["gene"][0])
        for i in 0, 1, 2:
            probabilities[person]["gene"][i] = \
                probabilities[person]["gene"][i] / gene_sum

        # Normalize trait probabilities (trait probability / trait sum)
        trait_sum = (
            probabilities[person]["trait"][True] +
            probabilities[person]["trait"][False])
        for i in True, False:
            probabilities[person]["trait"][i] = \
                probabilities[person]["trait"][i] / trait_sum


if __name__ == "__main__":
    main()
