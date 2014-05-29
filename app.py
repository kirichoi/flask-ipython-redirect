from flask import Flask, request, redirect, render_template
import ipythonify
import os, sys
import subprocess as sp

app = Flask(__name__)

home = os.path.dirname(sys.executable)
usrdir = os.path.expanduser('~')
dirname = os.path.join(usrdir, 'intPDF')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    return render_template('pickHost.html')


@app.route('/open')
def openAsNotebook():
    # host = request.args.get('host')

    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    ipythonify.pyprep(archive, dirname, title, encin)
    notebook = ipythonify.jsonify(os.path.join(dirname, title + '.py'), title)
    with open(os.path.join(dirname, title + '.ipynb'), "w") as notebook_file:
        notebook_file.write(notebook)
    dstloc = os.path.join(dirname, title + '.ipynb')
    sp.call('"' + os.path.join(home, "Scripts", "ipython") + '"' + " notebook" + " --matplotlib inline " + '"' +  dstloc + '"', creationflags = getattr(sp,"CREATE_NEW_CONSOLE",0))
    #return redirect('http://' + 'localhost:8888' + '/notebooks/' + title + '.ipynb', code=302)
    return render_template('pickHost.html')
    
    
@app.route('/spyder')
def openAsSpyder():
    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    ipythonify.pyprep(archive, dirname, title, encin)
    dstloc = os.path.join(dirname, title + '.py')
    sp.call([os.path.join(home, 'pythonw.exe'), os.path.join(home, 'Scripts', 'spyder'), dstloc], creationflags = getattr(sp,"CREATE_NEW_CONSOLE",0))
    return render_template('pickHost.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
