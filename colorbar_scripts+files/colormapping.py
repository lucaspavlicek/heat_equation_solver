import sys
import os
import numpy as np
import matplotlib.pyplot as plt

data = []
with open("ciexyz31_1.csv") as file:
    for line in file:
        data.append(line.strip().split(',')[1:])

array = np.array(data, dtype=np.float32)

numbins = 100
minn = 78
maxx = 264
addconstant = 80

indices = np.linspace(minn, maxx, numbins, dtype=int)

table = []


for i in range(numbins):
    #matrix from https://www.cs.rit.edu/~ncs/color/t_convert.html#RGB%20to%20XYZ%20&%20XYZ%20to%20RGB
    matrix = np.array([
        [3.240479, -1.53715, -0.498535],
        [-0.969256,  1.875992,  0.041556],
        [0.055648, -0.204043,  1.057311]
    ])
    
    #scale chosen by guess and check
    rgb = list(np.clip(np.int32(256*matrix.dot(array[indices[i]]))+addconstant, 0, 255))
    rgb.append(i)
    table.append(rgb)

#check that there are no repeats
#this is critical so that converting temperature to color is invertable
for i in range(len(table)):
   for j in range(len(table)):
      if i < j and table[i][:3] == table[j][:3]:
         print('Repeat found in rows: ', i, j)
         #sys.exit()

#write output file
with open('colortable.csv', 'w') as file:
    for line in table:
        if line[3] < 99:
            file.write(f"{str(line[0])},{str(line[1])},{str(line[2])},{str(line[3])}\n")
        else:
            file.write(f"{str(line[0])},{str(line[1])},{str(line[2])},{str(line[3])}")

image = np.zeros((50, 500, 3), dtype=int)
for i in range(100):
    image[:, 5*i:5*(i+1), 0] = table[i][0]
    image[:, 5*i:5*(i+1), 1] = table[i][1]
    image[:, 5*i:5*(i+1), 2] = table[i][2]

fig, ax = plt.subplots(1, figsize=(5, 1))
fig.subplots_adjust(0.02,0.4,0.98,1)

ax.set_xticks([0, 499], [0, 99])
ax.imshow(image)
ax.yaxis.set_visible(False)

ax.set_xlabel('Temperature')

fig.savefig('colorbar.png')
plt.show()