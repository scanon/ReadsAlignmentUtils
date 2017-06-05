# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time
import shutil
import hashlib
import requests
import inspect
import tempfile
from zipfile import ZipFile

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from Workspace.baseclient import ServerError as WorkspaceError
from Workspace.WorkspaceClient import Workspace
from DataFileUtil.baseclient import ServerError as DFUError
from DataFileUtil.DataFileUtilClient import DataFileUtil
from biokbase.AbstractHandle.Client import AbstractHandle as HandleService  # @UnresolvedImport
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
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ReadsAlignmentUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ReadsAlignmentUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.shockURL = cls.cfg['shock-url']
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.ws = Workspace(cls.wsURL, token=cls.token)
        cls.hs = HandleService(url=cls.cfg['handle-service-url'],
                               token=cls.token)
        # create workspace
        wssuffix = int(time.time() * 1000)
        wsname = "test_alignment_" + str(wssuffix)
        cls.wsinfo = cls.wsClient.create_workspace({'workspace': wsname})
        print('created workspace ' + cls.getWsName())

        cls.serviceImpl = ReadsAlignmentUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)

        cls.staged = {}
        cls.nodes_to_delete = []
        cls.handles_to_delete = []
        cls.setupTestData()


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')


    def getWsClient(self):
        return self.wsClient

    @classmethod
    def getWsName(cls):
        return cls.wsinfo[1]

    def getImpl(self):
        return self.serviceImpl

    def getContext(self):
        return self.ctx

    @classmethod
    def delete_shock_node(cls, node_id):
        header = {'Authorization': 'Oauth {0}'.format(cls.token)}
        requests.delete(cls.shockURL + '/node/' + node_id, headers=header,
                        allow_redirects=True)
        print('Deleted shock node ' + node_id)

    @classmethod
    def upload_file_to_shock(cls, file_path):
        """
        Use HTTP multi-part POST to save a file to a SHOCK instance.
        """

        header = dict()
        header["Authorization"] = "Oauth {0}".format(cls.token)

        if file_path is None:
            raise Exception("No file given for upload to SHOCK!")

        with open(os.path.abspath(file_path), 'rb') as dataFile:
            files = {'upload': dataFile}
            print('POSTing data')
            response = requests.post(
                cls.shockURL + '/node', headers=header, files=files,
                stream=True, allow_redirects=True)
            print('got response')

        if not response.ok:
            response.raise_for_status()

        result = response.json()

        if result['error']:
            raise Exception(result['error'][0])
        else:
            return result["data"]


    @classmethod
    def upload_file_to_shock_and_get_handle(cls, test_file):
        '''
        Uploads the file in test_file to shock and returns the node and a
        handle to the node.
        '''
        print('loading file to shock: ' + test_file)
        node = cls.upload_file_to_shock(test_file)
        pprint(node)
        cls.nodes_to_delete.append(node['id'])

        print('creating handle for shock id ' + node['id'])
        handle_id = cls.hs.persist_handle({'id': node['id'],
                                           'type': 'shock',
                                           'url': cls.shockURL
                                           })
        cls.handles_to_delete.append(handle_id)

        md5 = node['file']['checksum']['md5']
        return node['id'], handle_id, md5, node['file']['size']


    @classmethod
    def save_ws_obj(cls, obj, objname, objtype):
        tt = { 'type': objtype,
               'data': obj,
               'name': objname
              }
        return cls.ws.save_objects({
            'workspace': cls.getWsName(),
            'objects': [{'type': objtype,
                         'data': obj,
                         'name': objname
                         }]
        })[0]

    more_upload_params = {'library_type': 'single_end',
                          'read_sample_id': 'Ecoli_SE_8083_R1.fastq',
                          'genome_id': 'Escherichia_coli_K12',
                          'condition': 'test_condition'
                          }

    @classmethod
    def uploadTestData(cls, wsobjname, object_body, alignment):

        ob = dict(object_body)  # copy
        ob['wsname'] = cls.getWsName()
        #ob['name'] = wsobjname

        print('\n===============staging data for object ' + wsobjname +
              '================')
        print('uploading alignment file ' + alignment['file'])
        a_id, a_handle_id, a_md5, a_size = \
            cls.upload_file_to_shock_and_get_handle(alignment['file'])

        a_handle = {
            'hid': a_handle_id,
            'file_name': alignment['name'],
            'id': a_id,
            'url': cls.shockURL,
            'type': 'shock',
            'remote_md5': a_md5
        }

        ob['file'] = a_handle
        ob['size'] = a_size

        print('Saving object data')

        objdata = cls.save_ws_obj(ob, wsobjname, 'KBaseRNASeq.RNASeqAlignment')
        print('Saved object: ')
        pprint(objdata)
        pprint(ob)

        cls.staged[wsobjname] = {'info': objdata,
                                 'ref': cls.make_ref(objdata),
                                 'node_id': a_id,
                                 'handle': a_handle
                                }

    @classmethod
    def setupTestData(cls):

        ###  set up test data for download

        test_bam = {'file': 'data/samtools/accepted_hits_sorted.bam',
                         'name': 'accepted_hits_sorted.bam',
                         'type': ''}

        test_sam = {'file': 'data/samtools/accepted_hits.sam',
                    'name': 'accepted_hits.sam',
                    'type': ''}

        cls.uploadTestData('test_download_bam', cls.more_upload_params, test_bam)
        cls.uploadTestData('test_download_sam', cls.more_upload_params, test_sam)


    @classmethod
    def make_ref(cls, objinfo):
        return str(objinfo[6]) + '/' + str(objinfo[0]) + '/' + str(objinfo[4])


    @classmethod
    def getSize(cls, filename):
        return os.path.getsize(filename)


    @classmethod
    def md5(cls, filename):
        with open(filename, 'rb') as file_:
            hash_md5 = hashlib.md5()
            buf = file_.read(65536)
            while len(buf) > 0:
                hash_md5.update(buf)
                buf = file_.read(65536)
            return hash_md5.hexdigest()


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa


    def upload_alignment_success(self, params, expected):

        tf = params.get('file_path')
        target = os.path.join(self.scratch, tf)
        shutil.copy('data/samtools/' + tf, target)
        params['file_path'] = target

        ref = self.getImpl().upload_alignment(self.ctx, params)[0]

        obj = self.dfu.get_objects(
            {'object_refs': [params.get('destination_ref')]})['data'][0]

        print("============ GET OBJECTS OUTPUT ==============")
        pprint(obj)
        print("==============================================")

        self.assertEqual(ref['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseRNASeq.RNASeqAlignment'), True)
        d = obj['data']
        self.assertEqual(d['genome_id'], params.get('genome_id'))
        self.assertEqual(d['library_type'], params.get('library_type'))
        self.assertEqual(d['condition'], params.get('condition'))
        self.assertEqual(d['read_sample_id'], params.get('read_sample_id'))

        self.assertEqual(d['size'], expected.get('size'))

        f = d['file']
        self.assertEqual(f['file_name'], expected.get('file_name'))
        self.assertEqual(f['remote_md5'], expected.get('md5'))

        node = f['id']
        self.delete_shock_node(node)


    def test_upload_success_bam(self):

        params = dictmerge({'destination_ref': self.getWsName() + '/test_download_bam',
                            'file_path': 'accepted_hits_sorted.bam',
                            'validate': 'True'
                            }, self.more_upload_params)
        expected = {'file_name': 'accepted_hits_sorted.bam',
                    'size': 741290,
                    'md5': '96c59589b0ed7338ff27de1881cf40b3' }
        self.upload_alignment_success(params, expected)


    def test_upload_success_sam(self):

        params = dictmerge({'destination_ref': self.getWsName() + '/test_download_sam',
                            'file_path': 'accepted_hits.sam',
                            'validate': 'True'
                            }, self.more_upload_params)
        expected = {'file_name': 'accepted_hits_sorted.bam',
                    'size': 741290,
                    'md5': '96c59589b0ed7338ff27de1881cf40b3'}
        self.upload_alignment_success(params, expected)


    def download_alignment_success(self, obj_name, expected):

        test_name = inspect.stack()[1][3]
        print('\n**** starting expected downlaod success test: ' + test_name + ' ***\n')

        params = {'source_ref': self.getWsName() + '/' + obj_name,
                  'downloadSAM': 'True',
                  'downloadBAI': 'True'}

        ret = self.getImpl().download_alignment(self.ctx, params)[0]
        print('\n== Output from download_alignment:')
        pprint(ret)

        bam_file_path = ret['bam_file']
        out_dir, bam_file_name = os.path.split(bam_file_path)
        self.assertEqual(bam_file_name, expected['bam_file'])
        size = os.path.getsize(bam_file_path)
        md5 = self.md5(bam_file_path)
        self.assertEqual(size, expected['size'])
        self.assertEqual(md5, expected['md5'])


    def test_download_success(self):

        self.download_alignment_success('test_download_bam',
                                        {'bam_file': 'accepted_hits_sorted.bam',
                                         'size': 741290,
                                         'md5': '96c59589b0ed7338ff27de1881cf40b3'})


    def export_alignment_success(self, staged_name, bam_md5):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected export pass test: ' + test_name + ' **')
        shocknode = self.getImpl().export_alignment(
            self.ctx,
            {'source_ref': self.staged[staged_name]['ref']})[0]['shock_id']
        node_url = self.shockURL + '/node/' + shocknode
        headers = {'Authorization': 'OAuth ' + self.token}
        r = requests.get(node_url, headers=headers, allow_redirects=True)
        fn = r.json()['data']['file']['name']
        self.assertEquals(fn, staged_name + '.zip')
        tempdir = tempfile.mkdtemp(dir=self.scratch)
        file_path = os.path.join(tempdir, test_name) + '.zip'
        print('zip file path: ' + file_path)
        print('downloading shocknode ' + shocknode)
        with open(file_path, 'wb') as fhandle:
            r = requests.get(node_url + '?download_raw', stream=True,
                             headers=headers, allow_redirects=True)
            for chunk in r.iter_content(1024):
                if not chunk:
                    break
                fhandle.write(chunk)
        with ZipFile(file_path) as z:
            z.extractall(tempdir)
        print('zip file contents: ' + str(os.listdir(tempdir)))
        foundBAM = False
        for f in os.listdir(tempdir):
            if '.bam' in f :
                foundBAM = True
                print('BAM file: ' + f)
                with open(os.path.join(tempdir, f)) as fl:
                    md5 = hashlib.md5(fl.read()).hexdigest()
                    self.assertEqual(md5, bam_md5)
        if not foundBAM:
            raise TestError('no BAM file')


    def test_success_export_alignment(self):

        self.export_alignment_success('test_download_bam', '96c59589b0ed7338ff27de1881cf40b3')


    def test_valid_validate_alignment(self):
        params = {'file_path':'data/samtools/accepted_hits.sam',
                   'ignore':['MATE_NOT_FOUND','MISSING_READ_GROUP',
                         'INVALID_MAPPING_QUALITY']}

        ret = self.getImpl().validate_alignment(self.ctx, params)[0]

        self.assertEquals(True, ret['validated'])

        params = {'file_path': 'data/samtools/accepted_hits.sam'}

        ret = self.getImpl().validate_alignment(self.ctx, params)[0]

        self.assertEquals(True, ret['validated'])


    def test_valid_invalidate_alignment(self):
        params = {'file_path': 'data/samtools/accepted_hits_invalid.sam',
                  'ignore': ['MATE_NOT_FOUND', 'MISSING_READ_GROUP',
                             'INVALID_MAPPING_QUALITY']}

        ret = self.getImpl().validate_alignment(self.ctx, params)[0]

        self.assertEquals(False, ret['validated'])


    '''
    
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


    def test_upload_fail_non_existant_file(self):
        self.fail_upload_alignment(
            dictmerge({
                'ws_id_or_name': self.getWsName(),
                'obj_id_or_name': 'foo',
                'file_path': 'foo'
            }, self.more_upload_params),
            'File does not exist: foo')


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
    '''

    # TO DO:  add more tests

