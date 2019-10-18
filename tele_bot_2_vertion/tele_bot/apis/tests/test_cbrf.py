from collections import namedtuple
from unittest import TestCase
from unittest import mock

from apis.cbrf import get_rate
from apis.cbrf import str_to_float
from apis.cbrf import CentralBankError


MockResponse = namedtuple('MockResponse', 'status_code,text')


class CBRFTestCase(TestCase):

    def test_str_to_float_int(self):
        r = str_to_float('1')
        self.assertEqual(r, 1.0)

    def test_str_to_float_real(self):
        r = str_to_float('1,23')
        self.assertEqual(r, 1.23)

    def test_str_to_float(self):
        r = str_to_float('2.34')
        self.assertEqual(r, 2.34)

    @mock.patch('requests.get')
    def test_get_rate_bad_status_code(self, req):
        """ API ответило какой-то ошибкой
        """
        req.return_value = MockResponse(status_code=444, text='')

        with self.assertRaises(CentralBankError) as er:
            get_rate()

        self.assertEqual(str(er.exception), 'bad status code')

    @mock.patch('requests.get')
    def test_get_rate_bad_xml(self, req):
        """ API вернуло невалидный XML
        """
        req.return_value = MockResponse(status_code=200, text='xxx')

        with self.assertRaises(CentralBankError) as er:
            get_rate()

        self.assertEqual(str(er.exception), 'bad xml')

    @mock.patch('requests.get')
    def test_get_rate_bad_json(self, req):
        """ Успешный ответ API, валидный XML, но в нём нет опорных ключей
        """
        content = '''<?xml version="1.0" encoding="windows-1251"?>
            <ValCurs Date="03.08.2019" name="Foreign Currency Market">
                <SomeData ID="R01010">
                    <NumCode>036</NumCode>
                    <CharCode>AUD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Австралийский доллар</Name>
                    <Value>43,9051</Value>
                </SomeData>
                <SomeData ID="R01020A">
                    <NumCode>944</NumCode>
                    <CharCode>AZN</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Азербайджанский манат</Name>
                    <Value>38,4641</Value>
                </SomeData>
            </ValCurs>
        '''
        req.return_value = MockResponse(status_code=200, text=content)

        with self.assertRaises(CentralBankError) as er:
            get_rate()

        self.assertEqual(str(er.exception), 'json traversal error')

    @mock.patch('requests.get')
    def test_get_rate_no_rub(self, req):
        """ Успешный ответ API, но в нём нет курса рубля
        """
        content = '''<?xml version="1.0" encoding="windows-1251"?>
            <ValCurs Date="03.08.2019" name="Foreign Currency Market">
                <Valute ID="R01010">
                    <NumCode>036</NumCode>
                    <CharCode>AUD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Австралийский доллар</Name>
                    <Value>43,9051</Value>
                </Valute>
                <Valute ID="R01020A">
                    <NumCode>944</NumCode>
                    <CharCode>AZN</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Азербайджанский манат</Name>
                    <Value>38,4641</Value>
                </Valute>
            </ValCurs>
        '''
        req.return_value = MockResponse(status_code=200, text=content)

        r = get_rate()
        self.assertIsNone(r)

    @mock.patch('requests.get')
    def test_get_rate_ok(self, req):
        content = '''<?xml version="1.0" encoding="windows-1251"?>
            <ValCurs Date="03.08.2019" name="Foreign Currency Market">
                <Valute ID="R01020A">
                    <NumCode>944</NumCode>
                    <CharCode>AZN</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Азербайджанский манат</Name>
                    <Value>38,4641</Value>
                </Valute>
                <Valute ID="R01235">
                    <NumCode>840</NumCode>
                    <CharCode>USD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Доллар США</Name>
                    <Value>65,2543</Value>
                </Valute>
            </ValCurs>
        '''
        req.return_value = MockResponse(status_code=200, text=content)

        r = get_rate()
        self.assertIsNotNone(r)
        self.assertEqual(r.rate, 65.2543)
        self.assertEqual(r.name, 'USD')
