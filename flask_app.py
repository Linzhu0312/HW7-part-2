from flask import Flask, Response
from analysis import loadData, showRatingDistribution
df = loadData()
app = Flask(__name__, static_url_path='', static_folder='.') 
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route('/vis/<zipcode>')
def hello(zipcode):
    print("success!")
    response = ''
    if df is not None:
        response = showRatingDistribution(df,zipcode).to_json()
        
    return Response(response,
                    mimetype = 'application/json',
                    headers={
                            'Cache-Control': 'no-cache',
                            'Access-Control-Allow-Origin': '*'
                            }
                    )

if __name__ == '__main__': 
    app.run(port=8000)
