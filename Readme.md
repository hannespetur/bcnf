##Overiew 
This lib will tell you if the input is BCNF or not, print out for all combinations their closure, find all keys (and superkeys) and print out all function dependencies that have only one attributes on the right-hand-side. Forked from [Xuefeng-Zhu](https://github.com/Xuefeng-Zhu/bcnf). All prints were translated to Icelandic. 

##Instruction 
In order to run it, just type python BCNF.py in the terminal and input the attributes of the table and its function dependencies.

*Example*:

	Table Attributes:A,B,C,D,E
	Func Dependencies:AB->C,DE->C,B->D