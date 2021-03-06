
import webapp2
import jinja2
import os
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def render_front(self, title="", blog="", error=""):

        blogs = db.GqlQuery("SELECT * FROM BlogPost order by created DESC limit 5")
        self.render("main-blog.html", title=title, blog=blog, error=error, blogs=blogs)

    def get(self):
        self.render_front()


class MainBlog(Handler):
    def render_front(self, title="", blog="", error=""):

        blogs = db.GqlQuery("SELECT * FROM BlogPost order by created DESC limit 5")
        self.render("main-blog.html", title=title, blog=blog, error=error, blogs=blogs)

    def get(self):
        self.render_front()

class ViewPostHandler(Handler):
    def render_front(self, title="", blog="", error=""):
        self.render("grabbedblog.html", title=title, blog=blog, error=error)


    def get(self, id):
        grabbedblog = BlogPost.get_by_id(int(id))
        if not grabbedblog:
            self.response.write("That's not an existing blog id")
        else:
            title = grabbedblog.title
            blog = grabbedblog.blog
            self.render("grabbedblog.html", title=title, blog=blog, grabbedblog=grabbedblog)


class NewPost(Handler):
    def render_front(self, title="", blog="", error=""):

        blogs = db.GqlQuery("SELECT * FROM BlogPost order by created DESC limit 5")
        self.render("new-post.html", title=title, blog=blog, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            a = BlogPost(title = title, blog = blog)
            a.put()
            aid = str(a.key().id())
            #self.response.write(aid)
            time.sleep(1.0)
            #self.redirect('/')
            self.redirect('/blog/'+aid)
        else:
            error = "we need both a title and some story brah!"
            self.render("new-post.html", title=title, blog=blog, error=error)




app = webapp2.WSGIApplication([
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/', MainHandler),
    ('/blog', MainBlog),
    ('/new-post', NewPost)
], debug=True)
