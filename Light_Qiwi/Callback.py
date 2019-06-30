# -*- coding: utf-8 -*-
import cherrypy


class LightQiwiCallback(object):

    def __init__(self):
        cherrypy.quickstart(self, '/')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        data = cherrypy.request.json
        print(data)
