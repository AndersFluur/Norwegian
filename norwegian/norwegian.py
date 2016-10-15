import requests
import bs4
from datetime import date
from datetime import timedelta

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
  def get_outbound_name(self, D_City, A_City):
      return D_City+'-'+A_City
  def get_inbound_name(self, D_City, A_City):
     return A_City+'-'+D_City
  def _get_date_price_list(self, pricelist, month):
    '''

    '''
    Dates = [date(int(month[0:4]),int(month[4:]),int(elem.get_text())) for elem in pricelist if elem['class'] == ['fareCalDate'] ]
    PricesString = [elem.get_text().encode('ascii', 'ignore') for elem in pricelist if elem['class'] == ['fareCalPrice'] ]
    PricesInt = [to_int(p)  for p in PricesString ]
    return zip(Dates,PricesInt)
  def _getYearMonthStr(self, date):
      Year = str(date).split('-')[0]
      Month = str(date).split('-')[1]
      todayYearMonth = Year + Month
      return todayYearMonth
  def _getDayStr(self, date):
      dayStr = tr(date).split('-')[3]
      return dayStr
  def month_year_iter( self,  start_date, end_date ):
    ym_start= 12*start_date.year + start_date.month - 1
    ym_end= 12*end_date.year + end_date.month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield date(year=y, month=m+1, day=1)
  def getPriceList(self, D_City, # 'GOT' (Departure airport)
	A_City, # 'ALC' (arrival airport)
	D_Day,
	D_Month, # '201702'
	R_Day, # 01
	R_Month,
	AdultCount=2,
	IncludeTransit='false',
	AgreementCodeFK='-1',
	CurrencyCode='SEK'):
    '''
    Return a dict with of dates and prices for the two directions outbound and inbound for the months given.
    '''
    v = vars()
    request_params = ''
    for key, value in v.iteritems():
      if request_params:
        request_params += '&' # Only between parameters
      if not key == 'self':
        request_params += '{}={}'.format(key, value)
    request_text=self.request_price_base + request_params
    print(request_text)
    response = requests.get(request_text)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    #print(soup.prettify())
    fareCalendarTables = []
    for table in soup.find_all('table'):
      if table['class'] == [u'fareCalendarTable']:
        fareCalendarTables.append(table)
    fareCalendarOutbound=fareCalendarTables[0]
    fareCalendarInbound=fareCalendarTables[1]
    inbound = fareCalendarInbound.find_all(self._interesting_fields)
    outbound = fareCalendarOutbound.find_all(self._interesting_fields)
    return {self.get_inbound_name(D_City, A_City): self._get_date_price_list(inbound, D_Month), self.get_outbound_name(D_City, A_City): self._get_date_price_list(outbound, D_Month)}
  def get_trip_price_list(self, D_City, A_City, duration, months_ahead=2, IncludeTransit='false'):
        '''
        Return a list of trips with duration <= the given duration, looking months_ahead months.
        '''
        #end_date = date_1 + datetime.timedelta(days=10)
        todayYearMonth = self._getYearMonthStr(date.today())
        today = date.today()
        end_day = today + timedelta(months_ahead * 365/12)
        price_list = None
        outbound_name = self.get_outbound_name(D_City, A_City)
        inbound_name = self.get_inbound_name(D_City, A_City)
        # Fetch a concatenated list of dates and prices
        for month in self.month_year_iter( today, end_day):
            price_list_tmp = self.getPriceList(D_City, A_City,  '1', self._getYearMonthStr(month),
                                               '1', self._getYearMonthStr(month))
            if price_list: # extend current list of date,price
                price_list[outbound_name].extend(price_list_tmp[outbound_name])
                price_list[inbound_name].extend(price_list_tmp[inbound_name])
            else:
                price_list = price_list_tmp
        number_of_days = len(price_list[outbound_name])
        outbound_price_list_zip = zip(range(0, number_of_days-1), price_list[outbound_name])
        trip_list = [] # (outbund_date, outbund_price, inbound_date, inbound_price, duration, total_price)
        for i, (outbund_date, outbund_price) in outbound_price_list_zip:
            if outbund_price <= 0:
                continue
            #inbound_date = outbund_date +  timedelta(days=duration)
            if i + duration > number_of_days:
                break
            # Let's iterate over the inbound price_list, starting from the order of departure day plus the duration of the trips
            for inbound_date, inbound_price in price_list[inbound_name][i+duration-1:]:
                #print('outbund_date: {} price: {} inbound_date: {} order of date {}
                # inbound_date is from {}'.format(outbund_date, outbund_price , inbound_date, i, price_list[inbound_name][i+duration]))
                if inbound_price <= 0:
                    continue
                else:
                    trip_list = trip_list + [(outbund_date, outbund_price, inbound_date, inbound_price,
                                              (inbound_date-outbund_date).days, outbund_price+inbound_price)]
                    break # Found a date >= duration
        trip_list_sorted_by_price = sorted(trip_list, key=lambda tup: tup[5])
        return trip_list_sorted_by_price


def main():

    import argparse

    parser = argparse.ArgumentParser(description='''Read flights and prices from Norwegians web and
                                         present a list of trips and prices''')
    parser.add_argument('--origin', '-a', type=str, required=True,
                    help='The airport to travel from')
    parser.add_argument('--destination', '-z', required=True,
                    help='The airport to travel to')
    parser.add_argument('--duration','-u', type=int, dest='duration', required=True,
                    help='Wanted duration of the trip')
    parser.add_argument('--months-ahead','-m', type=int,  dest='months_ahead', required=True,
                    help='Number of months in the future to fetch flights for')

    args = parser.parse_args()
    #print(args)
    N=NorwegianReqest()
    trip_list = N.get_trip_price_list( args.origin, args.destination, args.duration, args.months_ahead)
    for trip in trip_list:
        print('Leaving: {} Returning: {} Price: {} Duration: {}'.format(trip[0].isoformat(), trip[2].isoformat(), trip[5], trip[4]))

if __name__ == "__main__":
    main()
