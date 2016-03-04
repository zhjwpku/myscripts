import sys
import string

## You should modify the infile to your input BigData file path
## The outfile shows the clarified result
infile = "bigdata.txt"
outfile = "output.txt"

column_m = ord('m') - ord('a')
column_w = ord('w') - ord('a')
column_x = ord('x') - ord('a')
clarify = {}

inputfile = open(infile, "r")

for line in inputfile:
  b = line.split(',')
  m = b[column_m]
  w = b[column_w]
  #print(m, w)
  x = float(b[column_x])
  if m in clarify:
    if w == '"0"':
      #print w, 1
      clarify[m] += x
    else:
      #print w, 2
      clarify[m] += (x * (-1))
  else:
    if w == '"0"':
      #print w, 3
      clarify[m] = x
    else:
      #print w, 4
      clarify[m] = (x * (-1))

outputfile = open(outfile, "w")
outputfile.write("The clarified results:\n")
outputfile.write("  M\t  X\n")

print ("The final result:")
print ("  M\t  X")
for i in clarify:
  print (i, clarify[i])
  outputfile.write("%s  %f\n" % (i, clarify[i]))

outputfile.close()
inputfile.close()
