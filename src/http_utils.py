
import http.cookies

def SetCookieHeaderToMorsels(headers):
    #headers is a list of (header, value) tuples like that returned from HTTPResponse.getheaders()
    morsels = http.cookies.SimpleCookie() 
    for (name, value) in headers:
        if(name == "Set-Cookie"):
            morsels.load(rawdata=value)
    return morsels
