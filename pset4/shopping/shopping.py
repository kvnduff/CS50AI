import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Initialize lists
    evidence = []
    labels = []

    # Populate lists
    with open(filename, "r") as file:
        reader = csv.reader(file)

        # Iterate over csv rows, skipping header
        header = next(reader)
        for i, row in enumerate(reader):

            # Append evidence data
            evidence.append(row[0:-1])

            # Append labels data
            labels.append(row[-1])

    # Translate evidence fields to required formats
    for i in evidence:
        match i[10]:                # Month
            case "Jan":
                i[10] = 0
            case "Feb":
                i[10] = 1
            case "Mar":
                i[10] = 2
            case "Apr":
                i[10] = 3
            case "May":
                i[10] = 4
            case "June":
                i[10] = 5
            case "Jul":
                i[10] = 6
            case "Aug":
                i[10] = 7
            case "Sep":
                i[10] = 8
            case "Oct":
                i[10] = 9
            case "Nov":
                i[10] = 10
            case "Dec":
                i[10] = 11
        if i[15] == "New_Visitor":  # VisitorType
            i[15] = 0
        if i[15] == "Other":
            i[15] = 0
        if i[15] == "Returning_Visitor":
            i[15] = 1
        if i[16] == "FALSE":        # Weekend
            i[16] = 0
        if i[16] == "TRUE":
            i[16] = 1

        # Translate evidence fields to required data types
        i[0] = int(i[0])    # Administrative
        i[1] = float(i[1])  # Administrative_Duration
        i[2] = int(i[2])    # Informational
        i[3] = float(i[3])  # Informational_Duration
        i[4] = int(i[4])    # ProductRelated
        i[5] = float(i[5])  # ProductRelated_Duration
        i[6] = float(i[6])  # BounceRates
        i[7] = float(i[7])  # ExitRates
        i[8] = float(i[8])  # PageValues
        i[9] = float(i[9])  # SpecialDay
        i[10] = int(i[10])  # Month
        i[11] = int(i[11])  # OperatingSystems
        i[12] = int(i[12])  # Browser
        i[13] = int(i[13])  # Region
        i[14] = int(i[14])  # TrafficType
        i[15] = int(i[15])  # VisitorType
        i[16] = int(i[16])  # Weekend

    # Translate labels to required format / data types
    for i in range(len(labels)):
        if labels[i] == "FALSE":
            labels[i] = 0
        else:
            labels[i] = 1

    # Return tuple of evidence, labels
    return tuple((evidence, labels))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Create KNeighborsClassifier model object where k=1
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit/train the model and return
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Initialize variables
    negative_prediction = float(0)
    negative_real = float(0)
    positive_prediction = float(0)
    positive_real = float(0)
    sensitivity = float(0)
    specificity = float(0)

    # Create tuple of predictions, labels using zip
    pairs = zip(predictions, labels)

    # Compare predictions to labels
    for pair in pairs:

        # If no purchase, sum real no purchases and predicted no purchases
        if pair[1] == 0:
            negative_real += 1
            if pair[0] == 0:
                negative_prediction += 1

        # If purchase, sum real purchases and predicted purchases
        if pair[1] == 1:
            positive_real += 1
            if pair[0] == 1:
                positive_prediction += 1

    # Calculate sensitivity and specificity
    sensitivity = positive_prediction / positive_real
    specificity = negative_prediction / negative_real

    # Return tuple of sensitivity, specificity
    return tuple((sensitivity, specificity))


if __name__ == "__main__":
    main()
