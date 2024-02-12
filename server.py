from flask import Flask, request, render_template_string
from ranking import search

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head><title>Search</title></head>
<body>
  <h1>Simple Search Engine</h1>
  <form action="/" method="post">
    <input type="text" name="query"/>
    <input type="submit" value="Search" />
  </form>
  {% if results %}
    <ul>
    {% for url, score in results.items() %}
      <li><a href="url">{{ url }}</a>, score: {{score}}</li>
    {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
'''


@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, results=None)


@app.route('/', methods=['POST'])
def search_page():
    query = request.form['query']
    results = search(query)  # get the search results
    return render_template_string(HTML_TEMPLATE, results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
