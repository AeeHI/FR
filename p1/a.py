import os
import shutil

if __name__ == '__main__':
    for j in range(100):

        place = 'D:/data/save/photo/' + str(j)
        i = 0
        for filename in os.listdir(place):
            if i>0:
                p1 = place + '/' + filename
                os.remove(p1)
            i += 1
        print(j, i)

        '''
        place1 = 'D:/a/a/' + str(j)
        place2 = 'D:/a/b/' + str(j)

        p1 = place1 + '/2.jpg'
        p2 = place2 + '/2.jpg'
        shutil.move(p1,p2)

        print(j)
        '''