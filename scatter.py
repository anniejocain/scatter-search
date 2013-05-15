import urllib2, json
from flask import Flask, render_template, jsonify
from lxml.html import parse

config = {}
execfile('etc/scatter.conf', config) 

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

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
  
  doc = parse('http://eresearch.lib.harvard.edu/V/?func=find-db-1-locate&format=000&F-WRD=' + term).getroot()
  #link = doc.cssselect('tr.find_db_table_view td.db_link_bold a')
  list = []
  for link in doc.cssselect('tr.find_db_table_view td.db_link_bold a')[0:5]:
    type = link.getparent().getnext().text_content()
    response_object = {"link": link.get('href'), "type": type, "title": link.text_content()}
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
  
@app.route('/api/libguides/<term>')
def api_libguides(term=None):
  
  doc = parse('http://libguides.law.harvard.edu/search_process.php?search=' + term + '&gid=&iid=1242&pid=&c=0&search_field=&display_mode=').getroot()
  list = []
  for guide in doc.cssselect('.search_item_result')[0:5]:
    title = guide.getchildren()[0].getchildren()[0].getchildren()[0].text_content()
    link = guide.getchildren()[0].getchildren()[0].getchildren()[0].get('href')
    description = guide.getchildren()[0].getchildren()[0].getnext().getnext()
    if description is not None:
      description = description.text_content()
    page_title = guide.getchildren()[0].getnext().getnext().getchildren()[0].getchildren()[0].getchildren()[0].text_content()
    page_link = guide.getchildren()[0].getnext().getnext().getchildren()[0].getchildren()[0].getchildren()[0].get('href')
    response_object = {"title": title, "link": link, "description": description, "page-title": page_title, "page-link": page_link}
    list.append(response_object)
    
  response = jsonify(guides = list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/website/<term>')
def api_website(term=None):
  
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:http://library.harvard.edu%20' + term
    
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
  
  url = 'http://webservices.lib.harvard.edu/rest/hollis/search/cite/?q="' + term + '"'
    
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
    title = result.get('dc:title')
    if not title:
      title = result['mods']['titleInfo']
    if isinstance(title, list):
      title = result['mods']['titleInfo'][0]['title']
      if 'nonSort' in result['mods']['titleInfo'][0]:
        nonsort = result['mods']['titleInfo'][0]['nonSort']
        title = nonsort + ' ' + title
      if 'subTitle' in result['mods']['titleInfo'][0]:
        subtitle = result['mods']['titleInfo'][0]['subTitle']
        title = title + ' ' + subtitle
    else:
      title = result['mods']['titleInfo']['title']
      if 'nonSort' in result['mods']['titleInfo']:
        nonsort = result['mods']['titleInfo']['nonSort']
        title = nonsort + ' ' + title
      if 'subTitle' in result['mods']['titleInfo']:
        subtitle = result['mods']['titleInfo']['subTitle']
        title = title + ': ' + subtitle
    link = result['catalogUrl']
    link = link.replace('http://hollis.harvard.edu/accessible.ashx?itemid=', 'http://hollis.harvard.edu/?itemid=')
    format = result['dc:format']
    format_icon = 'icon-book'
    if format == "Book":
      format_icon = 'icon-book'
    elif format == "Journal / Serial":
      format_icon = 'icon-bookmark'
    elif format == "Movie":
      format_icon = 'icon-film'
    elif format == "Recording":
      format_icon = 'icon-music'
    elif format == "Image":
      format_icon = 'icon-picture'
    response_object = {"link": link, "format": format_icon, "title": title}
    results_list.append(response_object)
    
  response = jsonify(results = results_list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response
  
@app.route('/api/via/<term>')
def api_via(term=None):
  
  url = 'http://webservices.lib.harvard.edu/rest/hollis/search/cite/?q="' + term + '"+format:matPhoto'
    
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
    title = result.get('dc:title')
    
    link = result['catalogUrl']
    link = link.replace('http://hollis.harvard.edu/accessible.ashx?itemid=', 'http://hollis.harvard.edu/?itemid=')
    thumbnail = result['thumbnail']
    response_object = {"link": link, "thumbnail": thumbnail, "title": title}
    results_list.append(response_object)
    
  response = jsonify(results = results_list)
  response.headers['Content-Type'] = "application/json"
  response.status_code = 201
    
  return response

if __name__ == '__main__':
    app.run(host=config['FLASK_HOST'], port=config['FLASK_PORT'], debug=config['FLASK_DEBUG'])