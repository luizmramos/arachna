import urllib2
import re
import multiprocessing.pool
from Queue import Queue
from threading import Thread
from crawl_problem import process_problem
import thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

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


user_points = {}

def crawl_problem(problem, lock):
	users, points = process_problem(problem)		
	with lock:	
		for user in users:
			if not user in user_points:
				user_points[user] = (0, 0)
			old = user_points[user];
			user_points[user] = (old[0] + 1, old[1] + points)


def crawl_all_problems():
	pool = ThreadPool(16)
	problem_sets = ["contest_noturno", "mineira", "obi", "regionais", "seletivas", "seletiva_ioi", 	"sulamericana"]	
	lock = thread.allocate_lock()
	for problem_set in problem_sets:
		offset = 0	
		while True:
			problem_set_url = "http://br.spoj.com/problems/" + problem_set + "/start=" + str(offset)
			html = urllib2.urlopen(problem_set_url).read()
			problems = getProblems(html)
			for problem in problems:
				pool.add_task(crawl_problem, problem, lock)
			offset = offset + len(problems)
			if hasFinished(html):
				break
		pool.wait_completion()
		print "------------------------------------------------------> " + problem_set + " done!"


if __name__ == "__main__":
	crawl_all_problems()
	