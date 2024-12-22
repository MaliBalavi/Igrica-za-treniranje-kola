
import math
from Classes import Line, Level, Car
import pygame.surfarray as surfarray
import pygame
import cv2
import pickle
import os
file_root="levels/"
file_ext = ".pkl"
bias=0

BACKGROUND_COLOR =([0,0,0])                #Please enter level's background color,not(255,255,255) and (0,255,0), that values are used for walls and checkpoints
width = 2000                               #Please enter level's width
height =  1200                              #Please enter level's height
FPS =  60                                  #Please enter level's FPS (60 recommended)
g=  9.81                                   #Please enter level's g (9.81 recommended)




for i in range(10,11):
        
        # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Continuous Line Drawing with Snap")

    # Initialize variables
    running = True
    lines = []  # Array to store Line objects
    checkpoints=[]
    is_drawing = False
    start_pos = None
    continuous_mode = False  # Toggle for continuous line drawing
    snap_distance = 15  # Distance threshold for snapping

    def snap_to_point(pos, points, threshold):
        for point in points:
            dist = math.hypot(pos[0] - point[0], pos[1] - point[1])
            if dist <= threshold:
                return point
        return pos

    # Main loop
    while running:
        for event in pygame.event.get():
            # Toggle continuous drawing mode with N key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    continuous_mode = not continuous_mode
                    if not continuous_mode:
                        is_drawing = False  # Stop drawing if leaving continuous mode
                if event.key==pygame.K_q:
                    running = False

            # Mouse button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if not is_drawing:
                        # Start drawing a new line
                        is_drawing = True
                        start_pos = event.pos
                        # Snap start position to existing endpoints
                        endpoints = [(line.x1, line.y1) for line in lines] + [(line.x2, line.y2) for line in lines]
                        start_pos = snap_to_point(start_pos, endpoints, snap_distance)
                    else:
                        # Draw a new line segment
                        end_pos = event.pos
                        # Snap end position to existing endpoints
                        endpoints = [(line.x1, line.y1) for line in lines] + [(line.x2, line.y2) for line in lines]
                        end_pos = snap_to_point(end_pos, endpoints, snap_distance)

                        # Create and store the new line
                        line = Line(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                        lines.append(line)

                        # Update start_pos for the next segment
                        if continuous_mode:
                            start_pos = end_pos
                        else:
                            is_drawing = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw all lines
        for line in lines:
            line.draw(screen,([255,255,255]))

        # Draw the currently drawn line (preview)
        if is_drawing and not continuous_mode and start_pos:
            current_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (200, 200, 200), start_pos, current_pos)

        # Update display
        pygame.display.flip()

    x1=0
    y1=0
    x2=0
    y2=0

    click_count = 0
    coords = []
    running=True
    
    
    
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse click handling
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    coords.append(event.pos)
                    click_count += 1

                    # Display selected coordinate
                    print(f"Selected coordinate {click_count}: {event.pos}")

                    # Stop if two points are selected
                    if click_count == 2:
                        running = False

        # # Clear screen and display instructions
        # font = pygame.font.Font(None, 36)
        # if click_count == 0:
        #     text = font.render("Click to select the first coordinate.", True, (255, 255, 255))
        # elif click_count == 1:
        #     text = font.render("Click to select the second coordinate.", True, (255, 255, 255))
        # else:
        #     text = font.render("Selection complete!", True, (255, 255, 255))
        # screen.blit(text, (50, 50))

        # Draw selected points
        for coord in coords:
            pygame.draw.circle(screen, (255, 0, 0), coord, 5)

        # Update display
        pygame.display.flip()


    if len(coords) == 2:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        print(f"x1, y1 = {x1}, {y1}")
        print(f"x2, y2 = {x2}, {y2}")
    else:
        print("Insufficient coordinates selected.")
    ori = math.atan2(y2-y1, x2-x1)




    continuous_mode=False
    car=Car(5,15,10,([100,200,255]),1000,10,(x1,y1,ori),5)
    running = True
    is_drawing = False
    while running:
        for event in pygame.event.get():
            # Toggle continuous drawing mode with N key
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    running = False

            # Mouse button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if not is_drawing:
                        # Start drawing a new line
                        is_drawing = True
                        start_pos = event.pos
                        # Snap start position to existing endpoints
                        endpoints = [(line.x1, line.y1) for line in checkpoints] + [(line.x2, line.y2) for line in checkpoints]
                        start_pos = snap_to_point(start_pos, endpoints, snap_distance)
                    else:
                        # Draw a new line segment
                        end_pos = event.pos
                        # Snap end position to existing endpoints
                        endpoints = [(line.x1, line.y1) for line in checkpoints] + [(line.x2, line.y2) for line in checkpoints]
                        end_pos = snap_to_point(end_pos, endpoints, snap_distance)

                        # Create and store the new line
                        line = Line(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                        checkpoints.append(line)

                        
                        is_drawing = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw all checkpoints
        for line in lines:
            line.draw(screen,([255,255,255]))
        for line in checkpoints:
            line.draw(screen,([0,255,0]))
        car.show(screen)
        

        # Draw the currently drawn line (preview)
        if is_drawing and not continuous_mode and start_pos:
            current_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (200, 200, 200), start_pos, current_pos)

        # Update display
        pygame.display.flip()













    # Quit Pygame
    pygame.quit()





    
    file_path=file_root+str(bias+i)+file_ext
    
    
    level =Level(lines,checkpoints,BACKGROUND_COLOR,(width,height),FPS,g,(x1,y1,ori))
    with open(file_path, 'wb') as f:
        pickle.dump(level, f)





#mozda ipak zelim sliku