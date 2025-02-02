import mysql.connector as mysql
import time
import random
import pygame
from datetime import datetime
mycon=mysql.connect(host="localhost",user="root",password="8921980499" ,database="Sudoku")
mycur=mycon.cursor()
original_grid_element_colour=(52,31,151)
width=550
background_colour=(251,247,245)
#grid and game
def game_no():
    print("Easy, Medium or Hard")
    level=input("Enter difficulty level:")
    a=random.randint(1,10)
    num=str(a)
    if len(num)==1:
        num="0"+str(a)
    if level.upper()=="EASY":
        game="E"
    elif level.upper()=="MEDIUM":
        game="M"
    elif level.upper()=="HARD":
        game="H"
    game_code="G"+game+num
    solved_code="S"+game+num
    return (game_code,solved_code)

def check():
    mycur.execute("select * from %s"%(game[1],))
    solved=mycur.fetchall()
    lsolved=[]
    for i in range(len(solved)):
        lsolved.append(list(solved[i]))
    count=0
    for row in range(len(lsolved)):
        if lsolved[row]==grid_check[row]:
            count+=1
    if count==9:
        print("Yay correct. Game over.")
        stop_time=time.time()
        global time_taken
        time_taken=round(stop_time-start_time,0)
        return "correct"
    return

def insert(win,position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont("monospace", 35)
    buffer=5
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != None):
                    return
                if(event.key == 48): #checking with 0
                    grid_original[i-1][j-1] = event.key - 48
                    grid_check[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background_colour, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    pygame.display.update()
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    pygame.draw.rect(win, background_colour, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50 +15, position[1]*50))
                    grid_original[i-1][j-1] = event.key - 48  #grid inputs the numbers, event key -48 gives the number to be inputed
                    grid_check[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
            
def sudoku():
    pygame.init()
    win=pygame.display.set_mode((width,width))
    pygame.display.set_caption("Sudoku")
    win.fill(background_colour)
    global myfont
    myfont=pygame.font.SysFont("monospace",35)
    for x in range(0,10):
        if (x%3==0):
            pygame.draw.line(win,(0,0,0),(50+50*x,50),(50+50*x,500),5)
            pygame.draw.line(win,(0,0,0),(50,50+50*x),(500,50+50*x),5) 
        pygame.draw.line(win,(0,0,0),(50+50*x,50),(50+50*x,500),2)
        pygame.draw.line(win,(0,0,0),(50,50+50*x),(500,50+50*x),2)
    font=pygame.font.SysFont('pixeltype.ttf',35)
    pygame.display.update()
    global game
    game=game_no()
    mycur.execute("select * from %s"%(game[0],))
    global grid
    grid=mycur.fetchall()
    global grid_check
    grid_check=[[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    for a in range(0,len(grid[0])):
        for b in range(0,len(grid[0])):
            if grid[a][b]==None:
                continue
            else:
                if(0<grid[a][b]<10):
                    value=myfont.render(str(grid[a][b]),True,original_grid_element_colour)
                    win.blit(value,((b+1)*50+15,(a+1)*50))
    pygame.display.update()
    global start_time
    start_time=time.time()
    #print(start_time)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win,(pos[0]//50,pos[1]//50))
                correct=check()
                if correct=="correct":
                    pygame.quit()
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                return

#backend work
def account_check():
    existing_player=input("Do you have an account?(y/n)")
    if existing_player.upper()=="N":
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        phoneno = input("Enter Phone Number: ")
        gender = input("Enter Gender(M/F): ")
        mycur.execute("select max(PlayerId) from profiles")
        lmax_playerid=mycur.fetchall()
        max_playerid=lmax_playerid[0][0]
        global playerid
        playerid=max_playerid + 1
        insert_query = "INSERT INTO profiles (PlayerId,PlayerName,PhoneNo,Age,Gender) VALUES ({},'{}',{},{},'{}')".format(playerid,name,phoneno,age,gender)
        mycur.execute(insert_query)
        mycur.execute("create table {} like Abigail".format(name))
        mycon.commit()
        print("Added!")
        print("Your player id is",playerid)
    elif existing_player.upper()=="Y":
        playerid=int(input("Enter your player id:"))
        return

def adding():
    mycur.execute("select PlayerName from profiles where PlayerId=%s"%(playerid,))
    player_table=mycur.fetchall()[0][0]
    insert_query="INSERT INTO "+player_table+" VALUES (%s, %s, curdate())"
    values=(game[0],time_taken)
    mycur.execute(insert_query,values)
    mycon.commit()
    return

def updation():
    def update_phoneno(player_id, new_phone_number):
        update_query = "UPDATE profiles SET PhoneNo = %s WHERE PlayerId = %s"
        inp= (new_phone_number, player_id)
        mycur.execute(update_query, inp)
        return
    def update_age(player_id, new_age):
        update_query = "UPDATE profiles SET Age = %s WHERE PlayerId = %s"
        inp = (new_age,player_id)
        mycur.execute(update_query,inp)
        return
    def update_gender(player_id,gender):
        update_query = "UPDATE profiles SET Gender = %s WHERE PlayerId = %s"
        inp = (gender,player_id)
        mycur.execute(update_query,inp)
        return
    while True:
        print("1. Update Phone Number")
        print("2. Update Age")
        print("3. Update gender")
        print("4. Quit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            player_id = int(input("Enter player ID: "))
            new_phoneno = input("Enter new phone number: ")
            update_phoneno(player_id, new_phoneno)
            mycon.commit()
            print("Phone number updated .")
        elif ch == 2:
            player_id = int(input("Enter player ID: "))
            new_age = int(input("Enter new age: "))
            update_age(player_id, new_age)
            mycon.commit()
            print("Age updated .")
        elif ch==3:
            player_id = int(input("Enter player ID: "))
            gender=input("Enter new gender: ")
            update_gender(player_id, gender)
            mycon.commit()
        elif ch == 4:
            break
        else:
            print("Invalid choice")
    return

def delete():
    player_id=input("Enter the ID of the player whose records you want to delete:")
    delete_query="DELETE FROM PROFILES WHERE PLAYERID=%s"
    data=(player_id,)#tuple containing id to delete
    mycur.execute(delete_query,data)
    print("The profile of player",player_id,"has been deleted")
    mycon.commit()
    return

def oldest_game():
    mycur.execute("select PlayerName from profiles where PlayerId=%s"%(playerid,))
    player_table=mycur.fetchall()[0][0]
    mycur.execute("select min(Date) from  "+player_table)
    oldest=mycur.fetchall()
    print("Your oldest/first game was played on",oldest[0][0].strftime("%d-%b-%Y"))
    return

def fastest_times():
    mycur.execute("select PlayerName from profiles where PlayerId=%s"%(playerid,))
    player_table=mycur.fetchall()[0][0]
    mycur.execute("select * from "+player_table+" order by timetaken")
    times=mycur.fetchall()
    col_names=[i[0] for i in mycur.description]
    for name in col_names:
        print(str(name).center(10),"\t",end="")
    print()
    for i in times:
        for j in i:
            print(str(j).center(10),"\t",end="")
        print()
    return

def no_of_games():
    mycur.execute("select PlayerName from profiles where PlayerId=%s"%(playerid,))
    player_table=mycur.fetchall()[0][0]
    mycur.execute("select count(GameCode) from "+player_table)
    count=mycur.fetchall()[0][0]
    print("You have played",count,"sudoku games,")
#main code
account_check()
print("1. Play Game")
print("2. How to play Sudoku")
print("3. See a players oldest game")
print("4. See a players fastest times")
print("5. See number of games played")
print("6. Update player profile")
print("7. Delete a players proflie completely")
print("8. Quit")
while True:
    opt=int(input("Enter your option:"))
    if opt==1:
        sudoku()
        adding()
    elif opt==2:
        print('''Traditional Sudoku is a 9x9 puzzle grid made up of nin 3x3 regions. What you need to do is to complete the Sudoku puzzle and make sure that the same single number may not appear twice in the same row, column, or any of the nine 3x3 regions.''')
    elif opt==3:
        oldest_game()
    elif opt==4:
        fastest_times()
    elif opt==5:
        no_of_games()
    elif opt==6:
        updation()
    elif opt==7:
        delete()
        break
    elif opt==8:
        break
    else:
        print("Invalid option")