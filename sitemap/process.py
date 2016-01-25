import gzip
from lxml import etree

for i in range(1,1000):
	text = gzip.open('sitemap.'+str(i)+'.xml.gz').read()
	root = etree.fromstring(text)
	for sitemap in root:
	    children = sitemap.getchildren()
	    if 'validurl' in children[0].text:
	    	print(children[0].text)
