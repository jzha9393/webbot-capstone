from urllib import parse
query_string = {
'_encoding' : 'UTF8'
}
result = parse.urlencode(query_string)
url = 'https://www.amazon.com.au/deal/a36a6368/?{}'.format(result)
print(url)