import os
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/releases')
def get_releases():
    try:
        url = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        releases = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            title_text = title.text if title is not None else ""
            
            updated = entry.find('atom:updated', ns)
            updated_text = updated.text if updated is not None else ""
            
            link = entry.find("atom:link[@rel='alternate']", ns)
            if link is None:
                link = entry.find("atom:link", ns)
            link_href = link.attrib.get('href', '') if link is not None else ""
            
            content = entry.find('atom:content', ns)
            content_html = content.text if content is not None else ""
            
            releases.append({
                'title': title_text,
                'updated': updated_text,
                'link': link_href,
                'content': content_html
            })
            
        return jsonify({
            'status': 'success',
            'releases': releases
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
