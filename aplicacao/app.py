import pandas
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*":{"origins" : "*"}})

df = pandas.read_csv('Relatorio_cadop.csv', delimiter=';')

def search_data(df, text):
    result = df[df.apply(lambda row: row.astype(str).eq(text).any(), axis=1)]
    
    final_result = []
    
    for index, row in result.iterrows():
        column = row[row.astype(str).str.contains(text, case=False)]
        if (text.lower() in row['Razao_Social'].lower() or
            str(row['Registro_ANS']) == text or
            row['UF'].lower() == text.lower()):
            final_result.append({
                'razao_social': str(row['Razao_Social']),
                'ans': str(row['Registro_ANS']),
                'UF': str(row['UF']),
                'add_column': False
            })
        else:
            final_result.append({
                'razao_social': str(row['Razao_Social']),
                'ans': str(row['Registro_ANS']),
                'UF': str(row['UF']),
                'add_column': True,
                column.index[0]: str(row[column.index[0]])
            })

    return final_result


@app.route('/search', methods=['GET'])
def search():
    text = request.args.get('query', '')
    if text:
        result = search_data(df, text)
        return jsonify(result)  
    return jsonify([])

@app.route('/teste', methods=['GET'])
def home():
    return ('teste')

if __name__ == '__main__':
    app.run(debug=True)