from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS

import collections

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def repeated_html():
    request_data = request.get_json()
    soup = BeautifulSoup(request_data['html'], 'html.parser')
    all_tags = soup.find_all()
    all_tags.reverse()
    duplicates = [item for item, count in collections.Counter(all_tags).items() if count > 1]
    for index, duplicate in enumerate(duplicates):
        if (index < len(duplicates) - 1 and str(duplicates[index + 1]).find(str(duplicate)) != -1):
            duplicates.remove(duplicate)
        duplicates[index] = {
            "html": str(duplicates[index]),
            "occurrences": str(soup).count(str(duplicates[index]))
        }

    return jsonify({"duplicates": duplicates})
    