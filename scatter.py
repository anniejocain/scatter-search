import urllib2, json, logging
from flask import Flask, render_template
from flask.ext.jsonpify import jsonify
from lxml.html import parse

config = {}

execfile('/var/www/html/scatter/etc/scatter.conf', config) 

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', web_base=config['WEB_BASE'])

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
    
@app.route('/search/')
@app.route('/search/<term>')
def search(term=None, type=None):
    return render_template('search.html', term=term, type=type, web_base=config['WEB_BASE'])
    
@app.route('/api/databases/<term>')
def api_databases(term=None):
  
  doc = parse('http://law.harvard.edu/apps/library/admin/proxy.php?url=http%3A%2F%2Feresearch.lib.harvard.edu%2FV%2F%3Ffunc%3Dfind-db-1-locate%26format%3D000%26F-WRD%3D' + term).getroot()
  list = []
  for link in doc.cssselect('tr.find_db_table_view td.db_link_bold a')[0:5]:
    type = link.getparent().getnext().text_content()
    response_object = {"link": link.get('href'), "type": type.strip(), "title": link.text_content()}
    list.append(response_object)
    
  response = jsonify(databases = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response

@app.route('/api/journals/<term>')
def api_journals(term=None):
  
  doc = parse('http://sfx.hul.harvard.edu/sfx_local/az/?param_services2filter_save=getFullTxt&param_current_view_save=table&param_type_save=textSearch&param_textSearchType_save=startsWith&param_type_value=textSearch&param_textSearchType_value=contains&param_starts_with_browse_value=0&param_pattern_value=' + term).getroot()
  list = []
  for link in doc.cssselect('#tableView td.TableRow a.Results')[0:5]:
    type = link.getparent().getnext().text_content()
    response_object = {"link": "http://sfx.hul.harvard.edu" + link.get('href'), "title": link.text_content()}
    list.append(response_object)
    
  response = jsonify(journals = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/libanswers/<term>')
def api_libanswers(term=None):
  
  url = 'http://api.libanswers.com/api_query.php?iid=' + config['LIBANSWERS_SITE_ID'] +  '&limit=20&format=json&q=' + term
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  list = []
  jsoned_response = json.loads(response)
    
  results = jsoned_response['query']['results']
  
  for result in results[0:5]:
    response_object = {"title": result['question'], "link": result['url']}
    list.append(response_object)
    
  response = jsonify(results = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/libguides/<term>')
def api_libguides(term=None):
  
  url = 'https://www.googleapis.com/customsearch/v1?key=' + config['GOOGLE_API'] +  '&cx=' + config['GOOGLE_CUSTOM'] + '&q=' + term
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  list = []
  jsoned_response = json.loads(response)
    
  results = jsoned_response['items']
  
  for result in results[0:5]:
    title_parts = result['title'].split(' - Research Guides')
    title = title_parts[0]
    response_object = {"title": title, "link": result['link']}
    list.append(response_object)
    
  response = jsonify(results = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/law-libguides/<term>')
def api_law_libguides(term=None):
  
  url = 'https://www.googleapis.com/customsearch/v1?key=' + config['GOOGLE_API'] +  '&cx=' + config['GOOGLE_LAW_CUSTOM'] + '&q=' + term
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  list = []
  jsoned_response = json.loads(response)
    
  results = jsoned_response['items']
  
  for result in results[0:5]:
    title_parts = result['title'].split(' - Research Guides')
    title = title_parts[0]
    response_object = {"title": title, "link": result['link']}
    list.append(response_object)
    
  response = jsonify(results = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/website/<term>')
def api_website(term=None):
  
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:http://library.harvard.edu%20-site:http://guides.library.harvard.edu%20' + term
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  list = []
  jsoned_response = json.loads(response)
    
  results = jsoned_response['responseData']['results']
  
  for result in results[0:5]:
    response_object = {"title": result['title'], "link": result['url']}
    list.append(response_object)
    
  response = jsonify(results = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
 
@app.route('/api/law-website/<term>')
def api_law_website(term=None):
  
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:http://law.harvard.edu/library%20' + term
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  list = []
  jsoned_response = json.loads(response)
    
  results = jsoned_response['responseData']['results']
  
  for result in results[0:5]:
    response_object = {"title": result['title'], "link": result['url']}
    list.append(response_object)
    
  response = jsonify(results = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
   
@app.route('/api/hollis/<term>')
def api_hollis(term=None):
  
  term = term.replace(' ', '+')
  
  #url = 'http://webservices.lib.harvard.edu/rest/hollis/search/cite/?q="' + term + '"'
  url = 'http://webservices.lib.harvard.edu/rest/v2/hollisplus/search/dc/?q="' + term + '"'
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  results_list = []
  jsoned_response = json.loads(response)
  
  if 'resultSet' not in jsoned_response['results']:
    response = jsonify(results = '')
    response.headers['Content-Type'] = "application/json"
    response.status_code = 201
    
    return response
    
  results = jsoned_response['results']['resultSet']['item']
  
  for result in results[0:5]:
    titles = result.get('dc:title')
    if isinstance(titles, list):
        title = titles[0]
    else:
        title = titles
    link = result.get('cataloglink')
    format = result.get('dc:type')
    format_icon = 'icon-book'
    if format == "book":
      format_icon = 'icon-book'
    elif format == "journal":
      format_icon = 'icon-bookmark'
    elif format == "video":
      format_icon = 'icon-film'
    elif format == "sound_recording":
      format_icon = 'icon-music'
    elif format == "image":
      format_icon = 'icon-picture'
    response_object = {"link": link, "format": format_icon, "title": title}
    results_list.append(response_object)
    
  response = jsonify(results = results_list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/via/<term>')
def api_via(term=None):
  
  term = term.replace(' ', '+')
  
  url = 'http://webservices.lib.harvard.edu/rest/v2/hollisplus/search/dc/?q="' + term + '"&query=rtype,exact,image'
    
  req = urllib2.Request(url)
  req.add_header("accept", "application/json")
    
  response = None
    
  try: 
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
  except urllib2.HTTPError, e:
    logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.warn('Item from Hollis, URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.warn('Item from Hollis, HTTPException')
  except Exception:
    import traceback
    logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
  results_list = []
  jsoned_response = json.loads(response)
  
  if 'resultSet' not in jsoned_response['results']:
    response = jsonify(results = '')
    response.headers['Content-Type'] = "application/json"
    response.status_code = 201
    
    return response
    
  results = jsoned_response['results']['resultSet']['item']
  
  for result in results[0:5]:
    titles = result.get('dc:title')
    if isinstance(titles, list):
        title = titles[0]
    else:
        title = titles
    link = result.get('cataloglink')
    thumbnail = ''
    links = result['links']
    thumbnails = links.get('a')
    if thumbnails:
        for content in thumbnails:
            if content['content'] == 'thumbnail':
                thumbnail = content['href']
    response_object = {"link": link, "thumbnail": thumbnail, "title": title}
    results_list.append(response_object)
    
  response = jsonify(results = results_list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response

if __name__ == '__main__':
    app.run(host=config['FLASK_HOST'], port=config['FLASK_PORT'], debug=config['FLASK_DEBUG'])