import requests
import datetime
import traceback
import socket
import threading
import json
from dateutil.relativedelta import relativedelta

socket.setdefaulttimeout(5)

headers={
"X-Unity-Version":"2018.4.30f1",
"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 10; Build/OKC1.180711.001)"
}
client_version = "client_ob_345"


#start_date=datetime.datetime(2022,5,1)
#end_date=datetime.datetime(2022,6,1)

start_date=datetime.datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)-relativedelta(days=1)
end_date=start_date+relativedelta(days=1)

errors=[]
old_errors=[]
finds=[]

def tryversion(trustversion):
    url = "https://l3-prod-patch-gzlj.bilibiligame.net/"+client_version+"/Manifest/AssetBundles/Android/"+trustversion+"/manifest/masterdata_assetmanifest"
    
    try:
        r = requests.get(url, headers=headers)
        
        if r.status_code == 404:
            return None
        if r.status_code == 200:
            return r.content
        
        print(trustversion,r.status_code)
        errors.append(trustversion)
        
    except Exception as e:
        traceback.print_exc()
        errors.append(trustversion)
        
    return None

def guess(date):
    print(date)
    for min in range(0,24*60):
        hm = date + datetime.timedelta(minutes=min)
        trustversion = hm.strftime("%Y%m%d%H%M")
        result = tryversion(trustversion)
        if result != None:
            print(trustversion)
            download(trustversion)
        #time.sleep(1)
        #print(trustversion)

def download(trustversion):
    try:
        url = "https://l3-prod-patch-gzlj.bilibiligame.net/"+client_version+"/Manifest/AssetBundles/Android/"+trustversion+"/manifest/masterdata_assetmanifest"
        r = requests.get(url, headers=headers)
        #a/masterdata_master.unity3d,7f80ea978e0215382420da20f1b3a7b9,tutorial2,3516927,
        _,md5,_,_,_ = r.text.split(",")
        url = "https://l3-prod-patch-gzlj.bilibiligame.net/"+client_version+"/pool/AssetBundles/Android/"+md5[:2]+"/"+md5
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            finds.append(trustversion)
            with open("bundle/master_"+trustversion+".unity3d","wb") as f:
                f.write(r.content)
        else:
            errors.append(trustversion)
    except Exception as e:
        traceback.print_exc()
        errors.append(trustversion)

now_date = start_date
threads = []
while now_date < end_date:
    thread = threading.Thread(target=guess, args=(now_date,))
    thread.start()
    threads.append(thread)
    now_date += datetime.timedelta(days=1)

for thread in threads:
    thread.join()
    print(thread)

while len(errors) > 0:
    print("errors",errors)
    old_errors=list(errors)
    errors=[]
    for trustversion in old_errors:
        result = tryversion(trustversion)
        if result != None:
            print(trustversion)
            download(trustversion)

with open("newtrustversions.txt","w") as f:
    f.write("\n".join(sorted(finds)))