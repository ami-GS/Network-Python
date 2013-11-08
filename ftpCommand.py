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

def RENAME(ftp, fromName, toName):
    ftp.rename(fromName, toName)
    print "file name was changed " + fromName + " -> " + toName

def MAKEDIR(ftp, name):
    ftp.mkd(name)

def SIZE(ftp, name):
    print ftp.size(name)
	
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
        elif command[0] == "mv":
            if len(command) != 3:
                print "Usage : mv [fromName] [toName]"
            RENAME(ftp, command[1], command[2])
        elif command[0] == "mkdir":
            if len(command) != 2:
                print "Usage : mkdir dirName"
        elif command[0] == "du":
            if len(command) == 2:
                SIZE(ftp, command[1])
            
        elif command[0] == "quit":
            ftp.quit()
            break
        else:
            print "command " + command[0] + " is not defined"  
