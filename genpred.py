#!/bin/python3

# TODO: remove spaces from team names for logo display (e.g. White Sox)
# TODO: calculate points totals IF actual column is populated
# TODO: data file names (currently data.dat and champs.dat) as input

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

def points_table(f, num_people):
    f.write("\n<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Points\n")
    for i in range(0, num_people):
        f.write("<td class=\"MYTABLE\">\n")
    f.write("</table>\n")
    f.write("<br>\n\n")
    f.write("<!--- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% --->\n")

###############################################################################
### PREDICTION TABLES ###

def standings_table(f, people, data):
    global YEAR
    
    table_header(f, people)
    for div in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + div + "\n")
        if "Loser" in div:
            size = "25"
        else:
            size = "50"
        for team in data[div]:
            f.write("<td class=\"MYTABLE\"><img width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + team.lower().strip() +".jpg\">\n")
        f.write("<td class=\"MYTABLE\">\n")
    points_table(f, len(people))

def playoffs_table(f, people, data):
    global YEAR
    
    table_header(f, people)
    for series in data:        
        if "Champion" in series:
            f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140><font color=\"#ffff66\"><b>" + series + "</b></font>\n")
        else:
            f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + series + "\n")
        for matchup in data[series]:
            if "Champion" in series:
                size = "70"
                border = "2"
                f.write("<td class=\"MYTABLE\"><img border=" + border + " width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + matchup.split('&')[0].lower().strip() +".jpg\"><br>in " + matchup.split('&')[1].strip() +"\n")
            else:
                size = "50"
                border = "1"
                f.write("<td class=\"MYTABLE\"><img border=" + border + " width=" + size + "% height=" + size +"% src=\"logos_" + YEAR + "/" + matchup.split('&')[0].lower().strip() +".jpg\"><br>over<br>" + matchup.split('&')[1].strip() + "<br>in " + matchup.split('&')[2].strip() +"\n")
        f.write("<td class=\"MYTABLE\">\n")
    points_table(f, len(people))

def awards_table(f, people, data):
    global YEAR
    
    table_header(f, people)
    for category in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + category + "\n")
        if "MotY" in category:
            ww = ""
            hh = ""
        else:
            ww = "38"
            hh = "54"
        for player in data[category]:
            first = player.strip().split(' ')[0]
            last =  player.strip().split(' ')[1:]
            f.write("<td class=\"MYTABLE\"><img width=" + ww + "% height=" + hh +"% src=\"players_" + YEAR + "/" + last[0].lower() +".jpg\"><br><font size=0.5>" + first[0] + ". " + ' '.join(last) + "</font>\n")
        f.write("<td class=\"MYTABLE\">\n")
    points_table(f, len(people))

def stats_table(f, people, data):
    global YEAR
    
    table_header(f, people)
    for category in data:
        f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>" + category + "\n")
        for leader in data[category]:
            first = leader.split('&')[0].strip()
            last = leader.split('&')[1].strip()
            num = leader.split('&')[2].strip()
            f.write("<td class=\"MYTABLE\">" + first + "<br>" + last + "<br>" + num + "\n") 
        f.write("<td class=\"MYTABLE\">\n")
    points_table(f, len(people))

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

def totals_table(f, people):
    f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Total Points\n")
    for i in range(0, len(people)+1):
        f.write("<td class=\"MYTABLE\">\n")
    f.write("<tr class=\"MYTABLE\"><td class=\"MYSIDES\" width=140>Rank\n")
    for i in range(0, len(people)+1):
        f.write("<td class=\"MYTABLE\">\n")
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

### Read from data file
standings = {}
playoffs = {}
awards = {}
stats = {}
anything = {}

standings_size = 3 #10
playoffs_size = 3
awards_size = 1 #10
stats_size = 2 #7

ii = 0
first = True
with open('data.dat', 'r') as f:
    for line in f:
        line = line.strip()
        if first:
            YEAR = line.split(',')[0]
            people = line.split(',')[1:]
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
            
### Create ouptut file
f = open('out.html', 'w')

### Top of page
top_of_page(f)

### Populate predictions
standings_table(f, people, standings)
playoffs_table(f, people, playoffs)
awards_table(f, people, awards)
stats_table(f, people, stats)
anything_else_table(f, people, anything)

### Totals
totals_table(f, people)

### Display champions table
champs_table(f)

### Close file
f.write("</div>\n<br>\n<br>\n\n</html>\n")
f.close()
