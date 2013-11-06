import ftplib


def PUT(ftp, fileName):
    with open(fileName, 'rb') as fp:
        ftp.storbinary("STOR " + fileName, fp)
    print 'UPLOAD COMPLETE'

def GET(ftp, fileName):
    with open(fileName, 'wb') as fp:
        ftp.retrbinary("RETR " + fileName, fp.write())
    print 'DOWNLOAD COMPLETE'
    
def PWD(ftp):
    print "PWD:" + ftp.pwd()

def CWD(ftp, path):
    ftp.cwd(path)

def NLST(ftp, path):
    fileList = ftp.nlst(path)
    for name in fileList:
        print name[2:],
    print 

if __name__ == "__main__":
    host = raw_input("input host name : ")
    username = raw_input("input user name : ")
    passwd = raw_input("input passward : ")
    ftp = ftplib.FTP(host, username, passwd)
    while True:
        command = raw_input(">> ").split()
        if command[0] == "put":
            PUT(ftp, command[1])
        elif command[0] == "get":
            GET(ftp, command[1])
        elif command[0] == "pwd":
            PWD(ftp)
        elif command[0] == "cd":
            CWD(ftp, command[1])
        elif command[0] == "ls":
            if len(command) >= 3:
                print 'Usage : ls [path]'
                continue
            elif len(command) == 1:
                command.append('./')
            NLST(ftp, command[1])
        elif command[0] == "quit":
            ftp.quit()
            break
        
