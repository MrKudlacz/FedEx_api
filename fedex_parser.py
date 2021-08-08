from bs4 import BeautifulSoup

class parser():
    def __init__(self, response_to_parse):
        self.response_to_parse = response_to_parse
        self.response_bs = BeautifulSoup(self.response_to_parse, 'xml')
        self.response_error = ''
        self.response_correct = self._check_tracking_received()

    def parse_response(self):
        
        #pretty_xml = self.response_bs.prettify()
        output_dict = {}
        carrier = self._get_tag_value(self.response_bs, 'CarrierCode')
        output_dict['carrier'] = carrier
        status = self._get_tag_value(self.response_bs, 'EventDescription')
        output_dict['status'] = status

        checkpoints_list = []
        for ev in self.response_bs.find_all('Events'):
            checkpoint = {}

            checkpoint['description'] = self._get_tag_value(ev, 'EventDescription')
            location = {}
            location['city'] = self._get_tag_value(ev, 'City')
            location['country'] = self._get_tag_value(ev, 'CountryName')
            location['postal_code'] = self._get_tag_value(ev, 'PostalCode')
            location['state'] = self._get_tag_value(ev, 'StateOrProvinceCode')

            checkpoint['location'] = location
            checkpoints_list.append(checkpoint)

            time = self._get_tag_value(ev, 'Timestamp')
            checkpoint['time'] = time

        output_dict['checkpoints'] = checkpoints_list
        return output_dict

    def _check_tracking_received(self):
        for notification in self.response_bs.find_all('Notification'):
            for el in notification.find_all('Severity'):
                if el.text == 'ERROR':
                    self.response_error = self._get_tag_value(notification, 'Message')
                    return False
        for notification in self.response_bs.find_all('v18:Notifications'):
            for el in notification.find_all('Severity'):
                if el.text == 'ERROR':
                    self.response_error = self._get_tag_value(notification, 'Message')
                    return False
        return True

    def _get_tag_value(self, bs_element, tag):
        if bs_element.find(tag) is None:
            return None
        else:
            return bs_element.find(tag).text



