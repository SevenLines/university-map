import sys
from server.base import app, api

if __name__ == "__main__":
    print (sys.argv)
    try:
        port = int(sys.argv[1])
    except:
        port = 5000
    app.run(port=port)