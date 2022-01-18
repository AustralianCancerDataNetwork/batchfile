# Example Collecting Data using GETSCU


This example collected dicom studies via getscu to a local directory.



## Creating the csv file
```
import pandas as pd
di={'pid':['HN-CHUM-001','HN-CHUM-002','HN-CHUM-003','HN-CHUM-004'],
    'studyUID':['1.3.6.1.4.1.14519.5.2.1.5168.2407.301393959337245377111689674220',
               '1.3.6.1.4.1.14519.5.2.1.5168.2407.278462739048615906206672147530',
               '1.3.6.1.4.1.14519.5.2.1.5168.2407.766493466637820861735930889471',
               '1.3.6.1.4.1.14519.5.2.1.5168.2407.113300888456684122231592384223']}
df=pd.DataFrame(di)
df.to_csv('patients.csv',index=False)

```

## Images retrieval from the localhost

An Orthanc server was running in the localhost.
It was configured to be able to retrieve dicom.
The script __patientbatch.py__ was used to collect the patients studies in _patients.csv_ to the __results__ directory. 