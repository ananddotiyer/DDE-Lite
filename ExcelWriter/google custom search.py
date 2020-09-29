def search_results (search):
    import requests
    import json
    
    domain_name = "https://www.googleapis.com/"
    api = "customsearch/v1"
    api_key = "AIzaSyCmIRuGHNlk_lQzL9_VnTMWNMvDneBwSkQ"
    cx = "002677408965362061794:0wbgub677qo"
    #search = "Moolya Testing"
    
    url = domain_name + api + "?" + "key=" + api_key + "&cx=" + cx + "&q=" + search
    
    response = requests.get (url)
    
    results = json.loads (response.text)
    
    links = [result["link"] for result in results["items"]]
    return '\n'.join(links)