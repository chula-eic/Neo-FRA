#import _thread
from multiprocessing import Process
import PCsocket
import WebCamServer

if __name__ == "__main__":
    try:
        p1 = Process(target=PCsocket.start, args=(6783,))
        p2 = Process(target=WebCamServer.start, args=(8554,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        #_thread.start_new_thread(PCsocket.start, (6783,))
        print('subprocess started')
    except Exception as e:
        print(e)
