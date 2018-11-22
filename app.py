# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import json
import os
import priorities
from datetime import datetime
from math import ceil

'''
Exemplo de requisição GET para esta API:
jsonReq = {
	"filter": {
		"date": {
			"start": "2017-01-09 01:34:49",
			"end": "2017-12-13 03:08:42"
		},
		"priority": "Alta"
	},
	"order": {
		"Priority": "ASC",
	},
	"pagination": {
		"limit": 20,
		"page": 2
	}
}
'''

app = Flask(__name__)

def addPrioritys(jsonData):
    for data in jsonData:
        customers = 0
        pontosPrioridade = 0

        for mensagem in data['Interactions']:
            if mensagem['Sender'] == "Customer":
                customers += 1
                # calcular a prioridade retornada para cada mensagem do json
                if priorities.retornaPrioridade(mensagem['Message']) == 'alta':
                    pontosPrioridade += 0.25
                else:
                    pontosPrioridade -= 0.25

        # descobrir se é a primeira interação com o cliente
        if customers > 1:
            pontosPrioridade += 0.25
        else:
            pontosPrioridade -= 0.25

        # verifica os meses de espera do cliente entre a primeira interação e a resposta
        diasDiferenca = datetime.strptime(data['DateUpdate'], '%Y-%m-%d %H:%M:%S') - datetime.strptime(data['DateCreate'], '%Y-%m-%d %H:%M:%S')
        qtdDias = diasDiferenca.days

        while True:
            if qtdDias >= 30:
                pontosPrioridade += 0.25
                qtdDias -= 30
            else:
                pontosPrioridade -= 0.25
                break

        #calcula a pontuação e define a prioridade
        if pontosPrioridade >= 0.25:
            data["Priority"] = "Alta"
        else:
            data["Priority"] = "Normal"

    with open("ticketsTestes.json", "w") as write_file:
        json.dump(jsonData, write_file, indent=2, sort_keys=True)
    
    return jsonData

with open('ticketsTestes.json') as f:
    dataJson = json.load(f)
    dataJson = addPrioritys(dataJson)

@app.route('/', methods=['GET'])
def home():
    dataFiltered = dataJson
    page = 1
    limit = 10

    data = request.get_json()

    if data.get('filter'):
        if data["filter"].get('date'):
            startDate = datetime.strptime(data["filter"]['date']["start"], '%Y-%m-%d %H:%M:%S')
            endDate = datetime.strptime(data["filter"]['date']["end"], '%Y-%m-%d %H:%M:%S')

            dataFiltered = [dat for dat in dataFiltered if  startDate <= datetime.strptime(dat["DateCreate"], '%Y-%m-%d %H:%M:%S') <= endDate]
        if data["filter"].get('priority'):
            priority = data["filter"]["priority"]
            dataFiltered = [dat for dat in dataFiltered if  dat.get("Priority") and dat["Priority"] == priority]

    if data.get('order'):
        if data['order'].get('DateCreate'):
            dataFiltered = sorted(dataFiltered, key=lambda k: datetime.strptime(k["DateCreate"], '%Y-%m-%d %H:%M:%S'), reverse=False if data['order'].get('DateCreate') == 'ASC' else True)
        elif data['order'].get('DateUpdate'):
            dataFiltered = sorted(dataFiltered, key=lambda k: datetime.strptime(k["DateUpdate"], '%Y-%m-%d %H:%M:%S'), reverse=False if data['order'].get('DateUpdate') == 'ASC' else True)
        elif data['order'].get('Priority'):
            dataFiltered = sorted(dataFiltered, key=lambda k: k["Priority"], reverse=False if data['order'].get('Priority') == 'ASC' else True)

    if data.get('pagination'):
        if data['pagination'].get('page'):
            page = data['pagination']['page']
        if data['pagination'].get('limit'):
            limit = data['pagination']['limit']

    totalPages = len(dataFiltered) / float(limit)
    totalResults = len(dataFiltered)

    #Paginação
    c = 1
    i = 0
    dataReturned = []
    dataPage = []
    newPage = page
    for dt in dataFiltered:
        if c > (limit * newPage) - limit and newPage <= page:
            dataPage.append(dt)
        if c == limit * newPage:
            dataReturned.append({
                'page': newPage,
                'results': dataPage,
                'limit': limit,
                'totalPages': int(ceil(totalPages)),
                'totalResults': totalResults
            })
            dataPage = []
            newPage += 1
            i += 1
        c += 1

    if len(dataPage) > 0:
        dataReturned.append({
            'page': page,
            'results': dataPage,
            'limit': limit,
            'totalPages': int(ceil(totalPages)),
            'totalResults': totalResults
        })

    return jsonify(dataReturned), 200

if __name__ == '__main__':
    app.run() #debug=True