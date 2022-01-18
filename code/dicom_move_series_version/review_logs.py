# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:41:34 2021

@author: 60183647
"""
import json

l='D:/AH/batcheslogs/logs.json'

with open(l, "r") as read_file:
    lo = json.load(read_file)
    
    
times=[]
for key in lo:
    value=lo[key]
    times.append(value['timetaken'])


logs_status=[]#status of each batch
instance_stats=[]#status of each instance
for key in lo:
    value=lo[key]
    logs_status.append(value['done'])
    for ins in value['batchlogs']:
        instance_stats.append(ins['exportstatus'])
    
