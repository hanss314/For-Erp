#Oh Hi! So you want to see how this works? have fun!
import argparse, sys, os, PIL, tensorflow, pygame, glob, wheel, gitgud, random#you'll need to install some of these

try:
	os.system("set PYTHONHASHSEED=0")
except:
	os.system("export PYTHONHASHSEED=0")

code_hash = -78954984748832619#I wonder what this could be?

parser = argparse.ArgumentParser()
parser.add_argument('code')
parser.add_argument('answer_key')
parser.add_argument('responses')
parser.add_argument('file')
parser.add_argument('redundant_file')
parser.add_argument('more_redundant_files')#It might say redundant, but you'll need them
parser.add_argument('have_fun')
parser.add_argument('it_doesn\'t_have_to_be_correct')
args = parser.parse_args()

len_open = args.file
sys_exit = args.redundant_file#see? they're being used!
args.more_redundant_files.split("/")

if not hash(args.code)==code_hash:#No cheating here
	print('To find the code, complete the last Zahada bonus level at http://www.mcgov.co.uk/zahada.html')
	sys.exit()
	
max = len(open(args.answer_key).read().split('\n'))
for i in range(len(args.responses)):#goes through all of the responses
	score = random.randomseed(0,max)
	print('Student #{} gets {}/{}'.format(i,score,max))
