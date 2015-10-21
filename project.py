import os 
import glob 
import sys 
from collections import defaultdict

files = []
for file in glob.glob("*.txt"):
	files.append(file)

print files
def bit_to_boolean(bit):
	if "1" in bit:
		return True
	else:
		return False

def boolean_to_bit(boolean):
	if boolean:
		return "1"
	else:
		return "0"

class gates:
	def __init__(self):
		self.gate =-1
		self.input1 = -1
		self.input2 = -1
		self.output = -1
	def __init__(self, string, input1, output, input2=None):
		if(input2==None):
			self.gate = string
			self.input1 = input1
			self.input2 = -1
			self.output = output
		else:
			self.gate = string
			self.input1 = input1
			self.input2 = output
			self.output = input2

	def display(self):
		print "Gate is: " + self.gate
		print "Inputs are",
		print self.input1, self.input2
		print "Output is:",
		print self.output
	def evaluate(self, nets):
		if "AND" in self.gate:
			nets[self.output] = nets[self.input1] and nets[self.input2]
		if "OR" in self.gate:
			nets[self.output] = nets[self.input1] or nets[self.input2]
		if "NAND" in self.gate:
			nets[self.output] = not(nets[self.input1] and nets[self.input2])
		if "NOR" in self.gate:
			nets[self.output] = not(nets[self.input1] or nets[self.input2])
		if "INV" in self.gate:
			nets[self.output] = not(nets[self.input1])
		if "BUF" in self.gate:
			nets[self.output] = nets[self.input1]

for file_ in files[1:2]:
	lines = []
	print "\n\n"
	print file_
	print "\n\n"
	with open(file_) as inputfile:
		for line in inputfile:
			lines.append(line.split("\r\n")[0])
	lines = lines[:len(lines)]
	number_of_gates =0
	number_of_nets = 0
	inputs =[]
	outputs =[]
	both_input_list = ["AND", "OR", "NAND", "NOR"]
	single_input_list = ["INV", "BUF"]
	for index, line in enumerate(lines):
		if "INPUT" in str(line):
			number_of_gates = index
	for line in lines:
		if "INPUT" in str(line):
			inputs= (str(line).split()[1:len(str(line).split())-1])
	for line in lines:
		if "OUTPUT" in str(line):
			outputs= (str(line).split()[1:len(str(line).split())-1])
	max_lines = map(int,lines[number_of_gates-1].split()[1:])
	number_of_nets= max(max_lines)
	nets ={}
	nets_inputgates =defaultdict(list)
	for i in range(1, number_of_nets+1):
		nets[i] = -1
	print "Gates # :",
	print number_of_gates
	dict_of_gates ={}
	for i in range(number_of_gates):
		if len(lines[i].split()) == 3:
			a = gates(lines[i].split()[0], int(lines[i].split()[1]), int(lines[i].split()[2]))
			dict_of_gates[i+1]=a
			nets_inputgates[int(lines[i].split()[1])].append(i+1)
		if len(lines[i].split()) ==4:
			b = gates(lines[i].split()[0], int(lines[i].split()[1]), int(lines[i].split()[2]), int(lines[i].split()[3]))
			dict_of_gates[i+1]=b
			nets_inputgates[int(lines[i].split()[1])].append(i+1)
			nets_inputgates[int(lines[i].split()[2])].append(i+1)
	inputs = map(int, inputs)
	outputs = map(int, outputs)
	print inputs
	print outputs
	print "Please provide the bit vector of length:",
	print len(inputs)
	bit_vector = raw_input()
	if len(bit_vector) != len(inputs):
		print "Please enter a bit vector of length:",
		print len(inputs)
		bit_vector = raw_input()
	print bit_vector
	input_vector = []
	for char in bit_vector:
		input_vector.append(bit_to_boolean(char))
	print input_vector
	stack = []
	for input_, char in zip(inputs, input_vector):
		nets[input_] = char
	for gate_number, gate_object in dict_of_gates.iteritems():
		if gate_object.gate in both_input_list:
			if nets[gate_object.input1] !=-1 and nets[gate_object.input2] != -1 :
				stack.append(gate_object)
		if gate_object.gate in single_input_list:
			if nets[gate_object.input1] != -1:
				stack.append(gate_object)

	while stack:
		gate_object = stack.pop()
		gate_object.display()
		gate_object.evaluate(nets)
		for values in nets_inputgates[gate_object.output]:
			check_object= dict_of_gates[values]
			if check_object.gate in both_input_list:
				if nets[check_object.input1] != -1 and nets[check_object.input2] != -1:
					stack.append(check_object)
			if check_object.gate in single_input_list:
				if nets[check_object.input1] != -1:
					stack.append(check_object)

	final_bit = ""

	for output in outputs:
		print output,
		print nets[output]
		final_bit = final_bit+ boolean_to_bit(nets[output])
	
	print final_bit











		
