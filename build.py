import sqlite3,glob

folder="redive_cn_master_db_diff" #redive_master_db_diff

with open(folder+"/!TruthVersion.txt","r",encoding="utf-8") as f:
    v=f.readline().strip()

conn=sqlite3.connect("redive_"+v+".db")
for file in glob.glob(folder+"/*.sql"):
    with open(file,"r",encoding="utf-8") as f:
        for sql in f.read().split(";"):
            try:
                conn.execute(sql)
            except Exception as e:
                print(file,sql,e)

conn.commit()
conn.close()