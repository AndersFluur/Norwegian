import requests
import bs4
import datetime

#from collections import namedtuple
def to_int(val):
  try:
    return int(val)
  except ValueError:
    return 0

class NorwegianReqest():
  def __init__(self):
    self.root_url = 'http://www.norwegian.com'
    self.request_price_base = self.root_url + '/se/bokning/flyg/lagpris/?'
  def _interesting_fields(self, tag):
    #print(tag.attrs)
    if tag.has_attr('class'):
      return tag['class'] == ['fareCalDate'] or tag['class'] == ['fareCalPrice']
    else:
      return False
  def _get_date_price_list(self, pricelist):
    Dates = [int(elem.get_text()) for elem in pricelist if elem['class'] == ['fareCalDate'] ]
    PricesString = [elem.get_text().encode('ascii', 'ignore') for elem in pricelist if elem['class'] == ['fareCalPrice'] ]
    PricesInt = [to_int(p)  for p in PricesString ]
    return zip(Dates,PricesInt)
  def getPriceList(self, D_City, #'GOT'
	A_City, # 'ALC'
	D_Day,
	D_Month, #201702
	R_Day, # 01
	R_Month,
	AdultCount=2,
	IncludeTransit='false',
	AgreementCodeFK='-1',
	CurrencyCode='SEK'):
    v = vars()
    request_params = ''	
    for key, value in v.iteritems():
      if request_params:
        request_params += '&' # Only between parameters
      if not key == 'self':
        request_params += '{}={}'.format(key, value)   
    request_text=self.request_price_base + request_params
    #print(request_text)
    response = requests.get(request_text)
    soup = bs4.BeautifulSoup(response.text)
    #print(soup.prettify())
    #return soup
    fareCalendarTables = []
    for table in soup.find_all('table'):
      if table['class'] == [u'fareCalendarTable']:
        fareCalendarTables.append(table)
    fareCalendarOutbound=fareCalendarTables[0]
    fareCalendarInbound=fareCalendarTables[1]
    inbound = fareCalendarInbound.find_all(self._interesting_fields)
    outbound = fareCalendarOutbound.find_all(self._interesting_fields)
    return {'inbound': self._get_date_price_list(inbound), 'outbound': self._get_date_price_list(outbound)}

n=NorwegianReqest()
n.getPriceList(D_City='GOT', A_City='ALC', D_Day=01, D_Month='201702',  R_Day='01', R_Month='201702')



fareCalendarTable
week
fareCalDate
fareCalPrice



getPriceList(D_City='GOT', A_City='ALC', D_Day=01, D_Month='201702',  R_Day=01, R_Month='201702')
	 #argReq+='{}='{}.format(arg.











