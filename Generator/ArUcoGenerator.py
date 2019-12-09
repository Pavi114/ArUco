import numpy as np

MIN_SIZE = 50


class ArUcoGenerator:

    def __init__(self, size_of_marker, thickness=50):
        self.id = -1
        self.marker_size = size_of_marker
        self.thickness_border = thickness
        self.image = np.zeros((size_of_marker, size_of_marker), dtype=int)
        self.b_id = []
        self.dictionary_size = 5
        self.width = int(size_of_marker / self.dictionary_size)

    def d2b_convert(self):
        id = self.id
        b_id = []
        while id > 0:
            b_id.append(id % 2)
            id = id // 2
        b_id.reverse()
        while len(b_id) < 10:
            b_id.append(0)
        return b_id

    def draw_row(self, row, d1, d2):
        p1 = d1 ^ d2
        p2 = not d1
        p3 = d2
        if p2 == 1:
            self.image[row * self.width: row * self.width + self.width, 0:self.width] = 255
        if d1 == 1:
            self.image[row * self.width: row * self.width + self.width, self.width: 2 * self.width] = 255
        if p3 == 1:
            self.image[row * self.width: row * self.width + self.width, 2 * self.width: 3 * self.width] = 255
        if d2 == 1:
            self.image[row * self.width: row * self.width + self.width, 3 * self.width: 4 * self.width] = 255
        if p1 == 1:
            self.image[row * self.width: row * self.width + self.width, 4 * self.width: 5 * self.width] = 255

        return self.image

    def add_padding(self):
        padding_image = np.zeros((self.marker_size + 2 * self.thickness_border, self.marker_size + 2 * self.thickness_border))
        padding_image[self.thickness_border:-self.thickness_border, self.thickness_border: -self.thickness_border] = self.image
        return padding_image

    def draw_marker(self, id):

        if id > 1024:
            print("ID out of range!")
            exit()
        if self.marker_size < MIN_SIZE:
            print("Out of bound size of marker")
            exit()

        self.id = id
        self.b_id = self.d2b_convert()
        row = 0
        for index in range(0, 2 * self.dictionary_size - 1, 2):
            d1 = self.b_id[index]
            index += 1
            d2 = self.b_id[index]
            self.image = self.draw_row(row, d1, d2)
            row += 1

        self.image = self.add_padding()
        return self

