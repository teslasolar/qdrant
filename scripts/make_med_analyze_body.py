import base64, json
p='collab/miracle/generated_images/P007_chest.png'
with open(p,'rb') as f:
    b=base64.b64encode(f.read()).decode('ascii')
obj={'image_base64':b,'metadata':{'source':'test','patient_id':'LOCAL_TEST'}}
with open('tmp_med_analyze_req.json','w',encoding='utf-8') as f:
    json.dump(obj,f,separators=(',',':'))
print('WROTE tmp_med_analyze_req.json')
