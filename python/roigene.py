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
import shutil
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
         # remove if exists
         shutil.rmtree(path,ignore_errors=True)


def contour3(im,l,dimtabx,dimtaby):  
    col=classifc[l]
    vis = np.zeros((dimtabx,dimtaby,3), np.uint8)
#    cv2.fillConvexPoly(vis, np.array(im),col)
    imagemax= cv2.countNonZero(np.array(im))
    if imagemax>0:
        cv2.fillPoly(vis, [np.array(im)],col)

    return vis

def click_and_crop(event, x, y, flags, param):
    global quitl,pattern
#    global posxdel1,posydel,posxquit,posyquit,posxdellast,posydellast,posxdelall,posydelall
#    global posxcomp,posycomp,posxreset,posyreset,posxvisua,posyvisua
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(menus, (150,12), (370,32), black, -1)
        posrc=0
        print x,y
        for key,value in classif.items():
            labelfound=False            
            xr=5
            yr=15*posrc
            xrn=xr+10
            yrn=yr+10
            if x>xr and x<xrn and y>yr and y< yrn:
               
                print 'this is',key   
                pattern=key
                cv2.rectangle(menus, (200,0), (210,10), classifc[pattern], -1)
                cv2.rectangle(menus, (212,0), (340,12), black, -1)
                cv2.putText(menus,key,(215,10),cv2.FONT_HERSHEY_PLAIN,0.7,classifc[key],1 )
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
                     
        if not labelfound:
            if len(pattern)>0:
                print 'len pattent',len(tabroi[pattern][scannumber])
                tabroi[pattern][scannumber].append((x, y)) 
                cv2.rectangle(images[scannumber], (x,y), 
                              (x,y), classifc[pattern], 1)
                for l in range(0,len(tabroi[pattern][scannumber])-1):
                    cv2.line(images[scannumber], (tabroi[pattern][scannumber][l][0],tabroi[pattern][scannumber][l][1]), 
                              (tabroi[pattern][scannumber][l+1][0],tabroi[pattern][scannumber][l+1][1]), classifc[pattern], 1)
                    l+=1
            else:
                cv2.rectangle(menus, (212,0), (340,12), black, -1)
                cv2.putText(menus,'No pattern selected',(215,10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
                    
def suppress():
    lastp=len(tabroi[pattern][scannumber])
    if lastp>0:
        cv2.line(images[scannumber], (tabroi[pattern][scannumber][lastp-2][0],tabroi[pattern][scannumber][lastp-2][1]), 
                 (tabroi[pattern][scannumber][lastp-1][0],tabroi[pattern][scannumber][lastp-1][1]), black, 1)
        tabroi[pattern][scannumber].pop()
        for l in range(0,len(tabroi[pattern][scannumber])-1):
            cv2.line(images[scannumber], (tabroi[pattern][scannumber][l][0],tabroi[pattern][scannumber][l][1]),
                     (tabroi[pattern][scannumber][l+1][0],tabroi[pattern][scannumber][l+1][1]), classifc[pattern], 1)
            l+=1

def completed(imagename):
#    global images[scannumber]
    for key,value in classif.items():
            for l in range(0,len(tabroi[key][scannumber])-1):
#                tabroifinal[pattern][tabroi[pattern][scannumber][l][0]][tabroi[pattern][scannumber][l][1]]=classifc[pattern]
                cv2.line(images[scannumber], (tabroi[key][scannumber][l][0],tabroi[key][scannumber][l][1]), 
                              (tabroi[key][scannumber][l+1][0],tabroi[key][scannumber][l+1][1]), black, 1)          
           
            vis=contour3(tabroi[key][scannumber],key,dimtabx,dimtaby)
            tabroifinal[key][scannumber]=cv2.add(vis, tabroifinal[key][scannumber])
            tabroi[key][scannumber]=[]
            imgray = cv2.cvtColor(tabroifinal[key][scannumber],cv2.COLOR_BGR2GRAY)
            imagemax= cv2.countNonZero(imgray)
            if imagemax>0:
                dirroi=os.path.join(dirpath_patient,key)
                if not os.path.exists(dirroi):
                    os.mkdir(dirroi)
                print dirroi
                print imagename,scannumber
                posext=imagename.find('.'+typei)
                imgcoreScan=imagename[0:posext]+'.'+typei   
                imgcoreScan=os.path.join(dirroi,imgcoreScan)
                if os.path.exists(imgcoreScan):
                    cv2.putText(menus,'ROI '+key+' slice:'+str(scannumber)+' overwritten',(150,30),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
                tabtowrite=cv2.cvtColor(tabroifinal[key][scannumber],cv2.COLOR_BGR2RGB)
                cv2.imwrite(imgcoreScan,tabtowrite)
                cv2.putText(menus,'stores done',(215,20),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )


    
def visua():
    global images

    for key,value in classif.items():
                if len(tabroi[key][scannumber])>0:
                    for l in range(0,len(tabroi[key][scannumber])-1):
        #                tabroifinal[pattern][tabroi[pattern][scannumber][l][0]][tabroi[pattern][scannumber][l][1]]=classifc[pattern]
                        cv2.line(images[scannumber], (tabroi[key][scannumber][l][0],tabroi[key][scannumber][l][1]), 
                                      (tabroi[key][scannumber][l+1][0],tabroi[key][scannumber][l+1][1]), black, 1)          
                   
                    vis=contour3(tabroi[key][scannumber],key,dimtabx,dimtaby)
                    images[scannumber]=cv2.add(vis, images[scannumber])
                
                
def reseted():
    global images
    for key,value in classif.items():
                for l in range(0,len(tabroi[key][scannumber])-1):
    #                tabroifinal[pattern][tabroi[pattern][scannumber][l][0]][tabroi[pattern][scannumber][l][1]]=classifc[pattern]
                    cv2.line(images[scannumber], (tabroi[key][scannumber][l][0],tabroi[key][scannumber][l][1]), 
                                  (tabroi[key][scannumber][l+1][0],tabroi[key][scannumber][l+1][1]), black, 1)          
                tabroifinal[key][scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
                tabroi[key][scannumber]=[]    
                images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
def dellast():
    global images
    if len(tabroi[pattern][scannumber])>0:
        for l in range(0,len(tabroi[pattern][scannumber])-1):
            cv2.line(images[scannumber], (tabroi[pattern][scannumber][l][0],tabroi[pattern][scannumber][l][1]), 
                     (tabroi[pattern][scannumber][l+1][0],tabroi[pattern][scannumber][l+1][1]), black, 1)          
        tabroi[pattern][scannumber]=[]   
    else:
        print'length null' 

def delall():
    global images
    for key,value in classif.items():
        for l in range(0,len(tabroi[key][scannumber])-1):
            cv2.line(images[scannumber], (tabroi[key][scannumber][l][0],tabroi[key][scannumber][l][1]), 
                (tabroi[key][scannumber][l+1][0],tabroi[key][scannumber][l+1][1]), black, 1)          
        tabroi[key][scannumber]=[]
        images[scannumber]=np.zeros((dimtabx,dimtaby,3), np.uint8)
 
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

        key = cv2.waitKey(1) & 0xFF
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
        imageview=cv2.add(image,images[scannumber])
        imageview=cv2.add(imageview,menus)
        for key,value in classif.items():
                imageview=cv2.add(imageview,tabroifinal[key][scannumber])
        imageview=cv2.cvtColor(imageview,cv2.COLOR_BGR2RGB)
        cv2.imshow("image", imageview)
    	# if the 'r' key is pressed, reset the cropping region
        if key == ord("c"):
                print 'completed'
                completed(imagename)
                
        elif key == ord("d"):
                print 'delete last'
                suppress()
                
        elif key == ord("l"):
                print 'delete last'
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
    
        elif key == ord("q")  or quitl or cv2.waitKey(20) & 0xFF == 27 :
        #            print 'on quitte', quitl
       
               cv2.destroyAllWindows()
               break

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
    global posxcomp,posycomp,posxreset,posyreset,posxvisua,posyvisua
    posrc=0
    for key,value in classif.items():
        tabroi[key]={}
        tabroifinal[key]={}
        for sln in range(1,slnt):
            tabroi[key][sln]=[]            
            tabroifinal[key][sln]= np.zeros((dimtabx,dimtaby,3), np.uint8)
        xr=5
        yr=15*posrc
        xrn=xr+10
        yrn=yr+10
        cv2.rectangle(menus, (xr, yr),(xrn,yrn), classifc[key], -1)
        cv2.putText(menus,key,(xr+15,yr+10),cv2.FONT_HERSHEY_PLAIN,0.7,classifc[key],1 )
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
    cv2.putText(menus,'(a) del all',(posxdelall-57, posydelall+10),cv2.FONT_HERSHEY_PLAIN,0.7,white,1 )
    
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
    

cwd=os.getcwd()
(top,tail) =os.path.split(cwd)

patient_path_complet=os.path.join(top,path_patient)
#patient_path_complet=os.path.join(patient_path_complet,images[scannumber]ource)
a= os.walk(patient_path_complet).next()[1]
#print patient_path_complet,a
for patient in a:
    dirpath_patient=os.path.join(patient_path_complet,patient)
    dirsource=os.path.join(dirpath_patient,source_name)
    tabscan,slnt,dimtabx,dimtaby=genebmp(dirsource) 
    dirsource=os.path.join(dirsource,scan_bmp)
    menus=np.zeros((dimtabx,dimtaby,3), np.uint8)
    for i in range(1,slnt):
        images[i]=np.zeros((dimtabx,dimtaby,3), np.uint8)
    imageview=np.zeros((dimtabx,dimtaby,3), np.uint8)
    menudraw(dimtabx,dimtaby,slnt)
    zoneverticalgauche=((0,0),(25,dimtaby))
    zonehorizontal=((0,0),(dimtabx,20))
    zoneverticaldroite=((dimtabx-25,0),(dimtabx,dimtaby))
    loop(slnt,dirsource,dimtabx,dimtaby)
