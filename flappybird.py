from pygame import*
import random
from time import sleep
init()
WIDTH, HEIGHT = 800, 600
FPS = 60

mixer.music.load('land.mp3')
mixer.music.play(-1)

hit = mixer.Sound('hit.mp3')


die = mixer.Sound('die.wav')

fly = mixer.Sound('fly.wav')
 
                                                           #----------------------------------------------------------------------------------------
window = display.set_mode((WIDTH, HEIGHT), FULLSCREEN)     #----------------- ЧТОБЫ ВЫЙТИ ОБРАТНО НУЖНО НАЖАТЬ КНОПКУ WINDOWS ----------------------
                                                           #----------------------------------------------------------------------------------------

mouse.set_visible(False)                                                                                                                                              #black green white red yellow window pipe bges base rect hit hitc

clock = time.Clock() 

font1 = font.Font (None, 35)
font2 = font.Font (None, 80)
font3 = font.Font (None, 80)

imgBG = image.load('background .png')
                                                                                                               #imgBird = image.load('yellowbirdMI.png')
imgBird = image.load('yellowbirdUP.png')

imgPB = image.load('pipeBT.png')
imgPT = image.load('pipeUP.png')
imgBA = image.load('base.png')
imgME = image.load('message.png')

py, sy, ay = HEIGHT // 2, 0, 0
player = Rect(WIDTH // 3, py, 34, 24)
frame = 0

timer = 10
state = 'start'




pipes = []
bges = []
bases = []

bges.append(Rect(0, 0, 288, 600))

lives = 3
scores = 0
highscore = 0
with open('highscore.txt', 'r') as file:
    highscore = int(file.read())

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    press = mouse.get_pressed()
    keys = key.get_pressed()
    click = press[0] or keys[K_SPACE]
    

    if timer  > 0:
        timer -= 1
    
    for i in range(len(bges) -1, -1, -1):
        bg = bges[i]
        bg.x -= 1

        if bg.right < 0:
            bges.remove(bg)
        
        if bges[len(bges)-1].right <= WIDTH:
            bges.append(Rect(bges[len(bges)-1].right, 0, 288, 600))

    for i in range(len(pipes) -1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 4
        
        
        if pipe.right < 0:
            pipes.remove(pipe)

        

    for i in range (len(bases) -1, -1, -1):
        ba = bases[1]
        ba.x -= 1

        if ba.right < 0:
            bases.remove(ba)

        
    if state == 'start':
        
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    
    elif state == 'play':
        if lives >= 0 and state != 'start':
            scores += 0.5
            if scores > highscore:
                highscore = int(scores)
        if click:
            ay = -2.6
            
            
            
        else:
            ay = 0
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 170:
            hei1 = random.randint(100,250)
            hei2 = random.randint(350, 550)
            pipes.append(Rect(WIDTH,  0, 50, hei1 ))
            pipes.append(Rect(WIDTH,  hei2, 50, 200))
        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'
            

    elif state == 'fall':
        hit.play()
        sy, ay = 0, 0
        state = 'start'
        lives -= 1
    if lives < 1:
        state = 'gameover'
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
        scores = 0
        if len(pipes) == 0 and click:
            lives += 3
            state = 'play'
        

        
    


    window.fill(Color('black'))
    for bg in bges:
        window.blit(imgBG, bg)
    

    for pipe in pipes:
        draw.rect(window, Color(18, 203, 30), pipe)
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPT.get_rect(topleft = pipe.topleft)
            window.blit(imgPB, rect)

    for base in bases:
        draw.rect(window, Color(18, 203, 30), base)
        

    image = imgBird.subsurface(34 * int(frame), 0, 34, 24)
    image = transform.rotate(image, -sy * 2)
    window.blit(image, player )



    text = font1.render('Score: ' + str(int(scores)), 1, Color('black'))
    window.blit(text, (10, 10))

    text = font1.render('Lives: ' + str(lives), 1, Color('black'))
    window.blit(text, (10, HEIGHT - 50))
    if state == 'gameover':
        text = font2.render('Game ' + 'Over', 1, Color('black'))
        window.blit(text, (230,300))
        text = font1.render('tap to try again', 1, Color('black'))
        window.blit(text, (230, 350))

        
    if state == 'start' and lives >= 1:
        text = font3.render('Tap here ', 1, Color('black'))
        window.blit(text, (125, 70))
        text = font3.render('to start the game', 1, Color('black'))
        window.blit(text, (300, 150))
    
    text = font1.render('Highscore: ' + str(int(highscore)), 1, Color('black'))
    window.blit(text, (10, 50))

    display.update()
    clock.tick(FPS)
with open('highscore.txt', 'w') as file:
    file.write(str(highscore))
quit()    