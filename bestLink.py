#!/usr/bin/python
# -*- coding: utf-8 -*-
import os;
import sys;
import bayes
import cosine_similarity
import keywordExtract
import pageCrawler
def run(query, DIR):
    rawdata = []
    print(DIR)
    x=0
    y=0
    while x<10:
        titleNo=os.popen("bash /var/www/project/getTitleNo "+ DIR +" "+ str(y)).read().strip();
        title=os.popen("bash /var/www/project/getTitle "+ DIR +" " + str(titleNo)).read().strip();
        abstract=os.popen("bash /var/www/project/getAbstract "+ DIR +" " + str(titleNo)).read().strip();
        link=os.popen("bash /var/www/project/getLink "+ DIR + " "+ str(titleNo)).read().strip();
        #paragraph=os.popen("bash getPara" + str(para)).read().strip();
        rawdata.append([]);
        y=y+1
        if ("www.youtube.com" not  in link) and (".pdf" not in link)and("images?" not in link):
            # to refer titleNo, use rawdata[x][0]
            rawdata[x].append(titleNo)
            #test to save

            # to refer title, use rawdata[x][1]
            rawdata[x].append(title)

            # to refer abstract, use rawdata[x][2]
            rawdata[x].append(abstract)

            # to refer link, use rawdata[x][3]
            rawdata[x].append(link)

            # to refer paragraph, use rawdata[x][4]
             
            x=x+1
    # convert query into vector
    query_vector=query.split()
    result=bayes.testingNB(query_vector)
    titles=[]
    for x in range(1,11):
       titles.append(rawdata[x-1][1])
    contents=[]
    for x in range(1,11):
       contents.append(rawdata[x-1][2])

       #classify the query and do the seperated search
    if(result==0):
      best_title=cosine_similarity.best_title_0(titles,query)
      for x in range(1,11):
           if(best_title==rawdata[x-1][1]):
              link=rawdata[x-1][3]
              print("Best title: ",rawdata[x-1][1])

    else:
      # best_content=cosine_similarity.best_title_1(titles,contents,query);
      best_content=cosine_similarity.best_title_1(titles,query,contents);
      for x in range(1,11):
           if(best_content==rawdata[x-1][2]):
              link=rawdata[x-1][3]
              print("Best title: ",rawdata[x-1][1])
    return link
      #         #according to link retrieve paragraphs
      #         #get keyword when finished
      #         #extract key word according toparagraph vector
      #         keywords=testSeperate.get_key_word(query)
      #         #get Synonyms
      #         Synonyms=testSeparate.get_synonyms(keywords)
      #         para_answer=get_best_paragraph(paras,keywords,Synonyms)
