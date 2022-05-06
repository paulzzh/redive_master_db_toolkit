import requests
import UnityPy
import sqlite3
import os
import shutil
import traceback
import random

#trustversion = "202003311059"

headers={
"X-Unity-Version":"2018.4.30f1",
"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 10; Build/OKC1.180711.001)"
}
client_version = "client_ob_345"


#https://stackoverflow.com/questions/6677540/how-do-i-dump-a-single-sqlite3-table-in-python
def dumpsql(trustversion):
    dbpath = "db/"+trustversion+".db"
    conn = sqlite3.connect(dbpath)
    cu = conn.cursor()
    
    q = """
        SELECT "name", "type", "sql"
        FROM "sqlite_master"
            WHERE "sql" NOT NULL AND
            "type" == 'table'
            ORDER BY "name"
        """
    schema_res = cu.execute(q)
    for table_name, type, sql in schema_res.fetchall():
        if table_name.startswith('sqlite_'):
            continue
        
        with open("redive_cn_master_db_diff/"+table_name+".sql","w",encoding="utf-8") as f:
            f.write('{0};\n'.format(sql))
            
            table_name_ident = table_name.replace('"', '""')
            res = cu.execute('PRAGMA table_info("{0}")'.format(table_name_ident))
            column_names = [str(table_info[1]) for table_info in res.fetchall()]
            q = """SELECT 'INSERT INTO `{0}` VALUES ({1})' FROM "{0}";""".format(
                table_name_ident,
                ", ".join("""/*{0}*/'||quote("{0}")||'""".format(col.replace('"', '""')) for col in column_names))
            query_res = cu.execute(q)
            for row in query_res:
                f.write("{0};\n".format(row[0]))
     
    q = """
        SELECT "tbl_name", "type", "sql"
        FROM "sqlite_master"
            WHERE "sql" NOT NULL AND
            "type" == 'index'
        """
    schema_res = cu.execute(q)
    for table_name, type, sql in schema_res.fetchall():
        with open("redive_cn_master_db_diff/"+table_name+".sql","a",encoding="utf-8") as f:
            f.write('{0};\n'.format(sql))

def getdb(trustversion):
    env = UnityPy.load("bundle/master_"+trustversion+".unity3d")
    for path,obj in env.container.items():
        data=bytes(obj.read().script)
        with open("db/"+trustversion+".db","wb") as f:
            f.write(data)
        break

def writev(trustversion):
    with open("redive_cn_master_db_diff/!TruthVersion.txt","w",encoding="utf-8") as f:
        f.write(trustversion)

def writemans(trustversion):
    url = "https://l3-prod-patch-gzlj.bilibiligame.net/"+client_version+"/Manifest/AssetBundles/Android/"+trustversion+"/manifest/manifest_assetmanifest"
    manifests=writeman(url,"manifest")
    for line in manifests.split("\n"):
        path,_,_,_,_ = line.split(",")
        name=path.replace("manifest/","").replace("_assetmanifest","")
        url = "https://l3-prod-patch-gzlj.bilibiligame.net/"+client_version+"/Manifest/AssetBundles/Android/"+trustversion+"/"+path
        #print(url,name)
        writeman(url,name)

def writeman(url,name):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception
    with open("redive_cn_master_db_diff/+manifest_"+name+".txt","w",encoding="utf-8") as f:
        f.write(r.text)
    return r.text

def commit(trustversion):
    os.system("python commit.py "+trustversion)

def cleanup():
    shutil.rmtree("db")
    os.mkdir("db")
    os.remove("newtrustversions.txt")


with open("newtrustversions.txt","r") as f:
    for trustversion in f.read().split("\n"):
        done=False
        if trustversion == "":
            break
        while not done:
            try:
                getdb(trustversion)
                dumpsql(trustversion)
                writemans(trustversion)
                writev(trustversion)
                done = True
            except Exception as e:
                print(trustversion)
                traceback.print_exc()
        commit(trustversion)

cleanup()
