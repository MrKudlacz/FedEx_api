import pytest
from fedex_request import req


TRACKING_NUMBER_DELIVERED = '122816215025810'
TRACKING_NUMBER_HOLD = '843119172384577'
TRACKING_NUMBER_WRONG = '8888888888888'
URL = "https://wsbeta.fedex.com:443/web-services"
CRED_DICT_VALID = {'parent_key': 'HicUfijJZSUAtqAG', 'parent_password': '2IX4AJyvWW9WltylOvw3RokcN',
            'user_key': 'mIAfOSJ0e32Zc4oV', 'user_password': 'gvTG2nBBVKwZq9dWJnBnJ7rVH',
            'client_account': '602091147', 'client_meter': '118785166'}
CRED_DICT_INVALID = {'parent_key': 'xxxx', 'parent_password': 'xxx',
            'user_key': 'xxx', 'user_password': 'xxx',
            'client_account': 'xxx', 'client_meter': 'xxx'}

@pytest.fixture
def correct_requestor():
    requestor = req(URL, CRED_DICT_VALID)
    return requestor


@pytest.fixture
def incorrect_requestor():
    in_requestor = req(URL, CRED_DICT_INVALID)
    return in_requestor

def test_track_delivered(correct_requestor):
    with open('.\\test_files\\DELIVERED.TXT', "r") as test_file_delivered:
        test_string_delivered = test_file_delivered.read()
    resp = correct_requestor.track(TRACKING_NUMBER_DELIVERED)
    assert resp.text == test_string_delivered 
    assert resp.status_code == 200

def test_track_hold(correct_requestor):
    with open('.\\test_files\\HOLD.TXT', "r") as test_file_hold:
        test_string_hold = test_file_hold.read()
    resp = correct_requestor.track(TRACKING_NUMBER_HOLD)
    assert resp.text == test_string_hold 
    assert resp.status_code == 200

def test_track_wrong_number(correct_requestor):
    with open('.\\test_files\\NUMBER_WRONG.TXT', "r") as test_file_number_wrong:
        test_string_number_wrong = test_file_number_wrong.read()
    resp = correct_requestor.track(TRACKING_NUMBER_WRONG)
    assert resp.text == test_string_number_wrong 
    assert resp.status_code == 200

def test_track_credentials(incorrect_requestor):
    with open('.\\test_files\\CREDENTIALS_WRONG.TXT', "r") as test_file_delivered:
        test_string_delivered = test_file_delivered.read()
    resp = incorrect_requestor.track(TRACKING_NUMBER_DELIVERED)
    assert resp.text == test_string_delivered 
    assert resp.status_code == 200

if __name__ == '__main__':
    requestor = req(URL, CRED_DICT_VALID)
    resp = requestor.track(TRACKING_NUMBER_DELIVERED)
    text_file = open('.\\test_files\\OVERLOADED.TXT', "w")
    text_file.write(resp.text)
    text_file.close

    with open('.\\test_files\\OVERLOADED.TXT', "r") as test_file_delivered:
        test_string_delivered = test_file_delivered.read()
