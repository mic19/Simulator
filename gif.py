import imageio


images = []
gif_data = ['output/test' + str(i) + '.png' for i in range(600, 700)]

for filename in gif_data:
	images.append(imageio.imread(filename))
	imageio.mimsave('output/b.gif', images)
