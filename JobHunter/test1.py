import json
import urllib.request
urlData = "https://jobs.github.com/positions.json?location=seattle"
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
json.loads(data.decode(encoding))
print(data)
