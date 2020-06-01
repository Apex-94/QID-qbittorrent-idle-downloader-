import win32gui
import time
import ctypes
import os


from qbittorrent import Client

qb = Client('http://127.0.0.1:8080/')

qb.login('admin', 'adminadmin')
# not required when 'Bypass from localhost' setting is active.
# defaults to admin:admin.
# to use defaults, just do qb.login()

torrents = qb.torrents(filter = 'downloading')
l=[]
# for torrent in torrents:
#     print (torrent['name'])
# Flag_idle = False

def Torrent_pause(Flag_idle):
    global l
    if Flag_idle == False:
        qb.pause_multiple(l)


def Torrent_resume(Flag_idle):
    global l
    if Flag_idle == True:
        qb.resume_multiple(l)





def lock_pc():
    global Flag_idle
    Flag_idle = True
    print("Idle")
    print(Flag_idle)
    Torrent_resume(Flag_idle)
    


def divide():
    log('*-*'*20, icon=None)


def log(log_txt, icon="[+]"):
    full_path = os.getcwd() + '\\log.txt'

    if os.path.exists(full_path):
        with open(full_path, 'a') as f:
            if icon is not None:
                f.write(icon + " " + log_txt + "\n")
            else:
                f.write(log_txt + "\n")
    else:
        with open(full_path, 'w') as f:
            if icon is not None:
                f.write(icon + " " + log_txt + "\n")
            else:
                f.write(log_txt + "\n")


def Main():
    divide()
    log(str(time.ctime(time.time())), icon="[<>]")
    divide()
    log("Starting..")

    orig_cords = win32gui.GetCursorPos()
    log("Original Cords :{}".format(str(orig_cords)))

    global l
    d={}
    for torrent in torrents:
        name = (torrent['name'])
        info_hash = (torrent['hash'])
        # d.add(name,info_hash)
        d[name] = info_hash
    l = list(d.values())
    # print(l)
    checks = 0
    while True:
        new_cords = win32gui.GetCursorPos()
        # start_time = time.time()
        if new_cords == orig_cords:
            checks += 1
            # log("Checks = {}".format(str(checks)))
            if checks > 30:
                # log("Locking PC...", icon="[!X!]")
                lock_pc()

                # print("--- %s seconds ---" % (time.time() - start_time))

                #break
            else:
                # log("Orig Cords: {}, New Cords: {}".format(str(orig_cords), str(new_cords)))
                # log("Sleeping for 15 secs...")
                time.sleep(60)
        else:
            orig_cords = new_cords
            # log("Orig cords equals new cords now, {}".format(str(new_cords)))
            # log("Sleeping for 15 secs...")
            time.sleep(60)
            checks = 0
            # log("Reset checks... Checks = {}".format(str(checks)))
            global Flag_idle
            Flag_idle = False
            print("Not Idle")
            print(Flag_idle)
            Torrent_pause(Flag_idle)



    # log("Exiting..")
    # divide()
    # exit(0)

if __name__ == "__main__":
    Main()

