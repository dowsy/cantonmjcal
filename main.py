import math
from datetime import datetime
import csv

faanTable = {0: 0, 1: 0, 2: 0, 3: 8, 4: 16, 5: 24, 6: 32, 7: 46, 8: 64}

winds = {1: "East", 2: "South", 3: "West", 0: "North"}
playerNames = ["Round"]
for a in winds:
    name = str(input("Please input the name of player " + winds[a] + ": \n"))
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

while True:
    a = math.ceil(b / 4 - 0.01)
    d += 1
    currRound = [winds[a % 4], winds[b % 4], c % 4]
    print("----------------------------------------------------------------------------")
    print(str(d) + ") " "Current round: \n" + str(currRound[0]) + " " + str(currRound[1]) + " " + str(currRound[2]) + ", Dealer: " + str(options[b % 4]))
    while True:
        options[0] = "No Winner"
        winner = int(input("Who's the winner?\n" + str(options) + "\n"))
        try:
            if winner not in options:
                print("Invalid input, try again.")
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
        faan = int(input("How many faan?\n"))
        try:
            if faan < 3:
                print("Invalid input, try again.")
            elif faan > 8:
                faan = 8
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
                print("Invalid input, try again.")
            elif loser == 0:
                baoJimo = int(input("Bao Jimo?\n 0: No; 1:Yes\n"))
                if baoJimo not in [0,1]:
                    print("Invalid input, try again.")
                elif baoJimo == 1:
                    del options[0]
                    unluckyGuy = int(input("Who bao Jimo?" + str(options)+ "\n"))
                    break
                else:
                    break
            else:
                break
        except ValueError:
            print("Invalid input, try again.")
    options = dict(zip(digitOptions, playerNames))

    # Calculate faan
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
            if loser != 0:
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
    with open('%s.csv' % filename, 'r') as f:
        reader = csv.reader(f)
        overall = list(reader)
        for e in range(1,5):
            sumList = []
            for i in range(1,d+1):
                sumList.append(int(overall[i][e]))
            results[options[e]] = sum(sumList)
    print("Total: " + str(results))
