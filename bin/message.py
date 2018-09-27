import sys
from subprocess import Popen, PIPE ,STDOUT
filename1=sys.argv[1]
filename2=sys.argv[2]
print("python {} {}".format(filename1,filename2))
string=''
p=Popen([sys.executable,'-u',filename1, filename2],stdout=PIPE,stderr=STDOUT,close_fds=True,bufsize=0)
for c in iter(lambda: p.stdout.read(1), ''):
  string+=c
p.stdout.close()
rc=p.wait()
if(string==''):print("##compiling done without syntax error : "+filename2)
else:print(string)
