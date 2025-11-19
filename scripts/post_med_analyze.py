import json, urllib.request, ssl
url='https://qdrant-ygtw.onrender.com/medical/analyze'
with open('tmp_med_analyze_req.json','rb') as f:
    data=f.read()
req=urllib.request.Request(url, data=data, headers={'Content-Type':'application/json','Accept':'application/json'})
# Create an unverified SSL context for environments missing root certs (local test only)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
    body=resp.read()
    status=resp.status
with open('tmp_med_analyze_resp.json','wb') as f:
    f.write(body)
print('WROTE tmp_med_analyze_resp.json', 'HTTP_STATUS:'+str(status))
