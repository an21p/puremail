import json

inf = open("rooms.json", "w")
inf.write('[\n')

for i in range(1, 701):
    data = {}
    fields = {}
    fields['number'] = i
    data['fields'] = fields
    data['pk'] = i
    data['model'] = "dashboard.room"
    json_data = json.dumps(data)
    inf.write(json_data+',\n')

inf.write(']\n')
inf.close()
