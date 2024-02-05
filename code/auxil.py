"""
A companion file to script.py
"""

from pathlib import Path

targetDir = r"\\hq3fsvip01\MPI Detection\Data Unit Projects\05 Project"
allTargets = Path(targetDir).rglob("*")

i = 0
j = 0
k = 0
li = []
lis = []
for path in allTargets:
    i += 1
    if len(path.suffixes) <= 1:
        j += 1
        li.append(path)
    elif len(path.suffixes) > 1:
        k += 1
        lis.append(path)

i
# 179693

j
# 151913

k
# 27780

j + k == i
# True

li[:5]
# [WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/05 & 91 Link Analyis/05 91 Owners Miami-Dade.anb'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/05 & 91 Link Analyis/05 91 Owners.txt'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/05 & 91 Link Analyis/05 91 Owners.xlsx'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/05 Automated Reports/.Rhistory'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/05 Automated Reports/05 Report Files')]

lis[:5]
# [WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/1.5 Report/10-28-2020 to 11-23-2020 1.5 Report.xlsx'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/1.5 Report/10-28-2020 to 11-27-2020 1.5 Report.xlsx'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/1.5 Report/11-23-2020 1.5 Report.xlsx'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/Backbilling General/Ranking_of_Backbilling_05_Billing.V2.xlsx'),
#  WindowsPath('//hq3fsvip01/MPI Detection/Data Unit Projects/05 Project/Backbilling General/Ranking_of_Backbilling_05_Billing.V2_AR.xlsx')]

s1 = set()
for path in li:
    s1.update([path.suffix])
s2 = set()
for path in lis:
    s2.update([path.suffix])

len(s1)
# 95
len(s2)
# 9

sl = sorted(list(s1), reverse=True)
print(sl)

di = {suffix: [] for suffix in s1.union(s2)}
for path in allTargets:
    suffix = path.suffix
    di[suffix].append(path)

# Trying to read partially decodable text-like files
# https://www.i18nqa.com/debug/bug-double-conversion.html

path = r"\\hq3fsvip01\MPI Detection\Data Unit Projects\05 Project\HHS Campillo Request\All Claims (New Behavior Billing).hyper"
with open(path, "r", encoding=None) as file:
    text = file.read()
    # print(text[5000:15000])

# None -> charmap -> 0x8d -> position 4094 (char maps to undefinied)
# utf-8 -> utf-8 -> 0xe3 -> position 24 (invalid continuation byte)
# ascii -> ascii -> 0xe3 -> position 24 (ordinal not in range(128))

encoding = None
texts = []
for encoding in [None, "utf-8", "ascii"]:
    with open(path, "r", encoding=encoding) as file:
        text = ""
        temp = True
        log = []
        i = 0
        while temp:
            i += 1
            try:
                temp = file.read(2)
                text += temp
            except:
                temp = "X"
                text += temp
                log.append(i)
    texts.append(text)

"""
Variable            Type           Data/Info
--------------------------------------------
Path                type           <class 'pathlib.Path'>
allTargets          generator      <generator object Path.rg<...>ob at 0x00000242CD9BAB30>
context             NoneType       None
detection           bool           True
df                  DataFrame                               <...>1554223 rows x 5 columns]
dfdict              dict           n=4
el                  dict           n=5
keyword             str            Provider
keywords            list           n=4
kwFind              function       <function kwFind at 0x00000242CCF443A0>
kwFind_file         function       <function kwFind_file at 0x00000242CCF44A60>
kwFind_file_excel   function       <function kwFind_file_exc<...>el at 0x00000242CCF44700>
kwFind_file_txt     function       <function kwFind_file_txt at 0x00000242CCF44C10>
kwFind_folder       function       <function kwFind_folder at 0x00000242CCF444C0>
line                float          nan
np                  module         <module 'numpy' from 'C:\<...>ges\\numpy\\__init__.py'>
os                  module         <module 'os' from 'C:\\Us<...>\\Anaconda3\\lib\\os.py'>
path                WindowsPath    \\hq3fsvip01\MPI Detectio<...> - Recipient Record 1.pdf
pd                  module         <module 'pandas' from 'C:<...>es\\pandas\\__init__.py'>
re                  module         <module 're' from 'C:\\Us<...>\\Anaconda3\\lib\\re.py'>
results             list           n=0
rowNum              int            28897
rowTracker          dict           n=4
split               function       <function split at 0x00000242C6E343A0>
target              str            PRIETO LEMUS, ANGELA M 8901948761
targetDir           str            \\hq3fsvip01\MPI Detectio<...> Unit Projects\05 Project

In [74]: rowTracker
Out[74]: {'Provider': 28897, 'EM': 1554223, 'Code': 28623, 'Distribution': 27236}

In [80]: dfdict['EM'].sum()
Out[80]:
target       0.0
path         0.0
detection    0.0
line         0.0
context      0.0
dtype: float64

In [81]: dfdict['Provider'].sum()
Out[81]:
target       0.0
path         0.0
detection    0.0
line         0.0
context      0.0
dtype: float64

In [82]: dfdict['Code'].sum()
Out[82]:
target       0.0
path         0.0
detection    0.0
line         0.0
context      0.0
dtype: float64

In [83]: df.shape
Out[83]: (1554223, 5)

In [84]: df.head
Out[84]:
<bound method NDFrame.head of                                                     target  ... context
0                 FBHA Member Medicaid IDs edited 1.4.xlsx  ...    None
1                                    05 91 Grp Members.txt  ...    None
2                                   05 91 Grp Members.xlsx  ...    None
3                                    05 91 Owners Base.anb  ...    None
4                              05 91 Owners Miami-Dade.anb  ...    None
...                                                    ...  ...     ...
1554218  Perera, Mirbelys (PID 103394100) - FMMIS Provi...  ...    None
1554219  Valladares, Aymara (PID 012915700) - FMMIS Pro...  ...    None
1554220  PMH Mental Health Inc CMPL - 0017735 recvd 9.2...  ...    None
In [87]: mask = df['detection'] == True

In [88]: mask.shape
Out[88]: (1554223,)

In [89]: mask.sum()
Out[89]: 1517623

In [90]: x = df[mask]

In [91]: x.shape
Out[91]: (1517623, 5)

In [92]: x.head
Out[92]:
<bound method NDFrame.head of                                                     target  ...
                   context
27449    Abreu Labrada Francisca RID 8907961280  Recipi...  ...  Code: F41.9 Description: Unspecified Anxiety D...    
27450    Abreu Labrada Francisca RID 8907961280  Recipi...  ...  Code: F32.9 Description: Major Depressive, Sin...    
27467    Abreu Labrada Francisca RID 8907961280  Recipi...  ...   SERVICE DAY/DATE: Monday,11/25/2019 Code H2017\n    
27470    Abreu Labrada Francisca RID 8907961280  Recipi...  ...   SERVICE DAY/DATE: Monday 11/18/2019 Code H2017\n    
27476    Abreu Labrada Francisca RID 8907961280  Recipi...  ...  SERVICE DAY/DATE: Tuesday 11/12/2019 Code H2017\n    
...                                                    ...  ...                                                ...    
1553443                                NAPOLES ARCA EMILIA  ...                                               None    
1553444                          SANTANA SANTANA BARDEMIRO  ...                                               None    
1554010                                LEYVA LOPEZ EMIGDIA  ...                                               None    
1554126                                          ADA LEMUS  ...                                               None    
1554222                  PRIETO LEMUS, ANGELA M 8901948761  ...                                               None    

[1517623 rows x 5 columns]>

In [93]: x.iloc[0]
Out[93]:
target       Abreu Labrada Francisca RID 8907961280  Recipi...
path         \\hq3fsvip01\MPI Detection\Data Unit Projects\...
detection                                                 True
line                                                        10
context      Code: F41.9 Description: Unspecified Anxiety D...
Name: 27449, dtype: object

In [94]: x.iloc[0]['context']
Out[94]: 'Code: F41.9 Description: Unspecified Anxiety Disorder\n'
"""