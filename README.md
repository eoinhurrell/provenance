#Provenance - provenance management for datasets in Python.

Provenance is an attempt to create a transparent means of showing the condition of a dataset, showing how it was created, the operatioons performed on it and its current condition. Since the integrity of a dataset is vitally important in data science this is an attempt to create an easy-to-use module to ensure data is not tampered with outside of the workflow.

Simply define the path to the dataset:

	provenance.setDataset('path/to/dataset')

A provenance file is then created alongside the dataset, by default named "<dataset>.provenance.json"

A series of decorators are provided for working with the defined dataset, which will add entries to the provenance file. 

* @provenance.create - for the method creates the dataset, creates the provenance file and notes creation details.
* @provenance.modify - for any method that writes or appends to the dataset.
* @provenance.read - for methods that read from but do not modify the dataset. 

Each of these decorators write a line in the provenance file, for example:
	{"function": "createDataset", "user": "Eoin", "file": "test.py", "time": 123141340, "integrity": "2b58790be3db9dbd9d5e5a8aa0578473", "mode": "CREATE"}
	
This line includes the name of the user who ran the code, the function and file that interacted with the dataset, and an integrity value, which is the MD5 of the file immediately after the function ran.
	
If the dataset is operated on without these decorators and changed they will detect an incorrect MD5 and throw an exception.