from PIL import Image
import os
import sys
import numpy as np
from scipy import linalg

def perform_svd(a,rank):
    u, s, v = linalg.svd(a)
    ur = u[:, :rank]
    sr = np.matrix(linalg.diagsvd(s[:rank], rank,rank))
    vr = v[:rank, :]
    return np.asarray(ur*sr*vr)

def mono(filename,rank):
    path, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w = img.width
    h = img.height
    gray_img = img.convert('L')
    gray_img.save(path + '_mono.jpg')
    a = np.asarray(gray_img)
    b = perform_svd(a,rank)
    img2 = Image.fromarray(np.uint8(b))
    file = path+'_r' + str(rank) + '_mono' + ext
    img2.save(file)
    print('Saved as ' + file)

def color(filename,rank):
    path, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w = img.width
    h = img.height
    data = img.getdata()
    rdata = [data[i][0] for i in range(w*h)]
    gdata = [data[i][1] for i in range(w*h)]
    bdata = [data[i][2] for i in range(w*h)]

    r = np.asarray(rdata)
    g = np.asarray(gdata)
    b = np.asarray(bdata)

    r = r.reshape((w,h))
    g = g.reshape((w,h))
    b = b.reshape((w,h))

    r = perform_svd(r,rank)
    g = perform_svd(g,rank)
    b = perform_svd(b,rank)

    r = r.reshape(h*w)
    g = g.reshape(h*w)
    b = b.reshape(h*w)
    
    data = [[(r[x+y*w],g[x+y*w],b[x+y*w]) for x in range(w)] for y in range(h)]
    img2 = Image.fromarray(np.uint8(data))
    file = path+'_r' + str(rank) + ext
    img2.save(file)
    print('Saved as ' + file)

def main():
    rank = 10
    argc = len(sys.argv)
    if (argc <2):
        print("usage:")
        print("$ python %s filename rank" % sys.argv[0])
        return
    filename = sys.argv[1]
    if (os.path.exists(filename) == False):
        print ("File is not found: %s" % filename)
        return

    if (argc >2):
        rank = int(sys.argv[2])

    mono(filename,rank)
    color(filename,rank)

if __name__ == '__main__':
        main()
