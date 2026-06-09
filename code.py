from livereload import Server

# Folder where your website files are located
WATCH_FOLDER = "."

server = Server()

# Watch all common website files
server.watch("*.html")
server.watch("*.css")
server.watch("*.js")
server.watch("*.py")
server.watch("static/*")
server.watch("templates/*")

# Serve the website
server.serve(
    root=WATCH_FOLDER,
    host="127.0.0.1",
    port=5500,
    open_url=True
)
