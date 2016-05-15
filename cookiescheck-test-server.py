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
maxage = None
referer = None

@app.route('/<path:path>')
def get(path):
    ret = make_response(send_from_directory(filepath, path))

    if path == mainpath:
        ret.set_cookie('auth', '1', max_age=maxage)
        if referer:
            ret.headers['Referer'] = referer
    elif request.cookies.get('auth') == '1':
        pass
    elif referer and request.headers.get('referer') == referer:
        pass
    else:
        abort(403)

    return ret

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("-m", "--max-age", dest="maxage", default=0, type=int,
                      help="Cookie max age")
    parser.add_option("-r", "--referer",
                      dest="referer", default="",
                      help="HTTP referer")

    (options, args) = parser.parse_args(sys.argv[1:])

    filepath = args[0]
    mainpath = args[1]

    if options.maxage:
        maxage = options.maxage

    if options.referer:
        referer = options.referer

    app.run(host='0.0.0.0')
