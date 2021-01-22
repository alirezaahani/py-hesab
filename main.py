import cherrypy
import chevron
import os
import os.path
import hashlib

import database
import config



def hasher(text):
    return hashlib.sha512(text.encode()).hexdigest()


@cherrypy.tools.register('before_handler')
def auth():
    if cherrypy.session.get("islogin"):
        return True
    else:
        raise cherrypy.HTTPRedirect("/login")



@cherrypy.tools.register('before_handler')
def admin():
    if cherrypy.session.get("level") == config.ADMIN_POWER_LEVEL:
        return True
    else:
        raise cherrypy.HTTPRedirect("/login")


class App(object):
    @cherrypy.expose
    def index(self):
        args = {
            'login_link':'/login'
        }
        with open('pages/index.html') as f:
            return chevron.render(f,args)
    

    @cherrypy.expose
    def login(self,username="",password=""):
        if cherrypy.session.get("islogin"):
            raise cherrypy.HTTPRedirect('/panel')
        
        args = {
            'form':True,
            'show_message':False,
            'message':'',
        }

        if username and password:
            if database.checkUserCorrect(username,hasher(password)):
                cherrypy.session['islogin'] = True
                cherrypy.session['level'] = database.getUserPower(username)
                raise cherrypy.HTTPRedirect('/panel')
            else:
                args['show_message'] = True
                args['message'] = 'Enter username or password correctly'
        
        with open('pages/login.html') as f:
                return chevron.render(f,args)
    
    @cherrypy.expose
    @cherrypy.tools.auth()
    def panel(self,page = 0):

        total_rows = database.getTotalRows(config.DATA_TABLE_NAME)
        max_pages = total_rows // 20

        start_from = 20 * int(page)
        end_from = start_from + 20

        print(page,start_from,end_from)

        if int(page) > max_pages or int(page) < 0:
            raise cherrypy.HTTPRedirect('/panel')


        raw_data = database.getDatas(statement1=start_from,statement2=end_from)
        table_rows = []
        
        for row in raw_data:
            table_rows.append({
                'id':row[0],
                'file_name':row[1],
                'date':row[2],
                'count':row[3],
                'price':row[4],
                'total':int(row[3]) * int(row[4]),
                'user1_precedent':row[5],
                'user2_precedent':row[6],
                'user3_precedent':row[7],
                'user4_precedent':row[8],
                'user5_precedent':row[9],
                'desc':row[10],
                'user1_share':int(row[5]) * int(row[4]) / int(row[3]),
                'user2_share':int(row[6]) * int(row[4]) / int(row[3]),
                'user3_share':int(row[7]) * int(row[4]) / int(row[3]),
                'user4_share':int(row[8]) * int(row[4]) / int(row[3]),
                'user5_share':int(row[9]) * int(row[4]) / int(row[3])
            })

            if cherrypy.session.get("level") == config.ADMIN_POWER_LEVEL:
                table_rows[-1]['op_link'] = f"/data_op?file_id={row[0]}"
            else:
                table_rows[-1]['op_link'] = ""
        
        args = {
            'table':table_rows,
            'show_next':True,
            'show_back':False,
            'show_message':False
        }

        if cherrypy.session.get("level") == config.ADMIN_POWER_LEVEL:
            args['show_message'] = True
        
        if int(page) < max_pages:
            args['Next'] = int(page)+1
        else:
            args['show_next'] = False

        if int(page) > 0:
            args['show_back'] = True
            args['Back'] = int(page)-1
        else:
            args['show_back'] = False

        with open('pages/panel.html') as f:
            return chevron.render(f,args)

    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_op(self,file_id=0):
        if file_id == 0:
            raise cherrypy.HTTPRedirect('/panel')
        
        args = {
            'show_controlls':False,
            'show_message':False,
            'message':'',
            'id':file_id
        }

        if database.checkDataExists(file_id):
            args['show_controlls'] = True
        else:
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Invuser4d ID'


        with open('pages/data_op.html') as f:
            return chevron.render(f,args)

    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_remove(self,file_id=0,confirm=""):
        if int(file_id) == 0:
            raise cherrypy.HTTPRedirect('/panel')
        
        args = {
            'id':file_id
        }
        
        if database.checkDataExists(file_id):
            args['show_controlls'] = True
            args['show_message'] = True
            args['message'] = f'Remove the row with ID {file_id}?'
            args['file_id'] = file_id
        else:
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Invuser4d ID'

        if confirm == "True":
            print(confirm)
            database.deleteData(file_id)
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Row removed.'

        elif confirm == "False":
            raise cherrypy.HTTPRedirect('/panel')

        with open('pages/data_remove.html') as f:
            return chevron.render(f,args) 
    
    
    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_edit(self,file_id=0):
        if int(file_id) == 0:
            raise cherrypy.HTTPRedirect('/panel')
        
        if not database.checkDataExists(int(file_id)):
            raise cherrypy.HTTPRedirect('/panel')

        args = {
            'id':int(file_id)
        }

        data = database.getDataByID(file_id)
        
        args['id'] = data[0]
        args['file_name'] = data[1]
        args['date'] = data[2]
        args['count'] = data[3]
        args['price'] = data[4]
        args['user1_precedent'] = data[5]
        args['user2_precedent'] = data[6]
        args['user3_precedent'] = data[7]
        args['user4_precedent'] = data[8]
        args['user5_precedent'] = data[9]
        args['desc'] = data[10]

        with open('pages/data_edit.html') as f:
            return chevron.render(f,args) 

    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_edit_proc(self,**args):
        print(len(args))
        if len(args) != 11:
            raise cherrypy.HTTPRedirect('/panel')
        
        if int(args['id']) == 0:
            raise cherrypy.HTTPRedirect('/panel')

        if not database.checkDataExists(int(args['id'])):
            raise cherrypy.HTTPRedirect('/panel')
        
        database.changeData(
            args['id'],
            args['file_name'],
            args['date'],
            args['count'],
            args['price'],
            args['user1_precedent'],
            args['user2_precedent'],
            args['user3_precedent'],
            args['user4_precedent'],
            args['user5_precedent'],
            args['desc'])
        
        with open('pages/data_edit_proc.html') as f:
            return chevron.render(f) 

    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_add(self):
        with open('pages/data_add.html') as f:
            return chevron.render(f) 
    
    @cherrypy.expose
    @cherrypy.tools.admin()
    def data_add_proc(self,**args):
        
        if len(args) != 10:
            raise cherrypy.HTTPRedirect('/panel')
        
        database.insertData(
            args['file_name'],
            args['date'],
            args['count'],
            args['price'],
            args['user1_precedent'],
            args['user2_precedent'],
            args['user3_precedent'],
            args['user4_precedent'],
            args['user5_precedent'],
            args['desc'])

        with open('pages/data_add_proc.html') as f:
            return chevron.render(f) 

    @cherrypy.expose
    @cherrypy.tools.admin()
    def users(self):
        data = database.getUsers()

        table_row = []

        for row in data:
            table_row.append({
                'id':row[0],
                'username':row[1],
                'power':row[3],
                'op_link':f'/user_op?user_id={row[0]}'
            })
        
        args = {'table':table_row}        

        with open('pages/users.html') as f:
            return chevron.render(f,args)
    
    @cherrypy.expose
    @cherrypy.tools.admin()
    def user_op(self,user_id=0):
        
        if user_id == 0:
            raise cherrypy.HTTPRedirect('/panel')
        
        args = {
            'show_controlls':False,
            'show_message':False,
            'message':'',
            'id':user_id
        }

        if database.checkUserExistsByID(user_id):
            args['show_controlls'] = True
        else:
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Invuser4d ID'
        
        with open('pages/user_op.html') as f:
            return chevron.render(f,args)

    @cherrypy.expose
    @cherrypy.tools.admin()
    def user_remove(self,user_id=0,confirm=""):
        if int(user_id) == 0:
            raise cherrypy.HTTPRedirect('/users')
        
        args = {
            'id':user_id
        }
        
        if database.checkUserExistsByID(user_id):
            args['show_controlls'] = True
            args['show_message'] = True
            args['message'] = f'Remove the user with ID {user_id}?'
            args['file_id'] = user_id
        else:
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Invuser4d ID'

        if confirm == "True":
            database.deleteUser(user_id)
            args['show_controlls'] = False
            args['show_message'] = True
            args['message'] = 'Row removed.'

        elif confirm == "False":
            raise cherrypy.HTTPRedirect('/users')

        with open('pages/user_remove.html') as f:
            return chevron.render(f,args) 
    
    @cherrypy.expose
    @cherrypy.tools.admin()
    def user_add(self):
        with open('pages/user_add.html') as f:
            return chevron.render(f) 
    
    @cherrypy.expose
    @cherrypy.tools.admin()
    def user_add_proc(self,**wargs):
        print(len(wargs))
        if len(wargs) != 3:
            raise cherrypy.HTTPRedirect('/users')
        
        args = {
            'message':''
        }
        if database.checkUserExists(wargs['username']):
            args['message'] = "Username already exists"
        else:
            database.insertUser(wargs['username'],hasher(wargs['password']),wargs['Power level'])
            args['message'] = "User added."

        with open('pages/user_add.html') as f:
            return chevron.render(f,args) 
        
if __name__ == "__main__":
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

    cherrypy.quickstart(App(),'/',conf)