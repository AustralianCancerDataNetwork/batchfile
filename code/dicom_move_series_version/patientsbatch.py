# -*- coding: utf-8 -*-
"""
This is a script used to export patients series from the DICOM PACS server into the research PACS
"""
import os
import pandas as pd
import json
import time
from datetime import datetime

def main():
    #patient batches load
    batches_names=['breast_6','breast_7','breast_8','breast_9']
    #batches_names=['breast_0']
    print(f'exporting: {batches_names}')
    
    #configfiles of 
    configfilename='../configfile/codesconfig_test.json'
    with open(configfilename) as json_file:
        codes = json.load(json_file)
    aet=codes['aet']
    aem=codes['aem']
    aec=codes['aec']
    ip=codes['ip']
    port=codes['port']
    
    #location of the log files.
    logsfilename='D:/AH/batcheslogs/new_logs_30_11.json'
    #open the log files
    with open(logsfilename) as json_file:
        logs = json.load(json_file)
    for abatch in batches_names:#for each batch in the batches 
        if abatch in logs:#check if the batch is already processed
            if 'done' in logs[abatch]:
                if logs[abatch]['done']:
                    #checking if the batch has already been done.
                    print('The batch has already been done.')
                    continue
        start=time.time()
        #reload the dataframe that contains the series uids + Patient ids.
        abatch_df=pd.read_csv(f'D:/AH/batches/batch_{abatch}.csv')
        print(f'starting the export process with {str(abatch_df.shape[0])} series {abatch}.')
        batchlogs=[]
        for index, row in abatch_df.iterrows():# for each row in the reloaded dataframe
            
            a_PatientId=row['PatientId']
            a_SeriesUID=row['SeriesUID']
            try:
                #move the series into the targeted location
                query=f'movescu -S -k 0008,0052=SERIES -k 0010,0020={a_PatientId} -k 0020,000e={a_SeriesUID} -aet {aet} -aem {aem} -aec {aec} {ip} {port}'
                os.system(query)
                alog={'batch':abatch,'PatientId':a_PatientId,'SeriesUID':a_SeriesUID,'exportstatus':'success'}
            except Exception as e:
                print(e)
                alog={'batch':abatch,'PatientId':a_PatientId,'SeriesUID':a_SeriesUID,'exportstatus':'error'}
            batchlogs.append(alog)
        finish=time.time()
        #add logs of the batch
        logs[abatch]={}
        logs[abatch]['batchlogs']=batchlogs#save the rows for each series
        logs[abatch]['timetaken']=finish-start#time taken for the export
        logs[abatch]['thedate']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logs[abatch]['done']=True
        print(f'time taken to export series in {abatch} was {finish-start}')
        
        
    #once finished save the logs     
    with open(logsfilename, 'w') as outfile:
        json.dump(logs, outfile)
    input('Enter to finish')

if __name__ == "__main__":
    main()

