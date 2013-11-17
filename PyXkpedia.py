import urllib.request
import re
from lxml import html

"""
Handle loops
Handle no article pages ("may refer to...") find disambigbox http://en.m.wikipedia.org/wiki/Valley_Lutheran_High_School

"""

def get_link(link):
	link = "http://en.m.wikipedia.org/wiki/" + link
	fh = urllib.request.urlopen(link)
	print(fh.geturl())
	return fh

def get_parsed_link(fh):
	return html.parse(fh)

def search(parsed):

	
	#print(fh.geturl())
	
	element_p_pos = 0
	pos = None

	while pos is None:
		element_p_pos += 1
		#print("element_p_pos :" + str(element_p_pos))
		p = parsed.xpath("//*[@id=\"content\"]/div[1]/p["+str(element_p_pos)+"]/node()")
		attrib = parsed.xpath("//*[@id=\"content\"]/div[1]/p["+str(element_p_pos)+"]/*")
		
		
		del_flag = False
		
		for i in range(len(p)):
			if re.search('\(',str(p[i])) is not None:
				del_flag = True
			if re.search('\)',str(p[i])) is not None and del_flag:
				p[i] = None
				del_flag = False
			if del_flag:
				p[i] = None


			
		p = [el for el in p if el in attrib]
	
		for i in range(len(p)):
			if p[i] != str:
				if p[i] is not None and p[i].tag == 'a':
					pos = i
					break
		if pos is not None:
			wiki_link = p[pos].attrib['href']
			next_link = re.sub(r'/wiki/','',wiki_link)

	
	#Go back if any 'a' in the 'p'
	print(next_link)
	return next_link


for i in range(10):
	link = "Special:Random"
	print("New Test")
	while link != "Philosophy":
		link = search(get_parsed_link(get_link(link)))


#print(pos)
#print(p)