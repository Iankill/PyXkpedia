import urllib.request
import re
from lxml import html


class BadArticleError(Exception): pass
class LoopingError(Exception): pass
class NoArticleError(Exception): pass

processed = []

def get_link(link):
	link = "http://en.wikipedia.org/wiki/" + link
	fh = urllib.request.urlopen(link)
	print(fh.geturl())
	return fh

def get_parsed_link(fh):
	return html.parse(fh)


def search(parsed):
	
	element_p_pos = 0
	pos = None


	while pos is None:
		if element_p_pos > 3:
			raise BadArticleError
		element_p_pos += 1
		

		if len(parsed.xpath("//*[@id=\"disambigbox\"]")) > 0: #Disambiguation article
			p = parsed.xpath("//*[@id=\"mw-content-text\"]/ul/li["+str(element_p_pos)+"]/node()")
			attrib = parsed.xpath("//*[@id=\"mw-content-text\"]/ul/li["+str(element_p_pos)+"]/*")
		elif parsed.xpath("//*[@id=\"noarticletext\"]") is True:
			raise NoArticleError
		else:
			p = parsed.xpath("//*[@id=\"mw-content-text\"]/p["+str(element_p_pos)+"]/node()")
			attrib = parsed.xpath("//*[@id=\"mw-content-text\"]/p["+str(element_p_pos)+"]/*")
			
		
		del_flag = False
		
		for i in range(len(p)):
			if re.search('\)[^\(]*\(',str(p[i])) is not None:
				del_flag = True
				p[i] = None
			if re.search('\)',str(p[i])) is not None and del_flag:
				p[i] = None
				del_flag = False
			if re.search('\([^\)]*$',str(p[i])) is not None:
				del_flag = True
			if del_flag:
				p[i] = None

			
		p = [el for el in p if el in attrib]
	
		for i in range(len(p)):
			if p[i] != str:
				if p[i] is not None and p[i].tag == 'a':
					if 'rel' in p[i].attrib:
						if p[i].attrib['rel'] == 'nofollow': #No follow link
							p[i] = None
					else:
						pos = i
						break

		if pos is not None:
			wiki_link = p[pos].attrib['href']
			next_link = re.sub(r'/wiki/','',wiki_link)

	if next_link in processed:
		raise LoopingError
	else:
		processed.append(next_link)
	print(next_link)
	return next_link	



for i in range(10):
	link = "Special:Random"
	processed = []
	print("New Test\n")
	while link != "Philosophy":
		try:
			link = search(get_parsed_link(get_link(link)))
		except BadArticleError:
			print("Bad Article Error")
			break
		except LoopingError:
			print("Detected a Loop")
			break
		except NoArticleError:
			print("No article Error")
			break
	print()

