# Desafio desenvolvedor backend

Precisamos melhorar o atendimento no Brasil, para alcançar esse resultado, precisamos de um algoritmo que classifique
nossos tickets (disponível em tickets.json) por uma ordem de prioridade, um bom parâmetro para essa ordenação é identificar o humor do consumidor.
Pensando nisso, queremos classificar nossos tickets com as seguintes prioridade: Normal e Alta.

### São exemplos:

### Prioridade Alta:
- Consumidor insatisfeito com produto ou serviço
- Prazo de resolução do ticket alta
- Consumidor sugere abrir reclamação como exemplo Procon ou ReclameAqui
    
### Prioridade Normal
- Primeira iteração do consumidor
- Consumidor não demostra irritação

Considere uma classificação com uma assertividade de no mínimo 70%, e guarde no documento (Nosso json) a prioridade e sua pontuação.

### Com base nisso, você precisará desenvolver:
- Um algoritmo que classifique nossos tickets
- Uma API que exponha nossos tickets com os seguintes recursos
  - Ordenação por: Data Criação, Data Atualização e Prioridade
  - Filtro por: Data Criação (intervalo) e Prioridade
  - Paginação
        
### Escolha as melhores ferramentas para desenvolver o desafio, as únicas regras são:
- Você deverá fornecer informações para que possamos executar e avaliar o resultado;
- Poderá ser utilizado serviços pagos (Mas gostamos bastante de projetos open source)
    
### Critérios de avaliação
- Organização de código;
- Lógica para resolver o problema (Criatividade);
- Performance
    
### Como entregar seu desafio
- Faça um Fork desse projeto, desenvolva seu conteúdo e informe no formulário (https://goo.gl/forms/5wXTDLI6JwzzvOEg2) o link do seu repositório

### Detalhes da API desenvolvida:
GET / 
- Retorna os tickets de serviço com as prioridades definidas, recebendo filtros por parâmetro e ordenando
- Parâmetros:

##### filter {
    date (optional) {
        start (date, optional): Data inicial no formato "Y-m-d h:i:s"
        end: (date, optional): Data final no formato "Y-m-d h:i:s"
    },
    priority (string, optional): Prioridade entre "Alta" ou "Normal"
},
##### order {
    Priority (string, optional): Ordenação do retorno por prioridade, pode ser em ASC ou DESC,
    DateCreate (string, optional): Ordenação do retorno por data de criação, pode ser em ASC ou DESC,,
    DateUpdate (string, optional): Ordenação do retorno por data de atualização, pode ser em ASC ou DESC
}
##### pagination {
    limit (int, optional): Configura quantos tickets virão por página,
    page (int, optional): Configura qual página será retornada 
}
