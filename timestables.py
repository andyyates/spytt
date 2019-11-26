#!/usr/bin/python

import random
import datetime
import os
import csv

table= 6
score = 0
question_count = 10


class bcolors:
    NORMAL = '\033[0m'
    HEADER = '\033[95m'
    GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.NORMAL)
print("")
print("your scores ... green=perfect, blue=v good, yellow=alright, purple=ok, red=rubbish, x = not attempted yet")
print("")

class Question:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.speed = 9999999
        self.speeds = []

    def get_question(self):
        return "%d x %d" % (self.a, self.b)

    def get_answer(self):
        return self.a * self.b

    def __gt__(self,b):
        return self.speed < b.speed


questions = []

for i in range(1,13):
    for j in range(0,13):
        q = Question(i,j)
        questions.append(q)

if os.path.exists("spy_tt_speed.csv"):
    with open("spy_tt_speed.csv", 'r') as fd:
        csv_reader = csv.reader(fd, delimiter=',')
        for row in csv_reader:
            try:
                date = datetime.datetime.fromisoformat(row[0])
            except:
                date = datetime.datetime.now()
            q = row[1]
            try:
                score = float(row[2])
            except:
                score = 9999999
            ql = [o for o in questions if o.get_question() == q]
            #ql[0].speed = min(ql[0].speed, score)
            ql[0].speed = score
            #min(ql[0].speed, score)
            ql[0].speeds.append( [date, score] )


print("     ", end="")
for i in range(0,13):
    print(bcolors.GRAY + "%4d " % (i), end='')
print("")

totals_keys = [bcolors.GREEN, bcolors.BLUE, bcolors.YELLOW, bcolors.PURPLE, bcolors.RED, bcolors.GRAY]
colour_times = {bcolors.GREEN:2, bcolors.BLUE:3, bcolors.YELLOW:5, bcolors.PURPLE:7, bcolors.RED:10, bcolors.GRAY:600}
totals = {}

for k in totals_keys:
    totals[k] = 0

for q in questions:
    if q.b == 0:
        print("")
        print(bcolors.GRAY + "%4d " % q.a, end="")

    if q.speed < 2:
        col = bcolors.GREEN
    elif q.speed < 3:
        col = bcolors.BLUE
    elif q.speed < 5:
        col = bcolors.YELLOW
    elif q.speed < 7:
        col = bcolors.PURPLE
    elif q.speed < 10:
        col = bcolors.RED
    if q.speed < 10:
        print(col + "%4d " % q.get_answer(), end="")
    else:
        col = bcolors.GRAY
        print(bcolors.GRAY + "   x ", end="")

    totals[col] += 1

print(bcolors.NORMAL)
print("")

print("totals: ", end = "")
for k in totals_keys:
    print(k + "%d " % (totals[k]), end = "")
print("")


print(bcolors.NORMAL)
input("press enter to start >")

def ms():
    return datetime.datetime.now().timestamp()

random.shuffle(questions)
questions.sort()

quiz = questions[0:20]

for q in quiz:
    ask_time = ms()
    a = input("What is " + q.get_question() + " ? ")
    try:
        a = int(a)
    except:
        print("nope")
    ans_time = ms()
    speed = ans_time - ask_time
    if a == q.get_answer():
        score += 1
        q.speed = speed
        print("yeh!")
    else:
        print("nope it actually is %d" % q.get_answer())
        q.speed += 100

    input(">")



print ("Well done, you got %d out of %d" % (score, question_count))

with open("spy_tt_speed.csv",'a') as fd:
    writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for q in quiz:
        row = []
        row.append(datetime.datetime.now().isoformat())
        row.append(q.get_question())
        row.append(q.speed)
        writer.writerow(row)




