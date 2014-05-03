import urllib2
import re

problem_regex = re.compile(r'<a href=\"\/problems\/([A-Z0-9]*)\/\"')
finished_regex = re.compile(r'<i>Pr&#243;ximo<\/i>')

def getProblems(line):
	it = problem_regex.finditer(line)
	all_problems = []
	for problem in it:
		all_problems.append(problem.group(1))
	return all_problems

def hasFinished(line):
	return len(finished_regex.findall(line)) != 0

def crawl_problems():
	problem_sets = ["contest_noturno", "mineira", "obi", "regionais", "seletivas", "seletiva_ioi", 	"sulamericana"]	
	for problem_set in problem_sets:
		offset = 0	
		while True:
			problem_set_url = "http://br.spoj.com/problems/" + problem_set + "/start=" + str(offset)
			html = urllib2.urlopen(problem_set_url).read()
			problems = getProblems(html)
			for problem in problems:
				print problem
			offset = offset + len(problems)
			if hasFinished(html):
				break

if __name__ == "__main__":
	crawl_problems()
	