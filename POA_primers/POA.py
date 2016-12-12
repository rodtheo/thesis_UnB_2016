import re
import sys

class POAHeader:
	def __init__(self):
		self.header_dict = dict()


	def parse_header_line(self, header_line):
		if header_line.startswith("VERSION="):
			self.header_dict["version"] = header_line.split("=")[1]
		elif header_line.startswith("NAME="):
			self.header_dict["primary_seq_name"] = header_line.split("=")[1]
		elif header_line.startswith("SOURCENAME="):
			if "seq_name" in self.header_dict.keys():
				self.header_dict["seq_name"].append(header_line.split("=")[1])
			else:
				self.header_dict["seq_name"] = [header_line.split("=")[1]]
		elif not (header_line.startswith("SOURCEINFO")):
			self.header_dict[header_line.split("=")[0]] = header_line.split("=")[1]
		return self.header_dict

		def get_header(self):
			return (self.header_dict)

		def __str__(self):
			return str(self.__dict__)

class POARecord:
	def __init__(self, record_string):
		label = record_string.split(":")[0]
		infos = record_string.split(":")[1]
		# print infos
		self.name = label
		self.fromNodes = re.findall('L(\d+)',infos)
		self.toNodes = re.findall('S(\d+)',infos)
		self.Aindex = re.findall('A(\d+)',infos)

	def getName(self):
		return self.name
	def getfromNodes(self):
		return self.fromNodes
	def gettoNodes(self):
		return self.toNodes
	def getAindex(self):
		return self.Aindex

	def __str__(self):
		print str(self.getName())

class POAReader:
	def __init__(self, file_name):
		self.file_fd = open(file_name) if file_name is not None else sys.stdin
		self.header = []
		self.dictionary = {}

	def __iter__(self):
		return self

	def next(self):
		while True:
			line = self.file_fd.next()
			if line.startswith("VERSION") or line.startswith("NAME") or line.startswith("TITLE") \
			or line.startswith("LENGTH") or line.startswith("SOURCECOUNT") or line.startswith("SOURCENAME")\
			or line.startswith("SOURCEINFO"):
				self.header.append((line.strip().split("=")[0],line.strip().split("=")[1]))
			else:
				return POARecord(line.strip())

	def get_header(self):
		return self.header

	def get_samples(self):
		self.samps = []
		for key,item in self.header:
			if key == 'SOURCENAME':
				self.samps.append(item.split("_")[0])
		return self.samps

	def get_len_alignments(self):
		samps=[]
		for key,item in self.header:
			print(key,item)
			if key == 'SOURCENAME':
				samps.append(item.split("_")[0])
		return len(samps)

	def get_point(self):
		samps=[]
		for key,item in self.header:
			if key == 'SOURCENAME':
				return (item.split("-")[1])

