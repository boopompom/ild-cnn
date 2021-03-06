# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:48:43 2017

@author: sylvain
tool for roi generation
"""

# import the necessary packages
import numpy as np
import cv2
import os
import dicom
import time

source_name='source'
pattern=''
typei='bmp'
scan_bmp='scan_bmp'
imageDepth=255

quitl=False
images={}
tabroi={}
tabroifinal={}
tabroinumber={}
path_patient='path_patient'

classif ={
        'back_ground':0,
        'consolidation':1,
        'HC':2,
        'ground_glass':3,
        'healthy':4,
        'micronodules':5,
        'reticulation':6,
        'air_trapping':7,
        'cysts':8,
        'bronchiectasis':9,
        'emphysema':10,
        'GGpret':11
        }

black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
cyan=(0,255,255)
purple=(255,0,255)
white=(255,255,255)
darkgreen=(11,123,96)
pink =(255,128,255)
lightgreen=(125,237,125)
orange=(255,153,102)
lowgreen=(0,51,51)
parme=(234,136,222)
chatain=(139,108,66)



classifc ={
    'back_ground':darkgreen,
    'consolidation':cyan,
    'HC':blue,
    'ground_glass':red,
    'healthy':darkgreen,
    'micronodules':green,
    'reticulation':yellow,
    'air_trapping':pink,
    'cysts':lightgreen,
    'bronchiectasis':orange,
    'emphysema':chatain,
    'GGpret': parme,



     'nolung': lowgreen,
     'bronchial_wall_thickening':white,
     'early_fibrosis':white,

     'increased_attenuation':white,
     'macronodules':white,
     'pcp':white,
     'peripheral_micronodules':white,
     'tuberculosis':white
 }

def remove_folder(path):
    """to remove folder"""
    # check if folder exists
    if os.path.exists(path):
         print 'remove folder'
         print path
         l =os.listdir(path)
         for i in l:
             os.remove(os.path.join(path,i))
         os.rmdir(path)
#         shutil.rmtree(path,ignore_errors=True)


def contour3(vis,im,l,dimtabx,dimtaby):  
    col=classifc[l]
    visi = np.zeros((dimtabx,dimtaby,3), np.uint8)
    vis2= np.zeros((dimtabx,dimtaby,3), np.uint8)
    imagemax= cv2.countNonZero(np.array(im))    
    if imagemax>0:
        mgray = cv2.cvtColor(vis,cv2.COLOR_BGR2GRAY)
        np.putmask(mgray,mgray>0,255)
        nthresh=cv2.bitwise_not(mgray)
       
        cv2.fillPoly(visi, [np.array(im)],col)
        vis1=cv2.bitwise_and(visi,visi,mask=nthresh)
        vis2=cv2.add(vis,vis1)


    return vis2


def click_and_crop(event, x, y, flags, param):
    global quitl,pattern
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(menus, (150,12), (370,32), black, -1)
        posrc=0
        print x,y
        for key1 in classif:
            labelfound=False            
            xr=5
            yr=15*posrc
            xrn=xr+10
            yrn=yr+10
            if x>xr and x<xrn and y>yr and y< yrn:
               
                print 'this is',key1   
                pattern=key1
                cv2.rectangle(menus, (200,0), (210,10), classifc[pattern], -1)
                cv2.rectangle(menus, (212,0), (340,12), black, -1)
                cv2.putText(menus,key1,(215,10),cv2.FONT_HERSHEY_PLAIN,0.7,classifc[key1],1 )
                labelfound=True
                break  
            posrc+=1 

        if  x> zoneverticalgauche[0][0] and y > zoneverticalgauche[0][1] and x<zoneverticalgauche[1][0] and y<zoneverticalgauche[1][1]:
            print 'this is in menu'
            labelfound=True
            
        if  x> zoneverticaldroite[0][0] and y > zoneverticaldroite[0][1] and x<zoneverticaldroite[1][0] and y<zoneverticaldroite[1][1]:
            print 'this is in menu'
            labelfound=True
            
        if  x> zonehorizontal[0][0] and y > zonehorizontal[0][1] and x<zonehorizontal[1][0] and y<zonehorizontal[1][1]:
            print 'this is in menu'
            labelfound=True
            
        if x>posxdel and x<posxdel+10 and y>posydel and y< posydel+10:
            print 'this is suppress'
            suppress()
            labelfound=True
            
        if x>posxquit and x<posxquit+10 and y>posyquit and y< posyquit+10:
            print 'this is quit'
            quitl=True
            labelfound=True
            
        if x>posxdellast and x<posxdellast+10 and y>posydellast and y< posydellast+10:
            print 'this is delete last'
            labelfound=True
            dellast()

        if x>posxdelall and x<posxdelall+10 and y>posydelall and y< posydelall+10:
            print 'this is delete all'
            labelfound=True
            delall()

        if x>posxcomp and x<posxcomp+10 and y>posycomp and y< posycomp+10:
            print 'this is completed for all'
            labelfound=True  
            completed(imagename)
        
        if x>posxreset and x<posxreset+10 and y>posyreset and y< posyreset+10:
            print 'this is reset'
            labelfound=True  
            reseted()
        if x>posxvisua and x<posxvisua+10 and y>posyvisua and y< posyvisua+10:
            print 'this is visua'
            labelfound=True  
            visua()
        if x>posxeraseroi and x<posxeraseroi+10 and y>posyeraseroi and y< posyeraseroi+10:
            print 'this is erase roi'
            labelfound=True  
            eraseroi(imagename)
            
        if x>posxlastp and x<posxlastp+10 and y>posylastp and y< posylastp+10:
            print 'this is last point'
            labelfound=True  
            closepolygon()
            
      
                     
        if not labelfound:
            print 'add point',pattern
            if len(pattern)>0:
                numeropoly=tabroinumber[pattern][scannumber]
                print 'length last pattent',len(tabroi[pattern][scannumber][numeropoly])
                tabroi[pattern][scannumber][numeropoly].append((x, y)) 
                print numeropoly, tabroi[pattern][scannumber][numeropoly]
                cv2.rectangle(images[scannumber], (x,y), 
                              (x,y), classifc[pattern], 1)
                for l in range(0,len(tabroi[pattern][scannumber][numeropoly])-1):
                    cv2.line(images[scannumber], (tabroi[pattern][scannumber][numeropoly][l][0],tabroi[pattern][scannumber][numeropoly][l][1]), 
                              (tabroi[pattern][scannumber][numeropoly][l+1][0],tabroi[pattern][scannumber][numeropoly][l+1][1]), classifc[pattern], 1)
                    l+=1
            else:
                cv2.rectangle(menus, (212,0), (340,12), black, -1)
                cv2.putText(menus,'No pattern selected',(215,10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )

def closepolygon():
    numeropoly=tabroinumber[pattern][scannumber]
    if len(tabroi[pattern][scannumber][numeropoly])>0:
        numeropoly+=1
        print 'numeropoly',numeropoly
        tabroinumber[pattern][scannumber]=numeropoly
        tabroi[pattern][scannumber][numeropoly]=[]
    else:
        'wait for new point'
    cv2.putText(menus,'polygone closed',(215,20),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
                    
def suppress():
    numeropoly=tabroinumber[pattern][scannumber]
    lastp=len(tabroi[pattern][scannumber][numeropoly])
    if lastp>0:
        cv2.line(images[scannumber], (tabroi[pattern][scannumber][numeropoly][lastp-2][0],tabroi[pattern][scannumber][numeropoly][lastp-2][1]), 
                 (tabroi[pattern][scannumber][numeropoly][lastp-1][0],tabroi[pattern][scannumber][numeropoly][lastp-1][1]), black, 1)
        tabroi[pattern][scannumber][numeropoly].pop()
        for l in range(0,len(tabroi[pattern][scannumber][numeropoly])-1):
            cv2.line(images[scannumber], (tabroi[pattern][scannumber][numeropoly][l][0],tabroi[pattern][scannumber][numeropoly][l][1]),
                     (tabroi[pattern][scannumber][numeropoly][l+1][0],tabroi[pattern][scannumber][numeropoly][l+1][1]), classifc[pattern], 1)
            l+=1
    cv2.putText(menus,'delete last entry',(215,20),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
def completed(imagename):
#    global images[scannumber]
    for key in classif:
        numeropoly=tabroinumber[key][scannumber]
        for n in range (0,numeropoly+1):
            if len(tabroi[key][scannumber][n])>0:
                for l in range(0,len(tabroi[key][scannumber][n])-1):
                        cv2.line(images[scannumber], (tabroi[key][scannumber][n][l][0],tabroi[key][scannumber][n][l][1]), 
                                      (tabroi[key][scannumber][n][l+1][0],tabroi[key][scannumber][n][l+1][1]), black, 1)           
           
#            vis=contour3(tabroi[key][scannumber],key,dimtabx,dimtaby)
                images[scannumber]=contour3(images[scannumber],tabroi[key][scannumber][n],key,dimtabx,dimtaby)
                tabroi[key][scannumber][n]=[]
                tabroifinal[key][scannumber]=cv2.add(images[scannumber],tabroifinal[key][scannumber])
        tabroinumber[key][scannumber]=0
        imgray = cv2.cvtColor(tabroifinal[key][scannumber],cv2.COLOR_BGR2GRAY)
        
#        cv2.imshow('a',tabroifinal[key][scannumber])
        imagemax= cv2.countNonZero(imgray)
        print key,imagemax
        if imagemax>0:
                dirroi=os.path.join(dirpath_patient,key)
                if not os.path.exists(dirroi):
                    os.mkdir(dirroi)
#                print dirroi
#                print imagename,scannumber
                posext=imagename.find('.'+typei)
                imgcoreScan=imagename[0:posext]+'.'+typei   
                imgcoreScan=os.path.join(dirroi,imgcoreScan)
                if os.path.exists(imgcoreScan):
                    cv2.putText(menus,'ROI '+key+' slice:'+str(scannumber)+' overwritten',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
                tabtowrite=cv2.cvtColor(tabroifinal[key][scannumber],cv2.COLOR_BGR2RGB)
                cv2.imwrite(imgcoreScan,tabtowrite)
                cv2.putText(menus,'Slice ROI stored',(215,20),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    

def eraseroi(imagename):
    print 'this is erase roi'
    if len(pattern)>0:             
        tabroifinal[pattern][scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
        images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
        dirroi=os.path.join(dirpath_patient,pattern)
        imgcoreScan=os.path.join(dirroi,imagename)
#        tabroifinal[pattern][scannumber]=cv2.add(images[scannumber],tabroifinal[key][scannumber])
        if os.path.exists(imgcoreScan):
            os.remove(imgcoreScan)
            cv2.putText(menus,'ROI '+pattern+' slice:'+str(scannumber)+' erased',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
        else:
                    cv2.putText(menus,'ROI '+pattern+' slice:'+str(scannumber)+' not exist',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    else:
        cv2.putText(menus,' no pattern defined',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )

    
def visua():
    global images
#    vis = np.zeros((dimtabx,dimtaby,3), np.uint8)
    for key in classif:
        numeropoly=tabroinumber[key][scannumber]
        for n in range (0,numeropoly+1):
            if len(tabroi[key][scannumber][n])>0:
                    for l in range(0,len(tabroi[key][scannumber][n])-1):
        #                tabroifinal[pattern][tabroi[pattern][scannumber][l][0]][tabroi[pattern][scannumber][l][1]]=classifc[pattern]
                        cv2.line(images[scannumber], (tabroi[key][scannumber][n][l][0],tabroi[key][scannumber][n][l][1]), 
                                      (tabroi[key][scannumber][n][l+1][0],tabroi[key][scannumber][n][l+1][1]), black, 1)          
                   
                    images[scannumber]=contour3(images[scannumber],tabroi[key][scannumber][n],key,dimtabx,dimtaby)
    cv2.putText(menus,' Visualization ROI',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
#    vis=contour4(images[scannumber],pattern,dimtabx,dimtaby)
#    images[scannumber]=cv2.add(vis, images[scannumber])
                
                
def reseted():
    global images
    for key in classif:
        numeropoly=tabroinumber[key][scannumber]
        for n in range (0,numeropoly+1):
            if len(tabroi[key][scannumber][n])>0:
                for l in range(0,len(tabroi[key][scannumber][n])-1):
                    
    #                tabroifinal[pattern][tabroi[pattern][scannumber][l][0]][tabroi[pattern][scannumber][l][1]]=classifc[pattern]
                    cv2.line(images[scannumber], (tabroi[key][scannumber][n][l][0],tabroi[key][scannumber][n][l][1]), 
                                  (tabroi[key][scannumber][n][l+1][0],tabroi[key][scannumber][n][l+1][1]), black, 1)          
                tabroi[key][scannumber][n]=[]    
#        tabroifinal[key][scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    cv2.putText(menus,' Delete all drawings',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )

def dellast():
#    global images
    numeropoly=tabroinumber[pattern][scannumber]
    if len(tabroi[pattern][scannumber][numeropoly])>0:
        print 'len>0'
        for l in range(0,len(tabroi[pattern][scannumber][numeropoly])-1):
            cv2.line(images[scannumber], (tabroi[pattern][scannumber][numeropoly][l][0],tabroi[pattern][scannumber][numeropoly][l][1]), 
                     (tabroi[pattern][scannumber][numeropoly][l+1][0],tabroi[pattern][scannumber][numeropoly][l+1][1]), black, 1)          
        tabroi[pattern][scannumber][numeropoly]=[]
#        tabroinumber[pattern][scannumber]=max(numeropoly-1,0)
    elif numeropoly >0 :
        print 'len=0 and num>0'
        numeropoly=numeropoly-1
        tabroinumber[pattern][scannumber]=numeropoly
        for l in range(0,len(tabroi[pattern][scannumber][numeropoly])-1):
            cv2.line(images[scannumber], (tabroi[pattern][scannumber][numeropoly][l][0],tabroi[pattern][scannumber][numeropoly][l][1]), 
                     (tabroi[pattern][scannumber][numeropoly][l+1][0],tabroi[pattern][scannumber][numeropoly][l+1][1]), black, 1)          
        tabroi[pattern][scannumber][numeropoly]=[]
    else:
        print'length null' 
    cv2.putText(menus,' Delete last polygon',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )

def delall():
    global images   
    for key in classif:
        numeropoly=tabroinumber[key][scannumber]
#        print key, numeropoly
        for n in range (0,numeropoly+1):
            for l in range(0,len(tabroi[key][scannumber][n])-1):
                cv2.line(images[scannumber], (tabroi[key][scannumber][n][l][0],tabroi[key][scannumber][n][l][1]), 
                    (tabroi[key][scannumber][n][l+1][0],tabroi[key][scannumber][n][l+1][1]), black, 1)          
            tabroi[key][scannumber][n]=[]
        tabroinumber[key][scannumber]=0
        images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    cv2.putText(menus,' Delete all polygons',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
 
def contrasti(im,r):
 
     r1=0.5+r/100.0
     tabi1=im*r1     
     tabi2=np.clip(tabi1,0,imageDepth)
     tabi3=tabi2.astype(np.uint8)
     return tabi3

def lumi(tabi,r):
 
    r1=r
    tabi1=tabi+r1
    tabi2=np.clip(tabi1,0,imageDepth)
    tabi3=tabi2.astype(np.uint8)
    return tabi3

def rsliceNum(s,c,e):
    ''' look for  afile according to slice number'''
    #s: file name, c: delimiter for snumber, e: end of file extension
    endnumslice=s.find(e)
    posend=endnumslice
    while s.find(c,posend)==-1:
        posend-=1
    debnumslice=posend+1
    return int((s[debnumslice:endnumslice])) 

def loop(slnt,pdirk,dimtabx,dimtaby):
    global image,images,menus,imageview,quitl,scannumber,imagename
    quitl=False
    list_image={}
    cdelimter='_'
    extensionimage='.'+typei
    limage=[name for name in os.listdir(pdirk) if name.find('.'+typei,1)>0 ]

    if len(limage)+1==slnt:
#        print 'good'
#    
        for iimage in range(0,slnt-1):
    #        print iimage
            s=limage[iimage]       
                #s: file name, c: delimiter for snumber, e: end of file extension
            sln=rsliceNum(s,cdelimter,extensionimage)
            list_image[sln]=s    
        fl=slnt/2
        imagename=list_image[fl+1]
        imagenamecomplet=os.path.join(pdirk,imagename)
        image = cv2.imread(imagenamecomplet,cv2.IMREAD_ANYDEPTH)
        image=cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
       
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.namedWindow("Slider2",cv2.WINDOW_NORMAL)
    
        cv2.createTrackbar( 'Brightness','Slider2',0,100,nothing)
        cv2.createTrackbar( 'Contrast','Slider2',50,100,nothing)
        cv2.createTrackbar( 'Flip','Slider2',slnt/2,slnt-2,nothing)
        cv2.setMouseCallback("image", click_and_crop)
        

    while True:

        key = cv2.waitKey(100) & 0xFF
        if key != 255:
            print key
            
        if key == ord("c"):
                print 'completed'
                completed(imagename)
                
        elif key == ord("d"):
                print 'delete entry'
                suppress()
                
        elif key == ord("l"):
                print 'delete last polygon'
                dellast()
        
        elif key == ord("a"):
                print 'delete all'
                delall()
                
        elif key == ord("r"):
                print 'reset'
                reseted()
                
        elif key == ord("v"):
                print 'visualize'
                visua()
        elif key == ord("e"):
                print 'erase'
                eraseroi(imagename)
        elif key == ord("f"):
                print 'close polygone'
                closepolygon()
        elif key == ord("q")  or quitl or cv2.waitKey(20) & 0xFF == 27 :
               print 'on quitte', quitl
               cv2.destroyAllWindows()
               break
        c = cv2.getTrackbarPos('Contrast','Slider2')
        l = cv2.getTrackbarPos('Brightness','Slider2')
        fl = cv2.getTrackbarPos('Flip','Slider2')
#        print fl
        scannumber=fl+1
        imagename=list_image[scannumber]
        imagenamecomplet=os.path.join(pdirk,imagename)
        image = cv2.imread(imagenamecomplet,cv2.IMREAD_ANYDEPTH)
        image=cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
        imglumi=lumi(image,l)
        image=contrasti(imglumi,c) 
#        print image.shape,images[scannumber].shape
        imageview=cv2.add(image,images[scannumber])
        imageview=cv2.add(imageview,menus)
        for key1 in classif:
                imageview=cv2.add(imageview,tabroifinal[key1][scannumber])
        imageview=cv2.cvtColor(imageview,cv2.COLOR_BGR2RGB)
        cv2.imshow("image", imageview)
def tagviews (tab,t0,x0,y0,t1,x1,y1,t2,x2,y2,t3,x3,y3,t4,x4,y4,t5,x5,y5):
    """write simple text in image """
    font = cv2.FONT_HERSHEY_SIMPLEX
    col=white
    viseg=cv2.putText(tab,t0,(x0, y0), font,0.3,col,1)
    viseg=cv2.putText(viseg,t1,(x1, y1), font,0.3,col,1)
    viseg=cv2.putText(viseg,t2,(x2, y2), font,0.3,col,1)

    viseg=cv2.putText(viseg,t3,(x3, y3), font,0.3,col,1)
    viseg=cv2.putText(viseg,t4,(x4, y4), font,0.3,col,1)
    viseg=cv2.putText(viseg,t5,(x5, y5), font,0.3,col,1)
    return viseg
 


def genebmp(fn):
    """generate patches from dicom files"""
   
    print ('load dicom files in :',fn)
    (top,tail) =os.path.split(fn)
    (top1,tail1) =os.path.split(top)


    fmbmpbmp=os.path.join(fn,scan_bmp)
    remove_folder(fmbmpbmp)
    os.mkdir(fmbmpbmp)
    
    listdcm=[name for name in  os.listdir(fn) if name.lower().find('.dcm')>0]

    FilesDCM =(os.path.join(fn,listdcm[0]))            
    RefDs = dicom.read_file(FilesDCM)
    dsr= RefDs.pixel_array
    dimtabx=dsr.shape[0]
    dimtaby=dsr.shape[1]
#    print dimtabx, dimtaby
    slnt=0
    for l in listdcm:
        
        FilesDCM =(os.path.join(fn,l))  
        RefDs = dicom.read_file(FilesDCM)
        slicenumber=int(RefDs.InstanceNumber)
        if slicenumber> slnt:
            slnt=slicenumber
    
    print 'number of slices', slnt
    slnt=slnt+1
    tabscan = np.zeros((slnt,dimtabx,dimtaby), np.uint8)
    for l in listdcm:
#        print l
        FilesDCM =(os.path.join(fn,l))            
        RefDs = dicom.read_file(FilesDCM)
        slicenumber=int(RefDs.InstanceNumber)
  
        dsr= RefDs.pixel_array
        dsr= dsr-dsr.min()
        c=float(imageDepth)/dsr.max()
        dsr=dsr*c     
        dsr = dsr.astype('uint8')
        endnumslice=l.find('.dcm') 
        imgcoreScan=l[0:endnumslice]+'_'+str(slicenumber)+'.'+typei                     
        bmpfile=os.path.join(fmbmpbmp,imgcoreScan)
       
        t2='Prototype Not for medical use'
        t1='Pt: '+tail1  
        t0='CONFIDENTIAL'
        t3='Scan: '+str(slicenumber)
        
        t4=time.asctime()
        t5=''
        dsr=tagviews(dsr,t0,dimtabx-80,dimtaby-10,t1,0,dimtaby-20,t2,dimtabx-250,dimtaby-10,
                     t3,0,dimtaby-30,t4,0,dimtaby-10,t5,0,dimtaby-20) 
        cv2.imwrite(bmpfile,dsr)
#        cv2.imshow('dd',dsr)
    return tabscan,slnt,dimtabx,dimtaby

def nothing(x):
    pass


def menudraw(dimtabx,dimtaby,slnt):
    global refPt, cropping,pattern,x0,y0,quitl,tabroi,tabroifinal,menus,images
    global posxdel,posydel,posxquit,posyquit,posxdellast,posydellast,posxdelall,posydelall
    global posxcomp,posycomp,posxreset,posyreset,posxvisua,posyvisua,posxeraseroi,posyeraseroi,posxlastp,posylastp
    posrc=0
    for key1 in classif:
        tabroi[key1]={}
        tabroifinal[key1]={}
        tabroinumber[key1]={}
        for sln in range(1,slnt):
            tabroinumber[key1][sln]=0
            tabroi[key1][sln]={}  
            tabroi[key1][sln][0]=[]    
            tabroifinal[key1][sln]= np.zeros((dimtabx,dimtaby,3), np.uint8)

        xr=5
        yr=15*posrc
        xrn=xr+10
        yrn=yr+10
        cv2.rectangle(menus, (xr, yr),(xrn,yrn), classifc[key1], -1)
        cv2.putText(menus,key1,(xr+15,yr+10),cv2.FONT_HERSHEY_PLAIN,0.7,classifc[key1],1 )
        posrc+=1
    
    posxdel=dimtabx-20
    posydel=15
    cv2.rectangle(menus, (posxdel,posydel),(posxdel+10,posydel+10), white, -1)
    cv2.putText(menus,'(d) del',(posxdel-40, posydel+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxquit=dimtabx-20
    posyquit=0
    cv2.rectangle(menus, (posxquit,posyquit),(posxquit+10,posyquit+10), white, -1)
    cv2.putText(menus,'(q) quit',(posxquit-45, posyquit+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxdellast=dimtabx-20
    posydellast=30
    cv2.rectangle(menus, (posxdellast,posydellast),(posxdellast+10,posydellast+10), white, -1)
    cv2.putText(menus,'(l) del last',(posxdellast-68, posydellast+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxdelall=dimtabx-20
    posydelall=45
    cv2.rectangle(menus, (posxdelall,posydelall),(posxdelall+10,posydelall+10), white, -1)
    cv2.putText(menus,'(e) del all',(posxdelall-57, posydelall+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxcomp=dimtabx-20
    posycomp=75
    cv2.rectangle(menus, (posxcomp,posycomp),(posxcomp+10,posycomp+10), white, -1)
    cv2.putText(menus,'(c) completed',(posxcomp-85, posycomp+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxreset=dimtabx-20
    posyreset=90
    cv2.rectangle(menus, (posxreset,posyreset),(posxreset+10,posyreset+10), white, -1)
    cv2.putText(menus,'(r) reset',(posxreset-55, posyreset+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxvisua=dimtabx-20
    posyvisua=60
    cv2.rectangle(menus, (posxvisua,posyvisua),(posxvisua+10,posyvisua+10), white, -1)
    cv2.putText(menus,'(v) visua',(posxvisua-55, posyvisua+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )

    posxeraseroi=dimtabx-20
    posyeraseroi=105
    cv2.rectangle(menus, (posxeraseroi,posyeraseroi),(posxeraseroi+10,posyeraseroi+10), white, -1)
    cv2.putText(menus,'(e) eraseroi',(posxeraseroi-75, posyeraseroi+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
    posxlastp=dimtabx-20
    posylastp=120
    cv2.rectangle(menus, (posxlastp,posylastp),(posxlastp+10,posylastp+10), white, -1)
    cv2.putText(menus,'(f) last p',(posxlastp-75, posylastp+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
#
#    
def populate(pp,sl):
    print 'populate'
    for key in classif:
        dirroi=os.path.join(pp,key)
#        print dirroi,sl
        if os.path.exists(dirroi):
                listroi =[name for name in  os.listdir(dirroi) if name.lower().find('.'+typei)>0]
                for roiimage in listroi:
#                    tabroi[key][sl]=genepoly(os.path.join(dirroi,roiimage)) 
                    img=os.path.join(dirroi,roiimage) 
                    imageroi= cv2.imread(img,1)
                    cdelimter='_'
                    extensionimage='.'+typei
                    slicenumber=rsliceNum(roiimage,cdelimter,extensionimage)
                    imageview=cv2.cvtColor(imageroi,cv2.COLOR_RGB2BGR)
                    tabroifinal[key][slicenumber]=imageview
#                    cv2.imshow('imageroi',imageroi)

    

cwd=os.getcwd()
(top,tail) =os.path.split(cwd)

patient_path_complet=os.path.join(top,path_patient)
#patient_path_complet=os.path.join(patient_path_complet,images[scannumber]ource)
a= os.walk(patient_path_complet).next()[1]
def openfichierroi(patient,patient_path_complet):
    global menus,imageview,zoneverticalgauche,zoneverticaldroite,zonehorizontal,dimtabx,dimtaby,dirpath_patient
    dirpath_patient=os.path.join(patient_path_complet,patient)
   
    dirsource=os.path.join(dirpath_patient,source_name)
    tabscan,slnt,dimtabx,dimtaby=genebmp(dirsource) 

    dirsourcescan=os.path.join(dirsource,scan_bmp)
    menus=np.zeros((dimtabx,dimtaby,3), np.uint8)
    for i in range(1,slnt):
        images[i]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    imageview=np.zeros((dimtabx,dimtaby,3), np.uint8)
    menudraw(dimtabx,dimtaby,slnt)
    populate(dirpath_patient,slnt)
    zoneverticalgauche=((0,0),(25,dimtaby))
    zonehorizontal=((0,0),(dimtabx,20))
    zoneverticaldroite=((dimtabx-25,0),(dimtabx,dimtaby))
    loop(slnt,dirsourcescan,dimtabx,dimtaby)
    return 'completed'