from flask import Flask, render_template, request, redirect
from fedex_request import req
from fedex_parser import parser
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
URL = "https://wsbeta.fedex.com:443/web-services"
CRED_DICT = {'parent_key': 'HicUfijJZSUAtqAG', 'parent_password': '2IX4AJyvWW9WltylOvw3RokcN',
            'user_key': 'mIAfOSJ0e32Zc4oV', 'user_password': 'gvTG2nBBVKwZq9dWJnBnJ7rVH',
            'client_account': '602091147', 'client_meter': '118785166'}

requestor = req(URL, CRED_DICT)

def get_message_from_request(tracking_number):
    """Gets message by parsing request to renderable response.

    Args:
        tracking_number (str): Fedex tracking number.   

    Returns:
        str: Parsed response or error messge.
    """    
    resp = requestor.track(tracking_number)
    if resp.status_code != 200:
        return f'FedEx API returns {resp.status_code}, server may be overloaded, please try again later.'
    pars = parser(resp.text)
    if pars.response_correct:
        response_dict = pars.parse_response()
        return json.dumps(response_dict, indent = 4, separators = (',', ': '))
    else:
        return pars.response_error  

def get_message_to_render(tracking_number):
    """Checks for tracking number and gets message from fedex api if available.

    Args:
        tracking_number (str): Fedex tracking number. 

    Returns:
        str: Parsed response, notification or error messge.
    """    
    if tracking_number is None:
        return 'Please enter tracking number.'
    elif tracking_number == '':
        return 'Please enter tracking number.'
    else:
        return get_message_from_request(tracking_number)

@app.route('/', methods=['POST','GET'])
def fedex_api_call_page():
    """Main response generating function.

    Returns:
        render_template: Renders basic response page.
    """    
    tracking_number = request.form.get('tracking_number')
    try:
        message_to_render = get_message_to_render(tracking_number)
    except:
        message_to_render = 'Unexpected error.'
    return render_template('index.html', input = message_to_render)

if __name__ == "__main__":
    app.run()


