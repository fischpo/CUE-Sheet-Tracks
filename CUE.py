import os
import subprocess
import argparse


def validate_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} does not exist.")
    return path


def validate_album_art(image_path):
    valid_extensions = ['.png','.jpg','.jpeg','.webp']
    if not os.path.isfile(image_path):
        raise argparse.ArgumentTypeError(f"Album art file {image_path} does not exist.")
    
    if not os.path.splitext(image_path)[1].lower() in valid_extensions:
        raise argparse.ArgumentTypeError(f"Album art file {os.path.basename(image_path)} has an unsupported extension.")
    
    return image_path


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
    
def chaff(time):
    min,sec=time.split(':')
    min=int(min)
    sec=int(sec)
    if min>59:
        hr=min//60
        min%=60
        if hr==0:
            return "%02d:%02d" % (min, sec)
        elif hr < 10:
            return "0%0d:%02d:%02d" % (hr, min, sec)
        else:
            return "%d:%02d:%02d" % (hr, min, sec)
    return time
    
def validtitle(name):
    for inva in ['/','\\','?','%','*',':', '|', '”', '<','>']:
        if inva in name:
            name=name.replace(inva,'')
    return name

def main(args):
    repm = args.i
    if args.o:
        dspth = args.o
    else:
        dspth=""
    
    print("\nLocation of CUE:", repm)
    print("Extract Location:", dspth)

    if args.c:
        asmodeus = args.c
        print("Custom Album Art:",os.path.basename(asmodeus))
    reps=os.listdir(repm)
    treatgm=0
    for rep in reps:
     if rep.lower().endswith('.cue'):
        treatgm=1
        chk=0
        rep=os.sep.join([repm,rep])
        for i in ['flac','m4a','mp3','aac','wav','ogg']:
            loc=rep[:-3]+i
            if os.path.exists(loc):
                chk=1
                break
        if chk:
            datacu=cuedata(rep)
            mfile=loc
            ext=loc[loc.rindex('.'):]
            if not args.c:
             cimg=["ffmpeg","-hide_banner","-y","-i",mfile,"-an","-vcodec","copy","cover.png"]
             aimg=subprocess.run(cimg,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
             asmodeus='cover.png'
            a=0
            b=0
            wolfe=0
            entrit=len(datacu[b'TITLE'])
            entri=len(datacu[b'INDEX'])
            if entrit==entri:
                adde=1
            elif entri==2*entrit:
                adde=2
            else:
                print("\nCue has some missing timestamps.")
                exit()
            print("\n","—"*55)
            for i in datacu[b'TITLE']:
                i=i.decode('utf-8')
                ior=validtitle(i)
                otfl=f'{ior+"_tmp"+ext}'
                otfl_fn=f'{ior+ext}'
                if dspth:
                    otfl=os.sep.join([dspth,otfl])
                    otfl_fn=os.sep.join([dspth,otfl_fn])
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
                stime=chaff(stime)
                a+=1
                b+=adde
                trno=f'track={a}'
                print(f"TRACK {a}: {i}")
                if wolfe:
                    if ext!='.flac':
                     cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-avoid_negative_ts","make_zero","-c","copy","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                    else:
                     cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-avoid_negative_ts","make_zero","-map","0","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                
                if ext!='.flac':
                    cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-t",diff,"-avoid_negative_ts","make_zero","-c","copy","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                else:
                    cmd=["ffmpeg","-hide_banner","-ss",stime,"-y","-i",mfile,"-t",diff,"-map","0","-metadata",tit,"-metadata",artt,"-metadata",trno,otfl]
                aa=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                cimgad=['ffmpeg','-hide_banner','-y','-i',otfl,'-i',asmodeus,'-map','0:a','-map','1','-codec','copy','-metadata:s:v','title="Album cover"','-metadata:s:v','comment="Cover (front)"','-disposition:v','attached_pic',otfl_fn]
                aimgad=subprocess.run(cimgad, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if b"No such file or directory" in aimgad.stdout:
                    subprocess.run(['ffmpeg','-hide_banner','-y','-i',otfl,'-c:v','copy','-c:a','copy',otfl_fn],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                os.remove(otfl)

            if not args.c:
                try:
                    os.remove(asmodeus)
                except:
                    pass
        else:
            print("\nAudio file not found.")
    if not treatgm:
     print("\nNo CUE file found.")        

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Extract tracks from a file with CUE sheet.Also can add custom album art to the tracks.")
    parser.add_argument("-i", help="Path to the CUE file", type=validate_path,required=True)
    parser.add_argument("-o", help="Path where to extract files", type=validate_path,required=False)
    parser.add_argument("-c", help="Optional path to custom album cover art image for the tracks", type=validate_album_art, required=False)
    
    args = parser.parse_args()
    
    main(args)
