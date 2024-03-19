#!/usr/bin/python3

import os.path
import tornado.httpserver
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
# from hardware folder load the board_ctrl.py
from hardware import board_ctrl
import time
import json
from copy import deepcopy
import requests
import logger

# following are the parameter used for server.py
# port =8000 is used by the browser. 
# If the IP address of Raspberry Pi is 192.16.2.200, enter http://192.168.2.200:8000
port = 8000
define("port", default=port, type=int)
name = ""
login_id = ""
login_pw = ""
LED_pin_arr = []


# BaseHandler is the starting point of server_py when a browser execute the hyberlink http://192.168.2.200:8000
class BaseHandler(RequestHandler):
    # u"/login" means ask the browser jump to login.html
    def get_login_url(self):
        return u"/login"

    # get the cookie from the browser using the name "user" and put the cookie in the user_json file
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        # if there are data in the user_json file, then ask tornado to decode the data
        # else do nothing
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

class LoginHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        # name and error are parameters pass to login.html
        self.render('login.html', name=name, error="To login, pls type your username & password")
#error=None
    def post(self):
        # check_user is a function within LoginHandler
        # get the user and password entered by the user and pass to function "check_user" for validation
        ret = self.check_user(self.get_argument('user'), self.get_argument('password'))
        if ret:
            # if validation pass, pass the username to another function within this handler
            self.set_current_user(self.get_argument('user'))
            self.redirect('/')
        else:
            # if validaton fail, reload the login.html so that the user can try again 
            # name and error are parameters pass to login.html 
            self.render('login.html', name=name, error="Invalid user id or password")

    # login_id and login_pw are data retrieve from file conf.json
    def check_user(self, user, password):
        result = False
        if user == login_id and password == login_pw:
            # check if the "user" and "password" entered by user match with the data retrieve from conf.json
            result = True
        return result

    # save the user name to the cookie of the browser under the name "user"
    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user), expires=time.time()+3600)
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):
    def get(self):
        # clear the cookie in the browser using the name "user"
        self.clear_cookie("user")
        # goto login.html
        self.redirect("/login")

class ConfigHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # name and conf are parameters pass to config.html 
        self.render('config.html',name=name,json_data=conf)

    def post(self):
        log.info("config.html post")
        data = json.loads(self.request.body)
        # Save the JSON data to a file
        log.info(data)
        with open('conf.json', 'w') as file:
            json.dump(data, file)
        self.write('Data saved successfully')
        load_conf()

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # name and LED_pin_arr are parameters pass to index.html 
        self.render('index.html', name=name, LED_pin_arr=LED_pin_arr)
        
    def post(self):
        key = self.get_argument('key', None)
        id = self.get_argument('id', None)
        if (key != None):
            if (key == 'cpu_temp'):
                # from board_ctrl.py function get_cpu_temp
                # self.write send string to index.html as msg
                cpuTemp = board_ctrl.get_cpu_temp()
                self.write(cpuTemp) 
                log.info('CPU temperature is {}'.format(cpuTemp))
                
            if (key == 'LED_status'):
                ret = deepcopy(LED_pin_arr)
                log.info('ret {}'.format(ret))
                for index, LED in enumerate(LED_pin_arr):
                    # from board_ctrl.py 
                    status = board_ctrl.LED_status(LED['pin'])
                    ret[index]['status'] = status
                self.write(json.dumps(ret))
                log.info('json dump {}'.format(json.dumps(ret)))
            if (id != None):
                id = int(id)
                if (key == 'LED_on'):
                    # from board_ctrl.py
                    board_ctrl.LED_on(id)
                    # from board_ctrl.py
                    ret = board_ctrl.LED_status(id)
                    self.write(key)
                    log.info('[Local] LED {} On - status: {}'.format(id, ret))

                if (key == 'LED_off'):
                    board_ctrl.LED_off(id)
                    ret = board_ctrl.LED_status(id)
                    self.write(key)
                    log.info('[Local] LED {} Off - status: {}'.format(id, ret))

@gen.coroutine
# load parameters from file conf.json into server.py
def load_conf():
    global name, login_id, login_pw, LED_pin_arr, conf
    # Open the file and read its contents
    file = open('conf.json', 'r', encoding='utf8')
    json_data = file.read()
    # Parse the JSON string into a Python object
    conf = json.loads(json_data)
    log.info(f"conf={conf}")
    name = conf['name']
    log.info(f"name={name}")
    login_id = conf['login_id']
    login_pw = conf['login_pw']
    LED_pin_arr = conf['LED_pin_arr']
    log.info(f"LED_pin_arr={LED_pin_arr}")
    file.close()
    log.info("configuration loaded")

##########################
# Server.py starts here
##########################
if __name__ == "__main__":
    try:
        requests.packages.urllib3.disable_warnings()
        log = logger.getLogger('server.py')
        log.debug('Program started')
        # load all parameters from json.conf
        load_conf()

        settings = dict(
            # set folder "template" and "static" under current path 
            # "template" stores the html files
            # "static" stores css, javascript and image files
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # when saving cookie, there is a key "dw7^&bPjqm(*Vsud!PkAs%jki1093d" for encoding
            cookie_secret="dw7^&bPjqm(*Vsud!PkAs%jki1093d",
            #login_url="/login",
            debug=True
        )

        # set different url path to defined Handler
        app = Application(
            handlers=[
                (r'/', IndexHandler),
                (r'/login', LoginHandler),
                (r'/logout', LogoutHandler),
                (r'/saveConfig', ConfigHandler),
            ], **settings
        )
        # listening at port 8080 and wait for anybody coming in using browser
        app.listen(port, address='0.0.0.0')
        log.info('listening....')
        # keep waiting for anybody coming in
        IOLoop.instance().start()
    except KeyboardInterrupt:
        log.info('Program terminated manually')
    except Exception as e:
        log.error('Program terminated unexpectedly: %s' % e)