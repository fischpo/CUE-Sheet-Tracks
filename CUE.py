import os
import sys
import subprocess
metadata={b"TITLE":[],b"PERFORMER":[],b"INDEX":[],b"REM COMPOSER":[]}
def timedif(i1,i2):
    i1,i2=i1.split(":"),i2.split(":")
    a=(int(i1[0])*60)+int(i1[1])
    b=(int(i2[0])*60)+int(i2[1])
    return b-a
def cuedata(pth):
 with open(pth,"+r",encoding="utf-8") as ff:
  f=ff.read()
  k=f.encode('utf-8')
 ff=k.split(b"TRACK")
 ff.pop(0)
 for i in ff:
  for spi in i.split(b"\n"):
    for ky in metadata:
        if ky in spi:
            if ky==b"INDEX":
                spi=spi.split(ky)[1].strip().split(b" ")[1]
            else:
                spi=spi.split(ky)[1].strip().strip(b'""')
            metadata[ky].append(spi)
            break
 return metadata
def validtitle(name):
    for inva in ['/','\\','?','%','*',':', '|', '”', '<','>']:
        if inva in name:
            name=name.replace(inva,'')
    return name
def main(arg=sys.argv[1:]):
    if arg:
        if os.path.isfile(arg[0]):
            if os.path.splitext(arg[0])[1].lower() in ['.png','.jpg','.jpeg','.webp']:
                asmodeus=arg[0]
            else:
                print(f"The extension of the file '{arg[0]}' is unrecognised.")
                exit()
        else:
            print(f"The path '{arg[0]}' is not valid.")
            exit()
    while True:
        repm=input("Location of CUE:")
        if repm.lower()=="break":
            exit()
        if not os.path.exists(repm):
            print('Location not valid.Try again or use "break" to exit')
        else:
            break
    while True:
        dspth=input("\nExtract Location:")
        if dspth=="":
            break
        if dspth.lower()=="break":
            exit()
        if not os.path.exists(dspth):
            print("Location not valid.Press Enter or enter a valid location")
        else:
            break
    reps=os.listdir(repm)
    treatgm=0
    for rep in reps:
     if rep.lower().endswith('.cue'):
        treatgm=1
        chk=0
        rep=repm+"\\"+rep
        for i in ['flac','m4a','mp3','aac','wav','ogg']:
            loc=rep[:-3]+i
            if os.path.exists(loc):
                chk=1
                break
        if chk:
            datacu=cuedata(rep)
            mfile=loc
            ext=loc[loc.rindex('.'):]
            if not arg:
             cimg=["ffmpeg","-hide_banner","-y","-i",mfile,"-an","-vcodec","copy","cover.png"]
             aimg=subprocess.run(cimg,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
             asmodeus='cover.png'
            a=0
            b=0
            wolfe=0
            print("\n","—"*55)
            for i in datacu[b'TITLE']:
                i=i.decode('utf-8')
                ior=validtitle(i)
                otfl=f'{ior+"_tmp"+ext}'
                otfl_fn=f'{ior+ext}'
                if dspth:
                    otfl=dspth+"\\"+otfl
                    otfl_fn=dspth+"\\"+otfl_fn
                tit=f'title={i}'
                artt='artist='+datacu[b'PERFORMER'][a].decode('utf-8')
                atime=datacu[b'INDEX'][b:b+2]
                if len(atime)==1:
                    wolfe=1
                    stime=atime[0].decode('utf-8')
                else:
                 stime,etime=atime[0].decode('utf-8').strip(),atime[1].decode('utf-8').strip()
                 diff=str(timedif(stime,etime))
                stime=stime.rsplit(":",1)[0]
                a+=1
                b+=2
                trno=f'track={a}'
                print(f"TRACK {a}: {i}")
                if wolfe:
                    if ext!='.flac':
                     cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-avoid_negative_ts","make_zero","-c","copy","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                    else:
                     cmd=cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-avoid_negative_ts","make_zero","-map","0","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                
                if ext!='.flac':
                    cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-t",diff,"-avoid_negative_ts","make_zero","-c","copy","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                else:
                    cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-t",diff,"-map","0","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                aa=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                cimgad=['ffmpeg','-hide_banner','-y','-i',otfl,'-i',asmodeus,'-map','0:a','-map','1','-codec','copy','-metadata:s:v','title="Album cover"','-metadata:s:v','comment="Cover (front)"','-disposition:v','attached_pic',otfl_fn]
                aimgad=subprocess.run(cimgad, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                os.remove(otfl)
            if not arg:
             os.remove(asmodeus)
        else:
            print("\nAudio file not found.")
    if not treatgm:
     print("\nNo CUE file found.")        
if __name__=='__main__':
  main()