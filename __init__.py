#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Provenance module, to track changes to a dataset.

Author: Eoin Hurrell <UltimateHurl@gmail.com>
Created: 13-12-28

"""
import hashlib
from functools import wraps
import os
import pwd
import json
import time

DATASET = None
RECORD = None
USE_MD5 = True

LAST_INTEGRITY = None


def setDataset(dataset):
    """Set the path to the dataset."""
    global DATASET
    global RECORD
    DATASET = dataset
    if RECORD is None:
        RECORD = dataset + '.provenance.json'


def setRecord(record):
    """Set the path to the provenance record."""
    global RECORD
    RECORD = record


def reset():
    """Reset provenance entirely, deleting the dataset and record."""
    global DATASET
    global RECORD
    global USE_MD5
    global LAST_INTEGRITY
    if RECORD is not None:
        os.remove(RECORD)
        os.remove(DATASET)
    DATASET = None
    RECORD = None
    USE_MD5 = True
    LAST_INTEGRITY = None


def create(creatorFunc):
    """Verify the creation of the dataset and provenance details."""
    def _decorator(*args, **kwargs):
        global LAST_INTEGRITY
        # pre-func work (check if the file exists etc)
        if DATASET is None:
            #raise ProvenanceViolationException
            raise Exception
        if LAST_INTEGRITY is not None:
            #raise ProvenanceViolationException
            print LAST_INTEGRITY
            raise Exception
        #create the record file
        fout = open(RECORD, 'w')
        fout.close()
        response = creatorFunc(*args, **kwargs)
        # post-func work ()
        LAST_INTEGRITY = getIntegrity()
        # write details of this change to the record
        changeDetails = {}
        changeDetails['time'] = 0
        changeDetails['mode'] = 'CREATE'
        changeDetails['function'] = creatorFunc.__name__
        changeDetails['file'] = creatorFunc.__code__.co_filename
        changeDetails['user'] = getUsername()
        changeDetails['integrity'] = LAST_INTEGRITY
        writeToRecord(changeDetails)
        return response
    return wraps(creatorFunc)(_decorator)


def modify(modifyFunc):
    """Verify modification of the dataset and provenance details."""
    def _decorator(*args, **kwargs):
        global LAST_INTEGRITY
        # pre-func work (check if the file exists etc)
        # get integrity check of file and compare against last time
        integrityCheck()
        response = modifyFunc(*args, **kwargs)
        # post-func work ()
        # update LAST_INTEGRITY to reflect new file (I.e. this was an authorised change)
        LAST_INTEGRITY = getIntegrity()
        # write details of this change to the record
        changeDetails = {}
        changeDetails['time'] = time.time()
        changeDetails['mode'] = 'MODIFY'
        changeDetails['function'] = modifyFunc.__name__
        changeDetails['file'] = modifyFunc.__code__.co_filename
        changeDetails['user'] = getUsername()
        changeDetails['integrity'] = LAST_INTEGRITY
        writeToRecord(changeDetails)
        # if set store diff of file
        return response
    return wraps(modifyFunc)(_decorator)


def read(readFunc):
    """Verify reading of the dataset and provenance details."""
    def _decorator(*args, **kwargs):
        global LAST_INTEGRITY
        # pre-func work (check if the file exists etc)
        if DATASET is None:
            #raise ProvenanceViolationException
            raise Exception
        if LAST_INTEGRITY is None:
            #raise ProvenanceViolationException
            raise Exception
        # get integrity check of file and compare against last time
        integrityCheck()
        response = readFunc(*args, **kwargs)
        # post-func work ()
        LAST_INTEGRITY = getIntegrity()
        # write details of this change to the record
        changeDetails = {}
        changeDetails['time'] = time.time()
        changeDetails['mode'] = 'READ'
        changeDetails['function'] = readFunc.__name__
        changeDetails['file'] = readFunc.__code__.co_filename
        changeDetails['user'] = getUsername()
        changeDetails['integrity'] = LAST_INTEGRITY
        writeToRecord(changeDetails)
        return response
    return wraps(readFunc)(_decorator)

def datasetMd5():
    """Get the MD5 of the dataset."""
    md5 = hashlib.md5()
    fin = open(DATASET, 'r')
    while True:
        data = fin.read(32768)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def datasetModificationTime():
    """Get the last modification time of the dataset."""
    pass


def integrityCheck():
    """Check to ensure file hasn't been tampered with outside of provenance."""
    integrity = getIntegrity()
    if integrity != LAST_INTEGRITY:
        # raise ProvenanceViolationException, file changed outside of provenance line
        raise Exception


def getIntegrity():
    """Get the info needed for an integrity check against the file."""
    if USE_MD5:
        integrity = datasetMd5()
    else:
        integrity = datasetModificationTime()
    return integrity


def getUsername():
    return pwd.getpwuid( os.getuid() )[ 0 ]


def writeToRecord(changeDetails):
    """Write details of an operation to the provenance record."""
    fout = open(RECORD, 'a')
    fout.write(json.dumps(changeDetails) + '\n')
    fout.close()


def loadFromRecord():
    """Load last known state of the dataset from the proveance record."""
    pass


loadFromRecord()
