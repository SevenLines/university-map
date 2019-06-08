import sys

from sqlalchemy import text
from base import app, api, db

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test_connection':
        try:
            session = db.create_scoped_session()
            session.execute('SELECT 1')
        except:
            raise
        else:
            print("connection is allright")
            exit(0)

    print(sys.argv)
    try:
        port = int(sys.argv[1])
    except:
        port = 8000
    app.run(port=port)