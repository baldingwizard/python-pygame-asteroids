#!/usr/bin/python

import pygame
import math
import random

pygame.init()

screensize = screenwidth, screenheight = 800, 600

screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()

# Valid states : titles, game-on, gameover, quit
gamestate = 'title'
gamestatepercent = 0.0
gamelevel = 7
lives = 0
score = 0
debugmode = False

#-------------------------------------------------------------------------------
def load_explosion_frames():

	global explosionframes

	explosion_spritesheet = pygame.image.load("images/explosion_4x5_alpha.png").convert_alpha()
	explosion_spritesheetwidth = explosion_spritesheet.get_width()
	explosion_spritesheetheight = explosion_spritesheet.get_height()
	explosionwidth = explosion_spritesheetwidth / 4
	explosionheight = explosion_spritesheetheight / 5
	for y in range(0,4):
		for x in range(0,3):
			rect = (x*explosionwidth, y*explosionheight, explosionwidth, explosionheight)
			explosionframes.append(explosion_spritesheet.subsurface(rect))

#-------------------------------------------------------------------------------

def load_powerup_frames():

	global powerupimages

	powerup_source_image = pygame.image.load("images/powerup.png").convert_alpha()

	# Create frames for powerup - combine source image, rotated and scaled
	for rotation in range(0,44,2):
		tmpimage1 = pygame.transform.rotozoom(powerup_source_image, rotation, 1.0)
		tmpimage2 = pygame.transform.rotozoom(powerup_source_image, -rotation, 0.9)

		#paste tmpimage2 over tmpimage1
		tmpimage1.blit(tmpimage2, ((tmpimage1.get_width()-tmpimage2.get_width())/2,(tmpimage1.get_height()-tmpimage2.get_height())/2));

		powerupimages.append(tmpimage1);
#-------------------------------------------------------------------------------

def load_asteroid_frames():

	global asteroidimages

	for x in range(1,59):
		asteroidimages.append(pygame.image.load("images/asteroid/"+str(x).zfill(4)+".png").convert_alpha())

#-------------------------------------------------------------------------------
def process_asteroids():

	global asteroids, asteroidimages, screenwidth, screenheight

	for asteroid in asteroids:
		asteroidimage = pygame.transform.rotozoom(asteroidimages[asteroid['frame']], asteroid['angle'], asteroid['scale'])
		asteroidimagewidth = asteroidimage.get_width()
		asteroidimageheight = asteroidimage.get_height()

		#Draw image
		screen.blit(asteroidimage, (asteroid['x']-asteroidimagewidth/2,asteroid['y']-asteroidimageheight/2))

		#If close to the edge then also draw at opposite edge for wrap
		if asteroid['x'] < asteroidimagewidth/2:
			screen.blit(asteroidimage, (asteroid['x']-asteroidimagewidth/2+screenwidth,asteroid['y']-asteroidimageheight/2))
		if asteroid['x'] > (screenwidth-asteroidimagewidth/2):
			screen.blit(asteroidimage, (asteroid['x']-asteroidimagewidth/2-screenwidth,asteroid['y']-asteroidimageheight/2))
		if asteroid['y'] < asteroidimageheight/2:
			screen.blit(asteroidimage, (asteroid['x']-asteroidimagewidth/2,asteroid['y']-asteroidimageheight/2+screenheight))
		if asteroid['y'] > (screenheight-asteroidimageheight/2):
			screen.blit(asteroidimage, (asteroid['x']-asteroidimagewidth/2,asteroid['y']-asteroidimageheight/2-screenheight))

		asteroid['x'] += asteroid['dx']
		if asteroid['x'] < 0:
			asteroid['x'] = screenwidth
		if asteroid['x'] > screenwidth:
			asteroid['x'] = 0

		asteroid['y'] += asteroid['dy']
		if asteroid['y'] < 0:
			asteroid['y'] = screenheight
		if asteroid['y'] > screenheight:
			asteroid['y'] = 0

		asteroid['frame'] += 1
		if asteroid['frame'] >= len(asteroidimages):
			asteroid['frame'] = 0

#-------------------------------------------------------------------------------
def process_powerups():

	global powerups, powerupimages, screenwidth, screenheight

	for powerup in powerups:
		powerupimage = pygame.transform.rotozoom(powerupimages[powerup['frame']], 0, powerup['scale'])
		powerupimagewidth = powerupimage.get_width()
		powerupimageheight = powerupimage.get_height()

		#Draw image
		screen.blit(powerupimage, (powerup['x']-powerupimagewidth/2,powerup['y']-powerupimageheight/2))

		#If close to the edge then also draw at opposite edge for wrap
		if powerup['x'] < powerupimagewidth/2:
			screen.blit(powerupimage, (powerup['x']-powerupimagewidth/2+screenwidth,powerup['y']-powerupimageheight/2))
		if powerup['x'] > (screenwidth-powerupimagewidth/2):
			screen.blit(powerupimage, (powerup['x']-powerupimagewidth/2-screenwidth,powerup['y']-powerupimageheight/2))
		if powerup['y'] < powerupimageheight/2:
			screen.blit(powerupimage, (powerup['x']-powerupimagewidth/2,powerup['y']-powerupimageheight/2+screenheight))
		if powerup['y'] > (screenheight-powerupimageheight/2):
			screen.blit(powerupimage, (powerup['x']-powerupimagewidth/2,powerup['y']-powerupimageheight/2-screenheight))

		powerup['x'] += powerup['dx']
		if powerup['x'] < 0:
			powerup['x'] = screenwidth
		if powerup['x'] > screenwidth:
			powerup['x'] = 0

		powerup['y'] += powerup['dy']
		if powerup['y'] < 0:
			powerup['y'] = screenheight
		if powerup['y'] > screenheight:
			powerup['y'] = 0

		powerup['frame'] += 1
		if powerup['frame'] >= len(powerupimages):
			powerup['frame'] = 0

#-------------------------------------------------------------------------------
def process_bullets():

	global bullets, asteroids, explosions, playership, screenwidth, screenheight, score
	for bullet in bullets[:]:
		#Draw bullet
		pygame.draw.circle(screen, (32,32,32), (int(bullet['x']-bullet['dx']*2.0),int(bullet['y']-bullet['dy']*2.0)), 1)
		pygame.draw.circle(screen, (64,64,64), (int(bullet['x']-bullet['dx']*1.5),int(bullet['y']-bullet['dy']*1.5)), 1)
		pygame.draw.circle(screen, (96,96,96), (int(bullet['x']-bullet['dx']*1.0),int(bullet['y']-bullet['dy']*1.0)), 2)
		pygame.draw.circle(screen, (128,128,128), (int(bullet['x']-bullet['dx']*0.5),int(bullet['y']-bullet['dy']*0.5)), 2)
		pygame.draw.circle(screen, (192,192,192), (int(bullet['x']),int(bullet['y'])), 3)

		bullet['x'] += bullet['dx']
		if bullet['x'] < 0:
			bullet['x'] = screenwidth
		if bullet['x'] > screenwidth:
			bullet['x'] = 0

		bullet['y'] += bullet['dy']
		if bullet['y'] < 0:
			bullet['y'] = screenheight
		if bullet['y'] > screenheight:
			bullet['y'] = 0

		# Collision
		for asteroid in asteroids[:]:
			d2 = math.pow(bullet['x'] - asteroid['x'],2) + math.pow(bullet['y'] - asteroid['y'],2)
			if d2 < math.pow(40 * asteroid['scale'],2):
				score += 100
				bullet['life'] = 0
				asteroids.remove(asteroid)
				if asteroid['scale'] > 0.3:
					split_asteroid(asteroid, bullet['dx'], bullet['dy'])
				explosions.append({'x':bullet['x'], 'y':bullet['y'], 'frame': 0.0, 'scale': asteroid['scale']/2})

		bullet['life'] -= 1
		if bullet['life'] <= 0:
			bullets.remove(bullet)

#-------------------------------------------------------------------------------
def process_explosions():

	global explosions, fragments

	for explosion in explosions[:]:

		if explosion['frame'] >= 0:
			explosionimage = pygame.transform.rotozoom(explosionframes[int(explosion['frame'])], 0, explosion['scale']*1.5)

			screen.blit(explosionimage, (explosion['x']-explosionimage.get_width()/2,explosion['y']-explosionimage.get_height()/2))

		explosion['frame'] += 1.1-explosion['scale']
		if explosion['frame'] >= len(explosionframes):
			explosions.remove(explosion)

#-------------------------------------------------------------------------------
def process_fragments():

	global fragments

	for fragment in fragments[:]:
		
		pygame.draw.circle(screen, (96,96,96), (int(fragment['x']),int(fragment['y'])), 1)

		fragment['x'] += fragment['dx']
		if fragment['x'] < 0:
			fragment['x'] = screenwidth
		if fragment['x'] > screenwidth:
			fragment['x'] = 0

		fragment['y'] += fragment['dy']
		if fragment['y'] < 0:
			fragment['y'] = screenheight
		if fragment['y'] > screenheight:
			fragment['y'] = 0
		fragment['life'] -= 1
		if fragment['life'] <= 0:
			fragments.remove(fragment)

#-------------------------------------------------------------------------------
def draw_playership():

	global playership, playershipimage, lives
	
	if playership['alive']:
		playershiprotatedimage = pygame.transform.rotozoom(playershipimage, -playership['angle'],1)
		screen.blit(playershiprotatedimage, (playership['x']-playershiprotatedimage.get_width()/2, playership['y']-playershiprotatedimage.get_height()/2))

	playershiplifeimage = pygame.transform.rotozoom(playershipimage, 0, 0.3)
	for life in range(0, lives):
		screen.blit(playershiplifeimage, (screenwidth-25-life*20,0))

#-------------------------------------------------------------------------------
def playership_collisions():

	global asteroids, playership, explosions

	if playership['alive']:
		for asteroid in asteroids[:]:
			d2 = math.pow(playership['x'] - asteroid['x'],2) + math.pow(playership['y'] - asteroid['y'],2)
			if d2 < math.pow(30 + 40 * asteroid['scale'],2):
				if asteroid['scale'] > 0.3:
					split_asteroid(asteroid, (asteroid['x']-playership['x'])/5, (asteroid['y'] - playership['y'])/5)
				asteroids.remove(asteroid)
				explosions.append({'x':asteroid['x'], 'y':asteroid['y'], 'frame': 0.0, 'scale': asteroid['scale']/2})
				playership['dx'] += asteroid['dx'] * asteroid['scale']
				playership['dy'] += asteroid['dy'] * asteroid['scale']

				playership['shield'] -= asteroid['scale']/2
				if playership['shield'] < 0:
					playership['shield'] = 0
					playership_explode()

#-------------------------------------------------------------------------------
def playership_explode():

	global explosions, playership

	playership['alive'] = False

	explosions.append({'x':playership['x'], 'y':playership['y'], 'frame': 0.0, 'scale': 0.75})

	for subexplosion in range(1,20):
		explosions.append({'x':playership['x']+random.randint(-40,40), 'y':playership['y']+random.randint(-40,40), 'frame': random.randint(-20,0), 'scale': 0.15 + float(random.randint(0,30))/100})
#-------------------------------------------------------------------------------
def draw_text(textstring, xpos, ypos, align='left', size=24, colour=(255,255,255)):

	font = pygame.font.Font(None,size)
	text = font.render(textstring, 1, colour)
	if align == 'right':
		screen.blit(text, (xpos-text.get_width(), ypos))
	elif align == 'center' or align == 'centre':
		screen.blit(text, (xpos-text.get_width()/2, ypos))
	else:
		screen.blit(text, (xpos, ypos))
	
#-------------------------------------------------------------------------------
# Split an asteroid based on the vector of impact and its own motion
def split_asteroid(asteroid, dx, dy):

	global asteroids

	# Give each fragment extra momentum perpendicular to the impact and
	# also push it back a bit too
	asteroids.append({'x':asteroid['x'], 'y':asteroid['y'], 'dx':(asteroid['dx']+dy/5+dx/15/asteroid['scale']), 'dy':(asteroid['dy']-dx/5+dy/15/asteroid['scale']), 'frame':0, 'scale':asteroid['scale']*0.65, 'angle':asteroid['angle']})
	asteroids.append({'x':asteroid['x'], 'y':asteroid['y'], 'dx':(asteroid['dx']-dy/5+dx/15/asteroid['scale']), 'dy':(asteroid['dy']+dx/5+dy/15/asteroid['scale']), 'frame':0, 'scale':asteroid['scale']*0.65, 'angle':asteroid['angle']})

#-------------------------------------------------------------------------------
def process_keys():

	global playership, bullets, gamestate, debugmode, fragments

	keys = pygame.key.get_pressed()

	if gamestate == 'title':
		if keys[pygame.K_ESCAPE]:
			set_gamestate('quit')
			return True

	if gamestate == 'quit':
		if keys[pygame.K_n]:
			set_gamestate('title')
			return True

		if keys[pygame.K_y]:
			return False

	if keys[pygame.K_d]:
		debugmode = True
	else:
		debugmode = False

	if gamestate == 'title':
		if keys[pygame.K_SPACE]:
			set_gamestate('starting')

		return True

	if gamestate == 'paused':
		if keys[pygame.K_ESCAPE]:
			set_gamestate('unpausing')

		if keys[pygame.K_q]:
			set_gamestate('aborting')

		return True

	if gamestate == 'pausing':
		return True

	if gamestate == 'unpausing':
		return True

	if gamestate == 'game-on':
		if keys[pygame.K_ESCAPE]:
			set_gamestate('pausing')
			return True

		if keys[pygame.K_LEFT]:
			playership['angle'] -= 5

		if keys[pygame.K_RIGHT]:
			playership['angle'] += 5

		if keys[pygame.K_UP]:
			playership['dx'] += math.sin(math.radians(playership['angle']))/2
			playership['dy'] -= math.cos(math.radians(playership['angle']))/2
			fragments.append({'x':playership['x'] - math.sin(math.radians(playership['angle']))*32, 'y':playership['y'] + math.cos(math.radians(playership['angle']))*32, 'dx':playership['dx'] - math.sin(math.radians(playership['angle']+random.randint(-30,30)))*3, 'dy':playership['dy'] + math.cos(math.radians(playership['angle']+random.randint(-30,30)))*3 , 'life':25})

		if playership['reload'] > 0:
			playership['reload'] -= 1

		if keys[pygame.K_SPACE] and playership['reload'] <= 0 and playership['alive']:
			bullets.append({'x':playership['x'] + math.sin(math.radians(playership['angle']))*38, 'y':playership['y'] - math.cos(math.radians(playership['angle']))*38, 'dx':playership['dx'] + math.sin(math.radians(playership['angle']))*15, 'dy':playership['dy'] - math.cos(math.radians(playership['angle']))*15 , 'life':25})
			playership['reload'] = 5

		return True

	return True
#-------------------------------------------------------------------------------
def set_gamestate(state):

	global gamestate, gamestatepercent, gamelevel, lives, score, asteroids

	gamestate = state
	gamestatepercent = 0

#-------------------------------------------------------------------------------

# Load images for explosion
explosionframes = []
load_explosion_frames()

# Load images for powerups
powerupimages = []
load_powerup_frames()

# Load images for asteroid
asteroidimages = []
load_asteroid_frames()

# Lists to hold objects
asteroids = []
powerups = []
bullets = []
explosions=[]
fragments=[]

# Player ship
playership = {'x':float(screenwidth/2), 'y':float(screenheight/2), 'dx':0.0, 'dy':0.0, 'angle':0, 'reload':0, 'alive': False, 'shield': 0}
playershipimage = pygame.image.load("images/playership.png").convert_alpha()


# Game loop
while True:
	pygame.event.pump()

	if not process_keys():
		break

	screen.fill((0,0,0))

	if gamestate == 'game-on' or gamestate == 'title': 
		playership['x'] += playership['dx']
		if playership['x'] < 0:
			playership['x'] = screenwidth
		if playership['x'] > screenwidth:
			playership['x'] = 0

		playership['y'] += playership['dy']
		if playership['y'] < 0:
			playership['y'] = screenheight
		if playership['y'] > screenheight:
			playership['y'] = 0

		playership['dx'] *= 0.985
		playership['dy'] *= 0.985


		process_fragments()
		#process_powerups()
		process_asteroids()
		process_bullets()

	if gamestate == 'game-on':
		draw_playership()
		playership_collisions()

	if gamestate == 'game-on' or gamestate == 'title':
		process_explosions()

	if debugmode:
		draw_text("Asteroids = "+str(len(asteroids)), 100, screenheight-80)
		draw_text("Explosions = "+str(len(explosions)), 100, screenheight-60)
		draw_text("Bullets = "+str(len(bullets)), 100, screenheight-40)
		draw_text("Fragments = "+str(len(fragments)), 100, screenheight-20)
		draw_text("Game State Percent = "+str(gamestatepercent), 300, screenheight-60)
		draw_text("Game State = "+gamestate, 300, screenheight-40)
		draw_text("Lives = "+str(lives), 300, screenheight-20)

	draw_text("Score     "+str(score), screenwidth*2/3, 0, align='centre')
	draw_text("Shield     "+str(int(playership['shield']*100))+"%", screenwidth/3, 0, align='centre')

	if gamestate == 'game-on':


		# If all asteroids have been destroyed, skip to next level
		if len(asteroids) == 0:
			
			# Give bonus of 10pts for each % of shield left
			if playership['shield'] > 0:
				playership['shield'] -= 0.01
				score += 10
			else:
				gamelevel += 1
				gamestatepercent = 0
				playership['shield'] = 1
				# Create asteroids
				for ast in range(0,gamelevel):
					maxspeed = gamelevel / 3 + 1
					if maxspeed > 3:
						maxspeed = 3
					asteroids.append({'x':float(random.randint(-100,100)), 'y':float(random.randint(-100,100)), 'dx':float(random.randint(-int(maxspeed),int(maxspeed)))+0.5, 'dy':float(random.randint(-int(maxspeed),int(maxspeed)))+0.5, 'frame':random.randint(0,10), 'scale':1.0, 'angle':random.randint(0,359)})

		if gamestatepercent < 10:
			brightness = gamestatepercent / 10
			draw_text("Level "+str(gamelevel), screenwidth/2, screenheight/2, size=48, align='centre', colour=(255*brightness, 255*brightness, 255*brightness))
			gamestatepercent += 0.2
		elif gamestatepercent < 20:
			brightness = 1.0- ((gamestatepercent-10)/10 * 0.8 )
			draw_text("Level "+str(gamelevel), screenwidth/2, screenheight/2+(screenheight/2-16)*(gamestatepercent-10)/10, size=48-int(24*(gamestatepercent-10)/10), align='centre', colour=(255*brightness, 255*brightness, 255*brightness))
			gamestatepercent += 0.5
		else:
			draw_text("Level "+str(gamelevel), screenwidth/2, screenheight-16, size=24, colour=(64,64,64),align='centre')
			
		if not playership['alive'] and len(explosions) == 0:
			if lives > 0:
				lives -= 1
				playership['x'] = float(screenwidth/2)
				playership['y'] =float(screenheight/2)
				playership['dx'] =0.0
				playership['dy'] =0.0
				playership['angle'] =0
				playership['reload'] =0
				playership['alive'] = True
				playership['shield'] = 1.0

			else:
				set_gamestate('gameover')

	if gamestate == 'gameover':
		
		gamestatepercent += 0.5
		draw_text("Game Over", screenwidth/2, screenheight/2, align='center', size=72)

		if gamestatepercent >= 100:
			set_gamestate('title')

	if gamestate == 'quit':
		gamestatepercent += 1.0

		draw_text("Really Quit? Y/N", screenwidth/2, screenheight/2, align='center', size=72)

		if gamestatepercent >= 100:
			set_gamestate('title')

	if gamestate == 'pausing':

		gamestatepercent += 5.0
		draw_text("Pausing...", screenwidth/2, screenheight/2, align='center', size=72)

		if gamestatepercent >= 100:
			set_gamestate('paused')

	if gamestate == 'unpausing':

		gamestatepercent += 5.0
		draw_text("Unpausing...", screenwidth/2, screenheight/2, align='center', size=72)

		if gamestatepercent >= 100:
			set_gamestate('game-on')

	if gamestate == 'paused':

		draw_text("Paused", screenwidth/2, screenheight/2, align='center', size=72)
		draw_text("Press Q to quit", screenwidth/2, screenheight/4*3, align='center', size=32)

	if gamestate == 'starting':
		gamelevel = 0
		lives = 3
		score = 0
		del asteroids[:]
		del powerups[:]
		del bullets[:]
		del explosions[:]

		powerups.append({'x':float(random.randint(-100,100)), 'y':float(random.randint(-100,100)), 'dx':float(random.randint(-3,3))+0.5, 'dy':float(random.randint(-3,3))+0.5, 'frame':0, 'scale':1.0})

		set_gamestate('game-on')

	if gamestate == 'aborting':
		gamelevel = 0
		lives = 0
		playership['shield'] = 0
		playership['alive'] = False

		set_gamestate('title')

	if gamestate == 'title':

		if len(asteroids) <= 4:
			asteroids.append({'x':float(0), 'y':float(0), 'dx':float(random.randint(-5,5)), 'dy':float(random.randint(-5,5)), 'frame':random.randint(0,10), 'scale':1.0, 'angle':random.randint(0,359)})

		if len(explosions) == 0:
			for asteroid in asteroids[:]:
				if random.randint(1,500) == 1:
					asteroids.remove(asteroid)
					if asteroid['scale'] > 0.3:
						split_asteroid(asteroid, random.randint(-5,5), random.randint(-5,5))
					explosions.append({'x':asteroid['x'], 'y':asteroid['y'], 'frame': 0.0, 'scale': asteroid['scale']/2})
		
		gamestatepercent += 0.5
		if gamestatepercent > 100:
			gamestatepercent = 0

		draw_text("Press SPACE to start", screenwidth/2, screenheight/2, align='center')
		draw_text("Controls", screenwidth*3/4, screenheight*3/4, align='left',colour=(196,196,196))
		draw_text("LEFT = Turn left", screenwidth*3/4, screenheight*3/4+24, align='left',colour=(128,128,128))
		draw_text("RIGHT = Turn right", screenwidth*3/4, screenheight*3/4+40, align='left',colour=(128,128,128))
		draw_text("UP = Thrust", screenwidth*3/4, screenheight*3/4+56, align='left',colour=(128,128,128))
		draw_text("SPACE = Fire", screenwidth*3/4, screenheight*3/4+72, align='left',colour=(128,128,128))

	pygame.display.flip()
	clock.tick(30)

pygame.quit()
