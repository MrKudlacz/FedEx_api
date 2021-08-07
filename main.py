import flask
from fedex_request import req
import xmltodict
import json

url = "https://wsbeta.fedex.com:443/web-services"
cred_dict = {'parent_key': 'HicUfijJZSUAtqAG', 'parent_password': '2IX4AJyvWW9WltylOvw3RokcN',
            'user_key': 'mIAfOSJ0e32Zc4oV', 'user_password': 'gvTG2nBBVKwZq9dWJnBnJ7rVH',
            'client_account': '602091147', 'client_meter': '118785166'}
tracking_number = '122816215025810'
tracking_number = '449044304137821'
tracking_number = '568838414941'
tracking_number = '076288115212522'
requestor = req(url, cred_dict)

resp = requestor.track(tracking_number)
xpars = xmltodict.parse(resp.text)
details_dict = xpars['SOAP-ENV:Envelope']['SOAP-ENV:Body']['TrackReply']['CompletedTrackDetails']['TrackDetails']
events_dict = details_dict['Events']
carrier = details_dict['CarrierCode']
status = events_dict['EventDescription']
checkpoints = {}
for event in events_dict:
    selected_event_dict = {}
    selected_event_dict['description'] = events_dict['event']['EventDescription']
    checkpoints.append(selected_event_dict)
print(json.dumps(events_dict, indent=4, sort_keys=True))

import xml.etree.ElementTree as ET
tree = ET.ElementTree(ET.fromstring(resp.text))
root = tree.getroot()

from bs4 import BeautifulSoup
bs = BeautifulSoup(resp.text, 'xml')
pretty_xml = bs.prettify()
print(pretty_xml)
carrier = bs.find_all('CarrierCode')[0].text
events = bs.find_all('CarrierCode')[0].text
for ev in bs.find_all('Events'):
    print(ev.find('EventDescription').text)
    print('/n')