"""
This script downloads the version of CORAAL I used in my project from the repository.
It automatically cleans garbage files to the best of its ability.
For ease of use, do not rename any directories!
Feel free to comment out subcorpora you don't want to include below. I used all of them.
Note that I am on a Windows system, and you may need to modify the unzip and clean commands on your system.

Outputs coraal/, a directory of .txt transcriptions of all publicly available CORAAL data.
Runs in ~ 5 seconds on my machine.
"""

import os
from requests import get
from subprocess import call

unzip_command = 'tar -xvzf'
clean_command = 'echo y | rd /s \"\\\\?\\\"'

def make_output_dir(output_dir: str): # make the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir

output_dir = make_output_dir('coraal')

files = [ # files to download
    'http://lingtools.uoregon.edu/coraal/atl/2020.05/ATL_textfiles_2020.05.tar.gz',
    'http://lingtools.uoregon.edu/coraal/dca/2018.10.06/DCA_textfiles_2018.10.06.tar.gz',
    'http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_textfiles_2018.10.06.tar.gz',
    'http://lingtools.uoregon.edu/coraal/les/2021.07/LES_textfiles_2021.07.tar.gz',
    'http://lingtools.uoregon.edu/coraal/prv/2018.10.06/PRV_textfiles_2018.10.06.tar.gz',
    'http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_textfiles_2020.05.tar.gz',
    'http://lingtools.uoregon.edu/coraal/vld/2021.07/VLD_textfiles_2021.07.tar.gz'
]

def download(url: str, path: str): # download a file from CORAAL
    with get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

for file in files: # download each file and unzip it
    fname = file.split('/')[-1]
    download(file, os.path.join(output_dir, fname))
    call(unzip_command + ' ' + fname, shell=True, cwd=output_dir)
    
for file in os.listdir(output_dir): # clean garbage as best as possible
    if file.endswith('.tar.gz') or file.startswith('.'):
        try:
            os.remove(os.path.join(output_dir, file))
        except:
            try:
                call(clean_command + os.path.join(output_dir, ''), shell=True)
            except:
                pass