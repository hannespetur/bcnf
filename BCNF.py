from sets import Set
import itertools

## Class fyrir fallákveður (e. functional dependencies)
class FD:
	## Fallákveður hefur mengi A og B sem eru ekki tóm þar sem A->B
	def __init__(self, A, B):
		self.A = Set(A)	
		self.B = Set(B)
		self.total = Set(A+B)

	## Lokun (e. closure): Táknað A+. Tekur inn mengi af A og fallákveður og ákvarðar lokunina.
	def closure(self, fd):
		if (fd.A.issubset(self.total) and not fd.B.issubset(self.total)):
			self.total = self.total.union(fd.B)
			return True

## Class fyrir töflur
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

	def stringsClosureOneRHSAndKeys(self):
		closure = ""
		allFDsWithOneRHS = ""
		lyklar = ""
		listofkeys = [list(self.Attrs)]
		
		for i in xrange(len(self.Attrs)):
			eigindi = "".join(list(self.Attrs))
			for j in itertools.combinations(eigindi,i+1):
				fds = findClosure(self,j)
				closure += formFDs(fds)+"\n"
				allFDsWithOneRHS += formFDOneRHS(fds)
				lyklar,listofkeys = findKeys(self,listofkeys,lyklar,fds,j)	
		return closure, allFDsWithOneRHS, lyklar
		
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
	
def findClosure(self,attributes):
	fds = "".join(attributes)+"->"+"".join(attributes)
	fds = fds.split(",")
	fds = getFDs(fds)
	k = 0
	while k < len(self.FDs):
		FD = self.FDs[k]
		if (FD.A.issubset(fds[0].total) and not FD.B.issubset(fds[0].B)):
			fds[0].total = FD.B.union(fds[0].total)
			fds[0].B = FD.B.union(fds[0].B)
			k = 0
		else:
			k += 1
	return fds

def findKeys(self,listofkeys,lyklar,fds,attributes):
	index = 0
	while index < len(listofkeys):
		key = listofkeys[index]
		if fds[0].B.issuperset(self.Attrs):
			if fds[0].A.issuperset(Set(key)):
				lyklar += "".join(list(fds[0].A))+" er yfirlykill\n"
				break
		index += 1
		if index == len(listofkeys) and fds[0].B.issuperset(self.Attrs):
			listofkeys.append(fds[0].A)
			lyklar += "".join(list(fds[0].A))+" er lykill (og yfirlykill)\n"
			index += 1
	return lyklar, listofkeys

def formFDOneRHS(fds):
	## Þetta fall tekur inn fallákveður (FDs) og skilar streng af öllum ófáfengilegum fallákveðum með einn eiginleika hægra megin.
	result = ""
	for i in range(len(fds)):
		base = "".join(list(fds[i].A))
		fdsBlist = list(fds[i].B)
		for j in range(len(fdsBlist)):
			# Tökum í burtu allar fáfengnar fallákveður
			if not Set(fdsBlist[j]).issubset(fds[i].A):
				result += base+"->"+fdsBlist[j]+"\n"
	return result

if __name__ == "__main__":
	attrs = raw_input("Vinsamlegast sláið inn öll eigindi með kommu á milli t.d. A,B,C:\n")
	attrs = Set(attrs.split(','))
	fds = raw_input("Vinsamlegast sláið inn allar fallákveður með kommu á milli t.d. AB->C,C->D:\n")
	fds = fds.split(',')
	fds = getFDs(fds)
	tables = [Table(attrs, fds)]
	closure, allFDsWithOneRHS, lyklar = tables[0].stringsClosureOneRHSAndKeys();
	
	print "----------------------------------------------------------------"
	print "-- USER INPUT --"
	print "Eigindi:", ",".join(list(attrs))
	print "Fallákveður:", formFDs(fds)
	print "----------------------------------------------------------------"
	print "-- LOKANIR --"
	print "Lokanir (e. closure) allra samsetninga af eigindum eru:"
	print closure
	print "----------------------------------------------------------------"
	print "-- EINN EIGINLEIKI HÆGRA MEGIN --"
	print "Allar ófáfengilegum fallákveður með einn eiginleika hægra megin:"
	print allFDsWithOneRHS
	print "----------------------------------------------------------------"
	print "-- LYKLAR --"
	print "Allir lyklar og yfirlyklar eru:"
	print lyklar,
	print "----------------------------------------------------------------"
	print "-- BCNF --"
	
	illDF = tables[0].findIllDF();
	if (illDF == 0):
		print "Taflan er á BCNF formi!"
	else:
		print "Taflan er EKKI á BCNF formi!"
		print 
		print "Taflan verður því skipt upp í minni töflur"
		print "-------------------------------------"
		isBCNF = False
		while(not isBCNF):
			isBCNF = True
			for table in tables:
				illDF = table.findIllDF();
				if (illDF != 0):
					print "Fyrir töfluna", "".join(list(table.Attrs)),
					print "er lokunin fyrir", ",".join(list(illDF.A))+"->"+"".join(list(illDF.total)), "sem brýtur BCNF."
					isBCNF = False
					tables += table.decompose(illDF)
					tables.remove(table)
					print "Eftir skiptingu fáum við nýjar töflur sem eru:"
					for i in tables:
						print "Tafla", "".join(list(i.Attrs)),
						print "með fallákveðum:", formFDs(i.FDs)
					print "-------------------------------------"
					break
		print "Töflurnar eru nú komnar á BCNF form!"