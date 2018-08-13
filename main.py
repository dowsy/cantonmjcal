import math
from datetime import datetime
import sys
import csv

# Rules setting
while True:
    try:
        minFaan = int(input("\nPlease enter minimum faan: \n"))
        maxFaan = int(input("Please enter maximum faan: \n"))
    except ValueError:
        print("Invalid input, enter again.")

    faanList = []
    for i in range(0, maxFaan + 1):
        faanList.append(i)

    faanTable = dict((el, 0) for el in faanList)
    styleDict = {1: '2-5-chick', 2 : '5-1', 3 : '1-2-munn'}
    spicyDict = {1 : 'Half-spicy-up', 2 : 'Full-spicy-up'}

    try:
        style = int(input("Play how big? Enter 1 for '2-5-chick'; 2 for '5-1'; 3 for '1-2-munn'\n"))
        if style not in [1, 2, 3]:
            raise ValueError
        spiciness = int(input("Enter 1 for 'Half-spicy-up'; 2 for 'Full-spicy-up'\n"))
        if spiciness not in [1, 2]:
            raise ValueError
    except ValueError:
        print("Invalid input, enter again")

    halfIndex = []
    if maxFaan <= 5:
        for i in range(0, maxFaan):
            halfIndex.append(2 ** i)
    elif maxFaan > 5:
        for i in range(0, 4):
            halfIndex.append(2 ** i)
        for i in range(5, maxFaan):
            halfIndex.append(2 ** (i-1))
            halfIndex.append(int((2 ** (i-1)) * 1.5))
    halfIndex = halfIndex[0:maxFaan+1]

    fullIndex = []
    for i in range(0, maxFaan+1):
        fullIndex.append(2 ** i)

    if spiciness == 1:
        faanIndex = halfIndex
    elif spiciness == 2:
        faanIndex = fullIndex

    for k in range (0, len(faanIndex)):
        if style == 1:
           faanIndex[k] *= 0.25
        elif style == 2:
            faanIndex[k] *= 0.5

    faanTable = dict(zip(faanList, faanIndex))
    for i in range(0, minFaan):
        del faanTable[i]

    for i in range(minFaan, maxFaan+1):
        print(str(i) + "番;  |   $" + str(faanTable[i]))

    try:
        confirm = str(input("\n" + styleDict[style] + " " + spicyDict[spiciness] + ", confirm? Y/N\n"))
        if confirm.lower() not in ['y', 'n']:
            raise ValueError
    except ValueError:
        print("Invalid input, try again.")
    if confirm.lower() == 'y':
        break
    elif confirm.lower == 'n':
        continue

winds = {1: "East", 2: "South", 3: "West", 0: "North"}
playerNames = ["Round"]
for a in winds:
    name = str(input("\nPlease input the name of player " + winds[a] + ": \n"))
    playerNames.append(name)

results = dict((el, 0) for el in playerNames)

# open csv file and print headers
filename = (datetime.now().isoformat(timespec='hours'))
with open('%s.csv' % filename, 'w+', newline='') as f:
    writer = csv.writer(f)
    fieldnames = []
    for i in range(0,5):
        fieldnames.append(playerNames[i])
    writer = csv.writer(f)
    writer.writerow(fieldnames)

a = b = c = 1
d = 0
digitOptions = []
for i in range(0, 5):
    digitOptions.append(i)
options = dict(zip(digitOptions, playerNames))
print("Let's get started!")


def ask_results():
    while True:
        winner = loser = faan = baoJimo = unluckyGuy = 9
        options = dict(zip(digitOptions, playerNames))
        options[0] = "No Winner"
        try:
            winner = int(input("Who's the winner?\n" + str(options) + "\n"))
            if winner not in options:
                raise ValueError
            elif winner == 0:
                break
            else:
                del options[winner]
                break
        except ValueError:
            print("Invalid input, try again.")
    while winner != 0:
        try:
            faan = int(input("How many faan?\n"))
            if faan < minFaan:
                raise ValueError
            elif faan > maxFaan:
                faan = maxFaan
                break
            else:
                break
        except ValueError:
            print("Invalid input, try again.")
    while winner != 0:
        options[0] = "Jimo"
        try:
            loser = int(input("Who's the loser?\n" + str(options) + "\n"))
            if int(loser) not in options:
                raise ValueError
            elif loser == 0:
                baoJimo = int(input("Bao Jimo?\n 0: No; 1:Yes\n"))
                if baoJimo not in [0, 1]:
                    raise ValueError
                elif baoJimo == 1:
                    del options[0]
                    unluckyGuy = int(input("Who bao Jimo?" + str(options) + "\n"))
                    if unluckyGuy not in options:
                        raise ValueError
                    break
                else:
                    break
            else:
                break
        except ValueError:
            print("Invalid input, try again.")
    calResult = [0, 0, 0, 0]
    if winner != 0:
        if loser == 0:
            if baoJimo == 0:
                calResult[(int(winner) - 1)] += faanTable[faan] * 2
                for k in range(0,4):
                    calResult[k] -= faanTable[faan] / 2
            elif baoJimo == 1:
                calResult[(int(winner) - 1)] += faanTable[faan] * 1.5
                calResult[(int(unluckyGuy) - 1)] -= faanTable[faan] * 1.5
        elif loser != 0:
            calResult[(int(winner)- 1)] += faanTable[faan]
            calResult[(int(loser) - 1)] -= faanTable[faan]
    return calResult


def cal_total(): # read overall results from csv
    with open('%s.csv' % filename, 'r') as f:
        reader = csv.reader(f)
        overall = list(reader)
        for e in range(1,5):
            sumList = []
            for i in range(1,len(overall)):
                sumList.append(int(float(overall[i][e])))
            results[options[e]] = sum(sumList)
    print("Total: " + str(results))

while True:
    a = math.ceil(b / 4 - 0.01)
    d += 1
    currRound = [winds[a % 4], winds[b % 4], c % 4]
    print("----------------------------------------------------------------------------")
    print(str(d) + ") " "Current round: \n" + str(currRound[0]) + " " + str(currRound[1]) + " " + str(currRound[2]) + ", Dealer: " + str(options[b % 4]))
    while True:
        options[0] = "No Winner"
        options[5] = "Menu"
        try:
            winner = int(input("Who's the winner?\n" + str(options) + "\n"))
            if winner not in options:
                raise ValueError
            elif winner == 5:
                while True:
                    menuInput = input("Enter 'q' to end game; 'c' to resume game; or 'e' to edit input.\n")
                    menuInput = menuInput.lower()
                    if menuInput not in ['e', 'q', 'c']:
                        print("Invalid input, try again.")
                    elif menuInput == 'c':
                        break
                    elif menuInput == 'q':
                        print("Game over.")
                        print("Total: " + str(results))
                        sys.exit()
                    else:
                        while menuInput =='e':
                            editInput = int(input("Which round's result you would like to edit? Enter '0' to cancel edit.\n"))
                            try:
                                if editInput == 0:
                                    break
                                elif editInput < 0 or editInput > d:
                                    raise ValueError
                                else:
                                    with open('%s.csv' % filename, 'r+') as f:
                                        reader = csv.reader(f)
                                        overall = list(reader)
                                        print(overall)
                                        replace = ask_results()
                                        replace.insert(0, editInput)
                                        overall[editInput] = replace
                                        for k in range(0, 5):
                                            replace[k] = str(replace[k])
                                    with open('%s.csv' % filename, 'w') as f:
                                        writer = csv.writer(f)
                                        writer.writerows(overall)
                                    cal_total()
                                    break
                            except ValueError:
                                print("Invalid input. Edit again.")
            elif winner == 0:
                b += 1
                c = 1
                break
            else:
                if winner == b:
                    c += 1
                else:
                    b += 1
                    c = 1
                del options[winner]
                break
        except ValueError:
            print("Invalid input, try again.")
    while winner != 0:
        try:
            faan = int(input("How many faan?\n"))
            if faan < minFaan:
                print("Invalid input, try again.")
            elif faan > maxFaan:
                faan = maxFaan
                break
            else:
                break
        except ValueError:
            print("Invalid input, try again.")
    while winner != 0:
        if 5 in options:
            del options[5]
        options[0] = "Jimo"
        try:
            loser = int(input("Who's the loser?\n" + str(options) + "\n"))
            if int(loser) not in options:
                print("Invalid input, try again.")
            elif loser == 0:
                baoJimo = int(input("Bao Jimo?\n 0: No; 1:Yes\n"))
                if baoJimo not in [0,1]:
                    print("Invalid input, try again.")
                elif baoJimo == 1:
                    del options[0]
                    unluckyGuy = int(input("Who bao Jimo?" + str(options)+ "\n"))
                    if unluckyGuy not in options:
                        raise ValueError
                    break
                else:
                    break
            else:
                break
        except ValueError:
            print("Invalid input, try again.")
    options = dict(zip(digitOptions, playerNames))

    # Calculate faan and write to csv
    roundResult = results
    for i in roundResult:
        roundResult[i] = 0
    if winner != 0:
        if loser == 0:
            if baoJimo == 0:
                roundResult[options[winner]] += faanTable[faan] * 2
                for k in roundResult:
                    roundResult[k] -= faanTable[faan] / 2
            elif baoJimo == 1:
                roundResult[options[winner]] += faanTable[faan] * 1.5
                roundResult[options[unluckyGuy]] -= faanTable[faan] * 1.5
        elif loser != 0:
            roundResult[options[winner]] += faanTable[faan]
            roundResult[options[loser]] -= faanTable[faan]
    results['Round'] = d
    print("This round: " + str(roundResult))
    writeLine = []
    for i in range(0,5):
        writeLine.append(roundResult[options[i]])
    with open('%s.csv' % filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(writeLine)

    cal_total()
