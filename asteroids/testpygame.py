import pygame

pygame.init()

screenwidth = 800
screenheight = 600

screen = pygame.display.set_mode((screenwidth,screenheight))

clock = pygame.time.Clock()

# Initialize stuff (replace with your own code)
frame = 0
circleheight = 400

# Main game loop
while True:
    pygame.event.pump()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        break

    if keys[pygame.K_UP]:
        circleheight = circleheight - 1
    elif keys[pygame.K_DOWN]:
        circleheight = circleheight + 1

    # Blank out the old frame
    screen.fill((0,0,0))

    # Draw the new frame (replace with your own code)
    frame += 1
    pygame.draw.circle(screen,(192,128,64),(frame % 800,circleheight),30)

    # Display frame
    pygame.display.flip()

    # Wait for next frame
    clock.tick(30)

pygame.quit()
