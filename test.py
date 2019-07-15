import tornado.web
import tornado.ioloop
import tornado.httpserver
import os
import os.path


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/", Index),
                    (r"/delete", Delete),
                    (r"/download", Download),
                    (r"/upload", Upload)
                    ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class Upload(tornado.web.RequestHandler):

    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        file_metas = self.request.files['upload']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
        files = getfiles()
        files.sort()
        self.render("index.html", filelist=files)


class Download(tornado.web.RequestHandler):

    def get(self):
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        filename = self.get_argument('filename')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header(
            'Content-Disposition', 'attachment; filename=' + filename)
        filepath = os.path.join(upload_path, filename)
        buf_size = 4096
        with open(os.path.join('', filepath), 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()


class Delete(tornado.web.RequestHandler):

    def get(self):
        fileurl = self.get_argument("fileurl")
        os.remove(os.getcwd() + fileurl)
        files = getfiles()
        files.sort()
        self.render("index.html", filelist=files)


class Index(tornado.web.RequestHandler):

    def get(self):
        files = getfiles()
        files.sort()
        self.render("index.html", filelist=files)


def getfiles():
    filels = []
    filespath = os.getcwd() + "/files/"
    for files in os.walk(filespath):
        for f in files[2]:
            filels.append(("/files/" + f, f))
    return filels[:]


if __name__ == "__main__":
    httpserver = tornado.httpserver.HTTPServer(Application())
    httpserver.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
