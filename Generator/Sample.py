import matplotlib.pyplot as plt
from ArUcoGenerator import ArUcoGenerator

while (True):
    id = int(input("Enter id:"))

    if id >= 1024:
        print("Enter value btwn 0-1023")
    else:
        aruco = ArUcoGenerator(400)
        aruco = aruco.draw_marker(id)
        image = aruco.image
        plt.imshow(image, 'gray')
        plt.xticks([])
        plt.yticks([])
        plt.savefig('Samples/'+ str(id) + '.png')
        exit()
