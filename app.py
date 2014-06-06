from flask import Flask, request, render_template
from flask import g, redirect
import ipythonify
import os, sys
import subprocess as sp

app = Flask(__name__)

home = os.path.dirname(sys.executable)
usrdir = os.path.expanduser('~')
dirname = os.path.join(usrdir, 'intPDF')
processid = str()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    return render_template('pickHost.html')


@app.route('/open')
def openAsNotebook():
    global processid
    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    ipythonify.pyprep(archive, dirname, title, encin)
    notebook = ipythonify.jsonify(dirname, title)
    dstloc = os.path.join(os.path.join(dirname, title), title + '.ipynb')
    with open(dstloc, "w") as notebook_file:
        notebook_file.write(notebook)
    
    if 'win32' in sys.platform:
        ipy = sp.Popen("ipython notebook --matplotlib inline " + '"' + dstloc + '"')
        processid = str(ipy.pid)
    elif 'linux' or 'darwin' in sys.platform:
        #import pwd
        #usrname = pwd.getpwuid(os.getuid())[0]
        ipy = sp.Popen(["ipython", "notebook", "--matplotlib inline", dstloc])
        processid = str(ipy.pid)
        #g.ipython = sp.Popen(["gnome-terminal","--working-directory=/home/" + usrname, "-e", "ipython", "notebook", "--matplotlib inline", dstloc])
    #return redirect('http://' + 'localhost:8888' + '/notebooks/' + title + '.ipynb', code=302)
    print "pid is" + processid
    return render_template('pickHost.html')
    
    
@app.route('/quit')
def q():
    global processid
    print "pid is " + processid
    if 'win32' in sys.platform:
        try: 
            os.system("taskkill /f /PID " + processid)
        except SyntaxError:
            pass
    elif 'linux' or 'darwin' in sys.platform:
        try:
            os.system("kill " + processid)
        except SyntaxError:
            pass
    processid = str()
    print "Killing IPython"
    return render_template('pickHost.html')
    
    
@app.route('/spyder')
def openAsSpyder():
    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    ipythonify.pyprep(archive, dirname, title, encin)
    dstloc = os.path.join(os.path.join(dirname, title), title + '.py')
    if 'win32' in sys.platform:
        sp.call("spyder " + '"' + dstloc + '"', shell=True)
    elif 'linux' or 'darwin' in sys.platform:
        sp.call(["spyder", dstloc], shell=True)
    #creationflags = getattr(sp,"CREATE_NEW_CONSOLE",0))
    return render_template('pickHost.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
