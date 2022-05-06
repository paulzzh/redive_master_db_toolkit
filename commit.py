import sys
import os
from datetime import datetime

trustversion = sys.argv[1]
ctime = datetime.strptime(trustversion,"%Y%m%d%H%M").ctime()+" +0800"
os.chdir("redive_cn_master_db_diff")
os.system("git add .")
os.system("git commit -m "+trustversion)
os.system("GIT_COMMITTER_DATE="+"\""+ctime+"\""+" git commit --amend --date \""+ctime+"\" --no-edit")
