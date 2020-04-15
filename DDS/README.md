This is code to create a DDS connection.
The code is thoroughly tested.
If the code gives an error, the problem will be the DDS settings.
Make sure to use the same 'Quality of service' on all DDS modules.

It's a bit tricky to get DDS up and running in python.
These are the steps i did:
* I use python 3.5.4
* I made an virtual environment and installed the DDS library in these folders. 
* I use the community version of OpenSplice

1. We need to use 'virtualenv' and 'Cython' so pip install these (if u don't have pip, also install this feature.)
2. Create a virtual environment:        
  virtualenv -p C:\Users\'UserName'\AppData\Local\Programs\Python\Python35\python.exe "Python_3.5.4“
3. call Python_3.5.4\Scripts\activate.bat
4. cd C:\OpenSplice_Community_V6.9\tools\python\src
5. python setup.py install
6. Try an import from the command prompt: py, import dds
7. Open Opensplice example: select the correct environment via the settings (settings.json):
   "python.pythonPath": "C:\\Users\\'UserName'\\Python_3.5.4\\Scripts\\python.exe"
8. Open Powershell as administrator, Set-ExecutionPolicy RemoteSigned
