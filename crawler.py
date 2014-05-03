import urllib2
import re


problem_regex = re.compile(r'<a href=\"\/problems\/.*\"')

def getProblems(line):
	return problem_regex.findall(line)



problem_sets = ["contest_noturno", "mineira", "obi", "regionais", "seletivas", "seletiva_ioi", 	"sulamericana"]

for problem_set in problem_sets:
	problems = getProblems(urllib2.urlopen("http://br.spoj.com/problems/" + problem_set).read())
	for problem in problems:
		print problem