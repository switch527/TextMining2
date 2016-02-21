
# coding: utf-8

# In[85]:

#import statements
import string
import math
from collections import Counter as ct
from nltk.tokenize import word_tokenize as wordTok
from nltk.tag import pos_tag


# In[86]:

#function to remove problem characters
def removeNonAscii(text):
    return ''.join(i for i in text if ord(i)<128)


# In[87]:

#open, read, remove problem characters, remove punctuation for tokenization
teslaSummary = removeNonAscii(open(
        "D:\Google Drive\Grad School\UIC\MS-MIS\IDS566\Assignment3\TeslaSummary1.txt", "r").read()).translate(None, string.punctuation)
NYTimes = removeNonAscii(open(
        "D:\Google Drive\Grad School\UIC\MS-MIS\IDS566\Assignment3\NYTimes.txt", "r").read()).translate(None, string.punctuation)
ESPN = removeNonAscii(open(
        "D:\Google Drive\Grad School\UIC\MS-MIS\IDS566\Assignment3\ESPN.txt", "r").read()).translate(None, string.punctuation)


# In[88]:

#tokenize the words
teslaSummaryTok = wordTok(teslaSummary)
NYTimesTok = wordTok(NYTimes)
ESPNTok = wordTok(ESPN)


# In[89]:

#tag the tokens
teslaSummaryPOS = pos_tag(teslaSummaryTok)
NYTimesPOS = pos_tag(NYTimesTok)
ESPNPOS = pos_tag(ESPNTok)


# In[90]:

#declare the list and dictionary variable that are about to be used
teslaSummaryTags = []
NYTimesTags = []
ESPNTags = []
#teslaSumTagCount = {}
#NYTimesTagCount = {}
#ESPNTagCount = {}
teslaSubLinearNorm = {}
NYTimesSubLinearNorm = {}
ESPNSubLinearNorm = {}


# In[91]:

#pull out only the tags, leave the words behind
x = 0
y = 0
z = 0
for i in teslaSummaryPOS:
    teslaSummaryTags.append(teslaSummaryPOS[x][1])
    x += 1
for i in NYTimesPOS:
    NYTimesTags.append(NYTimesPOS[y][1])
    y += 1
for i in ESPNPOS:
    ESPNTags.append(ESPNPOS[z][1])
    z +=1


# In[92]:

#count the tags
teslaSumTagCount = ct(teslaSummaryTags)
NYTimesTagCount = ct(NYTimesTags)
ESPNTagCount = ct(ESPNTags)


# In[93]:

#sublinear normalization
for key in teslaSumTagCount:
    x = teslaSumTagCount[key]
    if x > 0:
        teslaSubLinearNorm[key] =  1 + math.log(x)
for key in NYTimesTagCount:
    x = NYTimesTagCount[key]
    if x > 0:
        NYTimesSubLinearNorm[key] =  1 + math.log(x)
for key in ESPNTagCount:
    x = ESPNTagCount[key]
    if x > 0:
        ESPNSubLinearNorm[key] =  1 + math.log(x)


# In[94]:

#intersections
tesNYIntersection = {}
for item in teslaSubLinearNorm:
    if item in NYTimesSubLinearNorm:
        tesNYIntersection[item] = teslaSubLinearNorm[item] + NYTimesSubLinearNorm[item]

tesESPNIntersection = {}
for item in teslaSubLinearNorm:
    if item in ESPNSubLinearNorm:
        tesESPNIntersection[item] = teslaSubLinearNorm[item] + ESPNSubLinearNorm[item]

NYESPNIntersection = {}
for item in NYTimesSubLinearNorm:
    if item in ESPNSubLinearNorm:
        NYESPNIntersection[item] = NYTimesSubLinearNorm[item] + ESPNSubLinearNorm[item]


# In[95]:

#unions - I'm sure there is a more efficient way to do this but I don't know what it is
tesNYUnion = {}
for item in teslaSubLinearNorm:
    if item in NYTimesSubLinearNorm:
        tesNYUnion[item] = teslaSubLinearNorm[item] + NYTimesSubLinearNorm[item]
    else:
        tesNYUnion[item] = teslaSubLinearNorm[item]
for item in NYTimesSubLinearNorm:
    if item not in teslaSubLinearNorm:
        tesNYUnion[item] = NYTimesSubLinearNorm[item]
        
tesESPNUnion = {}
for item in teslaSubLinearNorm:
    if item in ESPNSubLinearNorm:
        tesESPNUnion[item] = teslaSubLinearNorm[item] + ESPNSubLinearNorm[item]
    else:
        tesESPNUnion[item] = teslaSubLinearNorm[item]
for item in ESPNSubLinearNorm:
    if item not in teslaSubLinearNorm:
        tesESPNUnion[item] = ESPNSubLinearNorm[item]
        
NYESPNUnion = {}
for item in NYTimesSubLinearNorm:
    if item in ESPNSubLinearNorm:
        NYESPNUnion[item] = NYTimesSubLinearNorm[item] + ESPNSubLinearNorm[item]
    else:
        NYESPNUnion[item] = NYTimesSubLinearNorm[item]
for item in ESPNSubLinearNorm:
    if item not in NYTimesSubLinearNorm:
        NYESPNUnion[item] = ESPNSubLinearNorm[item]


# In[96]:

#summations
tesNYIntSum = float(sum(tesNYIntersection.values()))
tesESPNIntSum = float(sum(tesESPNIntersection.values()))
NYESPNIntSum = float(sum(NYESPNIntersection.values()))
tesNYUnSum = float(sum(tesNYUnion.values()))
tesESPNUnSum = float(sum(tesESPNUnion.values()))
NYESPNUnSum = float(sum(NYESPNUnion.values()))


# In[98]:

#calculate jaccard sim
tesNYJaccard = tesNYIntSum / tesNYUnSum
tesESPNJaccard = tesESPNIntSum / tesESPNUnSum
NYESPNJaccard = NYESPNIntSum / NYESPNUnSum


# In[99]:

print tesNYJaccard, tesESPNJaccard, NYESPNJaccard

