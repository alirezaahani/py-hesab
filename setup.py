import cherrypy
import chevron
import os
import os.path
import hashlib

import database
import config

def hasher(text):
    return hashlib.sha512(text.encode()).hexdigest()

class SetupApp(object):
    @cherrypy.expose
    def index(self,password='',username=''):
        args = {
            'form':True,
            'show_message':False,
            'message':''
        }

        if password and username:
            args['form'] = False
            args['show_message'] = True
            if len(password) > 5: 
                database.insertUser(username,hasher(password),2)
                args['message'] = "User created! Now stop this script and run the main.py!"
            else:
                args['message'] = "Short password, try again."
                args['form'] = True
        
        with open('pages/setup.html') as f:
            return chevron.render(f,args)

conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    }
}

if not database.createTables():
    Exception("Failed to create the database")

cherrypy.quickstart(SetupApp(),'/',conf)  