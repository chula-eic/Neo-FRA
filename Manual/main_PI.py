from multiprocessing import Process
import PIsocket
import WebCamClient

IP = '172.16.0.126'
if __name__ == "__main__":
    try:
        p1 = Process(target=PIsocket.start, args=(IP, 6783))
        p2 = Process(target=WebCamClient.start, args=(IP, 8554))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        #_thread.start_new_thread(PCsocket.start, (6783,))
        print('subprocess started')
    except Exception as e:
        print(e)
