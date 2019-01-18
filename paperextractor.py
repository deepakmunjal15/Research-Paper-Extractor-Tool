from Tkinter import *
import Tkinter
import tkMessageBox
import httplib, urllib
import re
import csv
import json


def interpret(key, keyword, complete, count_limit):
    keyword=keyword
    
    #Request Headers
    headers = {
            'Ocp-Apim-Subscription-Key': key,
            }
    
    #Request Parameters
    params = urllib.urlencode({
            'query': keyword,
            'complete': complete,
            'count': count_limit,
            'offset': '0',
            'timeout': '100',
            'model': 'latest',
            })
    
    try:
        conn = httplib.HTTPSConnection('api.labs.cognitive.microsoft.com')
        conn.request("GET", "/academic/v1.0/interpret?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
        
    values=re.findall(ur'''value":"(.+?)"''', str(data))
    return values

def evaluate(key, values, count_limit, date1, date2, attributes):
    final_data=[]
    
    headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': key,
            }
    k=0
    limit=count_limit
    for i in range(len(values)):
        expr="And("+values[i]+",D=['"+date1+"','"+date2+"'])"
        params = urllib.urlencode({
                # Request parameters
                'expr': expr,
                'attributes': attributes,
                'count': count_limit,
                'offset': '0',
                'timeout': '100',
                'model': 'latest',
                })        
        
        try:
            conn = httplib.HTTPSConnection('api.labs.cognitive.microsoft.com')
            conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            
        data = json.loads(data)
        
        for m in range(len(data["entities"])):
            k=k+1
            #title
            try:
                final_data.append([str(data["entities"][m]["Ti"])])
                #final_data=np.append(final_data, data["entities"][m]["Ti"])
            except (KeyError, AttributeError):
                h=0
                
            #abstract
            try:
                final_data.append([str(data["entities"][m]["IA"]["InvertedIndex"])])
            except (KeyError, AttributeError):
                h=0
                
            #paper date
            try:
                final_data.append([str(data["entities"][m]["D"])])
            except (KeyError, AttributeError):
                h=0
                
            #list of authors
            try:
                authors=[]
                for j in range(len(data["entities"][m]["AA"])):
                    authors.append(str(((data["entities"][m]["AA"][j]["AuN"]).encode('utf-8')).decode('utf-8')))
                final_data.append([str(authors)])
            except (KeyError, AttributeError):
                h=0
            final_data.append([""])
            if (k==limit) or (k>limit):
                break
        if (k==limit) or (k>limit):
            break
        
    return final_data


def user_values():
    
    try:
        key=Entry.get(E1)
        key=str(key)
        
        keyword=Entry.get(E2)
        keyword=str(keyword)
        
        complete=var1.get()
        complete=int(complete)
        
        count_limit=Entry.get(E3)
        count_limit=int(count_limit)
        
        date1=Entry.get(E4)
        date1=str(date1)
        
        date2=Entry.get(E5)
        date2=str(date2)
        
        title=var2.get()
        title=int(title)
        abstract=var3.get()
        abstract=int(abstract)
        author_name=var4.get()
        author_name=int(author_name)
        date=var5.get()
        date=int(date)        
        
        attributes=""
        if title==1:
            attributes=attributes+"Ti,"
        if abstract==1:
            attributes=attributes+"E.IA,"
        if author_name==1:
            attributes=attributes+"AA.AuN,"
        if date==1:
            attributes=attributes+"D"
            
            
        values=interpret(key, keyword, complete, count_limit)
        final_data=evaluate(key, values, count_limit, date1, date2, attributes)
        
        with open('paper_data.csv', 'w') as fp:
            writer = csv.writer(fp, delimiter=str(','))
            writer.writerows(final_data)
        
        tkMessageBox.showinfo("Success","Data has been collected in the file name paper_data.csv")
            
    except ValueError:
        tkMessageBox.showwarning("Warning","Please enter correct input")



top = Tkinter.Tk()
L1 = Label(top, text="Microsoft Academic Paper Extractor",).grid(row=0,column=1)

L2 = Label(top, text="Microsoft Academic Key",).grid(row=1,column=0)
E1 = Entry(top, bd =5)
E1.grid(row=1,column=1)



L3 = Label(top, text="Keyword",).grid(row=2,column=0)
E2 = Entry(top, bd =5)
E2.grid(row=2,column=1)

var1 = IntVar()
C1=Checkbutton(top, text="Strict Check", variable=var1, onvalue=1, offvalue=0)
C1.grid(row=3,column=1,sticky=W)
#C1.pack()

L4 = Label(top, text="Number of Paper Limit",).grid(row=4,column=0)
E3 = Entry(top, bd =5)
E3.grid(row=4,column=1)

L5 = Label(top, text="Date Range (YYYY-MM-DD)",).grid(row=5,column=0)
E4 = Entry(top, bd =5)
E4.grid(row=5,column=1)
L6 = Label(top, text="to      ",).grid(row=5,column=2)
E5 = Entry(top, bd =5)
E5.grid(row=5,column=3)

L7 = Label(top, text="Attributes Required",).grid(row=6,column=0)

var2 = IntVar()
C2=Checkbutton(top, text="Title", variable=var2, onvalue=1, offvalue=0)
C2.grid(row=7,column=1,sticky=W)
C2.select()
#C2.pack()
var3 = IntVar()
C3=Checkbutton(top, text="Abstract", variable=var3, onvalue=1, offvalue=0)
C3.grid(row=8,column=1,sticky=W)
C3.select()
#C3.pack()
var4 = IntVar()
C4=Checkbutton(top, text="Author Name", variable=var4, onvalue=1, offvalue=0)
C4.grid(row=9,column=1,sticky=W)
C4.select()
#C4.pack()
var5 = IntVar()
C5=Checkbutton(top, text="Date", variable=var5, onvalue=1, offvalue=0)
C5.grid(row=10,column=1,sticky=W)
C5.select()
#C5.pack()

B=Button(top, text ="Collect Data",command=user_values).grid(row=11,column=1,)

top.mainloop()

