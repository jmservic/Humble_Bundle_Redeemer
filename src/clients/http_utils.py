import http.cookies
import re

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
    good_format_regex = re.compile(r"(?:(\w*), (\d{1,2})-(\w*)-(\d{4}) (\d{1,2}):(\d{1,2}):(\d{1,2}) (\w+))")
    bad_format_regex = re.compile(r"(?:(\w*), (\d{1,2}) (\w*) (\d{2,4}) (\d{1,2}):(\d{1,2}):(\d{1,2}) (\w+))|(?:(\w*), (\d{1,2})-(\w*)-(\d{2}) (\d{1,2}):(\d{1,2}):(\d{1,2}) (\w+))")

    if good_format_regex.match(date_str):
        return date_str
    else:
        m = bad_format_regex.match(date_str)
        if m is not None:
            return f"{m[1]}, {m[2]}-{m[3]}-{m[4] if len(m[4]) == 4 else 2000 + m[4]} {m[5]}:{m[6]}:{m[7]} {m[8]}"

        return date_str
