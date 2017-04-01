# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 09:27:11 2017
@author: sylvain
"""

import random
import string
import cherrypy
import webbrowser
import os
import simplejson
import sys
#'127.0.0.1'
import os, os.path
#import module
from moduleroi import *
#
#reservedparm=[ 'thrpatch','thrproba','thrprobaUIP','thrprobaMerge','picklein_file',
#                      'picklein_file_front','tdornot','threedpredictrequest',
#                      'onlyvisuaasked','cross','front','merge']
htmldir='html'

cwd=os.getcwd()
(cwdtop,tail)=os.path.split(cwd)
#path_pickle='CNNparameters'
path_patient=''
path_html=os.path.join(cwdtop,'static/html')
#dirpickle=os.path.join(cwdtop,path_pickle)

toproi = os.path.join(path_html, 'toproi.html')
listdicomtop = os.path.join(path_html, 'listdicomtop.html')
listdicombottom = os.path.join(path_html, 'listdicombottom.html')

generateroitop = os.path.join(path_html, 'generateroitop.html')
generateroibottom = os.path.join(path_html, 'generateroibottom.html')

visuabottomcross = os.path.join(path_html, 'visuabottomcross.html')
visuabottom = os.path.join(path_html, 'visuabottom.html')
visuatopfollow = os.path.join(path_html, 'visuatopfollow.html')

visuarestop = os.path.join(path_html, 'visuarestop.html')

visuaresbottom = os.path.join(path_html, 'visuaresbottom.html')


class PredictTool(object):
    
    @cherrypy.expose    
    def index(self):
        return open(toproi)
    

    @cherrypy.expose
    def generateroi(self,**kwargs):
        global path_patient,listdir
        print "generate"
        print "generate", kwargs
        print "generate", path_patient
#        runPredict=False
       
        listdir=roirun(kwargs,path_patient)
#            runPredict=True
#        else:
#            for key, value in kwargs.items():
#                if key not in reservedparm:
#                    listdir.append(key)
#        listdirdummy,stsdir=lisdirprocess(path_patient)        
##        if not runPredict:        
##        listdir,stsdir=lisdirprocess(path_patient)
##        oneatleast=0
###        print 'generate lisdir',listdir
###        print 'generate stsdir',stsdir
#        for key, value in stsdir.items():
#            for key1, value1 in value.items():
#                if  value1 == 'True':
#                    oneatleast+=1
#        print 'oneatleast',oneatleast
        a=open(generateroitop,'r')
        app=a.read()
        a.close()
        yield app   
#        if oneatleast>0:
#            yield "<h2 class = 'warningnopatient' > No patient has been selected </h2>"
        yield "<input type='hidden'  name = 'lisdir' value='"+path_patient+"' id='"+path_patient+"'/>"
                    
        a=open(generateroibottom,'r')
        app=a.read()
        a.close()
        yield app
#        return kwargs

    
            
    @cherrypy.expose
    def stop(self):
        cherrypy.engine.exit()
        sys.exit()
#        os.kill()
        
    @cherrypy.expose
    def listdicom(self,lisdir):
        print 'listdicom'

        global path_patient
        path_patient=lisdir
        print 'path_patient', path_patient
        some_sg,stsdir=lisdirprocess(lisdir)
        print some_sg
        print stsdir
        a=open(listdicomtop,'r')
        app=a.read()
        a.close()
        yield app
        iuser=0
        for user in some_sg:
            predictdoneF=False
            statustext=""
            if iuser==0:
                yield "<input type='radio' checked  name = 'lispatientselect' value='"+user+"' id='"+user+"'/>"
            else:
                yield "<input type='radio'  name = 'lispatientselect' value='"+user+"' id='"+user+"'/>"
            textlist=stsdir[user]
            if len(textlist)>0:
                statustext=' ROI exists:'
                predictdoneF=True
                for i in range (0,len(textlist)):
                    statustext=statustext+' '+textlist[i]
            else:
                    statustext=' No ROI'
            if predictdoneF:
                    predictdone='classpredictdone'
            else:
                    predictdone='classpredictnotdone'      
            yield "<label id='"+predictdone+"'for '"+user+"'>"+user+statustext+" </label> <br>"
        a=open(listdicombottom,'r')
        app=a.read()
        a.close()
        yield app
        
        
    index.exposed = True             
    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']
    
def open_page():
    webbrowser.open("http://127.0.0.1:8082/")
#cherrypy.tree.mount(AjaxApp(), '/', config=conf)
#tutconf = os.path.join(os.path.dirname(__file__), 'predict.conf')
if __name__ == '__main__':
    conf = {
        'global':{'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8082,
                        'server.thread_pool' : 10,
                        'tools.sessions.on' : True,
                         'tools.encode.encoding' : "Utf-8",
                         'log.error_file': "myapp.log",
                           'log.screen':True ,  
                           'tools.sessions.timeout': 100000
                        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.sessions.storage_class' : cherrypy.lib.sessions.FileSession,
            'tools.sessions.storage_path' : "/some/directory",
              'log.screen':True   

    
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../static'                                     
        }
       
    }

#        
cherrypy.engine.subscribe('start', open_page)
cherrypy.quickstart(PredictTool(), '/', conf)
 