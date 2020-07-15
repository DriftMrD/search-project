#!/usr/bin/env python
# coding=utf-8
import keywordExtract
import pageCrawler
import os
import download_snippets
import bestLink
import time
import loadParagraph
import best_answer
import paragraph_to_vector
import shutil
import sys

Query= "University of liverpool Engineering introduction"
userID="9999"
print("Modifiey: Query ", Query)
workDir = "/var/www/project/"
returnlist=[]
baseURL = Query.replace(" ","+")
# URL = "https://www.google.com/search?num=20&q=" +URL
URL = "https://www.google.com/search\?num\=30\&q\=" +baseURL
print(URL)
#userID = 1;
tempDir = "/var/www/project/temp"
tempDir = tempDir + str(userID) + "/"
if not os.path.exists(tempDir):
    os.makedirs(tempDir)
#method ot store google featuredSnippet
featuredSnippet = download_snippets.run(Query)
if len(featuredSnippet)>1000:
    featuredSnippet=featuredSnippet[0:1000]
print("Type of Sinppet:", type(featuredSnippet))
print("Type of URL:", type(URL))
#print(featuredSnippet)
print(sys.getsizeof(featuredSnippet))
if sys.getsizeof(featuredSnippet) > 100:
    URL = "https://www.google.com/search?num=30&q=" +baseURL
    returnlist.append(str(featuredSnippet))
    # print(returnlist)
    # returnlist.append(str(URL))
    print(returnlist)
    # if os.path.exists(tempDir):
        # shutil.rmtree(tempDir)

    # return  returnlist
else:
    #download google result // slowing down
    # os.system("bash googleCrawler.sh " +tempDir + " " + URL)
    print("Downloading Google Results....")
    print("lynx -dump "+ URL + " >"+ tempDir + "gone.tmp")
    # pageCrawler.run(URL, tempDir, "gone.html")
    # os.system("lynx -dump "+tempDir+"gone.html > " + tempDir + "gone.tmp")
    os.system("lynx -dump "+ URL + " >"+ tempDir + "gone.tmp")


    #method to store keyword in keywordResult
    keyword_Result = keywordExtract.run(Query)
    print(keyword_Result);

    #generate title No Abstract Links
    # os.system("bash generator.sh " + tempDir)
    os.system("bash /var/www/project/generator.sh " + tempDir)


    # generate best page
    bestPageURL= bestLink.run(Query , tempDir )
    bestPageURL= os.popen("bash /var/www/project/shortBestLink " + tempDir).read().strip();
    # bestPageURL= "https://www.liverpool.ac.uk/files/docs/maps/liverpool-university-campus-map.pdf"
    print("Best Link " + bestPageURL)


    #download Best Page
    print("Downloading Best Page....")
    # os.system("lynx -dump "+ bestPageURL + " >"+ tempDir + "target.html")
    pageCrawler.run(bestPageURL, tempDir, "target.html")

    ##generate paragraph
    print("Generateing paragraph")
    os.system("pwd")
    os.system("bash /var/www/project/generateParagraph " + tempDir)

    ## generate best paragraph
    paragraphNumber = os.popen("bash /var/www/project/getParagraphNo " + tempDir).read().strip();



    paragraphs=loadParagraph.run(tempDir, paragraphNumber)
    paragraph_vector=paragraph_to_vector.run(paragraphs)
    if (len(paragraph_vector)==0):
        best_para="No suitable paragraph. You can visit link."
    else:
        best_para=best_answer.run(paragraph_vector,keyword_Result,Query,paragraphs)
        if len(best_para)>1000:
            best_para=best_para[0:1000]

        # if os.path.exists(tempDir):
            # shutil.rmtree(tempDir)
        print("Best Paragraph:")
        print(best_para)

        returnlist.append(best_para)
        returnlist.append(bestPageURL)


    # return returnlist

