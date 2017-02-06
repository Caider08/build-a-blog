
import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class MainBlog(webapp2.RequestHandler):
    def get(self):
        pass
        #self.response.write('Your 5 most recent Posts!')

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        self.response.write(id)


app = webapp2.WSGIApplication([
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/', MainHandler),
    ('/blog', MainBlog)
], debug=True)
