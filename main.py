import os
import requests
import zipfile
import shutil
import time


ignore =[
    "ns_startup_args.txt","ns_startup_args_dedi.txt","mod.json","autoexec_ns_server.cfg"
]


def moveFromTemp(path,fresh:bool):
    for root, dirs, files in os.walk(os.path.join(path,'temp')):
        for file in files:
            #append the file name to the list
            f = os.path.join(root,file)
            if(ignoreF(file=f,ignore=ignore,fresh=fresh)):
                with open(f,"rb") as tf:
                    pfp = f.replace('\\temp','').rsplit('\\',1)[0]
                    if not os.path.exists(pfp):
                        os.makedirs(pfp)
                    with open(f.replace('\\temp',''),"wb") as pf:
                        pf.write(tf.read())

def ignoreF(ignore: list,file: str,fresh: bool) -> bool:
    if fresh:
        for i in ignore:
            if str(file.replace(os.path.dirname(os.path.realpath(__file__)),'')).find(i) != -1:
                #with open(file,"r") as f:
                #    safestuff[file.replace(os.path.dirname(os.path.realpath(__file__)),'')] = {file,f.read()}
                return False
    return True

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    fre = os.path.exists(os.path.join(path,'NorthstarLauncher.exe'))
    fr = requests.get(url='https://api.github.com/repos/R2Northstar/Northstar/releases')
    frj = fr.json()[0]
    #print(fr.json())
    
    print("Downloading latest Northstar version...\n")
    r = requests.get(url=frj["assets"][0]["browser_download_url"])
    print("Finished Download...\nCreating temp files")

    with open(os.path.join(path,'temp.zip'),"wb") as f:
       f.write(r.content)
    with zipfile.ZipFile(os.path.join(path,'temp.zip')) as z:
        z.extractall(os.path.join(path,'temp'))

    moveFromTemp(path,fre)

    print("Finished intalling. Removing temp files")

    shutil.rmtree(os.path.join(path,'temp'))
    os.remove(os.path.join(path,'temp.zip'))
    print("Done")
    

if __name__ == "__main__":
    main()