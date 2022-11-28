import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
	if len(sys.argv) != 2:
		sys.exit("Usage: python pagerank.py corpus")
	corpus = crawl(sys.argv[1])
	ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
	print(f"PageRank Results from Sampling (n = {SAMPLES})")
	for page in sorted(ranks):
		print(f"  {page}: {ranks[page]:.4f}")
	ranks = iterate_pagerank(corpus, DAMPING)
	print(f"PageRank Results from Iteration")
	for page in sorted(ranks):
		print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
	"""
	Parse a directory of HTML pages and check for links to other pages.
	Return a dictionary where each key is a page, and values are
	a list of all other pages in the corpus that are linked to by the page.
	"""
	pages = dict()

	# Extract all links from HTML files
	for filename in os.listdir(directory):
		if not filename.endswith(".html"):
			continue
		with open(os.path.join(directory, filename)) as f:
			contents = f.read()
			links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
			pages[filename] = set(links) - {filename}

	# Only include links to other pages in the corpus
	for filename in pages:
		pages[filename] = set(
			link for link in pages[filename]
			if link in pages
		)

	return pages


def transition_model(corpus, page, damping_factor):
	"""
	Return a probability distribution over which page to visit next,
	given a current page.

	With probability `damping_factor`, choose a link at random
	linked to by `page`. With probability `1 - damping_factor`, choose
	a link at random chosen from all pages in the corpus.
	"""
	#define dictionary with probabilities
	probability_dict = {}
	#get links from random page
	links_page = corpus[page]
	for link in links_page:
		probability_dict[link] = damping_factor * (1 / (len(links_page)))

	#get links from all pages in the corpus
	links_total = []
	for page in corpus:
		links_total.append(page)
		probability_dict[page] = 0
	for link in links_total:
		probability_dict[link] = probability_dict[link] + ((1 - damping_factor) * (1 / len(links_total)))
	return probability_dict

def sample_pagerank(corpus, damping_factor, n):
	"""
	Return PageRank values for each page by sampling `n` pages
	according to transition model, starting with a page at random.

	Return a dictionary where keys are page names, and values are
	their estimated PageRank value (a value between 0 and 1). All
	PageRank values should sum to 1.
	"""
	#get list of pages
	pages = list(corpus.keys())
	#set list of random pages
	pages_random = {}
	for page in pages:
		pages_random[page] = 0
	#choose random page
	page_one = random.choice(pages)
	#update probability of first page
	pages_random[page_one] = 1 / n
	#get probability of going to second page based on first page
	probability_current = transition_model(corpus, page_one, damping_factor)
	#sample through n -1 probabilities 
	for p in range(0, n - 1):
		# get random page based on current probability
		page_next = random.choices(list(probability_current.keys()), \
					list(probability_current.values()), k=1)
		pages_random[page_next[0]] = pages_random[page_next[0]] + 1 / n
		#update probability
		probability_current = transition_model(corpus, page_next[0], damping_factor)
	return pages_random

def iterate_pagerank(corpus, damping_factor):
	"""
	Return PageRank values for each page by iteratively updating
	PageRank values until convergence.

	Return a dictionary where keys are page names, and values are
	their estimated PageRank value (a value between 0 and 1). All
	PageRank values should sum to 1.
	"""
	raise NotImplementedError


if __name__ == "__main__":
	main()
