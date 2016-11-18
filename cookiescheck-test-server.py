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
user_agent = None

@app.route('/<path:path>')
def get(path):
    ret = make_response(send_from_directory(filepath, path))

    if path == mainpath:
        ret.location = "http://%s/%s" % (request.headers.get('Host'), path)
        if maxage > 0:
            ret.set_cookie('auth', '1', max_age=maxage)
    else:
        emit_error = False
        if maxage and request.cookies.get('auth') != '1':
            emit_error = True
        if check_referer and not request.headers.get('Referer').endswith(mainpath):
            emit_error = True
        if user_agent and request.headers.get('User-Agent') != user_agent:
            emit_error = True

        if emit_error:
            abort(403)

    return ret

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("-m", "--max-age", dest="maxage", default=0, type=int,
                      help="Cookie max age")
    parser.add_option("-r", "--referer", action="store_true", default=False,
                      dest="check_referer", help="Enforce HTTP Referer checking")
    parser.add_option("-u", "--user-agent", dest="user_agent", default="",
                      help="HTTP User-Agent filter")

    (options, args) = parser.parse_args(sys.argv[1:])

    filepath = args[0]
    mainpath = args[1]

    maxage = options.maxage
    check_referer = options.check_referer
    user_agent = options.user_agent

    app.run(host='0.0.0.0')
