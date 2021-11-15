# Isaac Lo
# Nov. 10 2021
# Honors Harry Potter Seminar!!

import random
from random import randint
import time
import threading
import pygame
from pygame import mixer

inventory = {'galleons': 42, 'wand': 1, 'dandelions': 4, 'bezoar stone': 1, 'potato': 1}
dragonLoot = ['Heart of Ember', 'Dark Sword', "Elder's gold", 'Ruby', 'manly armpit hair']
bruteyLoot = ['sparkling drink', 'brute\'s magical mace', 'potato', 'galleons', 'galleons', 'galleons', 'galleons']
baddyLoot = ['stolen boxers', 'thrice enchanted old wand', 'potato', 'galleons', 'galleons', 'galleons', 'galleons', 'galleons']
slappyLoot = ['dragon heartstring wand', 'potato', 'galleons', 'galleons', 'galleons', 'galleons', 'galleons',]

EqItem = 'potato'
name = ''
turn = True
position = 1
battmusic = 0
defaultSpeed = .035
textSpeed = defaultSpeed
playing = True
defDragonHP = 1000
defBaddyHP = 64
defSlappyHP = 64

weapons = {'galleons': -1, 'wand': 3, 'manly armpit hair': 1000, 'dandelions': 1, 'bezoar stone': 1, 'potato': 1,
           'Heart of Ember': 3, 'The Elder Wand': 170, "Elder's gold" : -3, 'Ruby': -2, 'stolen boxers' : -10, 'dragon heartstring wand': 5,
           'thrice enchanted old wand': 7, 'brute\'s magical mace': 10, 'the slap stick': 13, 'sparkling drink': 1, 'good humor token': 0, 'bad humor token': 0}
edibles = {'galleons': 1, 'wand': -17, 'manly armpit hair': 27, 'dandelions': 2, 'bezoar stone': 32, 'potato' : 7,
           'Heart of Ember': 17, 'The Elder Wand': -100, "Elder's gold" : 3, 'Ruby': 2, 'stolen boxers' : -10, 'dragon heartstring wand': 14,
           'good humor token': 0, 'sparkling drink': 15}
attacks = {'expelliarmus': weapons[EqItem]*2 + 9, 'crucio' : 17 + weapons.get(EqItem, 0), 'stupefy' : 14 + weapons.get(EqItem, 0),
           'episkey' : 0, 'slap' : 4 + weapons.get(EqItem, 0), 'turn the other cheek': -3, 'use item': 0, 'switch weapon': 0}

dude = [name, 17, [], ['poop filled boxers']]
health = dude[1]

brutey = ['Brutey', 77, ['brutish brawl battle bop' , 10, 'drunken bottle blow', 7, 'running slap', 6, 'glancing blow', 1, 'slap', 4], bruteyLoot]
punchy = ['Punchy, the punching bag', 10000, ['disappointed empty stare', 0, 'mean parenthetical sentence (you are lvl 0)', 0], ['tear of punchy']] 
slappy = ['Wizard Slappy', defSlappyHP, ['slap', 2, 'glancing blow', 1, 'roguish look', 1], slappyLoot]
baddy = ['Death Eater', defBaddyHP, ['crucio', 7, 'slap', 4, 'glancing blow', 3, 'imperius curse', 13], baddyLoot]
dragon = ['Burny', defDragonHP, ['uncommited scratch', 16, 'FIREBALL', 25, 'glancing blow', 10, 'bop', 17, 'full scale thrust', 32 ], dragonLoot]

def textMe(text):
    num = 0

    for i in text:
        if num != len(text)-1:
            print(i, end='', flush=True)
            num +=1
            time.sleep(textSpeed) 
        else:
            print(i, flush=True)

def text(text):
    num = 0

    for i in text:

        if num != len(text)-1:
            print(i, end='', flush=True)
            num +=1
            time.sleep(textSpeed)
        else:
            print(i, flush=True)
            time.sleep(.5)
            textMe(' ')
            
def addToInventory(newItems):
    for i in newItems:
        print('Added ' + i + ' to inventory')
        numOfItem = inventory.get(i, 0) + 1
        inventory[i] = numOfItem
    print(' ')
    
def Item():
    textMe('You have a ' + EqItem + ' in hand')
    textMe('If you would like to change weapon, type "weapon".')
    textMe('If you would like to use a consumable, type "use".')
    takeCommand()
    
def Inventory():
    textMe('Inventory: ')
    item_total = 0
    for k, v in inventory.items():
        print(' '+ str(v) + ' ' + str(k))
        item_total = item_total + v
    print('Total number of items: ' + str(item_total))
    print(' ')
    print('Equipped item is the ' + EqItem)

    
def takeCommand(*text):
    comDict = {'Item': Item,
        'item' : Item,
        'Inventory' : Inventory,
        'inventory': Inventory,
        'ok': specify,
        'Ok': specify,
        'okay': specify,
        'Okay' : specify,
        'yes' : specify,
        'Yes' : specify,
        'change item' : chooseItem,
        'Change item': chooseItem,
        'change weapon': chooseItem,
        'Change weapon': chooseItem,
        'weapon': chooseItem,
        'Weapon': chooseItem,
        'Change boxers': boxers,
        'boxers': boxers,
        'pants': boxers,
        'the baddy': yIsThisHere,
        'health' : checkHealth,
        'Health' : checkHealth,
        'restart': restart,
        'Restart' : restart,
        'retry' : retry,
        'Retry' : retry,
        'retry battle': retry,
        'Retry battle': retry,
        'Eat': eat,
        'eat': eat,
        'consume': eat,
        'Consume': eat,
        'use' : eat,
        'Use' : eat,
        'Use' : eat,
        'use item' : eat,
        'Use item' : eat,
        'help' : Help,
        'Help' : Help,
        'HELP' : Help,
        'ADMIN ADD' : add,
        'ADMIN REPOS' : reposition,
        'ADMIN HEAL' : adminHealth,
        'ADMIN BATTLE': adminBattle,
        'myself' : corona}
    
    if not text:
        comDict.get(input('--> '),noCommand)()
        
    elif text:
        comDict.get(input(*text),noCommand)()
        
def Help():
    comList = {'change an item.' : 'Item',
        'display inventory.': 'Inventory',
        'change your equipped item.' : 'Change Item',
        'check your current health' : 'Check Health' ,
        'restart game': 'Restart',
        'retry battle' : 'Retry',
        'consume item': 'Use',
        'conjure help list.' : 'Help',
        "I think I'm sick." : 'myself'}
    textMe('A LIST OF COMMANDS: ')
    for k, v in comList.items():
        print(v +': ' + k)

def eat():
    while True:
        print(' ')
        Inventory()
        print(' ')
        textMe('What do you want to consume? (leave blank to quit)')
        
        food = input('--> ')
        if food == '':
            break
        
        if food in inventory.keys() and food in edibles.keys():
            if inventory[food] != 1:
                textMe('How many ' + food + ' do you want to consume?')
                amount = input('--> ')
            
                if (inventory[food] - int(amount)) >= 0:
                    dude[1] += edibles[food]*int(amount)
                    inventory[food] -= int(amount)
                    textMe('You have gained ' + str(edibles[food]*int(amount)) + ' health.')
                    textMe('Your total is ' + str(dude[1]) + ' health.')

                else: #if chosen too much
                    textMe("You don't have that many " + food + " in your inventory.")
                    print(' ')
                    textMe('Do you want to consume all ' + inventory[food] + ' in your inventory?')
                    choice = input('--> ')
                    if 'yes' in choice.lower() or 'ok' in choice.lower():
                        amount = inventory[food]
                        dude[1] += edibles[food]*int(amount)
                        inventory[food] -= int(amount)
                        textMe('You have gained ' + str(edibles[food]*int(amount)) + ' health.')
                        textMe('Your total is ' + str(dude[1]) + ' health.')
                        break
                    
            else:
                dude[1] += edibles[food]
                inventory[food] -= 1
                textMe('You have gained ' + str(edibles[food]) + ' health.')
                textMe('Your total is ' + str(dude[1]) + ' health.')
                if food == 'dragon heartstring wand':
                    text('Hmmm, roughage.')
                    
            if inventory[food] == 0:
                del inventory[food]

        else:
            print("You don't have that in inventory.")
            
def retry():
    posDict = {1 : intro, 1.5: continueJourney, 2: afterIntro, 2.5: brutey, 3 : town} # 3.5 : theif, 4: dragon, 4.5: partayee}
    
    global health
    dude[1] = health

    try:
        posDict[position]()
    except TypeError:
        battle(posDict[position])

def reposition(*placeNum):
    posDict = {'1' : intro, '1.5': continueJourney, '2': afterIntro, '2.5': barFight, '3' : town} # '3.5' : theif, '4': dragon, '4.5': partayee}
    
    if not placeNum:
        choice = input('pos num: ')
        if choice == '':
            posDict.get(str(position))()
        else:
            posDict.get(str(choice))()
    elif placeNum:
        posDict.get(str(*placeNum))()

def restart():
    inventory = {'gold coin': 42, 'wand': 1, 'dandelion': 4, 'bezoar stone': 1, 'potato': 1}
    EqItem = 'potato'
    name = ''
    turn = True
    dude[1] = 17
    
    intro()

def add():
    while True:
        item = input()
        if (item == ''):
            break
        if item in weapons:
            list = []
            list.append(item)
            addToInventory(list)
        else:
            print('not an item, please retry (leave empty to escape)')
            
def adminHealth():
    healthNum = input('health: ')
    dude[1] = int(healthNum)
    
def adminBattle():

    enemyChosen = input('Enemy: ')
    enemies = {"punchy", "brutey", "baddy", "slappy", "punchy"}

    if enemyChosen in enemies:
        enemy = {"punchy": punchy, 
                        "brutey": brutey, 
                        "baddy": baddy, 
                        "slappy": slappy, 
                        "punchy": punchy}.get(enemyChosen)
        battle(enemy)

def checkHealth():
    textMe('You have ' + str(dude[1]) + ' health.')
    
def yIsThisHere():
    textMe("Yeah that's not going to be okay.")

def specify():
    textMe('Please specify what you want to check or change.')
    takeCommand()

def boxers():
    if 'stolen boxers' in inventory.keys():
        print('You changed into the stolen boxers...')
        dude[1] += 40
    elif position >= 2 and 'stolen boxers' not in inventory.keys():
        textMe('You only have your poop filled ones with you.')
    else:
        textMe('You already have a pair of nice clean boxers.')
        
def corona():
    textMe('I think I am coming down with a viral sickness. Maybe I should be in quarantine.')
    if 'poop filled boxers' not in inventory.keys():
        textMe('I feel like I might poop my pants.')
    else:
        textMe('Oh man, I think I have diarrhea.')
        addToInventory(dude[3])
    
def noCommand():
    textMe('We continue on.')
    #break time?
    
def intro():
    pygame.init()

    global name

    # background sound
    mixer.music.load('Ambience.wav')
    mixer.music.play(-1)

    textMe("Hello valiant wizard! ")
    textMe("What is your name? ")
    name = input('--> ')
    print(' ')
    
    textMe("Wizard "+ name + ", you are on a quest to do something–anything—about the criminals and dragons of Pigsmeade (reverse-Hogsmeade).")
    print(' ')
    print(' ')
    
    print('--> To see your inventory, type "Inventory".')
    print('--> To see your currently equipped item, type "Item".')
    print('--> To change your currently equipped item, type "Change item".')
    print('--> To check health, type "Health".')
    print('--> To use a consumable, type "Eat" or "Use".')
    print('--> To see a list of commands, type "Help".')
    
    print(' ')
    takeCommand('Want to use, check, or change anything? --> ')
    print(' ')
    
    textMe('Continue your dangerous journey?')
    choice = input('--> ')
    if('yes' in choice.lower() or 'continue' in choice.lower() or 'ok' in choice.lower()):
        textMe('Did you say "yes"? Oh, I mean, of course.')
        textMe('Let us continue on our quest to bring peace and balance to this confined village. How valiant!')
        textMe('You continue on your journey.')
        
        continueJourney()
    else:
        textMe('Is that a "no"? You are going anyways (how embarrasing).')

        continueJourney()
        
def continueJourney():
    global position
    border()
    textMe('You, the wizard, continues on your journey down a dark forest trail.')
    textMe('How are you feeling?')
    feelings = input('--> ')
    print(' ')
    print(' ')
    text('The wizard was feeling rather ' + feelings + '. Despite that, he was also getting sick, he was cold, and had to go to study for two exams.')
    text('Nevertheless, he had to continue on his text journey.')
    text('The wizard labored down the dirt path through the forest.')
    text('He could not see much.')

    print(' ')
    takeCommand('Want to use, check, or change anything? --> ')
    print(' ')

    text('The day was bright, but the clouds loomed for rain. The hero was tired and wished he had gone to bed eariler last night.')
    text('Along the way, Wizard ' + name + ', came upon a dark figure waiting in the shadows.')
    text('The wizard stopped in absolute terror as he was not in any way ready for a battle.')
    
    textMe('Alert, you hastily pick up your weapon...')
    chooseItem()
    
    print(' ')
    text('Just as he hurriedly fumbled for his weapon, a voice boomed a greeting to him.')
    textMe('<> Hellooo adventurer!')
    textMe('<> I am Wizard Slap of Kirona. What might your name be? Please do tell so that I may formally greet you.')
    print(' ')
    textMe('Type your name or type a fake name:')
    supposedName = input('--> ')
    if supposedName == name:
        addToInventory(['good humor token'])
    textMe('Type your greeting:')
    greeting = ""
    greeting += input('--> ')
    if greeting[0].islower():
        greeting = greeting[0].upper() + greeting[1:]
    print(' ')
    text('<Wizard Slap> Thank you! ' + greeting + ' to you too!')
    text('<Wizard Slap> Fantatstic! Another fine gentleman and wizard. I thank you for your fine greeting, Wizard ' + supposedName + '.')
    text("<Wizard Slap> Excuse me, but you looked a little unhinged and rather " + feelings + " earlier.")
    text("<Wizard Slap> Please pardon me, but it doesn't seem like you have been in many battles.")
    textMe("<Wizard Slap> To benefit you, would you like to duel? I promise I'll go easy on you!")
        
    while(True):
        border()
        textMe('"No" or "Fight"?')
        choice = input('--> ')
        if 'fight' in choice.lower():
            print(' ')
            text("<Wizard Slap> Before we begin I should let you know the rules of the battle.")
            print('')
            text("<Wizard Slap> First off, there are certain attacks that let you maintain your turn; you can make a maximum of 3 moves per turn.")
            text("<Wizard Slap> Second, there are certain moves that are more powerful than others; they are power moves, and you can use a max of 3 per battle.")
            text("<Wizard Slap> And finally third, attacks vary in power but all or useful at some moment.")
            time.sleep(2)
            textMe("<Wizard Slap> And number three and a half, consumables are very valuable.")
            textMe('<Wizard Slap> So the battle begins! Prepare yourself!')

            global health
            health = dude[1]
            position = 1.5
            battle(slappy)

            dude[1] = 17
            if(dude[1] > 12):
                text('<Wizard Slap> Good wizard–jolly–I have been bested! Please, you may call me "Slappy" as you are my equal. I do hope you learned something.')
                text('<Slappy?> Well I am off! I hope our duel and my items aid your surely valiant quest. Aye dios.')
                text('You continue on your quest to return order unto Pigsmeade.')
            else:
                text('<Wizard Slap> Well you surely needed that lesson. Perhaps next time we meet you will be more prepared. Good luck my wizard! Aye dios.')
                text('You continue on your quest to return order unto Pigsmeade.')
            break
        
        elif 'no' in choice.lower():
            text('<Wizard Slap> Well you surely needed that lesson. Perhaps next time we meet you will be more prepared. Good luck my wizard! Aye dios.')
            text('You continue on your quest to return order unto Pigsmeade.')
            break
        else:
            print("That's not an option!!")
        
    print(' ')
    takeCommand('Want to use, check, or change anything? --> ')
    print(' ')

    text("Your trek persists until the dark, even though you intended to find bed and bath (mostly bath) by now at the 'Quarry In Town' hotel.")
    text('The road is dark and you come upon a bridge.')
    text("You see a shadow in front of you.")
    time.sleep(2)
    print("It moves!")
    time.sleep(1)

    health = dude[1]
    position = 2
    
    border()
    print("A real life death-eater appears!")
    print(' ')
    time.sleep(2)
    
    while(True):
        textMe('"Run" or "Fight"?')
        choice = input('--> ')
        if 'fight' in choice.lower():
            print(' ')
            textMe('The battle begins!')
            battle(baddy)
            afterIntro()
            break
        elif 'run' in choice.lower():
            time.sleep(3)
            random.seed()
            if(random.choice([1, 2]) % 2 == 0):
                textMe('You narrowly escaped!')
                afterIntro()
                break
            else:
                textMe("You couldn't get away!")
                battle(baddy)
                afterIntro()
                break
        else:
            print("That's not an option!!")
        
def afterIntro():
    global position
    position = 2
    takeCommand('Want to use, check, or change anything? --> ')

    if baddy[1] == 0:
        text('The wizard was really getting into this text battling, so much so that he forgot all his previous troubles.')
        text('Typing and attacking, listening to the bongo drums, he was getting into the flow.')
        time.sleep(1)
        text('Wizard ' + name + ' carefully stepped over the death eater and crossed the bridge.')
        text('He was a man who could not be stopped.')
        text('A wizard whose honor was only rivaled by the amount of hearing loss he had undergone from his loud rock music, which was a lot.')
    else:
        text('The wizard barrelled past the baddy. "Sayonara!" he shouted as he sped away.')
        text('Fortunately, when he forgot about his new trouble, he remembered he desperately needed to go to the restroom.')
    town()
        
def barFight():
    text('But just as the wizard pulled out his ' + EqItem + ', an enormous brute, perhaps six feet tall, attempted to grab him (again).')
    text('But the wizard was too quick, and he dodged as if he had moves like Jagger.')
    text('"I am not so easily stopped!" the wizard shouted. Have at thee!')
    time.sleep(1)
    textMe('The battle begins!')

    global health
    health = dude[1]
    position = 2.5
    battle(brutey)

    border()
    time.sleep(1)
    textMe('The wizard was strong in this moment of conflict and he utterly beat his opponent.')
    textMe('The brute\'s still body lay there on the ground.')
    time.sleep(1)
    
    while(True):
        textMe('"Leave" him or "Finish" him?')
        choice = input('--> ')
        if 'leave' in choice.lower():
            border()
            textMe('Yet this time he showed compassion, and he left his unconscious body on the ground.')
            addToInventory(['good humor token'])
            break
        elif 'finish' in choice.lower():
            textMe('The wizard was full of rage, and in his rage he taunted the brute while he was down (how outrageous)!')
            addToInventory(['bad humor token'])
            break
        else:
            print("That's not an option!!")
            break
        
    text('The wizard had done it. He then asked for the drink that Wizard Slap needed.')
    drink = 1
    addToInventory(['cold alcoholic beverage'])
    text('He then left.')

def town():
    text('As he neared the town he had to decide where he was going...')

    barNum = 0
    hotelNum = 0
    drink = 0
    trys = 0
    roomAva = False
    coinsGiven = 0
    
    while(True):
        textMe('"\'Quarry In Town\' Hotel" or "tavern"?')
        choice = input('--> ')
        if 'tavern' in choice.lower():
            print(' ')
            text('You enter the tavern late in the night. It smells bad.')
            
            if baddy[1] <= 0 and barNum >= 1:
                text('You, with your dirty cloak enter and walk to the bar as the occupants give you looks.')
                text('The thug does not give you the stanky eye because his fake eye is tired.')
            elif baddy[1] <= 0 and barNum == 1:
                text('You, with your cloak blotched with dirt and string with leaves, enter and walk to the bar as the occupants give you looks.')
                text('One thug gives you the stanky eye.')
            else:
                text('As you enter and walk to the bar, the occupants give you looks; one gives you the stanky eye.')

            if barNum == 0:
                text('When you reach the bartender takes one good look at you and says, "We don\'t serve your kind here. GET OUT!"')
            else:
                text('When you reach the bartender says, "I TOLD YOU! WE DO NOT SERVE YOUR KIND. GET OUT!" (he angry)')
            
            while(True):
                textMe('"Leave" or demand a "Drink"?')
                choice = input('--> ')
                if 'drink' in choice.lower():
                    border()
                    time.sleep(1)
                    if (drink == 0):
                        text('The valiant wizard stayed, held his ground and demanded a drink. He could not stand for this injustice.')
                        if barNum < 2:
                            text('But just as the wizard pulled out his ' + EqItem + ', he was forcibly stopped by an enormous brute, perhaps six feet tall.')
                            text('He was easily wrapped up in his iron trunks of arms and thrown out.')
                            barNum += 1
                            break
                        elif barNum > 1 and roomAva != True:
                            text('But just as the wizard pulled out his ' + EqItem + ', he was forcibly stopped by an enormous brute, perhaps six feet tall.')
                            text('He was easily wrapped up in his iron trunks of arms and thrown out (again), as if this didn\'t already happen before.')
                            text('Maybe if he found a bathroom first, the wizard would be able to move with more freedom.')
                            barNum += 1
                            break
                        elif barNum >= 2 and roomAva:
                            barFight()
                            drink += 1
                            barNum += 1
                            break
                    else:
                        text('The bartender, infuriated, walked away from the counter.')
                        if drink < 3:
                            text('You take this opportunity to take a nice cold *sparkling* drink (not orange juice, way cooler).')
                            addToInventory(['sparkling drink'])
                            drink += 1
                        else:
                            
                            text('There unfortunately was no more *sparkling* drinks left, only OJ (not cool).')
                        takeCommand('Want to check anything? ')
                        text('You leave the bar.')
                        break
                    barNum += 1
                else:
                    text('You left the bar empty handed.')
                    break
                            
        elif ('quarry' in choice.lower() or 'hotel' in choice.lower()):
            border()
            time.sleep(1)
        
            text('You walk to the hotel. The light in the window is on.')

            if roomAva != True and trys == 0:
                text('You try the door, but it won\'t budge. A sliding trapdoor on the wall opens.')
            
            textMe('<> Hey, what do you want?')
            if trys > 0:
                textMe('<Inn Keeper> Oh you again.')
            else:
                textMe('<Inn Keeper> You want a room?')

            trys += 1
            random.seed()
            ranNum = random.choice([1, 5])
            if(ranNum == 1 and roomAva == False):
                roomAva = True
                textMe('<Inn Keeper> Alright, well we conveniently have a room for you.')
                text('They narrowly had room for you')
            
            elif ranNum != 1 and roomAva == False:
                if(random.choice([1, 2]) == 1):
                    text('<Inn Keeper> Well we don\'t got one for you. Beat it!')
                else:
                    text('<Inn Keeper> We don\'t have any room in the inn.')
                text("You couldn't get a room!")
                
            if roomAva == True:
                text('You go down the lamp lit hallway to the room.')
                if hotelNum == 0:
                    textMe('As you go through the door, you see a figure in the lamplight in your room.')
                    border()
                    time.sleep(3)
                    textMe('<> Hellloooo adventurer!')
                    time.sleep(2)
                    if slappy[1] == 0:
                        textMe('<Slappy> It is me, your good friend and acquaintence, Slappy!')
                        text('The other wizard was sitting in the room roasting his hat over a candle.')
                        
                        textMe('<Slappy> Would you happen to have a drink? I could definitely use one right now.')
                        textMe('<Slappy> There is a tavern across the bricks, and I am far too damaged from our battle to go.')
                        textMe('<Slappy> I would be grateful, if you would be so kind to get me a drink. I would be very obliged.')
                        textMe('<Slappy> Here take a coin or two, for the trouble.')
                        addToInventory(['galleons', 'galleons', 'galleons'])
                        coinsGiven += 3
                        
                        print(' ')
                        text('The other wizard obliged quickly, anything for such a close friend.')
                        text('You relieved yourself.')
                        hotelNum += 1
                    else:
                        text('<Wizard Slap> It is me, my good wizard, Wizard Slap.')
                        text('The other wizard was sitting in the room roasting his hat over a candle.')
                        
                        textMe('<Wizard Slap> Would you happen to have a drink? I could definitely use one right now.')
                        textMe('<Wizard Slap> There is a tavern across the bricks, and I am far too damaged from our battle to go.')
                        textMe('<Wizard Slap> I would be grateful, if you would be so kind to get me a drink. I would be very obliged.')
                        textMe('<Wizard Slap> Here take a coin or two, for the trouble.')
                        addToInventory(['galleons', 'galleons'])
                        coinsGiven += 2

                        print(' ')
                        text('The other wizard obliged quickly, anything for an anybody I guess?')
                        hotelNum += 1
                        
                elif hotelNum > 0 and drink > 0:
                    textMe('<Slap wizard dude> I thank thee for thy work.')
                    text('<Slap wizard> Please take this compensation for this deed.')
                    del inventory['cold alcoholic beverage']
                    addToInventory(['the slap stick', 'galleons', 'galleons', 'potato', 'good humor token'])

                    text('Subtracted cold alcoholic beverage from inventory.')
                    text('The other wizard promptly took the beverage, spilled it all over his dirty hat, and started to wash his hands and hat with it.')
                    text('<Wizard Slap> Weeeeh!! Woahhh! Sooo clean!!!')

                    text('You walk over to your bed, and in only a few minutes, fell asleep.')
                    break
                else:
                    takeCommand('Do you want to check or change anything? ')
                    if coinsGiven < 10:
                        text('<Slap wizard dude> Please, get me a drink. I am in much need, I thank thee for thy work.')
                        textMe('<Wizard Slap> Here take an extra coin or two, I heartfully ask you.')
                        addToInventory(['galleons', 'galleons'])
                        coinsGiven += 2
                    else:
                        textMe('<Wizard Slap> I cannot give you anymore coins, you scoundrel, now I can only hope you will come to my aid.')
                
        else:
            print("That's not an option!!")
    
def bossBattle():
    textMe('You open your eyes to darkness. . .')
    border()
    text('You have accidentally entered a dragon cave.')
    time.sleep(1)
    textMe('Rrrrrrooooaaaaaaahhhhhhhhhh')
    time.sleep(2)
    textMe('You are in front of a dragon.')
    
    
    global position
    global health
    health = dude[1]
    position = 4
    
    #mixer.music.load('HailtotheKing.wav')
    battle(dragon)

def chooseItem():
    global EqItem
    Inventory()
    print(' ')
    textMe("pick an item: ")

    while(True):
        choice = input('--> ')
        if choice in inventory.keys():
            addToInventory([EqItem])
            EqItem = str(choice)
            inventory[EqItem] -= 1
            if inventory[EqItem] == 0:
                del inventory[EqItem]
            textMe('Equipped ' + str(choice) + ' in hand.')
            break
        elif(choice == ''):
            textMe('You kept your current item.')
            break
        else:
            print("You don't have that item in your inventory. Choose again: (leave empty to keep current item or weapon)" )
            
def battle(enemy):
    if (enemy[0] == "Burny" or enemy[0] == "Punchy, the punching bag"):
        mixer.music.load('HailtotheKing.wav')
    else:
        random.seed(health)
        if (randint(1, 3) % 2 == 0):
            mixer.music.load('Battle.wav')
        else:
            mixer.music.load('DarkJungle.wav')
    mixer.music.play(-1)

    global position
    global attacks

    textMe(str(enemy[0]) + ' approaches with ' + str(enemy[1])+ ' health!')
    print(' ')
    takeCommand('Want to use, check, or change anything? --> ')
    time.sleep(1)
    border()
    global turn
    turn = True
    powerMoves = 0

    textMe('You have ' + str(dude[1]) + ' health.')
    print(' ')

    missnum = 0
    enemyMissnum = 0

    while(True):
        global EqItem
        
        if turn == True:
            enemyMissnum = 0
            attacks = {'expelliarmus': weapons[EqItem]*2 + 11, 'crucio' : 23 + weapons.get(EqItem, 0), 'stupefy' : 17 + weapons.get(EqItem, 0),
           'episkey' : 0, 'slap' : 4 + weapons.get(EqItem, 0), 'turn the other cheek': -3, 'use item': 0, 'switch weapon': 0}

            textMe('ACTIONS:')
            for k, v in attacks.items():
                   print(' ' + k + ': damage ' + str(v))
            print(' ')
            
            if position == 1:
                textMe("What move do you choose? ")
            else:
                print(' ')

            while True:
                move = input('--> ')
                if move in attacks.keys():
                    if powerMoves < 3 and (move == 'crucio' or move == 'stupefy'):
                        powerMoves += 1
                        break
                    elif move == 'crucio' or move == 'stupefy':
                        textMe("You are out of power moves.")
                    else:
                        break
                else:
                    textMe("That's not a move.")

            damage = attacks.get(str(move), 0)

            if (move == 'switch weapon' or move == 'stupefy'
                or move == 'episkey' or move == 'slap' or move == 'use item') and missnum < 2:
                if move == 'switch weapon':
                    chooseItem()
                if move == 'episkey':
                    dude[1] += 3
                    textMe('+3 Health! You now have ' + health + ' health.')
                if move == 'slap' or move == 'stupefy':
                    enemy[1] -= damage
                if move == 'use item':
                    eat()
                missnum += 1
            else:
            
                print('You ' + str(move) + ' with your ' + EqItem + '.')   
                enemy[1] -= damage
                if enemy[1] < 0:
                        enemy[1] = 0
                turn = False
                
            if enemy[1] <= 0:
                time.sleep(1)
                print('You defeated the ' + enemy[0] + '!!!')
                print(' ')
                addToInventory(enemy[3])
                break

            time.sleep(1)
            border()
            time.sleep(1)
            
            textMe('You did ' + str(damage) + ' damage.')
            print(' ')
            textMe('The ' + enemy[0] + ' has '+ str(enemy[1]) + ' health!')
            print(' ')
                
        if turn == False:
            missnum = 0
            atkNum = len(enemy[2])/2
            random.seed(health);
            moveInd = (randint(0, atkNum)-1)*2
            moveDam = moveInd + 1
            move = str(enemy[2][moveInd])
            
            time.sleep(1)
            textMe(str(enemy[0]) + ' attacks with a ' + str(enemy[2][moveInd]) + '. ')
                
            damage = enemy[2][moveDam]
            dude[1] -= damage
            border()
            time.sleep(2)
            textMe('You suffered ' + str(damage) + ' damage.')

            if (move == 'FIREBALL' or move == 'glancing blow' or move == 'slap') and enemyMissnum < 2:
                turn = False
                enemyMissnum += 1
            else:
                turn = True

            if dude[1] <= 0:
                time.sleep(2)
                border()
                textMe('You have been defeated by the ' + str(enemy[0]) + '!!!')
                failure()
                break
            
            textMe('You have ' + str(dude[1]) + ' health left.')
            print(' ')

    random.seed(health);
    if (randint(1, 3) % 2 == 0):
        mixer.music.load('Prologue.wav')
    else:
        mixer.music.load('Ambience.wav')
    mixer.music.play(-1)
            
def failure():
    textMe("Nice try wizard. . . You'll get him on the next one.")
    textMe('"Restart" or "Retry Battle"?')
    takeCommand()
    
def ending():
    ending = "This game doesn't have an ending yet."
    textMe(ending)
    takeCommand()
    
def border():
    for i in range(3):
        time.sleep(.005)
        print('.')
