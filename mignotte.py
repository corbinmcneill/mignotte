from sys import argv
from operator import mul
from math import log

Q = [ 179424673, 179426549, 179428399, 179430413, 179432233, 179434033]
K = 3;

a=1
for i in range(K-1):
	a*=Q[-i-1]
a += 1

b=1
for i in range(K):
	b*=Q[i]
b-=1

bitsPerSecret = log(b-a, 2)
bytesPerSecret = bitsPerSecret / 8 

M=1
for i in range(len(Q)):
	M*=Q[i]

def str2int(piece):
	assert(len(piece)<14)
	num = 0
	for i in range(bytesPerSecret):
		num *= 256
		if i < len(piece):
			num += ord(piece[i])
	return num

def int2str(num):
	string = ""
	while num > 0:
		string += chr(num % 256)
		num /= 256
	return string[::-1]

def split(infile, outfile):
	print "a: ", a
	print "b: ", b
	assert(b>a)
	print("b-a:", b-a)
	print("Starting split")
	message = infile.readline()
	for i in range((len(message)-1)/bytesPerSecret + 1):
		try:
			S = str2int(message[i*bytesPerSecret:(i+1)*bytesPerSecret])
		except IndexError:
			S = str2int(message[i*bytesPerSecret:])
		S += a
		print "S: ",S
		assert (a < S and S < b)
		for i in range(len(Q)):
			outfile.write(str(S % Q[i])+",")
		outfile.write("\n")

#Knuth TAOCP V2 (p342)
def exteuclid(u1,v1):
	u = [1,0,u1]
	v = [0,1,v1]
	t = [None, None, None]
	while v[2] != 0:
		q = u[2]/v[2]
		#print "q=" + str(q) 
		for i in range(3):
			t[i] = (u[i]) - q * (v[i])
		for i in range(3):
			u[i] = v[i]
		for i in range(3):
			v[i] = t[i]
		#print "u=" + str(u)
		#print "v=" + str(v)
		#print "t=" + str(t) 
	return u[1]

def combine(infile, outfile):
	while True:
		S = 0
		shares = infile.readline().strip()
		if shares == '':
			break
		shares = map(int, shares.split(',')[:-1])
		print shares
		for i in range(K):
			mprime = M / Q[i]
			S += (shares[i] * exteuclid(Q[i], mprime) * mprime)
			#print S % Q[1], shares[1]
		S -= a 

		S %= reduce(mul, Q[:K])

		outfile.write(int2str(S))

if __name__ == "__main__":
	if len(argv) == 4:
		direction = argv[1]
		infilename = argv[2]
		outfilename = argv[3]
	else:
		print("Bad number of args")
		exit()
	infile = open(infilename, 'r')
	outfile = open(outfilename, 'w')
	assert(argv[1] == "-s" or argv[1] == "-c")
	if (argv [1] == "-s"):
		split(infile, outfile)
	elif (argv [1] == "-c"):
		combine(infile, outfile)
	infile.close()
	outfile.close()
