import pygame
import cv2
import numpy as np

# Khởi tạo màn hình game(creat a screen game)
pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rắn săn mồi")

# Khởi tạo các biến cần thiết
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [300, 300]
food_spawned = False
direction = "RIGHT"
change_to = direction
score = 0

# Khởi tạo các hàm cần thiết
def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

def move_snake(snake_pos, snake_body, direction):
    if direction == "RIGHT":
        snake_pos[0] += 10
    elif direction == "LEFT":
        snake_pos[0] -= 10
    elif direction == "UP":
        snake_pos[1] -= 10
    elif direction == "DOWN":
        snake_pos[1] += 10
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        return 1
    else:
        snake_body.pop()
        return 0

def spawn_food(food_spawned, food_pos):
    if not food_spawned:
        food_pos[0] = np.random.randint(0, (width-10)//10)*10
        food_pos[1] = np.random.randint(0, (height-10)//10)*10
        food_spawned = True
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    return food_spawned, food_pos

def check_collision(snake_pos, snake_body):
    if snake_pos[0] < 0 or snake_pos[0] > width-10:
        return 1
    elif snake_pos[1] < 0 or snake_pos[1] > height-10:
        return 1
    for block in snake_body[1:]:
        if snake_pos == block:
            return 1
    return 0

def show_score(score):
    font = pygame.font.SysFont('Arial', 20)
    score_surface = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def process_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        if w > h:
            return "RIGHT"
        else:
            return "DOWN"
    else:
        return direction

# Vòng lặp chính của game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"

    # Xử lý hướng di chuyển của rắn
    direction = change_to

    # Xử lý di chuyển của rắn
    eaten = move_snake(snake_pos, snake_body, direction)
    if eaten:
        food_spawned = False
        score += 1

    # Vẽ các đối tượng trên màn hình
    screen.fill((0, 0, 0))
    draw_snake(snake_body)
    food_spawned, food_pos = spawn_food(food_spawned, food_pos)
    show_score(score)

    # Kiểm tra va chạm
    if check_collision(snake_pos, snake_body):
        pygame.quit()
        quit()

    # Xử lý hướng di chuyển của rắn dựa trên hình ảnh từ camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        direction = process_image(frame)
    cap.release()

    # Cập nhật màn hình
    pygame.display.update()
