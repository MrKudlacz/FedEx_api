"""Module for parsing Fedex API responses.
"""
from bs4 import BeautifulSoup

class parser():
    """Class for parsing response and checking for errors.
    """
    def __init__(self, response_to_parse):
        """init

        Args:
            response_to_parse (str): Fedex API response.
        """
        self.response_to_parse = response_to_parse
        self.response_bs = BeautifulSoup(self.response_to_parse, 'xml')
        self.response_error = ''
        self.response_correct = self._check_tracking_received()

    def parse_response(self):
        """Parses text to expexted response format.

        Returns:
            dict: expexted response dict
        """
        #pretty_xml = self.response_bs.prettify()
        output_dict = {}
        carrier = self._get_tag_value(self.response_bs, 'CarrierCode')
        output_dict['carrier'] = carrier
        status = self._get_tag_value(self.response_bs, 'EventDescription')
        output_dict['status'] = status

        checkpoints_list = []
        for response_event in self.response_bs.find_all('Events'):
            checkpoint = {}

            checkpoint['description'] = self._get_tag_value(response_event, 'EventDescription')
            location = {}
            location['city'] = self._get_tag_value(response_event, 'City')
            location['country'] = self._get_tag_value(response_event, 'CountryName')
            location['postal_code'] = self._get_tag_value(response_event, 'PostalCode')
            location['state'] = self._get_tag_value(response_event, 'StateOrProvinceCode')

            checkpoint['location'] = location
            checkpoints_list.append(checkpoint)

            time = self._get_tag_value(response_event, 'Timestamp')
            checkpoint['time'] = time

        output_dict['checkpoints'] = checkpoints_list
        return output_dict

    def _check_tracking_received(self):
        """Checks for basic errors in response.

        Returns:
            boolean: Is response correct?
        """
        for notification in self.response_bs.find_all('Notification'):
            for notification_element in notification.find_all('Severity'):
                if notification_element.text == 'ERROR':
                    self.response_error = self._get_tag_value(notification, 'Message')
                    return False
        for notification in self.response_bs.find_all('v18:Notifications'):
            for notification_element in notification.find_all('Severity'):
                if notification_element.text == 'ERROR':
                    self.response_error = self._get_tag_value(notification, 'Message')
                    return False
        return True

    def _get_tag_value(self, bs_element, tag):
        """Helper function for geting tag value.

        Args:
            bs_element (bs element): BS element to check.
            tag (tag): Tag to check by.

        Returns:
            str/none: Returs tag value if exists.
        """
        if bs_element.find(tag) is None:
            return None
        else:
            return bs_element.find(tag).text
