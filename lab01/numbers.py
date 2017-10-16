from pico2d import *

image = None

def draw(number, x, y, scale = 1):
	global image
	if image == None:
		image = load_image('numbers.png')
	dx = 40 * scale
	dy = 64 * scale
	while (True):
		digit = number % 10
		sx = digit * 40
		image.clip_draw(sx, 0, 40, 64, x, y, dx, dy)
		number = int(number / 10)
		if number == 0:
			break
		x -= dx

