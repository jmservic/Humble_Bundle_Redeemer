import http.cookies
from datetime import datetime

def SetCookieHeaderToMorsels(headers):
    #headers is a list of (header, value) tuples like that returned from HTTPResponse.getheaders()
    morsels = http.cookies.SimpleCookie() 
    for (name, value) in headers:
        if(name == "Set-Cookie"):
            morsels.load(rawdata=value)
            #print(morsels.keys())
            #print(value)
    for morsel in morsels.values():
        if "expires" in morsel.keys():
            #print("before", morsel["expires"])
            morsel["expires"] = createRequestDateTimeStr(morsel["expires"])
            #print("after", morsel["expires"])
    return morsels

def createRequestDateTimeStr(date_str):
    try:
        new_date_str = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        return new_date_str
    except:
        try:
            new_date_str = datetime.strptime(date_str, "%a, %d-%b-%y %H:%M:%S GMT").strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            return new_date_str
        except:
            return date_str
        
