import json
fn='tmp_med_analyze_resp.json'
with open(fn,'r',encoding='utf-8',errors='ignore') as f:
    text=f.read()
try:
    data=json.loads(text)
except Exception as e:
    print('JSON parse error:',e)
    # try to find last JSON object in text
    import re
    matches=list(re.finditer(r"\{\s*\"scores?\"|\{", text))
    try:
        data=json.loads(text[text.rfind('{'):])
    except Exception as e2:
        print('fallback parse failed:',e2)
        raise

out={}
# Heuristic: if response is a list or dict
if isinstance(data, dict):
    # look for top-level matches
    if 'matches' in data:
        out['matches_count']=len(data['matches'])
        out['top_matches']=[{ 'patient_id':m.get('payload',{}).get('patient_id'), 'score':m.get('score') } for m in data['matches'][:5]]
    elif 'count' in data and isinstance(data.get('result'), list):
        out['count']=data.get('count')
    else:
        # try to find 'matches' anywhere
        for k,v in data.items():
            if isinstance(v,list) and len(v)>0 and isinstance(v[0],dict) and 'score' in v[0]:
                out['matches_count']=len(v)
                out['top_matches']=[{ 'patient_id':m.get('payload',{}).get('patient_id'), 'score':m.get('score') } for m in v[:5]]
                break

# write summary
with open('tmp_ai_analyze_summary.json','w',encoding='utf-8') as f:
    json.dump(out,f,indent=2)
print('WROTE tmp_ai_analyze_summary.json')
print(json.dumps(out,indent=2))
