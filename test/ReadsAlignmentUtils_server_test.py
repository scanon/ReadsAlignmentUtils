# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time
import shutil
import hashlib

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from ReadsAlignmentUtils.ReadsAlignmentUtilsImpl import ReadsAlignmentUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsServer import MethodContext
from ReadsAlignmentUtils.authclient import KBaseAuth as _KBaseAuth


def dictmerge(x, y):
    z = x.copy()
    z.update(y)
    return z


class ReadsAlignmentUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ReadsAlignmentUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ReadsAlignmentUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        # create workspace
        wssuffix = int(time.time() * 1000)
        wsName = "test_alignment_" + str(wssuffix)
        cls.wsinfo = cls.wsClient.create_workspace({'workspace': wsName})
        print('created workspace ' + cls.getWsName())

        cls.serviceImpl = ReadsAlignmentUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.setupTestData()


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')


    @classmethod
    def setupTestData(cls):

        ### have a upload directory different from scratch

        cls.upload_dir = os.path.join(cls.scratch, 'upload')
        try:
            os.stat(cls.upload_dir)
        except:
            os.mkdir(cls.upload_dir)

        cls.upload_file = 'accepted_hits_sorted.bam'
        cls.upload_file_path = os.path.join('/kb/module/test/data/samtools', cls.upload_file)
        shutil.copy2(cls.upload_file_path, cls.upload_dir)
        cls.file_to_upload = os.path.join(cls.upload_dir, cls.upload_file)


    def getWsClient(self):
        return self.__class__.wsClient

    @classmethod
    def getWsName(cls):
        return cls.wsinfo[1]

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def md5(self, filename):
        with open(filename, 'rb') as file_:
            hash_md5 = hashlib.md5()
            buf = file_.read(65536)
            while len(buf) > 0:
                hash_md5.update(buf)
                buf = file_.read(65536)
            return hash_md5.hexdigest()


    more_upload_params = {'library_type': 'single_end',
                          'read_sample_id': 'Ecoli_SE_8083_R1.fastq',
                          'genome_id': 'Escherichia_coli_K12',
                          'condition': 'test_condition'
                         }

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    def test_alignment_upload_download(self):

        ##  file uploaded from self.scratch/upload directory
        ##  downloaded to self.scratch directory

        expected_md5 = self.md5(self.upload_file_path)

        params = dictmerge({'ws_id_or_name': self.getWsName(),
                            'obj_id_or_name': 'test_alignment',
                            'file_path': self.file_to_upload,
                            }, self.more_upload_params)

        ret = self.getImpl().upload_alignment(self.ctx, params)[0]

        print(" ====== Returned value from upload ======= ")
        pprint(ret)

        params = {'ws_id_or_name': self.getWsName(),
                  'obj_id_or_name': 'test_alignment' }

        ret = self.getImpl().download_alignment(self.ctx, params)[0]

        print("====== Returned value from download ======= ")
        pprint(ret)

        downloaded_file = os.path.join(self.scratch, ret['bam_file'])
        remote_md5 = self.md5(downloaded_file)
        self.assertEqual(expected_md5, remote_md5)


    def fail_upload_alignment(self, params, error, exception=ValueError, do_startswith=False):
        with self.assertRaises(exception) as context:
            self.getImpl().upload_alignment(self.ctx, params)
        if do_startswith:
            self.assertTrue(str(context.exception.message).startswith(error),
                            "Error message {} does not start with {}".format(
                                str(context.exception.message),
                                error))
        else:
            self.assertEqual(error, str(context.exception.message))


    def test_upload_fail_no_ws(self):
        self.fail_upload_alignment(
            dictmerge({
                        'condition': 'bar',
                        'obj_id_or_name': 'foo',
                        'file_path': 'test'
                       }, self.more_upload_params),
            'ws_id_or_name parameter is required')


    def test_upload_fail_no_obj_id(self):
        self.fail_upload_alignment(
            dictmerge({
                         'condition': 'bar',
                         'ws_id_or_name': self.getWsName(),
                         'file_path': 'test'
                       }, self.more_upload_params),
            'obj_id_or_name parameter is required')


    def test_upload_fail_no_file(self):
        self.fail_upload_alignment(
            dictmerge({
                         'ws_id_or_name': self.getWsName(),
                         'obj_id_or_name': 'foo'
                       },self.more_upload_params),
            'file_path parameter is required')


    def test_upload_fail_bad_wsname(self):
        self.fail_upload_alignment(
            dictmerge({
                        'ws_id_or_name': '&bad',
                        'obj_id_or_name': 'bar',
                        'file_path': 'foo'
                      }, self.more_upload_params),
            'Illegal character in workspace name &bad: &')


    def test_upload_fail_non_existant_wsname(self):
        self.fail_upload_alignment(
            dictmerge({
                         'ws_id_or_name': '1s',
                         'obj_id_or_name': 'foo',
                         'file_path': 'bar'
                       }, self.more_upload_params),
            'No workspace with name 1s exists')


    def test_upload_fail_non_existant_file(self):
        self.fail_upload_alignment(
            dictmerge({
                        'ws_id_or_name': self.getWsName(),
                        'obj_id_or_name': 'foo',
                        'file_path': 'foo'
                    }, self.more_upload_params),
            'File does not exist: foo')

    # TO DO:  add more tests

