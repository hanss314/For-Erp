#Oh Hi! So you want to see how this works? have fun!
import argparse, sys, os, PIL, tensorflow, pygame, glob, wheel, gitgud, random#you'll need to install some of these

def get_valid_moves(grid,turn):
	valid_kills = []
	valid_sacrafices = []
	valid_summons = []

	for x in range(width):
		for y in range(height):
			cell = grid[y][x]
			if cell >0:
				valid_kills.append((x,y,0))
			else:
				valid_summons.append((x,y,turn))
			if cell == turn:
				valid_sacrafices.append((x,y,0))

def draw(grid):
	surface.fill((255,255,255))

	squaresize = 760 // height

	for x in range(width):
		for y in range(height):
			rect = (x * squaresize,y * squaresize, squaresize, squaresize)
			pygame.draw.rect(surface, gridtocol[grid[y][x]], rect)
			pygame.draw.rect(surface, (0, 0, 0), rect, 1)



def getneighbors(row,col):

	neighbors = [
		[row + 1, col], 
		[row + 1, col + 1], 
		[row + 1, col - 1], 
		[row, col + 1], 
		[row, col - 1], 
		[row - 1, col - 1],
		[row - 1, col],
		[row - 1, col + 1]
	]
	toremove = []
	for coord in neighbors:
		if (-1 == coord[0]) or (-1 == coord[1]) or (height == coord[1]) or (width == coord[0]):
			toremove.append(coord)
			
	for coord in toremove:
		neighbors.remove(coord)
		
	return neighbors



def iteration(grid):
	newgrid = [[0 for i in range(width)] for j in range(height)]

	for row in range(width):
		for col in range(height):
			cellcount = [0,0,0,0]
			neighbors = getneighbors(row,col)

			for i in neighbors:
				try:
					cellvalue = grid[i[1]][i[0]]
					cellcount[cellvalue] += 1
				except:
					pass
			if row == 0 and col == 0:
			 print(str(neighbors))
			
			if grid[col][row] == 0 and sum(cellcount[1:]) in rulestring[0]:
				
				if cellcount[1] == cellcount[2]:
					newgrid[col][row] = 3

				elif cellcount[1] > cellcount[2]:
					newgrid[col][row] = 1
					
				elif cellcount[1] < cellcount[2]:
					newgrid[col][row] = 2

			elif grid[col][row] != 0 and sum(cellcount[1:]) in rulestring[1]:
				newgrid[col][row] = grid[col][row]
				
			else:
				newgrid[col][row] = 0

	return newgrid

def run():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-e", "--perc_elim", nargs='?', const=5, default=5)
	parser.add_argument("-t", "--num_gold", nargs='?', const=5, default=5)
	args = parser.parse_args()
	
	keys = ast.literal_eval(open('./'+args.input+'/dict.txt','r').read())
	responses = open('./'+args.input+'/responses.txt','r').read().split('\n')
	entirevotes = open('./'+args.input+'/votes.txt','r').read().replace('[','').replace(']','').split('\n')
	twowers = open('./'+args.input+'/twowers.txt','r').read().split('\n')
	indivTwowers = list(set(twowers))
	twowerCount = len(indivTwowers)
	prompt = open('./'+args.input+'/prompt.txt','r').read().split('\n')[0]
	votes = []
	scores=[[response,[]]for response in responses]
	
	topNumber = int(args.num_gold)
	elimNumber = 0
	
	if int(args.perc_elim) < 0:
		elimNumber = -int(args.perc_elim)
	else:
		elimNumber = round(int(args.perc_elim)*len(indivTwowers)/100)
	
	
	
	promptList = textwrap.wrap(prompt,100)
	prompt = ''
	for s in promptList:
		prompt += (s+'\n')
	
	arial = ImageFont.truetype('./resources/arial.ttf',20)
	bigArial =  ImageFont.truetype('./resources/arial.ttf',30)
	smallArial = ImageFont.truetype('./resources/arial.ttf',13)
	
	base = Image.new('RGBA',(1368,1368),color=(255,255,255))
	drawer = ImageDraw.Draw(base)
	headerHeight = drawer.textsize(prompt,bigArial)[1]+35
	base = Image.new('RGBA',(1368,headerHeight+int(67/2*len(responses))),color=(255,255,255,255))
	drawer = ImageDraw.Draw(base)
	
	drawer.text((15,0),prompt,font=bigArial, fill=(0,0,0,255))
	base.paste(Image.open('./resources/header.png'),(0,headerHeight-40))
	
	for v in entirevotes:
		if not v=='':
			voteTup=tuple(v.split(' '))
			voteTup = (voteTup[0].upper(),voteTup[1].lower())
			votes.append(voteTup)
	
	for vote in votes:
		try:
			mapping = keys[vote[0]]
			percentage = 100
			for c in vote[1]:
				scores[mapping[ord(c)-97]][1].append(percentage)
				percentage -= 11
		except KeyError:
			print('Invalid vote'+': ['+vote[0]+' '+vote[1].upper()+']')
		except Exception:
			pass
	
	for scoredata in scores:
		try:
			scoredata.append(statistics.mean(scoredata[1]))			
		except Exception:
			continue
			
		try:
			scoredata.append(statistics.stdev(scoredata[1]))
		except Exception:
			scoredata.append(0)
			
		scoredata.append(len(scoredata[1]))
		scoredata[1]= twowers[scores.index(scoredata)]
		scoredata[0],scoredata[1]=scoredata[1],scoredata[0]
		
	mergeSort(scores)
	backgroundCol=0
	addBackground=0
	ranking=1
	
	for i in range(len(scores)):	
		twower, response, mean, standev, voteCount = scores[i][0], scores[i][1], scores[i][2], scores[i][3], scores[i][4]
		
		if ranking == (topNumber+1): 
			backgroundCol = 1
			addBackground = 0
		elif ranking == (twowerCount-elimNumber+1) and twower in indivTwowers:
			backgroundCol = 2
			addBackground = 0
			
		if (addBackground % 2) ==0:
			if backgroundCol==0:
				base.paste(Image.open('./resources/top.png'),(0,int(67/2*i)+headerHeight))
			elif backgroundCol==1:
				base.paste(Image.open('./resources/normal.png'),(0,int(67/2*i)+headerHeight))
			elif backgroundCol==2:
				base.paste(Image.open('./resources/eliminated.png'),(0,int(67/2*i)+headerHeight))
		
		try:
			booksona = Image.open('./booksonas/'+twower+'.png')
			booksona.thumbnail((32,32),Image.BICUBIC)
			base.paste(booksona,(333,int(67/2*i)+headerHeight),booksona)
		except Exception:
			pass
		
		if twower in indivTwowers:
			indivTwowers.remove(twower)
			if ranking % 10 == 1:
				rankingString = str(ranking)+'st'
			elif ranking % 10 == 2:
				rankingString = str(ranking)+'nd'
			elif ranking % 10 == 3:
				rankingString = str(ranking)+'rd'
			else:
				rankingString = str(ranking)+'th'
				
			drawer.text((15,int(67/2*i+7)+headerHeight),rankingString,font=arial,fill=(0,0,0,255))
			ranking += 1
		if drawer.textsize(twower,arial)[0] > 255:
			drawer.text((320-drawer.textsize(twower,smallArial)[0],int(67/2*i+7)+headerHeight),
				twower,font=smallArial,fill=(0,0,0,255))
		else:
			drawer.text((320-drawer.textsize(twower,arial)[0],int(67/2*i+7)+headerHeight),
				twower,font=arial,fill=(0,0,0,255))
				
		if drawer.textsize(response,arial)[0] > 618:
			responseLines = textwrap.wrap(response,90)
			response = ''
			for s in responseLines:
				response += (s+'\n')
				
			drawer.text((378,int(67/2*i)+headerHeight),
				response,font=smallArial,fill=(0,0,0,255))
		else:
			drawer.text((378,int(67/2*i+7)+headerHeight),
				response,font=arial,fill=(0,0,0,255))
				
		drawer.text((998,int(67/2*i+7)+headerHeight),
			str(mean)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1164,int(67/2*i+7)+headerHeight),
			str(standev)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1309-drawer.textsize(str(voteCount),arial)[0]/2,
			int(67/2*i+7)+headerHeight),str(voteCount),
			font=arial,fill=(0,0,0,255))
				
		addBackground += 1		
		
	base.save('./'+args.input+'/results.png')


	
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][2] > righthalf[j][2]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
try:
	os.system("set PYTHONHASHSEED=0")
except:
	os.system("export PYTHONHASHSEED=0")

code_hash = -78954984748832619

parser = argparse.ArgumentParser()
parser.add_argument('code')
parser.add_argument('answer_key')
parser.add_argument('responses')
parser.add_argument('file')
parser.add_argument('redundant_file')
parser.add_argument('more_redundant_files')
parser.add_argument('have_fun')
parser.add_argument('it_doesn\'t_have_to_be_correct')
args = parser.parse_args()

len_open = args.file
sys_exit = args.redundant_file
args.more_redundant_files.split("/")

if not hash(args.code)==code_hash:
	print('To find the code, complete the last Zahada bonus level at http://www.mcgov.co.uk/zahada.html')
	sys.exit()
	
max = len(open(args.answer_key).read().split('\n'))
for i in range(len(args.responses)):
	score = random.randomseed(0,max)
	print('Student #{} gets {}/{}'.format(i,score,max))

	
	
sys.exit()
	
import random
import time

listSize = 3000
comparisons = 0
toSort=[]

def main():
	
	for i in range(listSize):
		toSort.append(i)
	random.shuffle(toSort)
	start = time.time()
	heapsort(toSort)
	print(time.time()-start)
	print(toSort)
	time.sleep(1000)	

def heapsort( aList ):
  length = len( aList ) - 1
  leastParent = length / 2
  for i in range ( leastParent, -1, -1 ):
    moveDown( aList, i, length )
 
  for i in range ( length, 0, -1 ):
    if aList[0] > aList[i]:
      swap( aList, 0, i )
      moveDown( aList, 0, i - 1 )
 
 
def moveDown( aList, first, last ):
  largest = 2 * first + 1
  while largest <= last:
    if ( largest < last ) and ( aList[largest] < aList[largest + 1] ):
      largest += 1
 
    if aList[largest] > aList[first]:
      swap( aList, largest, first )
      first = largest;
      largest = 2 * first + 1
    else:
      return 
 
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp
