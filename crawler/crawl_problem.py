import re
import urllib2

USER_PER_PROBLEM_PAGE = 20
PROBLEM_PAGE_PREFIX = "http://br.spoj.com/ranks/"
DISABLED_NEXT = "<i>Pr&#243;ximo</i>"
ENABLED_NEXT = r'<a href="/ranks/\w+(/start=\d+)?" class="pager_link">Pr&#243;ximo</a>'

user_points = {}


def process_problem(problem_name):
	response = urllib2.urlopen(PROBLEM_PAGE_PREFIX + problem_name).read()
	accepteds_regexp = re.compile(r'<tr class="lightrow">\s+<td>\d+</td>\s+<td>\d+</td>\s+<td>(\d+)</td>\s+<td>\d+</td>\s+<td>\d+</td>\s+<td>\d+</td>\s+<td>\d+</td>\s+</tr>')
 	accepteds = 0
	for match in accepteds_regexp.finditer(response):
		accepteds = int(match.group(1))
		break
	users = set()
	points = 80.0 / (40 + accepteds)
	start = 0
	page = 1
	while True:
		url = PROBLEM_PAGE_PREFIX + problem_name + "/start=" + str(start)
		content = urllib2.urlopen(url).read()
		nusers = process_problem_users(content, users)
		print str(page) + " (" + problem_name + ")"
		if nusers == 0 or \
		   len(re.findall(DISABLED_NEXT, content)) >= 1 or \
		   (len(re.findall(DISABLED_NEXT, content)) == 0) and (len(re.findall(ENABLED_NEXT, content)) == 0):
			break
		page += 1
		start += USER_PER_PROBLEM_PAGE
	print "------------------> " + problem_name + " done!"
	return (users, points)


def process_problem_users(content, users):
	users_regexp = re.compile(r'<a href="/users/(\w+)/" title="\w+">[^<]*</a>')
	nusers = 0
	for match in users_regexp.finditer(content):
		user = match.group(1)
		nusers += 1
		if user in users:
			continue
		users.add(user)
	return nusers
