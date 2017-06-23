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
    X = np.asarray(img)
    r = perform_svd(X[:,:,0],rank).reshape(w*h)
    g = perform_svd(X[:,:,1],rank).reshape(w*h)
    b = perform_svd(X[:,:,2],rank).reshape(w*h)
    B = np.asarray([r,g,b]).transpose(1,0).reshape(h,w,3)
    img2 = Image.fromarray(np.uint8(B))
    file = path+'_r' + str(rank) + ext
    img2.save(file)
    print('Saved as ' + file)

def color_tucker(filename,rank):
    path, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w = img.width
    h = img.height
    X = np.asarray(img)
    X1 =  X.transpose(0,2,1).reshape(h*3,w)
    X2 = X.transpose(1,2,0).reshape(w*3,h)
    U,s,A1 = linalg.svd(X1)
    U,s,A2 = linalg.svd(X2)
    r2 = rank*3
    a1 = A1[:r2, :]
    a2 = A2[:r2, :]
    pa1 = a1.T.dot(a1)
    pa2 = a2.T.dot(a2)
    X2 = np.tensordot(X,pa1,(1,0))
    X3 = np.tensordot(X2,pa2,(0,0))
    X4 = X3.transpose(2,1,0)
    img2 = Image.fromarray(np.uint8(X4))
    file = path+'_t' + str(rank) + ext
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
    color_tucker(filename,rank)


if __name__ == '__main__':
    main()
