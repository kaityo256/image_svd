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
    A = np.asarray(img)
    rank = 10
    r = perform_svd(A[:,:,0],rank).reshape(w*h)
    g = perform_svd(A[:,:,1],rank).reshape(w*h)
    b = perform_svd(A[:,:,2],rank).reshape(w*h)
    B = np.asarray([r,g,b]).transpose(1,0).reshape(h,w,3)
    img2 = Image.fromarray(np.uint8(B))
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
