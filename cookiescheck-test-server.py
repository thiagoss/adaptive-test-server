"""
Adaptive Cookies Check Test Server

Servers file from a directory passed at command line.
One of those files is considered the 'main' file. When I client
downloads this file it gets a cookie set, other files are only
downloaded after this cookie was set, otherwise it returns 403.
"""

import sys

from flask import Flask, request, send_from_directory, make_response, abort
app = Flask(__name__)

filepath = None
mainpath = None
maxage = None

@app.route('/<path:path>')
def get(path):
    ret = make_response(send_from_directory(filepath, path))

    if path == mainpath:
        ret.set_cookie('auth', '1', max_age=maxage)
    elif request.cookies.get('auth') == '1':
        pass
    else:
        abort(403)

    return ret

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print "Usage: %s <dir-to-serve> <main-file> [max-age (seconds / optional)]"
        sys.exit(1)

    print sys.argv
    filepath = sys.argv[1]
    mainpath = sys.argv[2]
    if len(sys.argv) > 3:
      maxage = int(sys.argv[3])
    app.run(host='0.0.0.0')

