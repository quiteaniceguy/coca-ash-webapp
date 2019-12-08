from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit
from random import random
from threading import Thread, Event
from time import sleep
import gevent

#init stuff
message_index=0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shh...dont tell anyone'
app.config['DEBUG'] = True
socketio = SocketIO(app, async_mode = None, logger=True, engineio_logger=True)

###Thread for retrieving live data
thread = Thread()
thread_stop_event = Event()

#each element of messages_to and messages_from are iterated over in index.html
#for more than 1 message to/from make each array longer than one
messages_to = [
    "This is my first text message on ios7 This is my first text message on ios7",
    "This is my third text message on ios7",
    "This is my fifth text message on ios7",
    "This is my seventh text message on ios7"
]
messages_from = [
    "This is my second text message on ios7",
    "This is my fourth text message on ios7",
    "This is my sixth text message on ios7",
    "This is my eigth text message on ios7"
]


    
def dataRetr():
    print("making random nums")
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace = '/test')
        socketio.sleep(5)

@app.route('/', methods=['GET', 'POST'])
def index():
    global message_index
    #Suggestion: when values come in from a the model, take them and store them in the same form as messages_to[i] and messages_from[i], then rerender template with m_to and m_from set to those arrays

    if request.method == "POST":
        #switch between pre-defined conversations
        if "prev" in request.form:
            message_index-=1
        if "next" in request.form:
            message_index+=1
        if message_index >= len(messages_to):
            message_index=0;
        if  message_index <0:
            message_index = len(messages_to)-1
    #rerender
    return render_template("index.html", m_to=messages_to[message_index], m_from=messages_from[message_index])


@socketio.on('connect', namespace = '/test')
def test_connect():
    global thread
    print('Client connected')

    #start thread if not started
    if not thread.isAlive():
        print("Starting thread")
        thread = socketio.start_background_task(dataRetr)
    else:
        print("not starting thread")

@socketio.on('disconnect', namespace = '/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    #app.run()
    print("running application")
    socketio.run(app, user_reloader=False, debug=True)

