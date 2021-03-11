#!/bin/python3

# TODO: calculate points totals IF actual column is populated
# TODO: config file with sizes of prediction tables and stats tolerances
# TODO: handle style sheet
# TODO: display actual winner in final column

import math
import numpy
import sys

###############################################################################
### TOP OF PAGE ###

def top_of_page(f):
    global YEAR

    f.write("<html>\n\n")
    f.write("<HEAD>\n")
    f.write("  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n")
    f.write("	<title>MLB Predictions " + YEAR + " </title>\n")
    f.write("       <LINK REL='stylesheet' TYPE='text/css' HREF='style/style" + YEAR + ".css'>\n")
    f.write("       <link rel=\"icon\"\n") 
    f.write("             type=\"image/png\"\n") 
    f.write("             href=\"favicon.ico\">\n")
    f.write("</HEAD>\n\n\n")

    f.write("<center>\n")
    f.write("<table class=\"MYHEADER\" width=35%>\n")
    f.write("<tr class=\"MYHEADER\"><td class=\"MYHEADER\" ><font face=\"bookman\" size=6 color=\"#ffffff\"><b><i>" + YEAR + " MLB PREDICTIONS</b></i></font>\n")
    f.write("</table>\n")
    f.write("</center>\n")
    f.write("<br>\n\n")

###############################################################################
### COMMON TABLES ###

def table_header(f, people):
    f.write("<table class=\"MYTABLE\">\n")
    f.write("<tr class=\"MYSIDES\"><th></th>")
    for person in people:
        f.write("<th>"+ person.split(' ')[0] + "<br>" + person.split(' ')[1])
    f.write("<th>Actual")

def points_table(f, num_people, points):
    print(points)
    f.write("\n<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Points\n")
    for i in range(0, num_people):
        if points:
            f.write("<td class=\"MYTABLE\">" + str(points[i]) + "\n")
        else:
            f.write("<td class=\"MYTABLE\">\n")
    f.write("</table>\n")
    f.write("<br>\n\n")
    f.write("<!--- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% --->\n")

###############################################################################
### PREDICTION TABLES ###

def standings_table(f, people, data, actuals, total_points):
    global YEAR
    points = [0]*len(people)
    
    table_header(f, people)
    for div in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + div + "\n")
        if "Loser" in div:
            size = "25"
        else:
            size = "50"
        for idx, team in enumerate(data[div]):
            team = team.lower().strip().replace(' ', '')
            bg = ""
            
            f.write("<td class=\"MYTABLE" + bg + "\"><img width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + team +".jpg\">\n")
        f.write("<td class=\"MYTABLE\">\n")

    points_table(f, len(people), points)
    total_points = [x+y for x,y in zip(points, total_points)]
    return total_points


def playoffs_table(f, people, data, actuals, total_points):
    global YEAR
    points = [0]*len(people)
    
    table_header(f, people)
    for series in data:        
        if "Champion" in series:
            f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140><font color=\"#ffff66\"><b>" + series + "</b></font>\n")
        else:
            f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + series + "\n")
        for idx, matchup in enumerate(data[series]):
            (winner, loser, numGames) = matchup.split('&')
            if "Champion" in series:
                size = "70"
                border = "2"
            else:
                size = "50"
                border = "1"
            bg = ""

            if "Champion" in series:
                f.write("<td class=\"MYTABLE\"><img border=" + border + " width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + winner.lower().strip() +".jpg\"><br>in " + numGames.strip() +"\n")
            else:            
                f.write("<td class=\"MYTABLE\"><img border=" + border + " width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + winner.lower().strip() +".jpg\"><br>over<br>" + loser.strip() + "<br>in " + numGames.strip() +"\n")
        f.write("<td class=\"MYTABLE\">\n")
    points_table(f, len(people), points)
    total_points = [x+y for x,y in zip(points, total_points)]
    return total_points

def awards_table(f, people, data, actuals, total_points):
    global YEAR
    points = [0]*len(people)
    
    table_header(f, people)
    for category in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + category + "\n")
        if "MotY" in category:
            ww = "30%"
            hh = "30%"
            location = "logos"
        else:
            ww = "38"
            hh = "54"
            location = "players"
        for idx, player in enumerate(data[category]):
            first = player.strip().split(' ')[0]
            last =  player.strip().split(' ')[1:]
            bg = ""

            if "MotY" in category:
                (last, team) = ' '.join(last).split('&')
                team = team.lower().strip().replace(' ', '')  
                f.write("<td class=\"MYTABLE" + bg + "\"><img width=" + ww + " height=" + hh +" src=\"" + location + "_" + YEAR + "/" + team +".jpg\"><br><font size=0.5>" + first[0] + ". " + last + "</font>\n")
            else:
                f.write("<td class=\"MYTABLE" + bg + "\"><img width=" + ww + " height=" + hh +" src=\"" + location + "_" + YEAR + "/" + last[0].lower() +".jpg\"><br><font size=0.5>" + first[0] + ". " + ' '.join(last) + "</font>\n")

        f.write("<td class=\"MYTABLE\">")
    points_table(f, len(people), points)
    total_points = [x+y for x,y in zip(points, total_points)]
    return total_points

def stats_table(f, people, data, actuals, total_points):
    global YEAR
    points = [0]*len(people)
    
    table_header(f, people)
    for category in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + category + "\n")
        for idx, leader in enumerate(data[category]):
            (first, last, num) = leader.split('&')
            fullName = first + ' ' + last
            first = fullName.split(' ')[0].strip()
            last = ''.join(fullName.split(' ')[1:]).strip()
            bg = ""
            bold = ("", "")
            nameRight = False
            numRight = False
                
           # f.write("<td class=\"MYTABLE" + bg + "\"f>" + bold[0] + first.strip() + "<br>" + last.strip() + "<br>" + num.strip() + bold[1] + "\n")
            f.write("<td class=\"MYTABLE" + bg + "\"f>" + bold[0] + leader.replace('&','<br>') + bold[1] + "\n")
        f.write("<td class=\"MYTABLE\">")
    points_table(f, len(people), points)
    total_points = [x+y for x,y in zip(points, total_points)]
    return total_points

def anything_else_table(f, people, data):
    f.write("<table class=\"MYSMALLTABLE\" width=\"50%\">\n")
    f.write("<tr class=\"MYSIDES\"><th></th><th>Anything Else</th>\n")
    for idx, pred in enumerate(data['Anything Else']):
        if pred.strip():
            f.write("<tr class=\"MYTABLE\"><td class=\"MYSMALLSIDES\">" + people[idx] + "\n")
            f.write("<td class=\"MYTABLE\">" + pred.strip() + "\n")
    f.write("</table>\n<br>\n\n")
    
###############################################################################
### TOTALS TABLE ###

def totals_table(f, people, total_points):
    table_header(f, people)
    f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Total Points\n")
    for points in total_points:
        f.write("<td class=\"MYTABLE\">" + str(points) + "\n")
    f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Rank\n")
    array = numpy.array(total_points)
    order = (-array).argsort()
    for r in order.argsort():
        f.write("<td class=\"MYTABLE\">" + str(r+1) + "\n")
    f.write("<td class=\"MYTABLE\">")
    f.write("</table>\n")
        
###############################################################################
### CHAMPIONS TABLES ###

def champs_table(f):
    f.write("\n\n<br><br><br>\n<div>\n")
    f.write("<table style=\"float:left;margin-right:30px\" class=\"MYSMALLTABLE\" width=400 bordercolor=\"000000\">\n")
    f.write("<CAPTION class=\"MYHEADER\"><font size=5 face=\"cursive\" color=\"#E8E8E8\"><b>Past Champions</b></font><pre></pre></CAPTION>\n")
    f.write("<tr class=\"MYSIDES\">\n")
    f.write("<th> <font color=\"#E8E8E8\">Year</font>\n")
    f.write("<th> <font color=\"#E8E8E8\">Champion</font>\n")
    f.write("<th> <font color=\"#E8E8E8\">Points</font>\n")
    f.write("<th> <font color=\"#E8E8E8\">Results</font>\n")
    with open('data/champs.csv', 'r') as q:
        for line in q:
            year = line.split(',')[0].strip()
            name = line.split(',')[1].strip()
            points = line.split(',')[2].strip()
            f.write("<tr class=\"MYHEADER\">\n")
            f.write("<td width=20% class=\"MYSMALLSIDES\">" + year + "\n")
            f.write("<td width=40% class=\"MYTABLE\"><b>" + name + "</b>\n")
            f.write("<td width=15% class=\"MYTABLE\">" + points + "\n")
            f.write("<td width=25% class=\"MYTABLE\"><a target=\"_blank\" href=\"predictions_" + year + "_3.html\">Results</a>\n")
    f.write("<tr class=\"MYHEADER\">\n")
    f.write("<td colspan=\"4\" class=\"MYTABLE\"><font size=1>*Note: Scoring changed in 2004</font>\n")
    f.write("</table>\n")
    
############################################################################### 
### MAIN

def main():
    global YEAR

    ### Read from data file
    standings = {}
    playoffs = {}
    awards = {}
    stats = {}
    anything = {}

    # This is the total number of items per category. Don't change it.
    standings_size = 10 #10
    playoffs_size = 3 #3
    awards_size = 8 #8
    stats_size = 7 #7


    if len(sys.argv) != 2:
        print("usage: ./genpred_bare.py <data_file_name>")
        sys.exit()

    datafile = sys.argv[1]
    ii = 0
    first = True
    with open(datafile, 'r') as f:
        for line in f:
            if line[0] != '#':
                line = line.strip()
                if first:
                    YEAR = line.split(',')[0]
                    people = [p.strip() for p in line.split(',')[1:]]
                    first = False
                else:
                    line_as_array = line.split(',')
                    if ii >= 0 and ii < standings_size:
                        standings[line_as_array[0]] = line_as_array[1:]
                    elif standings_size <= ii < standings_size + playoffs_size:
                        playoffs[line_as_array[0]] = line_as_array[1:]
                    elif standings_size + playoffs_size <= ii < standings_size + playoffs_size + awards_size:
                        awards[line_as_array[0]] = line_as_array[1:]
                    elif standings_size + playoffs_size + awards_size <= ii < standings_size + playoffs_size + awards_size + stats_size:
                        stats[line_as_array[0]] = line_as_array[1:]
                    elif standings_size + playoffs_size + awards_size + stats_size <= ii < standings_size + playoffs_size + awards_size + stats_size + 1:
                        anything[line_as_array[0]] = line_as_array[1:]
                    ii += 1

    actuals = {}            
#with open('data/winners.csv', 'r') as f:
#    for line in f:
#        if line[0] != '#':
#            line = line.strip()
#            actuals[line.split(',')[0]] = line.split(',')[1]        

    ### Create ouptut file
    f = open('predictions_' + YEAR + '.html', 'w')

    ### Top of page
    top_of_page(f)

    ### Populate predictions
    total_points = [0] * len(people)
    total_points = standings_table(f, people, standings, actuals, total_points)
    total_points = playoffs_table(f, people, playoffs, actuals, total_points)
    total_points = awards_table(f, people, awards, actuals, total_points)
    total_points = stats_table(f, people, stats, actuals, total_points)
    anything_else_table(f, people, anything)

    ### Totals
    totals_table(f, people, total_points)

    ### Display champions table
    champs_table(f)

    ### Close file
    f.write("</div>\n<br>\n<br>\n\n</html>\n")
    f.close()

if __name__ == "__main__":
    global YEAR
    main()
