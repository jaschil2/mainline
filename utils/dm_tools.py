from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import pylab as P
import matplotlib
"""The main functions you'll use here are read_dm and read_dm_offdiag.  
These take as arguments a filename, which should be the stdout of gosling as applied 
to your log file.
"""
################################################################

def plot_color(A,filename,ticklabels=None, annotate=True):
  nregion1=A.shape[0]
  nregion2=A.shape[1]
  P.clf()


  cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.5, 1.0, 1.0),
                 (1.0, 0.4, 0.4)),
         'green': ((0.0, 0.4, 0.4),
                   (0.5, 1.0, 1.0),
                   (1.0, 0.4, 0.4)),
         'blue': ((0.0, 0.4, 0.4),
                  (0.5, 1.0, 1.0),
                  (1.0, 1.0, 1.0))}
  my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
  vmax=np.max(A*100)
  vmin=np.min(A*100)
  vmax=max(-vmin,vmax)
  vmin=min(-vmax,vmin)
  #print vmax,vmin
#  P.pcolor(A*100,cmap=my_cmap,edgecolors='k',vmin=vmin,vmax=vmax,array=True)
  P.imshow(A*100,cmap=my_cmap,vmin=vmin,vmax=vmax,interpolation='nearest',origin='upper')

  thresh=0.05*(vmax-vmin)
    
  if annotate:  
    for r1 in range(0,nregion1):
      for r2 in range(0,nregion2):
        n=A[r1,r2]*100
        if abs(n) > thresh:
          P.annotate("%.1f"%(n), (r2,r1),ha="center",va="center",fontsize=2)
  a=P.gca()
  a.get_xaxis().tick_top()
  for i in ['top','right','left','bottom']:
    a.spines[i].set_visible(False)
  a.tick_params(labelsize=10,width=0)
  P.savefig(filename)

################################################################

def convert(s):
  return float(s)
  a=eval(s)
  m=float(a[0])
  for i in a:
    m=max(m,i)
  return m

################################################################


def read_dm(inpf):
  """Read in the 1-RDM and/or 1-RDM and diagonals of the 2-RDM, if only 
  the diagonals were calculated"""
  nmo=0
  while True:
    line=inpf.readline()
    if "tbdm" in line:
      spl=line.split()
      nmo=int(spl[2])
      break
    if line=="":
      return None
  data={}
  #one-body up, one-body up err,   two-body-uu, two-body-uu err
  for nm in ['ou','oue','od','ode','tuu','tuue','tud','tude','tdu','tdue','tdd','tdde']:
    data[nm]=np.zeros((nmo,nmo))
  
  while True:
    line=inpf.readline()
    if line=="" or "Trace" in line:
      break;
    if line.find("tbdm: states") != -1:
      data['states']=np.array(list(map(int,line.split()[3:-1])))
      #print data['states']
    if line.find("One-body density") != -1:
      line=inpf.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=inpf.readline().split()
          data['ou'][i,j]=convert(a[2])
          data['oue'][i,j]=convert(a[3])
          data['od'][i,j]=convert(a[4])
          data['ode'][i,j]=convert(a[5])
    if line.find("two-body density") != -1:
      line=inpf.readline()
      #print "two-body",line
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=inpf.readline().split()
          #print i,j,"a ",a
          data['tuu'][i,j]=convert(a[4])
          data['tuue'][i,j]=convert(a[5])
          data['tud'][i,j]=convert(a[6])
          data['tude'][i,j]=convert(a[7])
          data['tdu'][i,j]=convert(a[8])
          data['tdue'][i,j]=convert(a[9])
          data['tdd'][i,j]=convert(a[10])
          data['tdde'][i,j]=convert(a[11])
      break
  return data

################################################################


def read_dm_offdiag(f):
  """Read in the 1-RDM and 2-RDM, if the off-diagonal elements were calculated
    for the 2-RDM"""

  nmo=0
  while True:
    line=f.readline()
    if line.find("tbdm")!=-1:
      spl=line.split()
      nmo=int(spl[2])
      break
  data={}
  #one-body up, one-body up err,   two-body-uu, two-body-uu err
  for nm in ['ou','oue','od','ode']:
    data[nm]=np.zeros((nmo,nmo))
  for nm in ['tuu','tuue','tud','tude','tdu','tdue','tdd','tdde']:
    data[nm]=np.zeros((nmo*nmo,nmo*nmo))
  while True:
    line=f.readline()
    if line=="" or "Trace" in line:
      break;
    if line.find("tbdm: states") != -1:
      data['states']=np.array(list(map(int,line.split()[3:-1])))
    if line.find("One-body density") != -1:
      line=f.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=f.readline().split()
          data['ou'][i,j]=convert(a[2])
          data['oue'][i,j]=convert(a[3])
          data['od'][i,j]=convert(a[4])
          data['ode'][i,j]=convert(a[5])
    if line.find("two-body density") != -1:
      line=f.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          for k in range(0,nmo):
            for l in range(0,nmo):
              a=f.readline().split()
              #print i,j,"a ",a
              for n,index in zip(['tuu','tuue','tud','tude','tdu','tdue','tdd','tdde'],
                  range(4,12)):
                data[n][i*nmo+j,k*nmo+l]=convert(a[index])
      break
  return data
################################################################

def read_ekt(f):
  data={}
  while True:
    line=f.readline()
    if 'EKT' in line:
      data['nmo']=int(line.split()[2])
      break

  line=f.readline()
  data['states']=np.array(list(map(int,line.split()[3:-1])))
  print(data['states'],data['nmo'])
  nmo=data['nmo']
  for el in ['ou','oue','od','ode','vu','vue','vd','vde','cu','cue','cd','cde']:
    data[el]=np.zeros((data['nmo'],data['nmo']))
  while True:
    line=f.readline()
    if 'One-body density matrix' in line:
      f.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=f.readline().split()
          data['ou'][i,j]=convert(a[2])
          data['oue'][i,j]=convert(a[3])
          data['od'][i,j]=convert(a[4])
          data['ode'][i,j]=convert(a[5])
      
    if 'Valence band matrix' in line:
      f.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=f.readline().split()
          data['vu'][i,j]=convert(a[2])
          data['vue'][i,j]=convert(a[3])
          data['vd'][i,j]=convert(a[4])
          data['vde'][i,j]=convert(a[5])
    if 'Conduction band matrix' in line:
      f.readline()
      for i in range(0,nmo):
        for j in range(0,nmo):
          a=f.readline().split()
          data['cu'][i,j]=convert(a[2])
          data['cue'][i,j]=convert(a[3])
          data['cd'][i,j]=convert(a[4])
          data['cde'][i,j]=convert(a[5])
    if line=="" or "Trace" in line:
      break
  return data


################################################################

def clean_zeros(A,Ae,nsigma=4):
  A[np.abs(A-Ae) < nsigma*Ae]=0.0

################################################################

def calc_entropy(a):
  e=0.0
  tiny=1e-12
  n=int(np.sum(a)+0.5)
  for x in a:
    if abs(x) > tiny:
      e-=x*np.log(x)
  return e/float(n)

################################################################


def gen_excitation(exc,occ):
  ex=[]
  for o in occ:
    found=False
    for e in exc:
      if o==e[0]:
        ex.append(e[1])
        found=True
        break
    if not found:
      ex.append(o)
  return ex

################################################################


def _blob(x,y,area,colour):
    """
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates.
    """
    hs = np.sqrt(area) / 2
    xcorners = np.array([x - hs, x + hs, x + hs, x - hs])
    ycorners = np.array([y - hs, y - hs, y + hs, y + hs])
    P.fill(xcorners, ycorners, colour, edgecolor=colour)
################################################################

def hinton(W,filename="hinton.pdf", maxWeight=None):
    """
    Draws a Hinton diagram for visualizing a weight matrix. 
    Temporarily disables matplotlib interactive mode if it is on, 
    otherwise this takes forever.
    """
    reenable = False
    if P.isinteractive():
        P.ioff()
    P.clf()
    ax=P.subplot(111)
    height, width = W.shape
    if not maxWeight:
        maxWeight = 2**np.ceil(np.log(np.max(np.abs(W)))/np.log(2))

    P.fill(np.array([0,width,width,0]),np.array([0,0,height,height]),'gray')
    P.axis('off')
    #P.axis('equal')
    ax.set_yticklabels(['25','20','15','10','5','0'])
    for x in xrange(width):
        for y in xrange(height):
            _x = x+1
            _y = y+1
            w = W[y,x]
            if w > 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,w/maxWeight),'white')
            elif w < 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,-w/maxWeight),'black')
    if reenable:
        P.ion()
    P.title(filename)
    P.savefig(filename)
   # P.show()
################################################################


