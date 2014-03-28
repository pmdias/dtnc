#!/user/bin/python

# This is a special tool that converts files in the DIMACS file format
# to files in the IBM CPLEX NET file format. Atention must be made that
# this tool assumes that all the files passed as input describe a
# network flow problem in the minimum cost flow problem type.

import helper

# Open both input and output file descriptors:
#
#	* input file is an argument passed to the application
#	* output file is created and named after the name of the input file, 
#     minus any extensions, and is added a new extensions to identify it.


# Handle input file
input_file = raw_input("File to be converted: ")
fin = open(input_file, 'r')
in_data = input_file.split(".")
print 'File to be converted is ' + in_data[0]

# Handle output file
out_file = in_data[0] + '.net'
fout = open(out_file, 'w')

# DIMACS files have a lot of lines that are nothing more than comments.
# We want to discard these lines --- they aren't needed.
problem = 'min'
coments = 0
p_nodes = 0
p_arcs = 0
p_line_read = False
node_supply = []
arcs = []
arcs_count = 0

for line in fin:
	# Get the line and process it to tokens
	line_data = line.split()
	if line_data[0] == 'c':
		# comments are ignored
		coments = coments + 1
	elif line_data[0] == 'p':
		# problem line
		if p_line_read != True:
			problem = str(line_data[1])
			p_nodes = int(line_data[2])
			p_arcs = int(line_data[3])
		else:
			print 'Error: multiple problem lines in DIMACS input file.'
	elif line_data[0] == 'n':
		# node line
		t = line_data[1], line_data[2]
		node_supply.append(t)
	elif line_data[0] == 'a':
		# arc line
		a = helper.Arc(arcs_count)
		a.tail = line_data[1]
		a.head = line_data[2]
		a.lower = line_data[3]
		a.upper = line_data[4]
		a.cost = line_data[5]
		arcs.append(a)
		arcs_count = arcs_count + 1

# Check if number of elements in lists are equal to the expected
if arcs_count != p_arcs:
	print 'Error, number of arcs doesn\'t match!'
	print 'Number of arcs read: ' + arcs_count
	print 'Number of expected arcs: ' + p_arcs

# Check first line and verify if second token is 'min'



# Begin building the output file
if problem == 'min':
	fout.write('MINIMIZE NETWORK ' + in_data[0] + '\n')
elif problem == 'max':
	fout.write('MAXIMIZE NETWORK ' + in_data[0] + '\n')

fout.write('SUPPLY\n')
for i in node_supply:
	fout.write(helper.new_name('n', i[0]) + ' : ' + i[1] + '\n')

fout.write('ARCS\n')
for i in arcs:
	fout.write(helper.new_name('a', i.arc_id + 1))
	fout.write(' : ')
	fout.write(helper.new_name('n', i.tail))
	fout.write(' -> ')
	fout.write(helper.new_name('n', i.head))
	fout.write('\n')

fout.write('OBJECTIVE\n')
for i in arcs:
	fout.write(helper.new_name('a', i.arc_id + 1))
	fout.write(' : ')
	fout.write(i.cost + '\n')

fout.write('BOUNDS\n')
for i in arcs:
	fout.write(i.lower + ' <= ')
	fout.write(helper.new_name('a', i.arc_id + 1))
	fout.write(' <= ' + i.upper + '\n')

fout.write('ENDNETWORK\n')
