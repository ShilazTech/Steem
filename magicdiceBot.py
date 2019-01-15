from urllib.request import urlopen, HTTPError
import urllib.parse
from datetime import datetime
from datetime import timedelta
import time
import random
import re
from contextlib import suppress
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from beem.blockchain import Blockchain
from beem.block import Block
from Cryptodome.PublicKey import RSA
from Cryptodome import Random

#%%
def generate_keypair(bits=1024):
    random_generator = Random.new().read
    rsa_key = RSA.generate(bits, random_generator)
    return rsa_key.exportKey(), rsa_key.publickey().exportKey()
#%%
def bmpy(nodes,keys):                       
    from beem import Steem
    from beem.account import Account    
    from beem.comment import Comment  
    from beem.instance import set_shared_steem_instance
    s = Steem(keys=keys)
    set_shared_steem_instance(s)
    return Account, Comment, s  

def plot2D(x,y1,y2,y1label,y2label):
    fig, ax1 = plt.subplots(figsize=(14,3))
    tick_spacing = 15
    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-')
    ax2.plot(x, y2, 'r-')      
    ax1.set_xlabel('DateTime')
    ax1.set_ylabel(y1label, color='g')
    ax2.set_ylabel(y2label, color='r')  
    fig.autofmt_xdate()
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))    
    plt.show() 
    
def arvr(rollvalues,wind):
    rollvaluesS=rollvalues
    wfds=wind
    
    #for wind 1
    wind=wind    
    avgrollvalues=[]
    avgrollvaluesrands=[]
    index=[]
    lenv=len(rollvaluesS)
    rollvalues=rollvaluesS[lenv-2*wfds:lenv]
    lenv=len(rollvalues)
    for i in range(lenv):
        if i>=wind:
            index.append(i)
            minrollvalues=min(rollvalues[i-wind:i])
            maxrollvalues=max(rollvalues[i-wind:i])            
            rollvaluerand=[random.randint(minrollvalues,maxrollvalues) for x in range(wind)] 
            avgrand=int(sum(rollvaluerand)/(len(rollvaluerand)))
            avgrollvaluesrands.append(avgrand)   
            avgrollvalues.append(sum(rollvalues[i-wind:i])/wind)
#    try:        
    avgrollvaluesrand1=int(sum(avgrollvaluesrands)/(len(avgrollvaluesrands)))
    avgrollvalues1=int(avgrollvalues[len(avgrollvalues)-1])
    
    #for wind 2
    wind=wind-5
    avgrollvalues=[]
    avgrollvaluesrands=[]
    index=[]
    
    lenv=len(rollvaluesS)
    rollvalues=rollvaluesS[lenv-2*wfds:lenv]
    lenv=len(rollvalues)
    for i in range(lenv):
        if i>=wind:
            index.append(i)
            minrollvalues=min(rollvalues[i-wind:i])
            maxrollvalues=max(rollvalues[i-wind:i])            
            rollvaluerand=[random.randint(minrollvalues,maxrollvalues) for x in range(wind)] 
            avgrand=int(sum(rollvaluerand)/(len(rollvaluerand)))
            avgrollvaluesrands.append(avgrand)   
            avgrollvalues.append(sum(rollvalues[i-wind:i])/wind)
#    try:        
    avgrollvaluesrand2=int(sum(avgrollvaluesrands)/(len(avgrollvaluesrands)))
    avgrollvalues2=int(avgrollvalues[len(avgrollvalues)-1])
    
    #for wind 3
    wind=wind-5
    avgrollvalues=[]
    avgrollvaluesrands=[]
    index=[]
    lenv=len(rollvaluesS)
    rollvalues=rollvaluesS[lenv-2*wfds:lenv]
    lenv=len(rollvalues)
    for i in range(lenv):
        if i>=wind:
            index.append(i)
            minrollvalues=min(rollvalues[i-wind:i])
            maxrollvalues=max(rollvalues[i-wind:i])            
            rollvaluerand=[random.randint(minrollvalues,maxrollvalues) for x in range(wind)] 
            avgrand=int(sum(rollvaluerand)/(len(rollvaluerand)))
            avgrollvaluesrands.append(avgrand)   
            avgrollvalues.append(sum(rollvalues[i-wind:i])/wind)
#    try:        
    avgrollvaluesrand3=int(sum(avgrollvaluesrands)/(len(avgrollvaluesrands)))  
    avgrollvalues3=int(avgrollvalues[len(avgrollvalues)-1])
    
    #for wind 4
    wind=wind-5
    avgrollvalues=[]
    avgrollvaluesrands=[]
    index=[]
    lenv=len(rollvaluesS)
    rollvalues=rollvaluesS[lenv-2*wfds:lenv]
    lenv=len(rollvalues)
    for i in range(lenv):
        if i>=wind:
            index.append(i)
            minrollvalues=min(rollvalues[i-wind:i])
            maxrollvalues=max(rollvalues[i-wind:i])            
            rollvaluerand=[random.randint(minrollvalues,maxrollvalues) for x in range(wind)] 
            avgrand=int(sum(rollvaluerand)/(len(rollvaluerand)))
            avgrollvaluesrands.append(avgrand)   
            avgrollvalues.append(sum(rollvalues[i-wind:i])/wind)
       
    avgrollvaluesrand4=int(sum(avgrollvaluesrands)/(len(avgrollvaluesrands)))  
    avgrollvalues4=int(avgrollvalues[len(avgrollvalues)-1])
  
    return avgrollvaluesrand1,avgrollvaluesrand2,avgrollvaluesrand3,avgrollvaluesrand4,avgrollvalues1,avgrollvalues2,avgrollvalues3,avgrollvalues4
  

def MDrollavgs(wind,mylists):
    rollvalues=mylists[0]        
    owrollvalues=mylists[1]
    olrollvalues=mylists[2]
    uwrollvalues=mylists[3]
    ulrollvalues=mylists[4]
    
    lenro=len(rollvalues)
    lenow=len(owrollvalues)    
    lenol=len(olrollvalues)    
    lenuw=len(uwrollvalues) 
    lenul=len(ulrollvalues)
    
    avgrollvaluesrand1,avgrollvaluesrand2,avgrollvaluesrand3,avgrollvaluesrand4,avgrollvalues1,avgrollvalues2,avgrollvalues3,avgrollvalues4=arvr(rollvalues,wind)
    
    try:    
        avgrollvalues=int(sum(rollvalues[lenro-wind:lenro])/(lenro-wind))
    except:
        avgrollvalues=50
    try:        
        avgowrollvalues=int(sum(owrollvalues)/lenow)
    except:
        avgowrollvalues=55
    try:        
        avgolrollvalues=int(sum(olrollvalues)/lenol) 
    except:
        avgolrollvalues=50
    try:        
        avguwrollvalues=int(sum(uwrollvalues)/lenuw) 
    except:
        avguwrollvalues=45
    try:
        avgulrollvalues=int(sum(ulrollvalues)/lenul) 
    except:
        avgulrollvalues=50  
    MDavglist=[avgrollvalues,avgowrollvalues,avgolrollvalues,avguwrollvalues,avgulrollvalues,avgrollvaluesrand1,avgrollvaluesrand2,avgrollvaluesrand3,avgrollvaluesrand4,avgrollvalues1,avgrollvalues2,avgrollvalues3,avgrollvalues4]
    
    return MDavglist,rollvalues


def headdata(resultfound,wind,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,MDlists,blocknumber,accountset,newbetvalue,maxbet,nobtr,profitperbet,count,lossvalueMD,wonvalueMD):

    StartBlockLastloop=blocknumber
    now=datetime.utcnow()
    now=datetime.strftime(now, '%Y-%m-%d %H:%M:%S') 
    rollvaluesMD=MDlists[0]
    owrollvaluesMD=MDlists[1]
    olrollvaluesMD=MDlists[2]
    uwrollvaluesMD=MDlists[3]
    ulrollvaluesMD=MDlists[4]
    to_account="magicdice"
    blnend=2 
    blockstart=int(blocknumber) 
    if isinstance(timestamp, str): 
        timestampstartlastloop=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') 
        timestampstart=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  
    else:
        timestampstartlastloop=timestamp 
        timestampstart=timestamp
        
    headblock=b.get_current_block_num
    blockend=int(headblock())    
    rolladded=0
    time.sleep(1)
    
    print("Getting Data upto Latest Block")    
    if strategy==1:
        resultfoundT=resultfound
        resultfound=0
        if count<=1 or betted==0:           
            resultfound=resultfoundT+1
        betvaluescaled=0
        
        while blocknumber<=StartBlockLastloop or blnend>random.randint(0,0) or resultfound<resultfoundT:# or count>0:# or rolladded<=random.randint(0,0):# or bettingresult==0:# or #or  or :# bln<=blocknumberlast  
#            print(blocknumber,StartBlockLastloop,blnend)
            #print(blockstart,blockend,blnend)
            blst=list(b.stream(opNames=["transfer"], start=blockstart, stop=blockend))
            #print ("resultfound   ",resultfound)
            for msg in blst:            
                blocknumber=float(msg["block_num"])
#                print(blocknumber)
                timestamp=msg["timestamp"]        
                timestamp=timestamp.replace(tzinfo=None)
                #timestamp=datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
                if blocknumber>=blockstart and timestamp>timestampstart: 
                    #Data for MD account
                    if msg['to'] == to_account:
                        memo=msg["memo"]
                        if "under" in memo or "over" in memo:
                            lossvalueMD.append(float(msg["amount"]["amount"])) 
                            #bettingaccount=  msg['from']                              
                    if msg['from'] == to_account:
                        memo=msg["memo"]
                        if "won" in memo:# and msg['to']== bettingaccount: 
                            wonvalueMD.append(float(msg["amount"]["amount"])) 
                            #bettingresult=1
                    #Data for my accounts
                    if msg['from'] == to_account:                    
                        memo=msg["memo"]                    
                        memolist=memo.split()
                        if "lost" in memo and msg["to"] in accountset:                        
                            resultfound=resultfound+1  
                            if betvaluescaled==0:                                
                                newbetvalue=newbetvalue+random.randint(1,1)*newbetvalue
#                                newbetvalue=max(newbetvalue,betvalue)
#                                newbetvalue=min(maxbet,newbetvalue)
                                betvaluescaled=1
                                #rolladded=0
                        if "won" in memo and msg["to"] in accountset: 
                            wonvalue=wonvalue+float(msg["amount"]["amount"])
                            resultfound=resultfound+1 
                            newbetvalue=newbetvalue+random.randint(0,0)*newbetvalue
#                            newbetvalue=max(newbetvalue,betvalue)
#                            newbetvalue=min(maxbet,newbetvalue)
                        try:
                            if msg['to'] in accountset:                          
                                rollvalue=float(memolist[memolist.index("Roll:")+1]) 
                                rollvaluesMD.append(rollvalue)
                                #rolladded=0
                                if "over" in memo and "won" in memo:
                                    owrollvaluesMD.append(rollvalue)
                                if "over" in memo and "lost" in memo:
                                    olrollvaluesMD.append(rollvalue)
                                if "under" in memo and "won" in memo:
                                    uwrollvaluesMD.append(rollvalue)
                                if "under" in memo and "lost" in memo:
                                    ulrollvaluesMD.append(rollvalue)
                                rolladded=rolladded+1
                            
                        except:
                            x=1           
            try:
                timelast=timestamp
                now=datetime.utcnow()
                now=datetime.strftime(now, '%Y-%m-%d %H:%M:%S')  
                now=datetime.strptime(now, '%Y-%m-%d %H:%M:%S')                 
                timestampstart=timestamp
                if resultfound==0:
                    blockstart=blockstart   
                else:
                    blockstart=blockend
                time.sleep(0.05)
                headblock=b.get_current_block_num
                blockend=int(headblock())
                blnend=blockend-blockstart           
            except:
                time.sleep(0.05)   
    MDlists=[rollvaluesMD,owrollvaluesMD,olrollvaluesMD,uwrollvaluesMD,ulrollvaluesMD]
    TimeTaken=(timelast-timestampstartlastloop)/timedelta(seconds=1)    
    BlocksMined=blocknumber-StartBlockLastloop
    TimePerBlock=TimeTaken/BlocksMined
    try:
        TimePerRolling=TimeTaken/rolladded
    except:
        TimePerRolling=0
    TPB.append(TimePerBlock)
    TPR.append(TimePerRolling)     
    return resultfound,strategy,MDlists,blocknumber,newbetvalue,lossvalue,wonvalue,TPB,TPR,rolladded,timestamp,lossvalueMD,wonvalueMD    

def data(resultfound,wind,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,blocknumberlast,count,MDlists,keyset,accountset,to_account,datahistory,newbetvalue,maxbet,nobtr,profitperbet,lossvalueMD,wonvalueMD):
    rollvaluesMD=MDlists[0]
    owrollvaluesMD=MDlists[1]
    olrollvaluesMD=MDlists[2]
    uwrollvaluesMD=MDlists[3]
    ulrollvaluesMD=MDlists[4]
    rd=random.randint(0,len(accountset)-1)        
    keys=keyset[rd]
    Account, Comment, s=bmpy(nodes,keys)    
    acc = Account("magicdice")
    blocknumber=blocknumberlast
    #print("Getting History Data")
    if count==0:    
        for msg in acc.get_account_history(-1, datahistory,order=1):            
                try: 
                    if msg['from'] == to_account:
                        memo=msg["memo"]
                        memolist=memo.split()            
                        blocknumber=float(msg["block"])
                        timestamp=msg["timestamp"]  
                        timestamp=datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
                        timestamp=datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
                        if blocknumber>blocknumberlast:
                            try:
                                #if msg['to'] in accountset:
                                rollvalue=float(memolist[memolist.index("Roll:")+1]) 
                                rollvaluesMD.append(rollvalue)
                                if "over" in memo and "won" in memo:
                                    owrollvaluesMD.append(rollvalue)
                                if "over" in memo and "lost" in memo:
                                    olrollvaluesMD.append(rollvalue)
                                if "under" in memo and "won" in memo:
                                    uwrollvaluesMD.append(rollvalue)
                                if "under" in memo and "lost" in memo:
                                    ulrollvaluesMD.append(rollvalue)
                            except:
                                x=1
                except:
                    x=1
    MDlists=[rollvaluesMD,owrollvaluesMD,olrollvaluesMD,uwrollvaluesMD,ulrollvaluesMD]
    
    resultfound,strategy,MDlists,blocknumber,newbetvalue,lossvalue,wonvalue,TPB,TPR,rolladded,timestamp,lossvalueMD,wonvalueMD=headdata(resultfound,wind,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,MDlists,blocknumber,accountset,newbetvalue,maxbet,nobtr,profitperbet,count,lossvalueMD,wonvalueMD)
    
    return resultfound,strategy,betted,timestamp,blocknumber,MDlists,newbetvalue,lossvalue,wonvalue,TPB,TPR,rolladded,lossvalueMD,wonvalueMD


def mybetsignal(wind,strategy,MDlists,TPB,TPR,rolladded,newbetvalue,maxbet,betvalue,lossvalueMD,wonvalueMD,count):

    print("                                                  ")
    print("Roll added since last round             ", rolladded)
    
    MDavglist,rollvaluesMD=MDrollavgs(wind,MDlists)
    avgrollvaluesrandMD1=MDavglist[5]
    avgrollvaluesrandMD2=MDavglist[6]
    avgrollvaluesrandMD3=MDavglist[7]
    avgrollvaluesrandMD4=MDavglist[8]
    
    avgrollvaluesMD1=MDavglist[9]
    avgrollvaluesMD2=MDavglist[10]
    avgrollvaluesMD3=MDavglist[11]
    avgrollvaluesMD4=MDavglist[12]
    
    REavgrollvaluesrandMD1=100-avgrollvaluesrandMD1
    REavgrollvaluesrandMD2=100-avgrollvaluesrandMD2
    REavgrollvaluesrandMD3=100-avgrollvaluesrandMD3
    REavgrollvaluesrandMD4=100-avgrollvaluesrandMD4
    
    signal1=0
    signal2=0
    signal3=0
    signal4=0
    
    MinTvalue1=min(REavgrollvaluesrandMD1,avgrollvaluesMD1)
    MaxTvalue1=max(REavgrollvaluesrandMD1,avgrollvaluesMD1)
    
    MinTvalue2=min(REavgrollvaluesrandMD2,avgrollvaluesMD2)
    MaxTvalue2=max(REavgrollvaluesrandMD2,avgrollvaluesMD2)
    
    MinTvalue3=min(REavgrollvaluesrandMD3,avgrollvaluesMD3)
    MaxTvalue3=max(REavgrollvaluesrandMD3,avgrollvaluesMD3)
    
    MinTvalue4=min(REavgrollvaluesrandMD4,avgrollvaluesMD4)
    MaxTvalue4=max(REavgrollvaluesrandMD4,avgrollvaluesMD4)
    
    rollvalue1=10
    rolltype1="no"
    
    rollvalue2=10
    rolltype2="no"
    
    rollvalue3=10
    rolltype3="no"
    
    rollvalue4=10
    rolltype4="no"
             
    if avgrollvaluesMD1<avgrollvaluesrandMD1:# and rollvalueMD>MinTvalue1:
        signal1=1
        rolltype1="under "
        rollvalue1=MinTvalue1
    if  avgrollvaluesMD1>=avgrollvaluesrandMD1:# and rollvalueMD<=MaxTvalue1:  
        signal1=1        
        rolltype1="over "
        rollvalue1=MaxTvalue1
        
    if avgrollvaluesMD2<avgrollvaluesrandMD2:# and rollvalueMD>MinTvalue2:
        signal2=1
        rolltype2="under "
        rollvalue2=MinTvalue2
    if  avgrollvaluesMD2>=avgrollvaluesrandMD2:# and rollvalueMD<=MaxTvalue2:  
        signal2=1        
        rolltype2="over "
        rollvalue2=MaxTvalue2
        
    if avgrollvaluesMD3<avgrollvaluesrandMD3:# and rollvalueMD>MinTvalue3:
        signal3=1
        rolltype3="under "
        rollvalue3=MinTvalue3
    if  avgrollvaluesMD3>=avgrollvaluesrandMD3:# and rollvalueMD<=MaxTvalue3:  
        signal3=1        
        rolltype3="over "
        rollvalue3=MaxTvalue3
        
    if avgrollvaluesMD4<avgrollvaluesrandMD4:# and rollvalueMD>MinTvalue:
        signal4=1
        rolltype4="under "
        rollvalue4=MinTvalue4
    if  avgrollvaluesMD4>=avgrollvaluesrandMD4:# and rollvalueMD<=MaxTvalue:  
        signal4=1        
        rolltype4="over "
        rollvalue4=MaxTvalue4
    return signal1,signal2,signal3,signal4,rolltype1, rollvalue1,rolltype2, rollvalue2,rolltype3, rollvalue3,rolltype4, rollvalue4

def strategy1(accountset,keyset,lossvalue,newbetvalue,rolladded,signal1,rollvalue1,rolltype1,signal2,rollvalue2,rolltype2,signal3,rollvalue3,rolltype3,signal4,rollvalue4,rolltype4):
        
    resultfound=signal1+signal2+signal3
    betted=0
    while signal3==1: 
        slptime=0.05 
        a,b=generate_keypair(bits=1024)#rd=random.randint(0,len(accountset)-1)
        b=str(b)
        seed=b[100:120]
        seed = re.sub('[^a-zA-Z0-9 \n\.]', 'a', str(seed.lower()))
        rseed=seed[0:10]
        rd=random.randint(0,len(accountset)-1)
        from_account=accountset[rd]
        keys=keyset[rd] 
        try:                       
            Account, Comment, s=bmpy(nodes,keys)                                                    
            account = Account(from_account, steem_instance=s) 
            messageforseed=rolltype3  +str(rollvalue3)+ " " +str(rseed)            
            account.transfer("magicdice", newbetvalue, "STEEM", messageforseed)
            lossvalue=lossvalue+newbetvalue                             
            signal3=0
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("Account Used Was  :",  from_account) 
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO") 
            print("newbidvalue, messageforseed",newbetvalue, messageforseed) 
            betted=1
        except:
            signal3=1
            time.sleep(slptime)
            slptime=slptime+slptime
    
    while signal2==1:  
        slptime=0.05
        a,b=generate_keypair(bits=1024)#rd=random.randint(0,len(accountset)-1)
        b=str(b)
        seed=b[100:120]
        seed = re.sub('[^a-zA-Z0-9 \n\.]', 'a', str(seed.lower()))
        rseed=seed[0:10]
        rd=random.randint(0,len(accountset)-1)
        from_account=accountset[rd]
        keys=keyset[rd]        
        try:                       
            Account, Comment, s=bmpy(nodes,keys)                                                    
            account = Account(from_account, steem_instance=s)
            messageforseed=rolltype2  +str(rollvalue2)+ " " +str(rseed)            
            account.transfer("magicdice", newbetvalue, "STEEM", messageforseed)
            lossvalue=lossvalue+newbetvalue                             
            signal2=0
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("Account Used Was  :",  from_account) 
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO") 
            print("newbidvalue, messageforseed",newbetvalue, messageforseed) 
            betted=1
        except:
            signal2=1
            time.sleep(slptime)
            slptime=slptime+slptime
            
    while signal1==1:  
        slptime=0.05
        a,b=generate_keypair(bits=1024)#rd=random.randint(0,len(accountset)-1)
        b=str(b)
        seed=b[100:120]
        seed = re.sub('[^a-zA-Z0-9 \n\.]', 'a', str(seed.lower()))
        rseed=seed[0:10]
        rd=random.randint(0,len(accountset)-1)
        from_account=accountset[rd]
        keys=keyset[rd]           
        try:                       
            Account, Comment, s=bmpy(nodes,keys)                                                    
            account = Account(from_account, steem_instance=s) 
            messageforseed=rolltype1  +str(rollvalue1)+ " " +str(rseed)            
            account.transfer("magicdice", newbetvalue, "STEEM", messageforseed)
            lossvalue=lossvalue+newbetvalue                             
            signal1=0
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("Account Used Was  :",  from_account) 
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO") 
            print("newbidvalue, messageforseed",newbetvalue, messageforseed) 
            betted=1
        except:
            signal1=1
            time.sleep(slptime)
            slptime=slptime+slptime 
        
    return betted, lossvalue,resultfound
    
def mybet(StartPL,LastPL,pcount,resultfound,wind,pstrategy,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,blocknumberlast,count,MDlists,maxbet,keyset,accountset,to_account,datahistory,betvalue,profitperbet,newbetvalue,nobtr,lossvalueMD,wonvalueMD):
    rd=random.randint(0,len(keyset)-1)        
    keys=keyset[rd]
    Account, Comment, s=bmpy(nodes,keys)   
    now=datetime.utcnow()
    now=datetime.strftime(now, '%Y-%m-%d %H:%M:%S')  
    now=datetime.strptime(now, '%Y-%m-%d %H:%M:%S')     
    strategy=random.randint(strategy,strategy) 
    resultfound,strategy,betted,timestamp,blocknumberlast,MDlists,newbetvalue,lossvalue,wonvalue,TPB,TPR,rolladded,lossvalueMD,wonvalueMD=data(resultfound,wind,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,blocknumberlast,count,MDlists,keyset,accountset,to_account,datahistory,newbetvalue,maxbet,nobtr,profitperbet,lossvalueMD,wonvalueMD)
 
    PL=wonvalue/1000-lossvalue-0.1*newbetvalue*min(resultfound,3) -StartPL 
    print("                                                  ")
    print("LastPL     ", LastPL)
    print("Current PL ", PL) 
    
    if PL>0:
        newbetvalue=betvalue        
        wonvalue=0
        lossvalue=0
        pcount=0
        LastPL=0       
        pstrategy=strategy        
    else:
        newbetvalue=betvalue-PL/nobtr
        if PL<LastPL:
            pcount=pcount+1
            wttm=pcount*20
            print("waiting for  ", wttm,"seconds") 
            time.sleep(wttm)
        else:
            pcount=0
        newbetvalue=min(maxbet,newbetvalue)  
        if newbetvalue>=maxbet and newbetvalue>betvalue:  
            newbetvalue=betvalue
            wonvalue=0
            lossvalue=0
            pcount=0
        pstrategy=strategy 
    LastPL=PL
    
    signal1,signal2,signal3,signal4,rolltype1, rollvalue1,rolltype2, rollvalue2,rolltype3, rollvalue3,rolltype4, rollvalue4= mybetsignal(wind,strategy,MDlists,TPB,TPR,rolladded,newbetvalue,maxbet,betvalue,lossvalueMD,wonvalueMD,count)  
   
    if strategy==1:
        betted, lossvalue,resultfound=strategy1(accountset,keyset,lossvalue,newbetvalue,rolladded,signal1,rollvalue1,rolltype1,signal2,rollvalue2,rolltype2,signal3,rollvalue3,rolltype3,signal4,rollvalue4,rolltype4)
    
    return LastPL,pcount,pstrategy,strategy,betted,timestamp,TPB,TPR,blocknumberlast,newbetvalue,MDlists,lossvalue,wonvalue,from_account,lossvalueMD,wonvalueMD,resultfound

def mainloop(action,count,StartPL,pcount,resultfound,pstrategy,strategy,dv,betted,wonvalue,lossvalue,LastPL,wind,datasize,qc,datahistory,newbetvalue,betvalue,maxbet,profitperbet,nobtr,blocknumberlast,TPR,TPB,balsums,counts,to_account,from_account,accountset,keyset,timestamp):      
    while action==1:
        if count==0:       
            rollvaluesMD=[]
            owrollvaluesMD=[]
            olrollvaluesMD=[]
            uwrollvaluesMD=[]
            ulrollvaluesMD=[] 
            TPB=[]
            TPR=[]
            lossvalueMD=[]
            wonvalueMD=[]
        else:  
            datasize2=int(datasize/2)
            if len(rollvaluesMD)>=datasize:                   
                rollvaluesMD=rollvaluesMD[len(rollvaluesMD)-datasize:len(rollvaluesMD)]
            if len(owrollvaluesMD)>=datasize2:                   
                owrollvaluesMD=owrollvaluesMD[len(owrollvaluesMD)-datasize2:len(owrollvaluesMD)]
            if len(olrollvaluesMD)>=datasize2:                   
                olrollvaluesMD=olrollvaluesMD[len(olrollvaluesMD)-datasize2:len(olrollvaluesMD)]
            if len(uwrollvaluesMD)>=datasize2:                   
                uwrollvaluesMD=uwrollvaluesMD[len(uwrollvaluesMD)-datasize2:len(uwrollvaluesMD)]
            if len(owrollvaluesMD)>=datasize2:                   
                ulrollvaluesMD=ulrollvaluesMD[len(ulrollvaluesMD)-datasize2:len(ulrollvaluesMD)]
            if len(TPB)>=datasize:                   
                TPB=TPB[len(TPB)-datasize:len(TPB)]
            if len(TPR)>=datasize:                   
                TPR=TPR[len(TPR)-datasize:len(TPR)]     
            if len(lossvalueMD)>=datasize2:                   
                lossvalueMD=lossvalueMD[len(lossvalueMD)-datasize2:len(lossvalueMD)]
            if len(wonvalueMD)>=datasize2:                   
                wonvalueMD=wonvalueMD[len(wonvalueMD)-datasize2:len(wonvalueMD)]
            
        MDlists=[rollvaluesMD,owrollvaluesMD,olrollvaluesMD,uwrollvaluesMD,ulrollvaluesMD]
       
        LastPL,pcount,pstrategy,strategy,betted,timestamp,TPB,TPR,blocknumberlast,newbetvalue,MDlists,lossvalue,wonvalue,from_account,lossvalueMD,wonvalueMD,resultfound=mybet(StartPL,LastPL,pcount,resultfound,wind,pstrategy,strategy,betted,timestamp,TPB,TPR,from_account,lossvalue,wonvalue,blocknumberlast,count,MDlists,maxbet,keyset,accountset,to_account,datahistory,betvalue,profitperbet,newbetvalue,nobtr,lossvalueMD,wonvalueMD)
    
        if qc==1 and (count/dv) % 1 == 0:            
            balsum=0
            balstart=0
            for i in range(len(accountset)): 
                    keys=keyset[i]
                    acc=accountset[i]
                    Account, Comment, s=bmpy(nodes,keys)  
                    account = Account(acc)
                    bal=account.balances
                    bal=str(bal["available"][0])                
                    bal=bal.split()  
                    print(account,bal)
                    balsum=balsum+float(bal[0])        
            balsum=balsum+newbetvalue
            balstart=balsum    
            counts.append(count)
            balsums.append(balsum)
            print("Total Balance   ", balsum)                 
            plot2D(counts,balsums,balsums,"Total Balance","Total Balance") 
        count=count+1    
        print("##################################################################")
        print("Count   :", count)
        print("##################################################################")
       

#Parameters
b = Blockchain(mode="head")
nodes=['https://api.steemit.com','https://api.steem.house','https://appbasetest.timcliff.com']##,'https://appbase.buildteam.io']

account1=["postingkey","activekey"]
account2=["postingkey","activekey"]
keyset=[account1,account2]
accountset=["account1","account2"]

to_account="magicdice"
from_account=accountset[0]

timestamp=datetime.utcnow()
timestamp=datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')  
timestamp=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')



blocknumberlast=0 ## last bet block number
nobtr=10 ### number of bets to recover current loss
profitperbet=0.05 ## Target profit per bet
betvalue=0.1 # starting bet value
maxbet=1   #max bet value
newbetvalue=betvalue
datahistory=200 # hwo much data from past to extract to do comuptatios for strategy
qc=1  # to control ploting for QC
datasize=40  ## datsize of data that will be used
wind=int(datasize/2) # largest window for computations 
count=0 # betcount

LastPL=0  # loss till last bet since start of program
lossvalue=0 # starting loss value
wonvalue=0 # starting won value

betted=0  # if betting is successful
dv=20  # to control plot for QC after how many bets
strategy=1 # starting strategy, currently only one strategy is used
pstrategy=1 # to help switch among strategies
resultfound=0 # to make sure that rolling results are extracted from blockchain from our bet before betting again

pcount=0 ## to control waite time between successive losses
StartPL=0 ##if program stops then to start again with same loss

counts=[] ## sum of counts
balsums=[]  ## balance of all accounts
TPB=[]
TPR=[]

action=1 ### continue in while loop

##Main loop
print("###################################################################")
print("Count   :", count)
print("###################################################################")      

mainloop(action,count,StartPL,pcount,resultfound,pstrategy,strategy,dv,betted,wonvalue,lossvalue,LastPL,wind,datasize,qc,datahistory,newbetvalue,betvalue,maxbet,profitperbet,nobtr,blocknumberlast,TPR,TPB,balsums,counts,to_account,from_account,accountset,keyset,timestamp)

    
    
       
            
        
    
