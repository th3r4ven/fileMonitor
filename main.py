#  Copyright (c) 2020.
#  This code was designed and created by TH3R4VEN, its use is encouraged for academic and professional purposes.
#  I am not responsible for improper or illegal uses
#  Follow me on GitHub: https://github.com/th3r4ven

import hashlib
from datetime import datetime
from termcolor import colored
import pickle
from time import sleep
import subprocess as command
import os

if not os.geteuid() == 0:
    print("\nThis file requires high privileges, run as root or using sudo.")
    exit()


def getAllConfFiles():
    listinha = []
    # SSH config file
    listinha.append(["/etc/ssh/sshd_config", "ssh"])
    # User config file
    listinha.append(["/etc/passwd", "user"])
    # Network config file
    listinha.append(["/etc/network/interfaces", "network"])
    # DHCP config file
    listinha.append(["/etc/dhcp/dhclient.conf", "dhcp"])
    # DNS
    listinha.append(["/etc/resolv.conf", "dns"])
    # Password config file
    listinha.append(["/etc/shadow", "password"])

    listinha.append(["log.txt", "log"])

    return listinha


def setup():
    files = getAllConfFiles()
    data = {}
    for file in files:
        content = getContent(file[0])
        md5sum = getmd5sum(content)
        data[file[1]] = md5sum
        CreateBackupFile(file[1], content)
    savemd5(data)


def main():
    command.call(['clear'])
    setup()

    verify()


def verify():
    while True:
        files = getAllConfFiles()
        for file in files:
            key = file[1]
            content = getContent(file[0])
            md5sum = getmd5sum(content)

            md5Dict = getmd5()

            if md5Dict[key] != md5sum:
                print(colored("Seu arquivo localizado no " + file[0] + " foi alterado as " + str(getData()), 'red', attrs=['dark', 'bold']))
                resp = int(input(colored("\n1) Deseja voltar o backup do arquivo?\n2)Deseja salvar essa alteração no "
                                 "backup\n>>", 'red', attrs=['dark', 'bold'])))

                if resp == 1:
                    command.call(['clear'])
                    rollbackBackup(key, file[0])

                else:
                    command.call(['clear'])
                    saveNewbackup(key, file[0])
            else:
                pass

        sleep(10)


def rollbackBackup(prefix, file):
    with open('backup/' + prefix + '.config.bkp', 'rt') as arq:
        content = arq.read()
    arq.close()

    with open(file, 'wt') as arq:
        arq.write(content)
    arq.close()


def saveNewbackup(prefix, file):
    with open(file, 'rt') as arq:
        content = arq.read()
    arq.close()

    with open('backup/' + prefix + '.config.bkp', 'wt') as arq:
        arq.write(content)
    arq.close()


def getContent(filePath):
    with open(filePath, 'rt') as arq:
        content = arq.read()
    arq.close()

    return content


def getmd5sum(string):
    if type(string) != bytes:
        string = string.encode('utf-8')

    return hashlib.md5(string).hexdigest()


def savemd5(keys):
    with open('backup/md5.txt', 'wb') as arq:
        pickle.dump(keys, arq)
    arq.close()


def getmd5():
    with open('backup/md5.txt', 'rb') as arq:
        keys = pickle.load(arq)
    arq.close()

    return keys


def CreateBackupFile(prefix, content):
    with open('backup/' + prefix + '.config.bkp', 'wt') as arq:
        arq.write(content)
    arq.close()


def getData():
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def CreateBackup(md5sum):
    with open('md5_save', 'wt') as arq:
        arq.write(md5sum)
    arq.close()


# O arquivo log.txt deve ser usado para fazer os testes de backup, rollback e novo backup.

main()
