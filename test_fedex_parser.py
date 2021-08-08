import pytest
from fedex_parser import parser

def test_parse_wrong_credentials():
    with open('.\\test_files\\CREDENTIALS_WRONG.TXT', "r") as test_file:
        test_string = test_file.read()
    pars = parser(test_string)
    assert pars.response_correct == False
    assert pars.response_error == 'Authentication Failed'
    
def test_parse_wrong_number():
    with open('.\\test_files\\NUMBER_WRONG.TXT', "r") as test_file:
        test_string = test_file.read()
    pars = parser(test_string)
    assert pars.response_correct == False
    assert pars.response_error == 'This tracking number cannot be found. Please check the number or contact the sender.'

def test_parse_delivered():
    with open('.\\test_files\\DELIVERED.TXT', "r") as test_file:
        test_string = test_file.read()
    with open('.\\test_files\\DELIVERED_PARSED.TXT', "r") as test_file:
        expected_parsing = test_file.read()
    pars = parser(test_string)
    this_parsing = str(pars.parse_response())
    assert expected_parsing == this_parsing

def test_parse_hold():
    with open('.\\test_files\\HOLD.TXT', "r") as test_file:
        test_string = test_file.read()
    with open('.\\test_files\\HOLD_PARSED.TXT', "r") as test_file:
        expected_parsing = test_file.read()
    pars = parser(test_string)
    this_parsing = str(pars.parse_response())
    assert expected_parsing == this_parsing

    

