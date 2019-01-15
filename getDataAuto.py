"""
Created on Tue Jul 17 09:11:57 2018
"""

#%%
from steem import Steem
# from pprint import pprint
import csv
import ast
import math
from steem.amount import Amount
from datetime import datetime
import pandas as pd
import time
s = Steem()
#%%

"""Required values for calculating payout for each vote"""
rewardFund = s.steemd.get_reward_fund()
rewardBalance, recentClaims = rewardFund['reward_balance'], rewardFund['recent_claims']
basePrice = s.steemd.get_current_median_history_price()['base']
""""Required values for calculating Tag values"""
tag_value_df = pd.read_csv(r'C:\Users\shant\Documents\SteemJPython\Tag_Values.csv')
tag_dict = {tag_value_df.loc[i,'Tag'] : tag_value_df.loc[i,'Payouts'] for i in range(100)}
""""Required values for calculating Steem Power of author"""
global_prop = s.steemd.get_dynamic_global_properties()
steem_per_vests = Amount(global_prop['total_vesting_fund_steem']).amount/Amount(global_prop['total_vesting_shares']).amount

##%%

def getVotesNPayout(post):
    voteDict = {"15min":0,  "30min": 0, "1hr": 0, "2hr": 0, "4hr": 0, "6hr": 0}
    payoutDict = {"15min":0,  "30min": 0, "1hr": 0, "2hr": 0, "4hr": 0, "6hr": 0}
    timeCreated = datetime.strptime(post['created'], '%Y-%m-%dT%H:%M:%S')
    for vote in post['active_votes']:
        vote_time = datetime.strptime(vote['time'], '%Y-%m-%dT%H:%M:%S')
        diffVoteTime = ((vote_time-timeCreated).total_seconds())
        if (diffVoteTime < (0.25 * 3600)):
            voteDict['15min'] += 1
            payoutDict['15min'] += float(vote['rshares'])
        if(diffVoteTime<(0.5*3600)):
            voteDict['30min'] += 1
            payoutDict['30min'] += float(vote['rshares'])
        if(diffVoteTime<(1*3600)):
            voteDict['1hr'] += 1
            payoutDict['1hr'] += float(vote['rshares'])
        if(diffVoteTime<(2*3600)):
            voteDict['2hr'] += 1
            payoutDict['2hr'] += float(vote['rshares'])
        if(diffVoteTime<(4*3600)):
            voteDict['4hr'] += 1
            payoutDict['4hr'] += float(vote['rshares'])
        if(diffVoteTime<(6*3600)):
            voteDict['6hr'] += 1
            payoutDict['6hr'] += float(vote['rshares'])
    for k in payoutDict:
        payoutDict[k] = get_payout_from_rshares(payoutDict[k])
    return get_vote_payout_speed(list(voteDict.values()), list(payoutDict.values()), timeCreated)

##%%

def get_vote_payout_speed(vote, payout, timeCreated):
    k=0.25
    for i in range(0,5):
        vote[i] /= k
        payout[i] /= k
        k *= 2
    vote[5] /= 6
    payout[5] /= 6
    return vote, payout

##%%

def get_payout_from_rshares(rshares):
    fund_per_share = Amount(rewardBalance).amount/float(recentClaims)
    payout = float(rshares) * fund_per_share * Amount(basePrice).amount
    return payout    

##%%

def get_commentSpeed(post):
    post_comments = (s.steemd.get_content_replies(post['author'], post['permlink']))
    commentDict = {"15min":0,  "30min": 0, "1hr": 0, "2hr": 0, "4hr": 0, "6hr": 0}
    timeCreated = datetime.strptime(post['created'], '%Y-%m-%dT%H:%M:%S')
    for comment in post_comments:
        comment_time = datetime.strptime(comment['created'], '%Y-%m-%dT%H:%M:%S')
        diffCommentTime = ((comment_time-timeCreated).total_seconds())
        if (diffCommentTime < (0.25 * 3600)):
            commentDict['15min'] += 1
        if(diffCommentTime<(0.5*3600)):
            commentDict['30min'] += 1
        if(diffCommentTime<(1*3600)):
            commentDict['1hr'] += 1
        if(diffCommentTime<(2*3600)):
            commentDict['2hr'] += 1
        if(diffCommentTime<(4*3600)):
            commentDict['4hr'] += 1
        if(diffCommentTime<(6*3600)):
            commentDict['6hr'] += 1
    commentSpeedList = list(commentDict.values())
    k = 0.25
    for i in range(0, 5):
        commentSpeedList[i] /= k
        k *= 2
    commentSpeedList[5] /= 6
    return commentSpeedList

def adjusted_reputation(raw_Reputation):
    neg = raw_Reputation < 0
    neg = -1 if neg else 1
    level = math.log10(abs(raw_Reputation))
    level = max(level - 9, 0)
    level *= neg
    return math.floor(level * 9 + 25)

def get_tag_value(post_tags):
    tag_value = 0
    for tag in post_tags:
        tag_value += tag_dict.get(tag, 0)
    return round(tag_value,4)

def get_promotion(author, permlink, post):
    # Calculate SBD/STEEM spend on bots
    account_history = s.get_account_history(author, index_from=-1, limit=1000)
    bot_tran = []
    timeCreated = datetime.strptime(post['created'], '%Y-%m-%dT%H:%M:%S')
    promotion = {"15min": 0, "30min": 0, "1hr": 0, "2hr": 0, "4hr": 0, "6hr": 0}
    for tran in account_history:
        op = tran[1]['op']
        transac_time = datetime.strptime(tran[1]['timestamp'], '%Y-%m-%dT%H:%M:%S')
        diffTransac_time = ((transac_time - timeCreated).total_seconds())/3600
        if (op[0] == 'transfer' and op[1]['amount'] != '0.001 SBD'):
            if (op[1]['memo'].find(permlink) != -1):                # Transferred to bot
                if (diffTransac_time < 0.25):
                    promotion['15min'] += Amount(op[1]['amount']).amount
                if (diffTransac_time < 0.5):
                    promotion['30min'] += Amount(op[1]['amount']).amount
                if (diffTransac_time < 1):
                    promotion['1hr'] += Amount(op[1]['amount']).amount
                if (diffTransac_time < 2):
                    promotion['2hr'] += Amount(op[1]['amount']).amount
                if (diffTransac_time < 4):
                    promotion['4hr'] += Amount(op[1]['amount']).amount
                if (diffTransac_time < 6):
                    promotion['6hr'] += Amount(op[1]['amount']).amount
                bot_tran.append([op[1]['to'], op[1]['amount']])
            elif ([op[1]['from'], op[1]['amount']] in bot_tran):    # Transferred to author due to some error
                if (diffTransac_time < 0.25):
                    promotion['15min'] -= Amount(op[1]['amount']).amount
                if (diffTransac_time < 0.5):
                    promotion['30min'] -= Amount(op[1]['amount']).amount
                if (diffTransac_time < 1):
                    promotion['1hr'] -= Amount(op[1]['amount']).amount
                if (diffTransac_time < 2):
                    promotion['2hr'] -= Amount(op[1]['amount']).amount
                if (diffTransac_time < 4):
                    promotion['4hr'] -= Amount(op[1]['amount']).amount
                if (diffTransac_time < 6):
                    promotion['6hr'] -= Amount(op[1]['amount']).amount
    return list(promotion.values())

##%%

def getData(iterPass, limitQuery, dataFile, mode=1):
    #Query for first post
    lastentry = [None,None]
    if(mode==1):
        dataset = pd.read_csv(dataFile, encoding = "ISO-8859-1")
        lastentry = dataset.iloc[-1,[0,1]].values    
    query1 = {
            "limit": 1 ,
            "start_author": lastentry[1],
            "start_permlink": lastentry[0]
        }
    posts1 = s.steemd.get_discussions_by_trending(query1)
    print("Start author  : %s" %posts1[0]['author'])
    print("Start permlink: %s" %posts1[0]['permlink'])
    
    #Starting url containing author and permlink
    data =[posts1[0]['permlink'], posts1[0]['author']]
    # pprint(data[1]+"/"+data[0])
    
    # Open file "dataSteemjAuto.csv" and write data in it.
    if(mode == 0):
        with open(dataFile, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Permlink', 'Author', 'Date Created', 'Time Diff(min)', 'Tag Score', 'Replies',
                             'Followers', 'No of Posts', 'Author Reputation',
                             'Promotion 15min', 'Promotion 30min', 'Promotion 1hr', 'Promotion 2hr', 'Promotion 4hr',
                             'Promotion 6hr', 'SBD author has', 'Liquid Steem', 'Steem Power', 'ReBlogged',
                             'VS 15min', 'VS 30min', 'VS 1hr', 'VS 2hr', 'VS 4hr', 'VS 6hr',
                             'CS 15min', 'CS 30min', 'CS 1hr', 'CS 2hr', 'CS 4hr', 'CS 6hr',
                             'PS 15min', 'PS 30min', 'PS 1hr', 'PS 2hr', 'PS 4hr', 'PS 6hr', 'PPV'])
        csvFile.close()
    
    """Required when appending data instead of writing a new dataset or use the query dictionary"""
    with open(dataFile, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(int(iterPass)):
            # datarows = []
            # start_time = time.time()
            posts = s.steemd.get_posts(limit=limitQuery, sort='trending', category='', start=data[1]+"/"+data[0])
            # pprint(posts[1]['author'])
            # pprint(posts[1]['permlink'])
            # len(posts)
            # start_time = time.time()
            for post in posts:
                try:
                    post = s.steemd.get_content(post['author'], post['permlink'])
                    author_data =  s.steemd.get_account(post['author'])
                    data = []
                    timeToday = datetime.utcnow()
                    timeCreated = datetime.strptime(post['created'], '%Y-%m-%dT%H:%M:%S')
                    timeDiff = (timeToday-timeCreated).total_seconds()
                    if(timeDiff>7*24*3600):
                        raise ValueError('Data Older than a week')
                    data.append(str(post['permlink']))
                    data.append(str(post['author']))
                    data.append(timeCreated)
                    data.append(timeDiff/60)
                    try:
                        postDict = post['json_metadata']
                        postDict = ast.literal_eval(postDict)
                        tags = postDict['tags']
                        tag_value = get_tag_value(post_tags=tags)
                        data.append(tag_value)
                    except Exception as e:
                        print('Exception: ' + str(e))
                        data.append(0)
                    data.append(post['children'])
                    data.append(s.steemd.get_follow_count(post['author'])['follower_count'])
                    data.append(author_data['post_count'])
                    data.append(adjusted_reputation(raw_Reputation=int(post['author_reputation'])))
                    data.extend(get_promotion(author=post['author'], permlink=post['permlink'], post=post))
                    data.append(Amount(author_data['sbd_balance']).amount)
                    data.append(Amount(author_data['balance']).amount)
                    data.append(Amount(author_data['vesting_shares']).amount*steem_per_vests)
                    # data.append(len(s.steemd.get_reblogged_by(post['author'], post['permlink'])))
                    voteSpeed, payoutSpeed = getVotesNPayout(post=post)
                    commentSpeed = get_commentSpeed(post=post)
                    data.extend(voteSpeed)
                    data.extend(commentSpeed)
                    data.extend(payoutSpeed)
                    data.append(Amount(post['pending_payout_value']).amount)
                    # datarows.append(data)
                    writer.writerow(data)
                    # print(data[0])
                except Exception as e:
                    print('Exception: ' + str(e))
                    print("Invalid data, Skipping....")
            # writer.writerows(datarows)
            # end_time = time.time()
            # pprint("%.4f" %(end_time-start_time))
            print("Pass" + str(i+1))
    csvFile.close()         
    print("Data Added")


##%%
def main(file_no=0,mode=1):
    """Total number of entries in dataset"""
    iterPass = 4
    limitQuery1 = 5
    dataFile = r'C:\Users\shant\Documents\SteemJPython\dataSteemjAuto_v'+str(file_no)+'.csv'

    start_time = time.time()
    # Calling getData()
    # Mode 0: New Dataset.csv
    # Mode 1: Update older csv
    getData(iterPass, limitQuery1, dataFile, mode)
    end_time = time.time()
    time_span = end_time - start_time
    print("Total time  : %.4f" %time_span)
    print("Time per post: %.4f" %(time_span/(iterPass*limitQuery1)))

    # Adding .csv to dataset
    dataset = pd.read_csv(dataFile, encoding = "ISO-8859-1")
    print("Dataset Shape: %d, %d." %(dataset.shape[0],dataset.shape[1]))

##main(file_no=14, mode=1)
