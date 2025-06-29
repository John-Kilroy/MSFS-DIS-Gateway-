import os
import subprocess
from pymxs import runtime as rt

MAX2021 = 23000

def getP4info():
    """
    :return:
    clientName, clientRootFolder, clientStream
    """
    cmd = "p4 info"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate()
    exit_code = process.returncode
    
    if exit_code == 0:
            info = dict()
            if rt.maxversion()[0]>=MAX2021:
                datas = str(stdoutdata.decode("utf-8")).split("\r\n")
            else:            
                datas = (str(stdoutdata)).split("\r\n") 
            for data in datas:
                if data:
                    key = data.split(": ")[0]
                    value = data.split(": ")[1]
                    info.update({key: value})
            if "Client stream" in info:
                return info["Client name"], info["Client root"],info["Client stream"],info["User name"]
            else: 
                return info["Client name"], info["Client root"],"",info["User name"]
        

def P4delete(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 delete -c {0} -v {1}".format(changelistName,filePath )
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd


def P4edit(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 add -c {0} -v {1} | p4 edit -c {0} -v {1} -t restricted".format(changelistName,filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait() #wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd


def P4add(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 add -c {0} -v {1}".format(changelistName,filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd

def P4revert(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 revert -c {0} -w {1}".format(changelistName, filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        os.system('cmd /c "{0}"'.format(cmd))
        print(cmd)

def P4createChangelist(changelistName):
    #empthy changelist
    if changelistName:
        cmd = 'p4 --field "Description={0}" --field "Files=" change -t restricted -o | p4 change --t restricted -i'.format(changelistName )
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd