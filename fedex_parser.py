from bs4 import BeautifulSoup

def parse_response(xml_str):
    response_bs = BeautifulSoup(xml_str, 'xml')
    pretty_xml = response_bs.prettify()
    output_dict = {}
    carrier = get_tag_value(response_bs, 'CarrierCode')
    output_dict['carrier'] = carrier
    status = get_tag_value(response_bs, 'EventDescription')
    output_dict['status'] = status

    checkpoints_list = []
    for ev in response_bs.find_all('Events'):
        checkpoint = {}

        checkpoint['description'] = get_tag_value(ev, 'EventDescription')
        location = {}
        location['city'] = get_tag_value(ev, 'City')
        location['country'] = get_tag_value(ev, 'CountryName')
        location['postal_code'] = get_tag_value(ev, 'PostalCode')
        location['state'] = get_tag_value(ev, 'StateOrProvinceCode')

        checkpoint['location'] = location
        checkpoints_list.append(checkpoint)

        time = get_tag_value(ev, 'Timestamp')
        checkpoint['time'] = time

    output_dict['checkpoints'] = checkpoints_list



    return output_dict

def get_tag_value(bs_element, tag):
    if bs_element.find(tag) is None:
        return None
    else:
        return bs_element.find(tag).text



