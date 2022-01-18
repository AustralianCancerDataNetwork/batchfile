# Export Batch Files from DICOM PACS to the CENTRE

## Overview

This repo was used to retrieve DICOM images from DICOM PACS through batch files to a research data centre.

This repo contains two methods to export the DICOM images:
- via patient StudyUID: this work fine for some cases. However, it might include ConeBeam CT (CBCT) images and other unneeded modalities in the export
- Through the patient SeriesUIDs, which was followed to transfer data.

## Sending Dicom Data 
Here are some examples for sending data from the DICOM PACS to a centre. You can run this from the cmd in the data centre (assuming it is already configured):

__Study:__ 
movescu -S -v -d -k 0008,0052=STUDY -k 0010,0020=__pid__ -k 0020,000D=__StudyUID__ -aet __THECALLER__ -aec __THECALLEDDICOMPACS__ -aem __MOVEDESTINATION__ __11.1.111.111__ __yyy__

__Series:__
movescu -S -v -d -k 0008,0052=SERIES -k 0010,0020=__pid__ -k 0020,000e=__SeriesUID__ -aet __THECALLER__ -aec __THECALLEDDICOMPACS__ -aem __MOVEDESTINATION__ __11.1.111.111__ __yyy__

where

- pid: is the patient identifier
- StudyUID: study identifier
- SeriesUID: series identifier
- '-aet': the caller asking for the data, assuming that it is already configured in the server
- '-aec': the called dicom pacs
- '-aem': the move destination
- 11.1.111.111: ip address of the dicom PACS
- yyy: the port the pacs using to allow dicom retrieval

## Usage

A json file that represents the configuration details contains details about the calling AE title, called AE title, and move destination AE title. It will be saved in a __configfiles__ directory.

The patient batches would be assumed ready, as csv files, and saved to a specified location in the data centre (can be changed in code).

The csv file contains two columns: the __PatientId__ and the __SeriesUID__

When the batch file is executed, the selected csv files will be loaded and executed to transfer the series belonging to that record to the data centre.


## Other Examples

There is also examples for:
- Using getscu to retrieve studies from a dicom PACs running on the localhost : batchfile\code\get
- Targeting a PACs in the localhost, e.g. an Orthanc to check if the connection is working properly via echoscu batchfile\code\ecp




