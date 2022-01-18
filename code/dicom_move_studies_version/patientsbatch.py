# -*- coding: utf-8 -*-
"""
This is a script used to collect patient studies from the  DICOM PACS server

@author: Ali Haidar 1
"""
import os
import pandas as pd
import json
import time
from datetime import datetime

def main():
    #configfile
    configfilename='../configfile/codesconfig_test.json'
    with open(configfilename) as json_file:
        codes = json.load(json_file)
    aet=codes['aet']
    aem=codes['aem']
    aec=codes['aec']
    ip=codes['ip']
    port=codes['port']
    #patient batches load
    batch_name='batch_1'
    print(f'exporting: {batch_name}')
    logs=f'{batch_name}-logs.json'
    with open('batches.json') as json_file:
        batches = json.load(json_file)
    abatch=batches[batch_name]
    #This dataframe contains the pids with study status (if the study is in the local orthanc)
    df=pd.read_csv('required_studies_df_checkedlocally.csv')
    #select only the studies which are not found in the connected pacs
    df=df.loc[df['checkPACS']==False].reset_index(drop=True)
    #select the batch ids
    abatch['done']=False
    if abatch['done']:
        print('this batch is already exported.')
    df=df.loc[df['StudyUID'].isin(abatch['pids'])].reset_index(drop=True)#typooo should be pids, but already saved data in puds :( :(
    summary={}#to save logs
    v=df.shape[0]
    print(f'starting the export process with {str(v)} studies.')
    for index, row in df.iterrows():# for each study
        try:
            #set the unique identifier as the patient might have multiple studies
            descriptor=str(index)+'_'+ str(row['PatientId'])
            start=time.time()#start
            pid=row['PatientId']
            print(pid)
            studyUID=row['StudyUID']
            hashed_id=row['hashsed_id']#typo with s
            hashed_uid=row['hashed_uid']

            #print(query)
            query=f'movescu -S -v -d -k 0008,0052=IMAGE -k 0010,0020={pid} -k 0020,000D={studyUID} -aet {aet} -aem {aem} -aec {aec} {ip} {port}'
            os.system(query)
            #print(row['c1'], row['c2'])
            finish=time.time()
            summary[descriptor]={}
            summary[descriptor]['time']=finish-start
            summary[descriptor]['status']='success'
            summary[descriptor]['notes']=''
            summary[descriptor]['pid']=pid
            summary[descriptor]['studyUID']=studyUID
            summary[descriptor]['thedate']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            summary[descriptor]['hashed_id']=hashed_id
            summary[descriptor]['hashed_uid']=hashed_uid
        except Exception as e:
            print(e)
            summary[descriptor]={}
            summary[descriptor]['status']='error'
            summary[descriptor]['notes']=e
            summary[descriptor]['pid']=pid
            summary[descriptor]['studyUID']=studyUID
            summary[descriptor]['thedate']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            summary[descriptor]['hashed_id']=hashed_id
            summary[descriptor]['hashed_uid']=hashed_uid
            
    #update the batch, that it was executed
    batches[batch_name]['done']=True
    batches[batch_name]['thedate']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('batches.json', 'w') as outfile:
        json.dump(batches, outfile)
    
    #once finished save the logs     
    with open(logs, 'w') as outfile:
        json.dump(summary, outfile)
    
    print(summary)

if __name__ == "__main__":
    main()

