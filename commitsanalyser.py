import sys
import re
import copy
import matplotlib.pyplot as plt

# Regular expression to match file names ending with ".txt"
exp1 = "\.txt$"

try:
    commits = sys.argv[1]
    identities = sys.argv[2]

    if re.search(exp1, commits) and re.search(exp1, identities):  # Use re.search to find a match.
        pass
    else:
        raise Exception("No match found")
except IndexError:
    print("Please enter command line arguments...")
    exit(1)
except:
    print("Please use .txt files")
    exit(1)

data = {}
tempdata = {"SwM tasks": [0, 0, 0], "NFR Labeling": [0, 0, 0, 0, 0, 0], "SoftEvol tasks": [0, 0, 0, 0]}
contributors = {}
swmnames = ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"]
nfrnames = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
softevolnames = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]


def visualazition(title, data1, dataname):
    """
        Create and display a bar chart visualization.
        :param title: Title of the chart
        :param data1: Data for the chart
        :param dataname: Labels for the chart
    """

    plt.bar(dataname, data1)
    plt.xlabel('Features')
    plt.ylabel('Total Number of Commits')
    plt.title(title)
    plt.show()


def checkcondition(stringlist):
    """
        Check if the total sum of elements in a list is 1.
        :param stringlist: List of values
        :return: True if the sum is 1, False otherwise
    """

    total = 0
    for i in range(len(stringlist)):
        total += int(stringlist[i])
    if total == 1:
        return True
    else:
        return False


def readFile(filename, fileType):
    """
        Read data from the specified file and update the global data structures.
        :param fileType: Type of the file -> user or data
        :param filename: Name of the file to read
    """
    try:
        global data
        global tempdata
        global contributors

        if fileType == "data":
            with open(filename, 'r') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip().split(",")
                    # commit_id = line[0]
                    swm = line[1:4]
                    nfr = line[4:10]
                    softevol = line[10:14]
                    cmmtrid = line[14]
                    # commsg = line[15]
                    name = list(contributors[cmmtrid].values())[0]
                    if checkcondition(swm):
                        if data.get(name) is None:
                            data[name] = copy.deepcopy(tempdata)
                        data[name]["SwM tasks"][0] += int(swm[0])
                        data[name]["SwM tasks"][1] += int(swm[1])
                        data[name]["SwM tasks"][2] += int(swm[2])
                    if checkcondition(softevol):
                        if data.get(name) is None:
                            data[name] = copy.deepcopy(tempdata)
                        data[name]["SoftEvol tasks"][0] += int(softevol[0])
                        data[name]["SoftEvol tasks"][1] += int(softevol[1])
                        data[name]["SoftEvol tasks"][2] += int(softevol[2])
                        data[name]["SoftEvol tasks"][3] += int(softevol[3])
                    for i in range(6):
                        data[name]["NFR Labeling"][i] += int(nfr[i])


        elif fileType == "user":
            with open(filename, 'r') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    line = line.strip()
                    commiter_id, full_name, email = line.split(',')
                    contributors[commiter_id] = {email: full_name}

    except:
        print("Please use correct files...")
        sys.exit(1)


def menu():
    """
        Display a menu and get user choice.
        :return: User choice
    """

    try:
        choice = int(input("""\n1. Compare the number of commits done by a particular developer for a given classification scheme.\n
2. Compare the number of commits done by all developers, which are classified with a given feature (for example, developer X has Y commits, developer I has J commits, and developer A has B commits for a given feature).\n
3. Print the developer with the maximum number of commits for a given feature (for example, print the developer who has the maximum number of commits with Corrective Tasks).\n
4. Exit\nchoice: """))
    except ValueError:
        print("!!!Please choose one of the available options!!!")
        return 0

    return choice


if __name__ == "__main__":

    readFile(identities, "user")
    readFile(commits, "data")
    choice = 0
    while choice != 4:
        choice = menu()
        if choice == 1:
            print("Please choose id of one of the available developer: ")
            for i in range(len(data.values())):
                print(i + 1, ".", list(data.keys())[i])
            try:
                person = int(input("Choose: "))
                if person < 1 or person > len(data.values()):
                    raise Exception

                print("Please choose the id of one of the classification: ")
                print("1. SwM tasks\n2. NFR Labeling\n3. SoftEvol tasks")

                classification = int(input("Choose: "))
                if classification < 1 or classification > 3:
                    raise Exception

                person_name = list(data.keys())[person - 1]
                person_data = list(data[list(data.keys())[person - 1]].values())[classification - 1]

                if classification == 1:
                    title = "Comparison for " + person_name + "\'s Commits Classified by SwM Tasks"
                    visualazition(title, person_data, swmnames)

                elif classification == 2:
                    title = "Comparison for " + person_name + "\'s Commits Classified by NFR Labeling"
                    visualazition(title, person_data, nfrnames)

                elif classification == 3:
                    title = "Comparison for " + person_name + "\'s Commits Classified by SoftEvol tasks"
                    visualazition(title, person_data, softevolnames)

            except:
                print("!!!Please choose one of the available options!!!")

        elif choice == 2:
            try:
                print("Please choose the id of one of the classification: ")
                print("1. SwM tasks\n2. NFR Labeling\n3. SoftEvol tasks")

                classification = int(input("Choose: "))
                if classification < 1 or classification > 3:
                    raise Exception

                if classification == 1:
                    print("Please choose the id of one of the feature: ")
                    print("1. Corrective tasks\n2. Adaptive tasks\n3. Perfective tasks")

                    feature = int(input("Choose: "))
                    if classification < 1 or classification > 3:
                        raise Exception

                    names = []
                    values = []

                    for name in data.keys():
                        names.append(name)
                        values.append((list(data[name].values())[classification - 1][feature - 1]))

                    if feature == 1:

                        title = "Total Commits for Corrective Tasks of Every Developer"
                        visualazition(title, values, names)

                    elif feature == 2:

                        title = "Total Commits for Adaptive Tasks of Every Developer"
                        visualazition(title, values, names)

                    elif feature == 3:

                        title = "Total Commits for Perfective Tasks of Every Developer"
                        visualazition(title, values, names)

                elif classification == 2:
                    print("Please choose the id of one of the feature: ")
                    print(
                        "1. Maintainability\n2. Usability\n3. Functionality\n4. Reliability\n5. Efficiency\n6. Portability")

                    feature = int(input("Choose: "))
                    if classification < 1 or classification > 6:
                        raise Exception

                    names = []
                    values = []

                    for name in data.keys():
                        names.append(name)
                        values.append((list(data[name].values())[classification - 1][feature - 1]))

                    if feature == 1:

                        title = "Maintainability"
                        visualazition(title, values, names)

                    elif feature == 2:

                        title = "Usability"
                        visualazition(title, values, names)

                    elif feature == 3:

                        title = "Functionality"
                        visualazition(title, values, names)

                    elif feature == 4:

                        title = "Reliability"
                        visualazition(title, values, names)

                    elif feature == 5:

                        title = "Efficiency"
                        visualazition(title, values, names)

                    elif feature == 6:

                        title = "Portability"
                        visualazition(title, values, names)

                elif classification == 3:
                    print("Please choose the id of one of the feature: ")
                    print("1. Forward Engineering\n2. Re-Engineering\n3. Corrective Engineering\n4. Management")

                    feature = int(input("Choose: "))
                    if classification < 1 or classification > 4:
                        raise Exception

                    names = []
                    values = []

                    for name in data.keys():
                        names.append(name)
                        values.append((list(data[name].values())[classification - 1][feature - 1]))

                    if feature == 1:

                        title = "Forward Engineering"
                        visualazition(title, values, names)

                    elif feature == 2:

                        title = "Re-Engineering"
                        visualazition(title, values, names)

                    elif feature == 3:

                        title = "Corrective Engineering"
                        visualazition(title, values, names)

                    elif feature == 4:

                        title = "Management"
                        visualazition(title, values, names)

            except:
                print("!!!Please choose one of the available options!!!")
        elif choice == 3:
            try:
                print("Please choose the id of one of the classification: ")
                print("1. SwM tasks\n2. NFR Labeling\n3. SoftEvol tasks")

                classification = int(input("Choose: "))
                if classification < 1 or classification > 3:
                    raise Exception

                feature = -1

                if classification == 1:
                    print("Please choose the id of one of the feature: ")
                    print("1. Corrective tasks\n2. Adaptive tasks\n3. Perfective tasks")
                    feature = int(input("Choose: "))

                elif classification == 2:
                    print("Please choose the id of one of the feature: ")
                    print(
                        "1. Maintainability\n2. Usability\n3. Functionality\n4. Reliability\n5. Efficiency\n6. Portability")
                    feature = int(input("Choose: "))

                elif classification == 3:
                    print("Please choose the id of one of the feature: ")
                    print("1. Forward Engineering\n2. Re-Engineering\n3. Corrective Engineering\n4. Management")
                    feature = int(input("Choose: "))

                names = []
                values = []

                for name in data.keys():
                    names.append(name)
                    values.append((list(data[name].values())[classification - 1][feature - 1]))

                print("The maximum number of commits: ", names[values.index(max(values))], max(values))

            except:
                print("!!!Please choose one of the available options!!!")

        elif choice == 4:
            print("See You...")
            sys.exit(1)

        elif choice > 4 or choice < 0:
            print("!!!Please choose one of the available options!!!")

        elif choice == 0:
            pass
