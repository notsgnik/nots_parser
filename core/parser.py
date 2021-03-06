#!/usr/bin/env python
# -*- coding: utf-8 -*- 


class Parser:
	
	def __init__(self,name):
	
		self.rules = []
		self.buffer = ""
		self.full_sentence = ""
		self.flags = [ 0,0,0,0,0,0 ] # secces , nl , end_instrc, interupt, no print , autoexec sentence
		self.eatch_run = ""
		self.separator = "\n"
		self.argsep = " "
		self.load_rules("core/rules_fld/%s" % name)
		self.fl = self.load_functions("function_fld.%s" % name)
		self.fl.__init__(self)

	def load_functions(self,function_name):
		return __import__(function_name, globals(), locals(), ['*'], -1)			

	
	def load_rules(self,file_name):
		f = open( file_name, "r" )
		for line in f:
			if line[0] == "#":
				continue
			line = line.strip().split(":")
			if line[1][0:3] == '"\\x' :
				line[1] = line[1][3:-1].decode('hex')
			if line[1][0:1] == '"' and line[1][-1] == '"':
				line[1] = line[1][1:-1]
			self.rules.append( line )
			if line[0] == "*":
				self.eatch_run =  "self.fl.%s" % line[1]
			if line[0] == "|":
				self.separator =  "%s" % line[1]
			
		f.close()


	def add_char_to_buffer(self,c):
		self.buffer = "%s%s" % (self.buffer,c)
		
	def rem_char_from_buffer(self,c = 1):
		if len(self.buffer) > 0:
			self.buffer = self.buffer[:-1*c]
			return True
		else:
			return False
	
	def rem_char_from_sentence(self,c = 1):
		if len(self.full_sentence) > 0:
			self.full_sentence = self.full_sentence[:-1*c]
			return True
		else:
			return False
	def add_char_to_sentence(self,c):
		self.full_sentence = "%s%s" % (self.full_sentence,c)
		
	def store_buffer_arg(self):
		tmp = self.buffer
		if tmp != "":
			if self.full_sentence != "":
				self.full_sentence = "%s %s" % (self.full_sentence,self.buffer)
			else:
				self.full_sentence = "%s" % self.buffer
			self.buffer = ""
		return tmp
	
	def flush(self):
		self.buffer = ""
		self.full_sentence = ""
		return True
		
	def load_first_arg(self):
		index = 0
		self.buffer= ""
		while self.full_sentence[index] != " ":
			 self.buffer = "%s%s" % (self.buffer, self.full_sentence[index] )
			 index = index + 1
		self.full_sentence = self.full_sentence[index:]
		
	def run(self):
		found = False
		self.load_first_arg()
		for rule in self.rules:
			if rule[0] == "+.":
				if self.buffer == rule[1]:
					exec("self.fl.%s" % rule[2])
					found = True
		return found
		
	def feed(self,char):
		for rule in self.rules:
			if rule[0] == ".":
				if rule[1] == char :
					exec("self.fl.%s" % rule[2])
		if self.flags[3] == 1:
			self.flags[3] = 0
			return True
		self.add_char_to_sentence(char)
		if char != self.argsep:
			self.add_char_to_buffer(char)
		else:
			self.buffer = ""
		if self.buffer != "":
			for rule in self.rules:	
				if rule[0] == ".+":
					if self.buffer.strip() == rule[1]:
						exec("self.fl.%s" % rule[2])
		if self.flags[3] == 1:
			self.flags[3] = 0
			return True
		if self.flags[4] == 1:
			self.flags[4] = 0
			char = ""
		code = compile(self.eatch_run,'<string>','exec')
		exec code	
		return True
		#self.fl.printtofile("%s\n" % (self.buffer))
		
		
		
		
		
		
		
		
		
		
		
		
		
		
