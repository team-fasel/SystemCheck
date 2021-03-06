from unittest import TestCase
from systemcheck.systems.ABAP.utils import Connection
from systemcheck.utils import Result, Fail
from pprint import pprint
from systemcheck.config import CONFIG


class TestConnection(TestCase):
    incorrect_logoninfo = dict(ashost='abap001c.team-fasel.lab',
                               sysnr='00',
                               user='DEVELOPER',
                               client='001',
                               passwd='Appl1ance')

    correct_logoninfo = dict(ashost='abap001.team-fasel.lab',
                             sysnr='00',
                             client='001',
                             user='DEVELOPER',
                             passwd='Appl1ance')

    def setUp(self):
        self.XBP_EXT_PRODUCT = CONFIG['systemtype_ABAP']['xbpinterface.XBP_EXT_PRODUCT']
        self.XBP_EXT_COMPANY = CONFIG['systemtype_ABAP']['xbpinterface.XBP_EXT_COMPANY']
        self.XBP_EXT_USER = CONFIG['systemtype_ABAP']['xbpinterface.XBP_EXT_USER']
        self.XPB_INTERFACE_VERS = CONFIG['systemtype_ABAP']['xbpinterface.XPB_INTERFACE_VERS']
        self.conn=Connection()
        self.conn.logon(self.correct_logoninfo)

    def test_connection(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)

        result = conn.logon(self.incorrect_logoninfo)
        self.assertIsInstance(result, Fail)

    def test_instances(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        result = conn.instances
        self.assertIsInstance(result, Result)
        self.assertEqual(result.data, ['abap001_NPL_00'])

    def test_clients(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        result = conn.clients
        pprint(result.data)
        self.assertIsInstance(result, Result)
        self.assertEqual(result.data, {'data': [{'MANDT': '000', 'MTEXT': 'SAP AG Konzern'},
                                                {'MANDT': '001', 'MTEXT': 'SAP AG Konzern'}],
                                       'headers': ['MANDT', 'MTEXT']})

    def test_call_fm(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        # Test a successful execution
        result = conn.call_fm('RFC_SYSTEM_INFO')
        self.assertIsInstance(result, Result)
        expected_result = {'CURRENT_RESOURCES': 2,
                           'MAXIMAL_RESOURCES': 3,
                           'RECOMMENDED_DELAY': 0,
                           'RFCSI_EXPORT': {'RFCCHARTYP': '4103', 'RFCDATABS': 'NPL', 'RFCDAYST': '',
                                            'RFCDBHOST': 'abap001',
                                            'RFCDBSYS': 'SYBASE', 'RFCDEST': 'abap001_NPL_00', 'RFCFLOTYP': 'IE3',
                                            'RFCHOST': 'abap001', 'RFCHOST2': 'abap001', 'RFCINTTYP': 'LIT',
                                            'RFCIPADDR': '10.0.2.165', 'RFCIPV6ADDR': '10.0.2.165', 'RFCKERNRL': '745',
                                            'RFCMACH': '  390', 'RFCOPSYS': 'Linux', 'RFCPROTO': '011',
                                            'RFCSAPRL': '750', 'RFCSI_RESV': '', 'RFCSYSID': 'NPL',
                                            'RFCTZONE': '     0'}}
        self.assertEqual(result.data, expected_result)

        # test a failed execution
        result = conn.call_fm('RFC_SYSTEM_INFO_XXX')
        self.assertIsInstance(result, Fail)
        self.assertEqual(result.message, 'ABAP Application Error')

    def test_download_table(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        # Successful Download
        result = conn.download_table(tabname='T000', tab_fields=['MANDT', 'MTEXT'])
        self.assertIsInstance(result, Result)
        expected_result = {'data': [{'MANDT': '000', 'MTEXT': 'SAP AG Konzern'},
                                    {'MANDT': '001', 'MTEXT': 'SAP AG Konzern'}],
                           'headers': ['MANDT', 'MTEXT']}

        self.assertEqual(result.data, expected_result)
        # Failed Download
        result = conn.download_table(tabname='USR02')
        self.assertIsInstance(result, Fail)
        self.assertEqual(result.message, 'requested column length of 559 is larger than maximum possible (512)')

        # Download with where clause
        result = conn.download_table(tabname='T000', tab_fields=['MANDT', 'MTEXT'], where_clause="MANDT EQ '000'")
        self.assertIsInstance(result, Result)
        expected_result = {'data': [{'MANDT': '000', 'MTEXT': 'SAP AG Konzern'}],
                           'headers': ['MANDT', 'MTEXT']}
        self.assertEqual(result.data, expected_result)

    def test_fm_interface(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        result = conn.fm_interface('SUSR_SUIM_API_RSUSR002')
        pprint(result)

    def test_btc_xmi_logon(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        result = conn.btc_xmi_logon()
        self.assertIsInstance(result, Result)

    def test_btc_xmi_logoff(self):
        conn = Connection()
        result = conn.logon(self.correct_logoninfo)
        self.assertIsInstance(result, Result)
        result = conn.btc_xmi_logon()
        self.assertIsInstance(result, Result)
        result = conn.btc_xmi_logoff()
        self.assertIsInstance(result, Result)

    def test_btc_xbp_variant_create(self):
        fm_parameters=dict(abapProgramName='NROWS', abapVariantName='TEST_T000', abapVariantText='Test Variant')
        variantInfo=[dict(REPORT='NROWS', VARIANT='TEST_T000', PNAME='TABLE1', PLOW='T000', PKIND='P')]

        result=self.conn.btc_xbp_variant_create(variantInfo=variantInfo, **fm_parameters)
        self.assertIsInstance(result, Result)

        fm_parameters=dict(abapProgramName='XXXNROWS', abapVariantName='TEST_T000', abapVariantText='Test Variant')
        variantInfo=[dict(REPORT='XXXNROWS', VARIANT='TEST_T000', PNAME='TABLE1', PLOW='T000', PKIND='P')]

        result=self.conn.btc_xbp_variant_create(variantInfo=variantInfo, **fm_parameters)
        self.assertIsInstance(result, Fail)

    def test_btc_xbp_variant_change(self):
        fm_parameters=dict(abapProgramName='NROWS', abapVariantName='TEST_T000', abapVariantText='Test Variant')
        variantInfo=[dict(REPORT='NROWS', VARIANT='TEST_T000', PNAME='TABLE1', PLOW='T000', PKIND='P')]

        result=self.conn.btc_xbp_variant_create(variantInfo=variantInfo, **fm_parameters)
        self.assertIsInstance(result, Result)

        fm_parameters=dict(abapProgramName='NROWS', abapVariantName='TEST_T000')
        variantInfo=[dict(REPORT='NROWS', VARIANT='TEST_T000', PNAME='TABLE1', PLOW='T001', PKIND='P')]

        result=self.conn.btc_xbp_variant_change(variantInfo=variantInfo, **fm_parameters)
        self.assertIsInstance(result, Result)

    def test_btc_xbp_variant_delete(self):
        fm_parameters=dict(abapProgramName='NROWS', abapVariantName='TEST_T000', abapVariantText='Test Variant')
        variantInfo=[dict(REPORT='NROWS', VARIANT='TEST_T000', PNAME='TABLE1', PLOW='T000', PKIND='P')]

        result=self.conn.btc_xbp_variant_create(variantInfo=variantInfo, **fm_parameters)
        self.assertIsInstance(result, Result)

        fm_parameters=dict(abapProgramName='NROWS', abapVariantName='TEST_T000')

        result=self.conn.btc_xbp_variant_delete(**fm_parameters)
        self.assertIsInstance(result, Result)

    def test_btc_xbp_variant_info_get(self):
        fm_parameters=dict(abapProgramName='NROWS')

        result=self.conn.btc_xbp_variant_info_get(**fm_parameters)
        self.assertIsInstance(result, Result)

    def test_fm_interface_for_BAPI(self):
        result = self.conn.fm_interface('BAPI_XBP_JOB_ADD_ABAP_STEP')
        if not result.fail:
            parameter_data = result.data
            params = [item['PARAMETER'] for item in parameter_data['PARAMS']]
            pprint(params)

