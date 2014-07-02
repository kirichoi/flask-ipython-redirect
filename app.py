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
    ipythonify.str2py(archive, dirname, title, encin)
    notebook = ipythonify.jsonify(dirname, title)
    dstloc = os.path.join(os.path.join(dirname, title), title + '.ipynb')
    with open(dstloc, "w") as notebook_file:
        notebook_file.write(notebook)
    if 'win32' in sys.platform:
        ipy = sp.Popen("ipython notebook --no-browser --matplotlib inline --ip=0.0.0.0 --notebook-dir=" + '"' + os.path.join(dirname, title) + '"')
        processid = str(ipy.pid)
    elif 'linux' or 'darwin' in sys.platform:
        ipy = sp.Popen(["ipython", "notebook", "--no-browser", "--matplotlib", "inline", "--ip=0.0.0.0", "--notebook-dir=" + os.path.join(dirname, title)])
        processid = str(ipy.pid)
    #print "pid is " + processid
    return redirect('http://' + 'localhost:8888' + '/notebooks/' + title + '.ipynb', code=302)
    #return render_template('pickHost.html')
    
    
@app.route('/quit')
def q():
    global processid
    #print "pid is " + processid
    print "Killing IPython"
    if 'win32' in sys.platform:
        try: 
            os.system("taskkill /f /t /PID " + processid)
        except SyntaxError:
            pass
    elif 'linux' or 'darwin' in sys.platform:
        try:
            os.system("kill " + processid)
        except SyntaxError:
            pass
    processid = str()
    return render_template('pickHost.html')
    
    
@app.route('/spyder')
def openAsSpyder():
    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    ipythonify.str2py(archive, dirname, title, encin)
    dstloc = os.path.join(os.path.join(dirname, title), title + '.py')
    if 'win32' in sys.platform:
        sp.call("spyder " + '"' + dstloc + '"', shell=True)
    elif 'linux' or 'darwin' in sys.platform:
        sp.call(["spyder", dstloc], shell=True)
    return render_template('pickHost.html')


@app.route('/cloud')
def openAsCloud():
    title = request.args.get('title', type=str)
    host = request.args.get('host', type=str)
    return redirect('http://' + host + '/notebooks/' + title + '.ipynb', code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
