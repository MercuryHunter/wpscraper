import urllib.request
import re

REDDIT = "http://www.reddit.com"
R = "/r/"

options = [["Luna_Lovewell", 10, True, 0, 2],
		   ["WritingPrompts", 10, False, 4, 1]]

def main():
	print("What would you like to retrieve?", end = "")
	question = ""
	for index, option in enumerate(options):
		question = question + "\n" + str(index) + " - " + option[0]
	answer = int(input(question + "\n"))
	print(get_from_options(answer))

def get_top_posts(subredditName="writingprompts", numPosts=10, description=False, numTopComments=1, ignoreFirst = 0):
	"""
	Get post contents of each of the top x posts of a subreddit
	"""
	page = get_html(REDDIT + R + subredditName)
	#print(page.encode("utf-8", 'ignore'))
	matches = re.findall('<a class="title.*?href="(.*?)".*?>(.*?)</a>', page)[ignoreFirst : ignoreFirst + numPosts]

	output = []
	outputfile = open('out.html', 'wb')
	for match in matches:
		current_line = []

		# Extract Title
		current_line.append(match[1].encode("utf-8", "ignore"))

		if description or numTopComments > 0:
			inner_page = get_html(REDDIT + match[0])

			# Extract Description
			if description:
				description_text = re.search('<div class="expando.*?<div class="usertext-body.*?<div class="md">(.*?)</div>', inner_page, re.DOTALL | re.MULTILINE)
				if not description_text:
					description_text = "NO CONTENT"
				else:
					description_text = description_text.group(0)
				#description_text = re.sub("<.*?>", "", description_text)
				current_line.append(description_text.encode("utf-8", "ignore"))

			# Extract Comments - TODO: Fix up
			comments = []
			comment_texts = re.findall('<div class="entry.*?<form action=.*?<div class="usertext-body.*?<div class="md">(.*?)</div>', inner_page, re.DOTALL | re.MULTILINE)
			for i in range(numTopComments):
				if i >= len(comment_texts):
					comment_text = "NO CONTENT"
				else:
					comment_text = comment_texts[i]
				comments.append(comment_text.encode("utf-8", "ignore"))
			current_line.append(comments)

		# Append to output array
		output.append(current_line)

		# Write to file
		index = 1
		outputfile.write(current_line[0] + b'\n')
		if description:
			outputfile.write(current_line[index] + b'\n<hr/>\n')
			index += 1
		for comment in current_line[index]:
			outputfile.write(comment + b'\n<hr/>')

	return "Written to out.html"

def get_from_options(number):
	return get_top_posts(*options[number])

def get_html(page):
	req = urllib.request.Request(page, headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
	with urllib.request.urlopen(req) as response:
   		return response.read().decode('utf-8')

if __name__ == '__main__':
	main()