#16 August 2020
from random import randint
#global varribles 
hero = {'Damage': '2-4', 
        'Defence': 1,
        'HP': 20
}
coordinates = {'horizontal' : 0,
                'vertical' : 0
}
day_counter = 1
orb = {'horizontal' : 'unassigned', 
        'vertical' : 'unassigned'
}

location = 'town'
checklist = False

#determine location of player
def location_checker(coordinates, location):
    if coordinates['horizontal'] == town_coordinates['horizontal'][0] and coordinates['vertical'] == town_coordinates['vertical'][0] or coordinates['horizontal'] == town_coordinates['horizontal'][1] and coordinates['vertical'] == town_coordinates['vertical'][1] or coordinates['horizontal'] == town_coordinates['horizontal'][2] and coordinates['vertical'] == town_coordinates['vertical'][2] or coordinates['horizontal'] == town_coordinates['horizontal'][3] and coordinates['vertical'] == town_coordinates['vertical'][3] or coordinates['horizontal'] == town_coordinates['horizontal'][4] and coordinates['vertical'] == town_coordinates['vertical'][4]:
        location = 'town'
    elif coordinates['horizontal'] == 7 and coordinates['vertical'] == 7: #matching to king
        location = 'Rat King'
    else:
        location = 'Rat' #normal outside
    return location  

#leaderboard things
def leaderboard_contents():
    leaderboard_contents = []
    print('--------------------')#printing
    print('{:^20}'.format('LEADERBOARD'))
    print('--------------------')
    with open("leaderboard.txt","r") as f: #splitting name and score
        for line in f:
            line = line.strip('\n').strip().split(',')
            line[1] = int(line[1])           
            leaderboard_contents.append(line) #adding line to list
    #Sort the list from lowest to highest score
    leaderboard_contents = sorted(leaderboard_contents, key=lambda x:x[1], reverse = False) #take in multiple arguements and give 1 output
    return leaderboard_contents

def update_leaderboard(day_counter):
    leaderboard = leaderboard_contents() #call leaderboard function
    with open("leaderboard.txt","w+") as fw:
        #Check if leaderboard.txt has 5 positions.
        if len(leaderboard) == 5:
            #Check if new winstreak is higher than the last places streak.
            if day_counter > int(leaderboard[-1][1]): #check if score is lesser than lowest name
                p_name = input("Congratulations! You have entered the top 5 places in the leaderboard, please enter your name to this score: ")
                new_profile = [p_name, day_counter]
                del leaderboard[-1] #remove the previous guy
                leaderboard.append(new_profile)
                
                for i in range(len(leaderboard)): #rewriting the new file
                    fw.write("{},{}\n".format(leaderboard[i][0],leaderboard[i][1]))
            else:
                for i in range(len(leaderboard)): #rewrite original file
                    fw.write("{},{}\n".format(leaderboard[i][0],leaderboard[i][1]))
        elif day_counter > 1: #if leaderboard doesnt have 5 people yet
            p_name = input("Congratulations! You have entered the top 5 places in the leaderboard, please register a name to this score: ")
            new_profile = [p_name, day_counter]
            leaderboard.append(new_profile)

            for i in range(len(leaderboard)): #write leaderboard
                fw.write("{},{}\n".format(leaderboard[i][0],leaderboard[i][1]))
        else: 
            pass

def view_leaderboard(): #show leaderboard
    leaderboard = leaderboard_contents()
    print("")
    for i in range(len(leaderboard)):
        print("[{}] {} completed the game in {} days.".format(i + 1, leaderboard[i][0].upper(), leaderboard[i][1])) #capatilise name
        print()
    print('--------------------') #look nice and show end of leaderboard

#set random towns
def randomise_town(town_coordinates):
    while len(town_coordinates['horizontal']) < 5:
        x = randint(0, 7)#random x and y coords for town
        y = randint(0, 7)
        for i in range(len(town_coordinates['horizontal'])):
            if abs(town_coordinates['horizontal'][i] - x)<3 and abs(town_coordinates['vertical'][i] - y) < 3:#check if town location is 3 steps away
                success = False
                break
            elif abs(town_coordinates['horizontal'][i] - x) + abs(town_coordinates['vertical'][i] - y) <= 3:
                success = False
                break
            else:
                success = True #town can generate
        if success == True:#add new town to coords
            town_coordinates['horizontal'].append(x)
            town_coordinates['vertical'].append(y)
            
    return town_coordinates

#set random orb position
def randomise_orb(town_coordinates): #random orb
    var = False #variable for while loop
    while var != True:
        
        for i in range(len(town_coordinates['horizontal'])):
            orb_horizontal = randint(4, 7) #coords for orb
            orb_vertical = randint(4, 7)
            if [orb_horizontal, orb_vertical] == [7, 7]:#check orb to king
                continue
            elif [orb_horizontal, orb_vertical] == [town_coordinates['horizontal'][i], town_coordinates['vertical'][i]]:#check orb to town
                continue
            else:# orb is in the open
                orb['horizontal'] = orb_horizontal#add orb coords
                orb['vertical'] = orb_vertical
                var = True
                break
    return orb
#1 Main menu 
def main_menu(hero, day_counter, checklist, coordinates, orb):
    main_text = ["New Game",\
                "Resume Game",\
                "View Leaderboard",\
                "Exit Game"
                ]
    town_coordinates = {'horizontal' : [0], #unfinished town locations
                        'vertical' : [0]
                }
    print("Welcome to Ratventure!")
    print("----------------------")
    while True:
        for i in range(len(main_text)):
            print('{}) {}'.format(i + 1, main_text[i])) #print main menu
        try:
            user = int(input('Enter choice: '))#check for user choice below
            print()
            if user == 1:#new game
                randomise_town(town_coordinates)
                orb = randomise_orb(town_coordinates)
                break
            elif user == 2:
                try:
                    hero, day_counter, checklist, coordinates, town_coordinates, orb = resume_game()
                    break
                except:
                    print('File not found, please choose new game')
            elif user == 3:
                view_leaderboard()
            elif user == 4:
                exit_game()
            else:
                print('Invalid choice')
                print()
                continue
        except ValueError: #if user enters string
                print('Invalid option. Enter only integers!')
                print()
                continue
    return hero, day_counter, checklist, town_coordinates, orb

#1.2 Resume game
def resume_game():
    town_coordinates = {} #set dictonary for reading
    horizontal_list = []
    vertical_list = []
    with  open('saved_game.txt', 'r') as saved_file:
        hero['Damage'] = saved_file.readline().strip('\n')
        hero['Defence'] = int(saved_file.readline().strip('\n'))
        hero['HP'] = int(saved_file.readline().strip('\n'))
        day_counter = int(saved_file.readline().strip('\n'))
        if saved_file.readline().strip('\n')=="False":#check True or False
            checklist=False
        else:
            checklist=True
        coordinates['horizontal'] = int(saved_file.readline().strip('\n'))#extracting dictonary for town coords
        coordinates['vertical'] = int(saved_file.readline().strip('\n'))#extracting dictonary for town coords
        for i in saved_file.readline().strip('\n'):
            try:
                horizontal_list.append(int(i))
            except:
                continue
        for i in saved_file.readline().strip('\n'):
            try:
                vertical_list.append(int(i))
            except:
                continue
        town_coordinates['horizontal'] = horizontal_list
        town_coordinates['vertical'] = vertical_list
        orb['horizontal'] = int(saved_file.readline().strip('\n'))#changing str to int 
        orb['vertical'] = int(saved_file.readline().strip('\n'))
    return hero, day_counter, checklist, coordinates, town_coordinates, orb

#1.3 Exit game
def exit_game():
    exit()
    return

#2 Town menu
def town_options(location, hero, day_counter, checklist, coordinates, town_coodinates):
    town_text = ["View Character", "View Map", "Move", "Rest", "Save Game", "Exit Game"]
    print('Day {}: You are in a {}.'.format(day_counter, location))
    while True:#keep looping till user input is accepted
        #show town text
        for i in range(len(town_text)):
            print('{}) {}'.format(i + 1, town_text[i]))
        try:
            user = int(input('Enter choice: '))
            #check user input for town text
            if user == 1:
                view_character()
                continue
            elif user == 2:
                show_map(coordinates)
                print()
                continue
            elif user == 3:
                show_map(coordinates)
                day_counter = movement(day_counter)#map movement map
                show_map(coordinates)
                break
            elif user == 4:
                #regenerate health
                hero, day_counter = rest(hero, day_counter)
                break
            elif user == 5:
                #save hero stats and location to file
                save_game(hero, day_counter, checklist, coordinates, town_coordinates)
                continue
            elif user == 6:
                exit_game()
                break
            else:
                print('Invalid choice')
                print()
        except ValueError: #if user inputs str
            print('Invalid option. Enter only integers!')
            print()
    return day_counter

#2.1 View character
def view_character():
    print('The Hero')
    for i in hero: #see character stats
        print(i, hero[i])
    print()
    return

#2.2 show map
def show_map(coordinates):
    world_map = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]
    for i in range(len(town_coordinates['horizontal'])): #adding T to world map
        if world_map[town_coordinates['horizontal'][i]][town_coordinates['vertical'][i]] == ' ':
            world_map[town_coordinates['horizontal'][i]][town_coordinates['vertical'][i]] = 'T'
    shapes = '+---+---+---+---+---+---+---+---+'
    max_rows = len(world_map)
    max_cols = len(world_map[0])
    for column in range(max_rows):
        print(shapes)
        print('|', end = '')
        for row in range(max_cols):
            if coordinates['horizontal'] == row and coordinates['vertical'] == column:
                if world_map[coordinates['horizontal']][coordinates['vertical']] == 'T':#if T is in the current location, user is in town
                    print('{:^3}|'.format('H/T'), end = '')
                elif coordinates['horizontal'] == 7 and coordinates['vertical'] == 7:# if coordsd matches rat king, user at king
                    print('{:^3}|'.format('H/K'), end = '')
                else:#user in nowhere
                    print('{:^3}|'.format('H'), end = '')
            else:#print the border
                print('{:^3}|'.format(world_map[row][column]), end = '')
        print()
    print(shapes)
    return

#2.3 move
def movement(day_counter):
    print('W = up; A = left; S = down; D = right')
    while True:#loop till user gives accepted input
        try:
            user = input('Your choice: ')
        except:
            continue
        #new coords
        if user == 'w' or user == 'W':
            coordinates['vertical'] -= 1
        elif user == 's' or user == 'S':
            coordinates['vertical'] += 1
        elif user == "a" or user == 'A':
            coordinates['horizontal'] -= 1
        elif user == 'd' or user == 'D':
            coordinates['horizontal'] += 1
        else:
            print('Invalid choice!')
            continue

        if coordinates['vertical'] > 7 or coordinates['vertical'] < 0 or coordinates['horizontal'] > 7 or coordinates['horizontal'] < 0:
            print('Invalid choice! Hero is out of designated map!')
            #revert coordinates back to original value if user out of map
            if user == 'w' or user == 'W':
                coordinates['vertical'] += 1
            elif user == 's' or user == 'S':
                coordinates['vertical'] -= 1
            elif user == "a" or user == 'A':
                coordinates['horizontal'] += 1
            elif user == 'd' or user == 'D':
                coordinates['horizontal'] -= 1
            continue
        else:
            break
    return day_counter

#2.4 rest
def rest(hero, day_counter):
    hero['HP'] = 20
    print('You are fully healed.')#healing process
    print()
    return hero, day_counter

#2.5 save game
def save_game(hero, day_counter, checklist, coordinates, town_coodinates):#huge chunk to save important info
    with open("saved_game.txt","w+") as saved_file: #overwriting existing info
        saved_file.write('{}\n'.format(hero['Damage']))
        saved_file.write('{}\n'.format(hero['Defence']))
        saved_file.write('{}\n'.format(hero['HP']))
        saved_file.write('{}\n'.format(day_counter))
        saved_file.write('{}\n'.format(checklist))
        saved_file.write('{}\n'.format(coordinates['horizontal']))
        saved_file.write('{}\n'.format(coordinates['vertical']))
        saved_file.write('{}\n'.format(str(town_coordinates['horizontal'])))
        saved_file.write('{}\n'.format(str(town_coordinates['vertical'])))
        saved_file.write('{}\n'.format(orb['horizontal']))
        saved_file.write('{}\n'.format(orb['vertical']))
        print()
    return

#3 combat menu
def rat_combat_menu(hero, location, day_counter, checklist):
    coward = False
    print('Day {}: You are in the open.'.format(day_counter))
    rat = {'Damage' : '1-3', 'Defence' : 1, 'HP' : 10}
    is_rat_alive = True#loop till input accepted
    while True:
        print('Encounter! - Rat')
        for i in rat:#rat info
            print(i , rat[i])
        fight_text = ["Attack", "Run"]
        for i in range(len(fight_text)):#fight text
            print('{}) {}'.format(i + 1, fight_text[i]))
        try:
            user = int(input('Enter choice: '))
            if user == 1:
                hero, rat, is_rat_alive = attack_rat(is_rat_alive, hero, rat, checklist)#fight rat
                if is_rat_alive == True:#rat alive
                    pass
                else:
                    print('The Rat is dead! You are victorious!')
                    break#yay rat ded
            elif user == 2:
                coward = run() #EWWW run away from combat
                break
            else:
                print('Number entered is out of range')
                print()
        except ValueError:
            print('Invalid option. Enter only integers!')
            print()
        print()
    return coward


#3.1 attack
def attack_rat(is_rat_alive, hero, rat, checklist):
    if checklist == True:#orb is obtained
        user_damage = randint(7, 9) 
        user_damage -= 1
    elif checklist == False:#no orb
        user_damage = randint(2, 4)
        user_damage -= 1
    rat['HP'] -= user_damage 
    rat_damage = randint(1, 3) #damage to rat
    print('You dealt {} damage to the Rat'.format(user_damage))
    if rat['HP'] < 1:
        is_rat_alive = False # rat survived
        return hero, rat, is_rat_alive
    elif rat['HP'] > 1:
        if checklist == True:# have orb damage taken
            rat_damage -= 6
            if rat_damage <= 0:
                rat_damage = 0
        else: #no orb damage taken
            rat_damage -= 1
        hero['HP'] -= rat_damage
        print('Ouch! the Rat hit you for {} damage!'.format(rat_damage))#damage taken
        print('You have {} HP left.'.format(hero['HP']))#hp left
    if hero['HP'] < 1:# hero died, sad
        print('--------------------')
        print('{:^20s}'.format('YOU DIED!'))
        print('{:^20s}'.format('GAME OVER!'))
        print('--------------------')
        exit()
    return hero, rat, is_rat_alive

#3.2 run
def run():#cowardly behaviour of running
    print('You run and hide.')
    coward = True
    return coward

#4 display outdoor menu
def outdoor_menu(day_counter, coward, hero, checklist): #after facing the rat
    open_text = ["View Character", "View Map", "Move", "Sense Orb", "Exit Game"]
    while True:
        print()
        for i in range(len(open_text)):
            print('{}) {}'.format(i + 1, open_text[i]))
        try:
            user = int(input('Enter choice: '))
        except ValueError:
            print('Invalid option. Enter only integers!')
            print()
            continue
        if user == 1:
            view_character()
            continue
        elif user == 2:
            show_map(coordinates)
            print()
            continue
        elif user == 3:
            show_map(coordinates)
            movement(day_counter)
            show_map(coordinates)
            break
        elif user == 4:
            if coward == True:#cant get orb till you kill rat coward
                coward = rat_combat_menu(hero, location, day_counter, checklist)
            else:
                hero, checklist = sense_orb(hero, coordinates)
                
            continue
        elif user == 5:
            exit_game() #leave
            break
        else:#didnt enter write int
            print('Invalid choice')
            print()
            continue  
    return hero, checklist

#4.4 sense orb
def sense_orb(hero, coordinates): #finding orb
    checklist = False
    if orb['horizontal'] < coordinates['horizontal'] and orb['vertical'] < coordinates['vertical']:
        print('You sense that the Orb of Power is to the northwestt.')
    elif orb['horizontal'] == coordinates['horizontal'] and orb['vertical'] < coordinates['vertical']:
        print('You sense that the Orb of Power is to the north.')
    elif orb['horizontal'] > coordinates['horizontal'] and orb['vertical'] < coordinates['vertical']:
        print('You sense that the Orb of Power is to the northeast.')
    elif orb['horizontal'] < coordinates['horizontal'] and orb['vertical'] == coordinates['vertical']:
        print('You sense that the Orb of Power is to the west.')
    elif orb['horizontal'] > coordinates['horizontal'] and orb['vertical'] == coordinates['vertical']:
        print('You sense that the Orb of Power is to the east.')
    elif orb['horizontal'] < coordinates['horizontal'] and orb['vertical'] > coordinates['vertical']:
        print('You sense that the Orb of Power is to the southwest.')
    elif orb['horizontal'] == coordinates['horizontal'] and orb['vertical'] > coordinates['vertical']:
        print('You sense that the Orb of Power is to the south.')
    elif orb['horizontal'] > coordinates['horizontal'] and orb['vertical'] > coordinates['vertical']:
        print('You sense that the Orb of Power is to the southeast.')
    elif orb['horizontal'] == coordinates['horizontal'] and orb['vertical'] == coordinates['vertical']: #found orb
        print('You found the Orb of Power!')
        print('Your attack increases by 5!')
        print('Your defence increases by 5!')
        hero['Damage'] = '7-9'
        hero['Defence'] = 6
        checklist = True
    return hero, checklist

#rat king menu
def king_combat_menu(hero, day_counter): #fight king hopefully
    print('Day {}: You see the Rat King!'.format(day_counter))
    rat_king = {'Damage' : '8-12', 'Defence' : 5, 'HP' : 25}
    is_king_alive = True #run till king == False
    while True:
        print('Encounter! - Rat King')
        for i in rat_king:
            print(i, rat_king[i])
        fight_text = ["Attack", "Run"]
        for i in range(len(fight_text)):# show fight or run
            print('{}) {}'.format(i + 1, fight_text[i]))
        print()
        try:
            user = int(input('Enter choice: '))
            if user == 1:#brave fight?
                if checklist == True:#heng ah got bring orb
                    hero, rat_king, is_king_alive = king_attack(hero, rat_king, checklist, is_king_alive)
                    if is_king_alive == False:#king died
                        print('The Rat King is dead! You are victorious!')
                        print('Congratulations! You have defeated the Rat King!')
                        print('The world is saved, you WIN!!')
                        break
                    else:
                        pass
                else:#siao never being orb ah
                    failure_attack(hero)
            elif user == 2:#run from king
                run()
                break
            else:#user enters weird number
                print('Invalid choice!')
                print()
        except ValueError: #user cant enter int for some reason so keep looping
            print('Invalid option. Enter only integers!')
            print()
    return 

#successful attack
def king_attack(hero, rat_king, checklist, is_king_alive):#orb attack
    user_damage = randint(7, 9) #randomise damage
    user_damage -= 5
    rat_king['HP'] -= user_damage 
    king_damage = randint(6,10) #randomise damage
    print('You dealt {} damage to the Rat King'.format(user_damage))
    king_damage -= 6
    hero['HP'] -= king_damage
    if hero['HP'] < 1: #no health and died
        print('--------------------')
        print('{:^20s}'.format('You died!'))
        print('{:^20s}'.format('GAME OVER!'))
        print('--------------------')
        exit()
    elif rat_king['HP'] < 1: #yay king died
        is_king_alive = False
    else:#normal combat report
        print('Ouch! the Rat King hit you for {} damage!'.format(king_damage))
        print('You have {} HP left.'.format(hero['HP']))
    return hero, rat_king, is_king_alive

#no orb attack
def failure_attack(hero):#no orb attack sure die
    print('You do not have the Orb of Power - the Rat King is immune!')
    print('You deal 0 damage to the Rat King')
    king_damage = randint(6, 10)#randomise damage
    print('Ouch! The Rat King hit you for {} damage!'.format(king_damage))
    hero['HP'] -= king_damage
    print('You have {} HP left.'.format(hero['HP']))#normal attack report
    return hero

#start actual programme
hero, day_counter, checklist, town_coordinates, orb = main_menu(hero, day_counter, checklist, coordinates, orb) #main menu
while location != 'Rat King': #check and assign function for location
    if location == 'town':
        day_counter = town_options(location, hero, day_counter, checklist, coordinates, town_coordinates)
    elif location == 'Rat':#fight rat then can see town
        coward = rat_combat_menu(hero, location, day_counter, checklist)
        hero, checklist = outdoor_menu(day_counter, coward, hero, checklist)
    location = location_checker(coordinates, location)
    day_counter += 1 #end of day
king_combat_menu(hero, day_counter)#king fight
update_leaderboard(day_counter)#reach leaderboard finally