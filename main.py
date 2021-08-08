from flask import Flask, render_template, request, redirect
from fedex_request import req
import fedex_parser as parser
import xmltodict
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
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
response_dict = parser.parse_response(resp.text)


print(response_dict)

print('end')

@app.route('/fedex', methods=['POST','GET'])
def fedex_api_call_page():
    response_json = ''
    tracking_number = request.form.get('tracking_number')
    if tracking_number is not None:
        resp = requestor.track(tracking_number)
        response_dict = parser.parse_response(resp.text)
        print(response_dict)
        response_json = json.dumps(response_dict, indent = 4, separators = (',', ': '))
        return render_template('index.html', input = response_json)
    else:
        return render_template('index.html')#, input = None)

    

@app.route('/fedex/call')
def fedex_api_call():
    tracking_number = request.args.get('tracking_number')
    resp = requestor.track(tracking_number)
    response_dict = parser.parse_response(resp.text)
    print(response_dict)
    render_template('index.html')


app.run(debug = True)


