import __init__ as provenance
import unittest
import os

DATASET = 'data.csv'

@provenance.create
def createDataset():
    fout = open(DATASET, 'w')
    fout.write('CREATED\n')
    return True

@provenance.modify
def modifyDataset(string):
    fout = open(DATASET, 'a')
    fout.write(str(string) + '\n')
    return True

@provenance.read
def readDataset():
    numLines = 0
    for line in open(DATASET, 'r'):
        numLines += 1
    return numLines

def countRecordEntries():
    numLines = 0
    for line in open(provenance.RECORD, 'r'):
        numLines += 1
    return numLines

# Here's our "unit tests".
class ProvenanceTests(unittest.TestCase):

    def setUp(self):
        # Create dataset
        provenance.setDataset(DATASET)
        createDataset()

    def tearDown(self):
        # Remove dataset and record
        provenance.reset()

    def testCreation(self):
        # Fails if dataset and record haven't been created.
        self.failUnless(os.path.exists(DATASET))
        self.failUnless(os.path.exists(provenance.RECORD))

    def testRead(self):
        self.failUnless(readDataset() == 1)

    def testModify(self):
        self.failUnless(countRecordEntries() == 1)
        modifyDataset('Testing')
        self.failUnless(countRecordEntries() == 2)

    def testViolate(self):
        fout = open(DATASET, 'a')
        fout.write('ILLEGAL CHANGE\n')
        fout.close()
        self.assertRaises(Exception, readDataset)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

green
