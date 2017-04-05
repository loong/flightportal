#!/usr/bin/python3

import os
import csv

from skyscanner.skyscanner import FlightsCache

SKYSCANNER_API_KEY = os.environ['SKYSCANNER_API_KEY']

flights_cache_service = FlightsCache(SKYSCANNER_API_KEY)

def get_all_quotes(origin, destination):
    # Assumes majority of trips are 1 month or shorter

    # Skyscanner only goes up to 1 month in the future
    # So I'm just using the current month until the next
    result = flights_cache_service.get_cheapest_quotes(
        market='US',
        currency='USD',
        locale='en-US',
        originplace=origin,
        destinationplace=destination,
        outbounddate='2017-04',
        inbounddate='2017-05').parsed

    carriers = dict([tuple(carrier.values()) for carrier in result['Carriers']])

    places = dict([(p['PlaceId'], p['IataCode']) for p in result['Places']])

    quotes = [flatten_quote(quote, carriers, places) for quote in result['Quotes']]

    quotes = [quote for quote in quotes if quote is not None]

    return quotes

# So we can spend less time doing unnecessary joins
def flatten_quote(quote, carriers, places):
    if 'OutboundLeg' not in quote or 'InboundLeg' not in quote:
        return None

    quote['Origin'] = places[quote['InboundLeg']['DestinationId']]
    quote['OutboundCarriers'] = [carriers[cid] for cid in quote['OutboundLeg']['CarrierIds']]
    quote['OutboundDepartureTime'] = quote['OutboundLeg']['DepartureDate']

    quote['Destination'] = places[quote['OutboundLeg']['DestinationId']]
    quote['InboundCarriers'] = [carriers[cid] for cid in quote['InboundLeg']['CarrierIds']]
    quote['InboundDepartureTime'] = quote['InboundLeg']['DepartureDate']

    quote['Currency'] = 'USD'
    quote['QuoteTime'] = quote['QuoteDateTime']

    del quote['OutboundLeg']
    del quote['InboundLeg']
    del quote['QuoteDateTime']

    return quote

fieldnames = [
    'QuoteId',
    'MinPrice',
    'Direct',
    'Origin',
    'Destination',
    'OutboundDepartureTime',
    'OutboundCarriers',
    'InboundDepartureTime',
    'InboundCarriers',
    'QuoteTime',
    'Currency'
]

# Expects a CSV file to read routes from, generated with:
# \copy (Select * From routes_unique) To '/tmp/test.csv' With CSV
with open('routes_unique.csv', newline='') as routesfile:
    with open('prices.csv', 'w') as pricesfile:
        rows = csv.reader(routesfile, delimiter=',', quotechar='|')
        w = csv.DictWriter(pricesfile, fieldnames=fieldnames)

        w.writeheader()

        for idx, row in enumerate(rows):
            print('#{} {}, {}'.format(idx+1, row[0], row[1]))
            try:
                quotes = get_all_quotes(row[0], row[1])
                for quote in quotes:
                    w.writerow(quote)
            except Exception as e:
                print(e)

