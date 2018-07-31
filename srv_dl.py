from flask import Flask, send_from_directory, make_response, request, current_app, redirect, jsonify
from functools import update_wrapper
from sys import argv
from os.path import exists, dirname, basename, join
from os import walk, mkdir
from datetime import timedelta

app = Flask('download_srv')

download_path = '/download/'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def index():
    return 'downlaod service'

@app.route('/download', defaults={'path': ''})
@app.route('/download/<path:path>')
@crossdomain(origin='*')
def download(path):

    if not path:
        for dirpath, dirnames, filenames in walk(download_path):
            return str(filenames)

        return 'Download folder is empty.'

    else:
        file_abs_path = join(download_path, path)
        if exists(file_abs_path):

            dirpath = dirname(file_abs_path)
            filename = basename(file_abs_path)

            print 'trying to provide download service :\n package: {}/{}'.format(dirpath,filename)
            return send_from_directory(directory=dirpath, filename=filename, as_attachment=True)

        else:
            return '"{}" is no longer available.'.format(path)

def main():
    if not exists(download_path):
        mkdir(download_path)

    app.run(host='0.0.0.0', port=8080, debug=True);

if __name__ == '__main__':
    '''
    if len(argv) != 2:
        print "invalid usage -\n  $ python {arg0} {{file_path}}".format(arg0=argv[0])
        exit()

    if not exists(argv[1]):
        print 'not a valid target.'
        print argv[1]
        exit()
    '''

    main()
