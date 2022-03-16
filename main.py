import PIL
from PIL import Image,ImageOps
import numpy as np
import matplotlib.pyplot as plt
import cv2

def make_image(data,resolution):
  img=Image.new('RGB',resolution)
  img.putdata(data)
  return img

def encode(img_cover,img_secret,n_bits):
  w,h=img_secret.size
  wc,hc=img_cover.size
  ran=int(8/n_bits)
  lim=int(8-n_bits)
  cover=img_cover.load()
  secret=img_secret.load()
  data=[]
  count=0
  p=0
  i=0
  j=0
  q=0
  for y in range(h):
    for x in range(w):
      value=secret[x,y]
      rs='{0:08b}'.format(value[0])
      gs='{0:08b}'.format(value[1])
      bs='{0:08b}'.format(value[2])
      p=0
      for q in range(ran):
        val=cover[i,j]
        rc='{0:08b}'.format(val[0])
        gc='{0:08b}'.format(val[1])
        bc='{0:08b}'.format(val[2])
        #print(val)
        rc=rc[0:lim]+rs[p:p+n_bits]
        gc=gc[0:lim]+gs[p:p+n_bits]
        bc=bc[0:lim]+bs[p:p+n_bits]
        int_r=int(rc,2)
        int_g=int(gc,2)
        int_b=int(bc,2)
        p+=n_bits
        #print((int_r,int_g,int_b))
        data.append((int_r,int_g,int_b))
        if(i==(wc-1)):
          i=0
          j+=1
        else:
          i+=1
  count=len(data)
  remain_height=j
  if(i!=0):
    remain_height=j+1
    for x in range(i,wc):
      val=cover[x,j]
      rc=val[0]
      gc=val[1]
      bc=val[2]
      data.append((rc,gc,bc))
  for y in range(remain_height,hc):
    for x in range(wc):
      val=cover[x,y]
      rc=val[0]
      gc=val[1]
      bc=val[2]
      data.append((rc,gc,bc))
  img=make_image(data,img_cover.size)
  return (img,count,(w,h))

def decode(encoded_img,resolution,n_bits,size):
  w,h=encoded_img.size
  encoded=encoded_img.load()
  data=[]
  lim=8-n_bits
  r=''
  g=''
  b=''
  i=0
  x=0
  y=0
  while(i<resolution):
    value=encoded[x,y]
    re='{0:08b}'.format(value[0])
    ge='{0:08b}'.format(value[1])
    be='{0:08b}'.format(value[2])
    r=r+re[lim:8]
    g=g+ge[lim:8]
    b=b+be[lim:8]
    if(len(r)==8):
      int_r=int(r,2)
      int_g=int(g,2)
      int_b=int(b,2)
      data.append((int_r,int_g,int_b))
      r=''
      g=''
      b=''
    if(x==(w-1)):
      x=0
      y+=1
    else:
      x+=1
    i+=1
  return make_image(data,(size))
###########################
#loading the images
img_secret=Image.open('Resources/5.jpg')
img_cover=Image.open('Resources/f.jpg')
ws,hs=img_secret.size
wc,hc=img_cover.size
print('Secret img size',img_secret.size)
print('Cover img size',img_cover.size)
###########################
#calling the functions
n_bits=1 #no. of lsb to be replaced in cover image
pixel=int(8/n_bits)
if((ws*hs*pixel)<(wc*hc)):
  encoded_img,count,size=encode(img_cover,img_secret,n_bits)
  decoded_img=decode(encoded_img,count,n_bits,size)
  ###########################
  # Plotting the images with their respective histograms
  c = np.array(img_cover)
  c = c[:, :, ::-1].copy()
  c=cv2.cvtColor(c,cv2.COLOR_BGR2GRAY)
  histc,bin_edgesc=np.histogram(c.flatten(),256,[0,256])
  e = np.array(encoded_img)
  e = e[:, :, ::-1].copy()
  e=cv2.cvtColor(e,cv2.COLOR_BGR2GRAY)
  s = np.array(img_secret)
  s = s[:, :, ::-1].copy()
  s=cv2.cvtColor(s,cv2.COLOR_BGR2GRAY)
  d = np.array(decoded_img)
  d = d[:, :, ::-1].copy()
  d=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
  histc,bin_edges_c=np.histogram(c.flatten(),256,[0,256])
  histe,bin_edges_e=np.histogram(e.flatten(),256,[0,256])
  hists,bin_edges_s=np.histogram(s.flatten(),256,[0,256])
  histd,bin_edges_d=np.histogram(d.flatten(),256,[0,256])
  fig = plt.figure(figsize=(21,8))
  ax1 = fig.add_subplot(241)
  ax1.imshow(img_cover)
  ax1.title.set_text('Cover Image')
  ax2=fig.add_subplot(242)
  ax2.plot(histc)
  ax2.title.set_text('histogram')
  ax3 = fig.add_subplot(243)
  ax3.imshow(img_secret)
  ax3.title.set_text('Secret Image')
  ax2=fig.add_subplot(244)
  ax2.plot(hists)
  ax2.title.set_text('histogram')
  ax5 = fig.add_subplot(245)
  ax5.imshow(encoded_img)
  ax5.title.set_text('Encoded Image')
  ax6=fig.add_subplot(246)
  ax6.plot(histe)
  ax6.title.set_text('histogram')
  ax7 = fig.add_subplot(247)
  ax7.imshow(decoded_img)
  ax7.title.set_text('Decoded Image')
  ax8=fig.add_subplot(248)
  ax8.plot(histd)
  ax8.title.set_text('histogram')
  plt.subplots_adjust(left=0.1,
                      bottom=0.1,
                      right=0.9,
                      top=0.9,
                      wspace=0.4,
                      hspace=0.4)
  plt.show()
else:
  print('Secret image is not small enough to be hidden in cover image')