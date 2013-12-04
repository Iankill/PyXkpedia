import urllib2, urllib
import re
from lxml import html




class BadArticleError(Exception): pass
class LoopingError(Exception): pass
class NoArticleError(Exception): pass



class Pediapy():

	def __init__(self):
		self.processed = []
		self.article = None

	def get_link(self,link):
		link = "http://en.wikipedia.org/wiki/" + link 
		fh = urllib2.urlopen(link)
		return fh
	
	def get_parsed_link(self,fh):
		return html.parse(fh)
	
	def search(self,parsed):
		
		element_p_pos = 0
		pos = None
	
	
		while pos is None:
			if element_p_pos > 3:
				raise BadArticleError
			element_p_pos += 1
			
	
			if len(parsed.xpath(u"//*[@id=\"disambigbox\"]")) > 0: #Disambiguation article
				p = parsed.xpath(u"//*[@id=\"mw-content-text\"]/ul/li["+unicode(element_p_pos)+u"]/node()")
				attrib = parsed.xpath(u"//*[@id=\"mw-content-text\"]/ul/li["+unicode(element_p_pos)+u"]/*")
			elif parsed.xpath(u"//*[@id=\"noarticletext\"]") is True:
				raise NoArticleError
			else:
				p = parsed.xpath(u"//*[@id=\"mw-content-text\"]/p["+unicode(element_p_pos)+u"]/node()")
				attrib = parsed.xpath(u"//*[@id=\"mw-content-text\"]/p["+unicode(element_p_pos)+u"]/*")
				
			
			del_flag = False
			
			for i in xrange(len(p)):
				if re.search(u'\)[^\(]*\(',unicode(p[i])) is not None:
					del_flag = True
					p[i] = None
				if re.search(u'\)',unicode(p[i])) is not None and del_flag:
					p[i] = None
					del_flag = False
				if re.search(u'\([^\)]*$',unicode(p[i])) is not None:
					del_flag = True
				if del_flag:
					p[i] = None
	
				
			p = [el for el in p if el in attrib]
		
			for i in xrange(len(p)):
				if p[i] != unicode:
					if p[i] is not None and p[i].tag == u'a':
						if u'rel' in p[i].attrib:
							if p[i].attrib[u'rel'] == u'nofollow': #No follow link
								p[i] = None
						else:
							pos = i
							break
	
			if pos is not None:
				wiki_link = p[pos].attrib[u'href']
				next_link = re.sub(ur'/wiki/',u'',wiki_link)
	
		if next_link in self.processed:
			raise LoopingError
		else:
			self.processed.append(next_link)

		return next_link	

	def new_search(self, article="Special:Random"):
		self.processed = []
		self.article = article
		while self.article != u"Philosophy":
			try:
				self.article = self.search(self.get_parsed_link(self.get_link(self.article)))	
				yield self.article
			except BadArticleError:
				print u"Bad Article Error"
				break
			except LoopingError:
				print u"Detected a Loop"
				break
			except NoArticleError:
				print u"No article Error"
				break


	def get_random_article_name(self):
		fh = self.get_link("Special:Random")
		url = fh.geturl()
		article_name = re.sub(ur'.*/wiki/',r'',url)
		return str(article_name)

	def is_valid_article(self, article):
		valid = True
		try:
			self.get_link(article)
		except urllib2.HTTPError:
			valid = False
		return valid


if __name__ == "__main__":
	wiki = Pediapy()
	wikiGenerator = wiki.new_search("France")
	for article in wikiGenerator:
		print article