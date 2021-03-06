'''
Created on 19 Aug 2016

@author: romeokienzler
'''
from scipy.integrate import odeint
# import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, Response, redirect
import os
from cStringIO import StringIO
from rexec import RHooks


app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))

state="healthy"
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def Lorenz(state, t):
  # unpack the state vector
  x = state[0]
  y = state[1]
  z = state[2]


  # compute state derivatives
  xd = sigma * (y - x)
  yd = (rho - z) * x - y
  zd = x * y - beta * z

  # return the state derivatives
  return [xd, yd, zd]



@app.route('/')
def root():
    global state
    return 'Current state: '+state+'<p><a href="healthy">Switch to healthy</a><p><a href="broken">Switch to broken</a>'

@app.route('/data')
def lorenz():
    state0 = [2.0, 3.0, 4.0]
    t = np.arange(0.0, 30.0, 0.01)

    state = odeint(Lorenz, state0, t)
    x = np.array(t)
    x.shape = (3000, 1)
    returnValue = np.concatenate((x, state), axis=1)
    output = StringIO()
    np.savetxt(output, returnValue, delimiter=";", newline='\n')
    csv_string = output.getvalue()
    response = Response(csv_string, mimetype='text/csv')
    response.headers['Content-Disposition'] = u'attachment; filename=lorenz.csv'
    return response

@app.route('/healthy')
def healthy(): 
    global state
    global sigma
    global rho
    global beta 
    state="healthy"
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    return redirect("/", code=302)
  
@app.route('/broken')
def broken():
    global state
    global sigma
    global rho
    global beta 
    state="broken"
    sigma = 30.0
    rho = 128.0
    beta = 28.0 / 3.0
    return redirect("/", code=302)

@app.route('/test')
def test():
    global sigma
    global rho
    global beta 
    return str(sigma)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
#
