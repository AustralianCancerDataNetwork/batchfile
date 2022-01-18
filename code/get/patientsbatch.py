# -*- coding: utf-8 -*-

import os
import pandas as pd
import json
import time


def main():
    #example. four patients with four studies
    df=pd.read_csv('patients.csv')
    summary={}#to save logs
    for index, row in df.iterrows():# for each study
        try:
            #set the unique identifier as the patient might have multiple studies
            descriptor=str(index)+'_'+ row['pid']
            start=time.time()#start
            pid=row['pid']
            print(pid)
            studyUID=row['studyUID']
            query=f'getscu -v -S -k 0008,0052="STUDY" -k 0010,0020={pid} -k 0020,000D={studyUID} -od results localhost 4242'
            #query=f'getscu -v -P -k 0008,0052="PATIENT" -k 0010,0020="{pid}" localhost 4242'
            print(query)
            os.system(query)
            #print(row['c1'], row['c2'])
            finish=time.time()
            summary[descriptor]={}
            summary[descriptor]['time']=finish-start
            summary[descriptor]['status']='success'
            summary[descriptor]['notes']=''
            summary[descriptor]['pid']=pid
            summary[descriptor]['studyUID']=studyUID
        except Exception as e:
            print(e)
            summary[descriptor]={}
            summary[descriptor]['status']='error'
            summary[descriptor]['notes']=e
            summary[descriptor]['pid']=pid
            summary[descriptor]['studyUID']=studyUID
    
    
    #once finished save the logs     
    with open('logs.json', 'w') as outfile:
        json.dump(summary, outfile)
    
    print(summary)

if __name__ == "__main__":
    main()

