import threading
import pygame
import socket
import sys
import random

## Variables
# window name
name = "Bucket Drop Game"

# Position of the bucket/player
posx = 300
posy = 300

# Position of the object
objx = random.randint(20, 580)
objy = -50

# Speed modifier
gameSpeed = 1.0
speedLimit = 4.0

# Game Score
score = 0

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)
    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400
    rect2 = pygame.Rect(0, 0, 75, 75)
    rect1 = pygame.Rect(0, 0, 50, 50)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(name)

    pygame.font.init()
    game_font = pygame.font.Font(None, 30)
    
    colorRect = (shapeColor)
    colorRect2 = (shapeColorOver)
    global posx 
    global posy
    global objx
    global objy
    global gameSpeed
    global score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)
        rect1.center = (posx, posy)
        if objy >= 450:
            game_over_text = game_font.render(f'Game Over', True, (0, 0, 0))
            game_over_instruct = game_font.render(f'Press "space" to restart.', True, (0, 0, 0))
            screen.blit(game_over_text, (240, 150))
            screen.blit(game_over_instruct, (180, 180))
        else:
            objy += 0.7 * gameSpeed
        rect2.center = (objx, objy)
        collision = rect1.colliderect(rect2)
        pygame.draw.rect(screen, colorRect, rect1)
        if collision:
            score += 1

            pygame.draw.rect(screen, colorRect2, rect2, 6, 1)
            objx = random.randint(20, 580)
            objy = -50
            if (gameSpeed <= speedLimit): gameSpeed += 0.20
        else:
            pygame.draw.rect(screen, colorRect, rect2, 6, 1)

        score_text = game_font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        fps.tick(60)


    pygame.quit()
    
def RestartGame():
    global posx 
    global posy
    global objx
    global objy
    global gameSpeed
    global score
    posx = 300
    posy = 300
    objx = random.randint(20, 580)
    objy = -50
    gameSpeed = 1.0
    score = 0
    print("Game Reset.")

def ServerThread():
    global posy
    global posx
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            posy -= 10 * gameSpeed
        if(data == 's'):
            posy += 10 * gameSpeed
        if(data == 'a'):
            posx -= 10 * gameSpeed
        if(data == 'd'):
            posx += 10 * gameSpeed
        if(data == " "):
            RestartGame()
            
            
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()