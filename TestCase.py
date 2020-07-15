#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import time
import signal
import threading
import gc

print()
print("--------------------------------------------------------------")
print("START SOFTWARE TESTING")
print("--------------------------------------------------------------")
print()
print()

Query = "The light Phone"
Query = sys.argv[1]
userID = "9999"

try:
    
    print("The User Query is [", Query ,"]")
    workDir = "/var/www/project/"
    returnlist=[]
    baseURL = Query.replace(" ","+")
    # URL = "https://www.google.com/search?num=20&q=" +URL
    URL = "https://www.google.com/search\?num\=30\&q\=" +baseURL
    print()
    print("--------------------------------------------------------------")
    print("\tSTART TEST Generate Correct URL")
    print("--------------------------------------------------------------")
    print()
    print(URL)
    print()
    print("--------------------------------------------------------------")
    print("\tEND TEST Generate Correct URL")
    print("--------------------------------------------------------------")
    print()
    #userID = 1;
    tempDir = "/var/www/project/Temp/temp"
    tempDir = tempDir + str(userID) + "/"
    if not os.path.exists(tempDir):
        os.makedirs(tempDir)
    print()
    print("--------------------------------------------------------------")
    print("\tSTART TEST Download Feature Snippt")
    print("--------------------------------------------------------------")
    print()
    #method ot store google featuredSnippet
    featuredSnippet = download_snippets.run(Query)
    if len(featuredSnippet)>1000:
        featuredSnippet=featuredSnippet[0:1000]
    print("\nHere is feature snippet")
    # print("Type of Sinppet:", type(featuredSnippet))
    # print("Type of URL:", type(URL))
    if sys.getsizeof(featuredSnippet) < 100:
        print("\nThere is no Snippet for this Query")
    else:
        print("\n", featuredSnippet)
        print()
        print("--------------------------------------------------------------")
        print("\tEND TEST Download Feature Snippt")
        print("--------------------------------------------------------------")
        print()

    # print(sys.getsizeof(featuredSnippet))
    if sys.getsizeof(featuredSnippet) > 100:
        URL = "https://www.google.com/search?num=30&q=" +baseURL
        returnlist.append(str(featuredSnippet))
        # print(returnlist)
        returnlist.append(str(URL))
        # print(returnlist)
        if os.path.exists(tempDir):
            shutil.rmtree(tempDir)

        # return  returnlist
    else:
        print()
        print("--------------------------------------------------------------")
        print("\tSTART TEST Keyword Extract")
        print("--------------------------------------------------------------")
        print()
        #method to store keyword in keywordResult
        keyword_Result = keywordExtract.run(Query)
        print(keyword_Result);
        print()
        print("--------------------------------------------------------------")
        print("\tEND TEST Keyword Extract")
        print("--------------------------------------------------------------")
        print()

        print()
        print("--------------------------------------------------------------")
        print("\tSTART TEST Generate Best URL")
        print("--------------------------------------------------------------")
        print()
        #download google result // slowing down
        # os.system("bash googleCrawler.sh " +tempDir + " " + URL)
        print("Downloading Google Results....")
        print("lynx -dump "+ URL + " >"+ tempDir + "gone.tmp")
        # pageCrawler.run(URL, tempDir, "gone.html")
        # os.system("lynx -dump "+tempDir+"gone.html > " + tempDir + "gone.tmp")
        os.system("timeout 8 lynx -dump "+ URL + " >"+ tempDir + "gone.tmp")



        #generate title No Abstract Links
        # os.system("bash generator.sh " + tempDir)
        print("generate info success")
        os.system("bash /var/www/project/generator.sh " + tempDir)


        # generate best page
        bestPageURL= bestLink.run(Query , tempDir )
        shortbestPageURL=bestPageURL
        # shortbestPageURL= os.popen("bash /var/www/project/shortBestLink " + bestPageURL).read().strip();

        # bestPageURL= "https://www.liverpool.ac.uk/files/docs/maps/liverpool-university-campus-map.pdf"
        print("Best Link " + bestPageURL)
        print()
        print("--------------------------------------------------------------")
        print("\tEND TEST Generate Best URL")
        print("--------------------------------------------------------------")
        print()

#done
        print()
        print("--------------------------------------------------------------")
        print("\tSTART TEST Generate Best Paragraph")
        print("--------------------------------------------------------------")
        print()

        #download Best Page
        print("Downloading Best Page....", shortbestPageURL)
        # os.system("lynx -dump "+ bestPageURL + " >"+ tempDir + "target.html")
        pageCrawler.run(shortbestPageURL, tempDir, "target.html")

        ##generate paragraph
        print("Generateing paragraph")
        os.system("pwd")
        os.system("bash /var/www/project/generateParagraph " + tempDir)
        os.system("chown www-data:www-data " + tempDir +"*")
        os.system("chown www-data:www-data " + tempDir)
        os.system("chmod 777 " + tempDir +"*")

        ## generate best paragraph
        paragraphNumber = os.popen("bash /var/www/project/getParagraphNo " + tempDir).read().strip();



        paragraphs=loadParagraph.run(tempDir, paragraphNumber)
        print("Testing the load Paragraph")
        # print(paragraphs)
        paragraph_vector=paragraph_to_vector.run(paragraphs)
        if (len(paragraph_vector)==0):
            best_para="Vec 1 No suitable paragraph. You can visit link."
        else:
            #probelm
            best_para=best_answer.run(paragraph_vector,keyword_Result,Query,paragraphs)
            if len(best_para)>1000:
                best_para=best_para[0:1000]
            # else:
                # best_para="Vec 2 No suitable paragraph. You can visit link."

            # if os.path.exists(tempDir):
                # shutil.rmtree(tempDir)
            print()
            print(best_para)
            print()
            print("--------------------------------------------------------------")
            print("\tEND TEST Generate Best Paragraph")
            print("--------------------------------------------------------------")
            print()

            returnlist.append(best_para)
            returnlist.append(bestPageURL)
            gc.collect()


        # return returnlist
except Exception:
        best_para="null"
        bestPageURL="null"
        returnlist.append(best_para)
        returnlist.append(bestPageURL)
        # return returnlist

print()
print("--------------------------------------------------------------")
print("END SOFTWARE TESTING")
print("--------------------------------------------------------------")
print()
print()
