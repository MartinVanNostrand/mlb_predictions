#!/bin/python3

# TODO: remove spaces from team names for logo display (e.g. White Sox)
# TODO: calculate points totals IF actual column is populated
# TODO: data file names (currently data.dat and champs.dat) as input
# TODO: config file with sizes of prediction tables and stats tolerances
# TODO: handle style sheet
# TODO: display actual winner in final column

import math
import numpy

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
            if div in actuals:
                actualWinner = actuals[div].strip().lower().replace(' ', '')
                if int(YEAR) >= 2020:
                    if "Wildcard" in div:
                        wcCount = 0
                        for t in team.split('&'):
                            if t in actualWinner:
                                points[idx] += 1
                                wcCount += 1
                        if wcCount == 1:
                            bg = "3"
                        elif wcCount == 2:
                            bg = "2"
                    elif actualWinner == team:
                        points[idx] += 3
                        bg = "1"
                    else:
                        leagueWC = div.split(' ')[0] + " Wildcard"
                        if leagueWC in actuals:
                            if team in actuals[leagueWC].lower().strip().split('&'):
                                points[idx] += 2
                                bg = "2"
        
            f.write("<td class=\"MYTABLE" + bg + "\"><img width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + team +".jpg\">\n")
        if div in actuals:
            if "Wildcard" in div:
               f.write("<td class=\"MYTABLE\"><img width=25% height=25% src=\"logos_" + YEAR + "/" + actuals[leagueWC].lower().strip().split('&')[0] +".jpg\">&nbsp;<img width=25% height=25% src=\"logos_" + YEAR + "/" + actuals[leagueWC].lower().strip().split('&')[1] +".jpg\">\n")
            else:
               f.write("<td class=\"MYTABLE\"><img width=50% height=50% src=\"logos_" + YEAR + "/" + actualWinner +".jpg\">\n")
        else:
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
            if series in actuals:
                (actualWinner, actualLoser, actualNumGames) = actuals[series].split('&')
                rightLoser = False
                rightWinner = False
                actualWinner = actualWinner.strip()
                actualLoser = actualLoser.strip()
                actualNumGames = actualNumGames.strip()
                if "Champion" in series: # World Series
                    if actualWinner == winner:
                        points[idx] += 5
                        rightWinner = True
                        bg = "2"
                    if actualLoser == loser and rightWinner:
                        points[idx] += 5
                        bg = "1"
                    if rightWinner and actualNumGames == numGames:
                        points[idx] += 2
                        # TODO: make bold
                else: # ALCS, NLCS
                    if actualLoser == loser or actualLoser == winner or actualWinner == loser or actualWinner == winner:
                        points[idx] += 2
                        bg = "3"
                    if actualWinner == winner:
                        points[idx] += 2
                        rightWinner = True
                        bg = "2"
                    if rightWinner and actualNumGames == numGames:
                        points[idx] += 1
                        # TODO: make bold
                    if actualLoser == loser and rightWinner:
                        points[idx] += 3
                        bg = "1"

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
            if category in actuals:
                actualNames = actuals[category].split('&')
                for nameIdx, name in enumerate(actualNames):
                    if name.strip() == first + " " + ' '.join(last):
                        if "MotY" in category:
                            points[idx] += 3 - nameIdx
                        else:
                            points[idx] += 5 - 2*nameIdx
                        bg = str(nameIdx + 1)
            f.write("<td class=\"MYTABLE" + bg + "\"><img width=" + ww + " height=" + hh +" src=\"" + location + "_" + YEAR + "/" + last[0].lower() +".jpg\"><br><font size=0.5>" + first[0] + ". " + ' '.join(last) + "</font>\n")
    if category in actuals:
        f.write("<td class=\"MYTABLE\">")
        for idx, name in enumerate(actuals[category].split('&')):
            first = name.strip().split(' ')[0]
            last = name.strip().split(' ')[1:]
            f.write("<font size=0.5>" + str(idx+1) + ") " + first[0] + " " + ' '.join(last) + "</font><br>")
        f.write("\n")
    else:
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
            if category in actuals:                
                actualName = actuals[category].split('&')[0]
                actualNum = actuals[category].split('&')[1]

                if "Batting Title" in category:
                    tol = 0.003
                elif "Home Runs" in category or "Stolen Bases" in category or "Wins" in category:
                    tol = 1
                elif "RBI" in category:
                    tol = 2

                if num == actualNum:
                    numRight = True
                    bg = "3"
                    points[idx] += 1
                if first + " " + last == actualName:
                    nameRight = True
                    bg = "2"                    
                    points[idx] += 3
                if nameRight and math.isclose(float(num), float(actualNum), abs_tol=tol) and numRight == False:
                    bg = "1"
                    points[idx] += 1
                if nameRight and numRight:
                    bg = "1"
                    points[idx] += 2
                    bold = ("<b>", "</b>")
                
           # f.write("<td class=\"MYTABLE" + bg + "\"f>" + bold[0] + first.strip() + "<br>" + last.strip() + "<br>" + num.strip() + bold[1] + "\n")
            f.write("<td class=\"MYTABLE" + bg + "\"f>" + bold[0] + leader.replace('&','<br>') + bold[1] + "\n")
    if category in actuals:
        f.write("<td class=\"MYTABLE\">" + actualName.strip().split(' ')[0] + "<br>" + ''.join(actualName.split(' ')[1:]) + "<br>" + actualNum.strip() + "\n")
    else:
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
    with open('champs.dat', 'r') as q:
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

### Read from data file
standings = {}
playoffs = {}
awards = {}
stats = {}
anything = {}

standings_size = 10 #10
playoffs_size = 3 #3
awards_size = 6 #10
stats_size = 7 #7

ii = 0
first = True
#with open('data.dat', 'r') as f:
with open('predictions_test.csv', 'r') as f:
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
#with open('winners.dat', 'r') as f:
#    for line in f:
#        if line[0] != '#':
#            line = line.strip()
#            actuals[line.split(',')[0]] = line.split(',')[1]        

### Create ouptut file
#f = open('out.html', 'w')
f = open('predictions_test.html', 'w')

### Top of page
top_of_page(f)

### Populate predictions
total_points = [0] * len(people)
total_points = standings_table(f, people, standings, actuals, total_points)
total_points = playoffs_table(f, people, playoffs, actuals, total_points)
total_points = awards_table(f, people, awards, actuals, total_points)
total_points = stats_table(f, people, stats, actuals, total_points)
#anything_else_table(f, people, anything)

### Totals
totals_table(f, people, total_points)

### Display champions table
champs_table(f)

### Close file
f.write("</div>\n<br>\n<br>\n\n</html>\n")
f.close()
