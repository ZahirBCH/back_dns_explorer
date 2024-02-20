from flask import Flask, render_template, request
from flask_restful import Api, Resource
from dns_explorer import get_dns_records
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class DNSExplorerResource(Resource):
    def post(self):
        url = request.args.get('url')
        result = get_dns_records(url)
        return {'result': result}

api.add_resource(DNSExplorerResource, '/dns-explorer')

if __name__ == "__main__":
    app.run(debug=True)