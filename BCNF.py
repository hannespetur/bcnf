# author Xuefeng Zhu 

from sets import Set
class FD:
	def __init__(self, A, B):
		self.A = Set(A)	
		self.B = Set(B)
		self.total = Set(A+B)

	def closure(self, fd):
		if (fd.A.issubset(self.total) and not fd.B.issubset(self.total)):
			self.total = self.total.union(fd.B)
			return True

class Table:
	def __init__(self, Attrs, FDs):
		self.Attrs = Attrs
		self.FDs = FDs

	def findIllDF(self):
		for FD1 in self.FDs:
			for FD2 in self.FDs:
				if (FD1.closure(FD2)):
					FD2 = FD1
			if (not FD1.total.issuperset(self.Attrs)):
				return FD1
		return 0
	
	def decompose(self, df):
		result = []
		attrs1 = df.total
		dfs1 = self.project(attrs1)
		result.append(Table(attrs1,dfs1))
		attrs2 = self.Attrs.difference(attrs1).union(df.A)
		dfs2 = self.project(attrs2)
		result.append(Table(attrs2, dfs2))
		return result

	def project(self, attrs):
		result = [];
		for FD in self.FDs:
			if (FD.A.issubset(attrs) and FD.B.issubset(attrs)):
				result.append(FD)
		return result
		
def getFDs(fds):
	result = []
	for i in fds:
		temp = i.split('->')
		result.append(FD(list(temp[0]), list(temp[1])))
	return result

def formFDs(fds):
	result = ""
	for i in range(len(fds)):
		result += "".join(list(fds[i].A)) + "->" + "".join(list(fds[i].B)) ;
		if (i != len(fds)-1):
			result += ", "
	return result

if __name__ == "__main__":
	attrs = raw_input("Please enter table attributes, seperated by comma\n")
	attrs = Set(attrs.split(','))
	fds = raw_input("Please enter function dependencies, like AB->C, seperated by comma\n")
	fds = fds.split(',')
	fds = getFDs(fds)
	tables = [Table(attrs, fds)]

	print 
	print "USER INPUT"
	print "Attributes:", ",".join(list(attrs))
	print "FDs:", formFDs(fds)

	illDF = tables[0].findIllDF();
	if (illDF == 0):
		print "The given Table and its Functional Dependencies is in BCNF"
	else:
		print "The given Table and its Functional Dependencies is not in BCNF"
		print 
		print "Step by Step Decomposition:"
		isBCNF = False
		while(not isBCNF):
			isBCNF = True
			for table in tables:
				illDF = table.findIllDF();
				if (illDF != 0):
					print "For Table:", ",".join(list(table.Attrs))
					print "the closrure of", ",".join(list(illDF.A)), "is", ",".join(list(illDF.total)), "violates BCNF."
					isBCNF = False
					tables += table.decompose(illDF)
					tables.remove(table)
					print "After decomposition this table, we have:"
					for i in tables:
						print "Table:", ",".join(list(i.Attrs))
						print "FDs:", formFDs(i.FDs)
						print 
					print "-------------------------------------"
					break;

		print "BCNF Decomposition Result:"		
		for i in tables:
			print "Table:", ",".join(list(i.Attrs))
			print "FDs:", formFDs(i.FDs)
			print 

	

