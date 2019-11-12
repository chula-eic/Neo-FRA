import _thread
import PCsocket
import WebCamServer

try:
    _thread.start_new_thread(PCsocket.start, (6783,))
    print('thread started')
except Exception as e:
    print(e)
WebCamServer.start(8554)