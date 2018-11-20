# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import json
import os
import priorities
from datetime import datetime

jsonFileReq = {
	"filter": {
		"date": {
			"start": "2017-12-09 01:34:49",
			"end": "2017-12-13 03:08:42"
		},
		"priority": "Alta"
	},
	"order": {
		"DateCreate": "DESC",
		"DateUpdate": "ASC",
		"Priority": "DESC"
	}
}

app = Flask(__name__)

def prioridadeMensagem(mensagem):
    #Colocar aqui o código das priorities.py
    #os.system("python priorities.py " + mensagem)
    pass

def addPrioritys(jsonData):
    jsonData[0]["CategoryID"] = 11111
    jsonData[0]["Priority"] = "Alta"

    for data in jsonData:
        for mensagem in data['Interactions']:
            if mensagem['Sender'] == "Customer":
                # calcular a prioridade retornada para cada mensagem do json
                print(priorities.retornaPrioridade(mensagem['Message']))

    with open("ticketsTestes.json", "w") as write_file:
        json.dump(jsonData, write_file, indent=2, sort_keys=True)
    
    return jsonData

with open('ticketsTestes.json') as f:
    dataJson = json.load(f)
    dataJson = addPrioritys(dataJson)

@app.route('/', methods=['GET'])
def home():
    data = request.get_json()

    dataFiltered = dataJson

    if data.get('filter'):
        if data["filter"].get('date'):
            startDate = datetime.strptime(data["filter"]['date']["start"], '%Y-%m-%d %H:%M:%S')
            endDate = datetime.strptime(data["filter"]['date']["end"], '%Y-%m-%d %H:%M:%S')
            
            dataFiltered = [dat for dat in dataFiltered if  startDate <= datetime.strptime(dat["DateCreate"], '%Y-%m-%d %H:%M:%S') <= endDate]
        if data["filter"].get('priority'):
            priority = data["filter"]["priority"]
            dataFiltered = [dat for dat in dataFiltered if  dat.get("Priority") and dat["Priority"] == priority]

    if data.get('order'):
        if data['order'].get('DateCreate') and data['order'].get('DateUpdate') and data['order'].get('Priority'):
            dataFiltered = sorted(dataFiltered, key=lambda k: (datetime.strptime(k["DateCreate"], '%Y-%m-%d %H:%M:%S'), datetime.strptime(k["DateUpdate"], '%Y-%m-%d %H:%M:%S')))

    return jsonify(dataFiltered), 200

if __name__ == '__main__':
    app.run(debug=True)