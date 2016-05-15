"""
Adaptive Cookies Check Test Server

Servers file from a directory passed at command line.
One of those files is considered the 'main' file. When I client
downloads this file it gets a cookie set, other files are only
downloaded after this cookie was set, otherwise it returns 403.
"""

import sys, optparse

from flask import Flask, request, send_from_directory, make_response, abort
app = Flask(__name__)

filepath = None
mainpath = None
maxage = 0
check_referer = False

@app.route('/<path:path>')
def get(path):
    ret = make_response(send_from_directory(filepath, path))

    if path == mainpath:
        if maxage > 0:
            ret.set_cookie('auth', '1', max_age=maxage)
    elif request.cookies.get('auth') == '1':
        pass
    elif check_referer and request.headers.get('Referer').endswith(mainpath):
        pass
    else:
        abort(403)

    return ret

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("-m", "--max-age", dest="maxage", default=0, type=int,
                      help="Cookie max age")
    parser.add_option("-r", "--referer", action="store_true", default=False,
                      dest="check_referer", help="Enforce HTTP Referer checking")

    (options, args) = parser.parse_args(sys.argv[1:])

    filepath = args[0]
    mainpath = args[1]

    maxage = options.maxage
    check_referer = options.check_referer

    app.run(host='0.0.0.0')
