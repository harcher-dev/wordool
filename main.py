import pygame, sys, requests
from random import randint
from time import sleep

def draw_text(textval, x, y, fontsize, colour):
    font = pygame.font.Font('fonts/Ambra-Sans.ttf', fontsize)
    text = font.render(textval, True, colour) 
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text,textRect)    

def draw_guess(indicator,guess,attempt):
    font = pygame.font.Font('fonts/Ambra-Sans.ttf', 64)
    guesslist = list(guess)
    
    for step,val in enumerate(indicator):           #draws coloured boxes
        pos = pygame.Rect((80*step),(80*attempt),80,80)
        if val == 1:
            pygame.draw.rect(screen, (0,255,100), pos)
        if val == 2:
            pygame.draw.rect(screen, (255,0,0), pos)
        if val == 3:
            pygame.draw.rect(screen, (255,150,0), pos)
    
    for step,letter in enumerate(guesslist):           #draws letters
        text = font.render(letter, True, (255,255,255)) 
        textRect = text.get_rect()
        textRect.center = (80*(step+0.5),80*(attempt+0.5))
        screen.blit(text,textRect)
    
def draw_textbox(guess):
    font = pygame.font.Font('fonts/Ambra-Sans.ttf', 64)
    text = font.render(guess, True, (255,255,255)) 
    textRect = text.get_rect()
    textRect.center = (200,450)
    screen.blit(text,textRect)
    
def evaluate_guess(guess):
    guess_chars = list(guess)
    indicator = []
    word_split = list(word)
    
    for x, letter in enumerate(guess_chars):          #assigns 1 if letter in correct place    2 if letter in wrong place
        if letter == word_split[x]:
            indicator.append(1)
        else:
            indicator.append(2)
            
    for x, value in enumerate(indicator):       #checks all 2s to see if still in word but not in right place - reassigns 2 to 3 if condition met
        if value == 2:
            for letter in word_split:
                if letter == guess[x]:
                    indicator[x] = 3
    return(indicator)
    
def validate_guess(guess):
    r = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + str(guess))

    if (r.text[3]) == 'w':
        return 'valid'
    else:
        return 'invalid'

def reset():
    word = randint(1,1000)
    word = (rawtext[word])
    guess = ''
    screen.fill((50,50,50))
    attempt = 0
    word = word.lower()
    return word


attempt = 0
indicator = [] # 1 = green    2= red    3=amber
guess= ''


filename = "words.txt"                  #selects random word
file = open(filename, "r")
rawtext = file.readlines()
file.close()

for x, item in enumerate(rawtext):
        rawtext[x] = item.replace('\n', '')

word = randint(1,1000)
word = (rawtext[word])


pygame.init()
screen_width = 400
screen_height = 575
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Wordool')
clock = pygame.time.Clock()

enterkey_down = False
fill = True
state = 'menu'
keypressed = False
mousedown = False
mouseup = False
invalidword = False
timer = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouseup = True
            
        if event.type == pygame.KEYDOWN:
            if state == 'win':
                keypressed = True
            
            if state == 'lose':
                keypressed = True
            
            if not event.key == pygame.K_RETURN:
                enterkey_down = False
            
            if event.key == pygame.K_BACKSLASH:
                state = 'menu'
            
            if event.key == pygame.K_BACKSPACE:
                guess = guess[:-1]
            elif event.key == pygame.K_RETURN:
                enterkey_down = True
            else:
                guess += event.unicode
    

    if state == 'menu':
        screen.fill((100,100,255))
        draw_text('WORDOOL' ,200,150,40,(255,255,255))
        draw_text(':)' ,375,535,60,(255,255,255))
        clickboxRect = pygame.Rect(200, 350, 300, 50)
        clickboxRect.center = (200,350)
        pygame.draw.rect(screen, (255,255,255), clickboxRect)
        draw_text('Play',200,350,40,(100,100,255))
        if mouseup and clickboxRect.collidepoint(pygame.mouse.get_pos()):
            word = reset()
            print(word)
            state = 'game'
            mouseup = False
        elif clickboxRect.collidepoint(pygame.mouse.get_pos()):
            draw_text('Play',200,350,40,(70,70,255))
            if mousedown:
                draw_text('Play',200,350,40,(0,70,255))
                mousedown = False
        
    elif state == 'win':
        coverRect = pygame.Rect(0,400,400,175)
        pygame.draw.rect(screen,(0,200,0), coverRect)
        draw_text('The word was: ' + word,200,475,30,(255,255,255))
        draw_text('YOU WIN!' ,200,430,30,(255,255,255))
        draw_text('press any key to continue' ,200,550,20,(255,255,255))
        if keypressed == True:
            state = 'menu'
            keypressed = False
    
    elif state == 'lose':
        coverRect = pygame.Rect(0,400,400,175)
        pygame.draw.rect(screen,(200,0,0), coverRect)
        draw_text('The word was: ' + word,200,475,30,(255,255,255))
        draw_text('YOU RAN OUT OF GUESSES!' ,200,430,30,(255,255,255))
        draw_text('press any key to continue' ,200,550,20,(255,255,255))
        if keypressed == True:
            state = 'menu'
            keypressed = False
        
        
    elif state == 'game':
        
        
        while fill == True:
            screen.fill((50,50,50))
            fill = False
            
        pygame.draw.line(screen, (255,255,255), (0,400), (400,400), 7)
        pygame.draw.line(screen, (255,255,255), (0,500), (400,500), 7)
        pygame.draw.line(screen,(50,50,50), (0,450), (400,450), 90)
        
        guess_split = list(guess)
        
        if guess == '' and invalidword == False:
            draw_text('start typing',200,450,30,(255,255,255))
            
        
        if len(guess_split) == 5 and enterkey_down == True:
            if validate_guess(guess) == 'valid':
                indicator = (evaluate_guess(guess))
                draw_guess(indicator, guess, attempt)
                
                if guess == word:
                    print('player won. resetting.')
                    draw_guess(indicator, guess, attempt)
                    attempt = 0
                    state = 'win'
                else:
                    attempt += 1
                    if attempt == 5:
                        print('player lost. the word was -', word)
                        state = 'lose'
                        attempt = 0
                guess = ''
                enterkey_down = False
            else:
                guess = ''
                draw_text('not a word',200,540,30,(255,255,255))
                timer = 0
                enterkey_down = False
        
        if timer >= 60:
            pygame.draw.line(screen, (50,50,50), (0,540),(400,540), 30)
        
        col = 1
        for x in range(0,4):
            pygame.draw.line(screen, (155,155,155), (80*col,0), (80*col,400), 2)
            col+=1

        row = 1
        for x in range(0,4):
            pygame.draw.line(screen, (100,100,100), (0,80*row), (400,80*row), 2)
            row+=1
            
        draw_textbox(guess)
            
    timer += 1
    
    pygame.display.update()
    clock.tick(60)