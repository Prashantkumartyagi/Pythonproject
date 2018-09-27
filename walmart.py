import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import urllib2
#%matplotlib inline

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.google.co.in/search?ei=EsSYW97nG4SA8gWXi6DQAw&q=walmart+20186&oq=walmart+20186&gs_l=psy-ab.3..0j0i22i30k1l5.70212.71156.0.71437.5.5.0.0.0.0.237.237.2-1.1.0....0...1c.1.64.psy-ab..4.1.237....0.Cyxc0yLTjOI#lrd=0x89b67d7455fbcca1:0x702639a09cfef5d8,1,,,"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
type(soup)
bs4.beautifulSoup
# Get the title
title = soup.title
print(title)
# Print out the text
text = soup.get_text()

