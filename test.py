import sys
print sys.argv
#in1,in2,in3=[eval(i) for i in sys.argv[1:4]]
in1 = sys.argv[1]
in2 = sys.argv[2]
try : in3 = sys.argv[3]
except : in3 = 0

print in1,in2,in3
if in3==0:
  print "aaa"
sys.exit(1)
