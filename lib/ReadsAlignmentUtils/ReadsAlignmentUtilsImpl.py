# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import re
import time
import shutil
import logging
import tempfile
from datetime import datetime

from pprint import pprint
from pprint import pformat

from core import script_utils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DataFileUtil.baseclient import ServerError as DFUError
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsUtils.baseclient import ServerError
from ReadsAlignmentUtils.core.sam_tools import SamTools
from Workspace.WorkspaceClient import Workspace
from Workspace.baseclient import ServerError as WorkspaceError

#END_HEADER


class ReadsAlignmentUtils:
    '''
    Module Name:
    ReadsAlignmentUtils

    Module Description:
    A KBase module: ReadsAlignmentUtils

This module is intended for use by Aligners and Assemblers to upload and download alignment files.
The alignment may be uploaded as .sam or .bam files. Once uploaded, the alignment can be
downloaded in .sam, sorted .bam or .bai file formats. This utility also generates stats from
the stored alignment.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/ReadsAlignmentUtils.git"
    GIT_COMMIT_HASH = "4eff9c09cd33f22100efc38cc25cfd112eadd07f"

    #BEGIN_CLASS_HEADER

    ### required params
    PARAM_IN_FILE = 'file_path'
    PARAM_IN_SRC_REF = 'source_ref'
    PARAM_IN_DST_REF = 'destination_ref'
    PARAM_IN_CONDITION = 'condition'
    PARAM_IN_READ_LIB_REF = 'read_library_ref'
    PARAM_IN_ASM_GEN_REF = 'assembly_or_genome_ref'

    ### optional params
    PARAM_IN_ALIGNED_USING = 'aligned_using'
    PARAM_IN_ALIGNER_VER = 'aligner_version'
    PARAM_IN_ALIGNER_OPTS = 'aligner_opts'
    PARAM_IN_REPLICATE_ID = 'replicate_id'
    PARAM_IN_PLATFORM = 'platform'
    PARAM_IN_BOWTIE2_INDEX = 'bowtie2_index'
    PARAM_IN_SAMPLESET_REF = 'sampleset_ref'
    PARAM_IN_MAPPED_SAMPLE_ID = 'mapped_sample_id'

    INVALID_WS_OBJ_NAME_RE = re.compile('[^\\w\\|._-]')
    INVALID_WS_NAME_RE = re.compile('[^\\w:._-]')


    def log(self, message, prefix_newline=False):
        print(('\n' if prefix_newline else '') +
              str(time.time()) + ': ' + message)


    def _get_file_path_info(self, file_path):

        ### returns the dir name, file name, base name and extension

        dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)

        return dir, file_name, file_base, file_ext


    def _check_required_param(self, in_params, param_list):

       ###  Checks if each of the params in the list are in the input params

       for param in param_list:
            if (param not in in_params or not in_params[param]):
                raise ValueError(param + ' parameter is required')


    def _proc_ws_obj_params(self, ctx, params):

        ###  Checks the validity of workspace and object params and returns them

        dst_ref = params.get(self.PARAM_IN_DST_REF)

        ws_name_id, obj_name_id = os.path.split(dst_ref)

        if not bool(ws_name_id.strip()) or ws_name_id == '/':
            raise ValueError("Workspace name or id is required in " + self.PARAM_IN_DST_REF)

        if not bool(obj_name_id.strip()):
            raise ValueError("Object name or id is required in " + self.PARAM_IN_DST_REF)

        dfu = DataFileUtil(self.callback_url, token=ctx['token'], service_ver='dev')

        if not isinstance(ws_name_id, int):

            try:
                ws_name_id = dfu.ws_name_to_id(ws_name_id)
            except DFUError as se:
                prefix = se.message.split('.')[0]
                raise ValueError(prefix)

        self.log('Obtained workspace name/id ' + str(ws_name_id))

        return ws_name_id, obj_name_id


    def _proc_upload_alignment_params(self, ctx, params):

        ###  Checks the presence and validity of upload alignment params

        self._check_required_param(params, [self.PARAM_IN_DST_REF,
                                            self.PARAM_IN_FILE,
                                            self.PARAM_IN_CONDITION,
                                            self.PARAM_IN_READ_LIB_REF,
                                            self.PARAM_IN_ASM_GEN_REF
                                            ])

        ws_name_id, obj_name_id = self._proc_ws_obj_params(ctx, params)

        file_path = params.get(self.PARAM_IN_FILE)

        if not (os.path.isfile(file_path)):
            raise ValueError('File does not exist: ' + file_path)

        return ws_name_id, obj_name_id, file_path


    def _get_ws_info(self, obj_ref):

        # get WS metadata to get obj_name
        ws = Workspace(self.ws_url)
        try:
            info = ws.get_object_info_new({'objects': [{'ref': obj_ref}]})[0]
        except WorkspaceError as wse:
            self.log('Logging workspace exception')
            self.log(str(wse))
            raise
        return info


    def _get_read_lib_type(self, ctx, read_lib_ref):

        ws_info = self._get_ws_info(read_lib_ref)
        readcli = ReadsUtils(self.callback_url, token=ctx['token'], service_ver='dev')
        reads_ref = ws_info[7] + '/' + ws_info[1]

        typeerr = ('Supported types: KBaseFile.SingleEndLibrary ' +
                   'KBaseFile.PairedEndLibrary ' +
                   'KBaseAssembly.SingleEndLibrary ' +
                   'KBaseAssembly.PairedEndLibrary')

        try:
            reads = readcli.download_reads({'read_libraries': [reads_ref],
                                            'interleaved': 'false',
                                            'gzipped': None
                                            })['files']
        except ServerError as se:
            self.log('logging stacktrace from dynamic client error')
            self.log(se.data)
            if typeerr in se.message:
                prefix = se.message.split('.')[0]
                raise ValueError(
                    prefix + '. Only the types ' +
                    'KBaseFile.SingleEndLibrary KBaseAssembly.PairedEndLibrary ' +
                    'KBaseAssembly.SingleEndLibrary and KBaseFile.PairedEndLibrary are supported')

        self.log('Got reads data from converter:\n' + pformat(reads))

        return reads[reads_ref]['files']['type']


    def _get_aligner_stats(self, file):

        ###  Gets the aligner stats from BAM file

        return self.samtools.get_stats(file)


    def _validate(self, params):
        samt = SamTools(self.config, self.__LOGGER)
        if 'ignore' in params:
            rval = samt.validate(ifile=params['file_path'], ipath=None,
                                 ignore=params['ignore'])
        else:
            rval = samt.validate(ifile=params['file_path'], ipath=None)

        return rval


    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.__LOGGER = logging.getLogger('KBaseRNASeq')
        if 'log_level' in config:
              self.__LOGGER.setLevel(config['log_level'])
        else:
              self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        script_utils.check_sys_stat(self.__LOGGER)

        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        self.samtools = SamTools(config)
        #END_CONSTRUCTOR
        pass


    def validate_alignment(self, ctx, params):
        """
        :param params: instance of type "ValidateAlignmentParams" (* Input
           parameters for validating a reads alignment *) -> structure:
           parameter "file_path" of String, parameter "ignore" of list of
           String
        :returns: instance of type "ValidateAlignmentOutput" (* Results from
           validate alignment *) -> structure: parameter "validated" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN validate_alignment

        rval = self._validate(params)

        if rval == 0:
            returnVal = {'validated': True }
        else:
            returnVal = {'validated': False }

        #END validate_alignment

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method validate_alignment return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def upload_alignment(self, ctx, params):
        """
        Validates and uploads the reads alignment  *
        :param params: instance of type "UploadAlignmentParams" (* Required
           input parameters for uploading a reads alignment string
           destination_ref -  object reference of alignment destination. The
           object ref is 'ws_name_or_id/obj_name_or_id' where ws_name_or_id
           is the workspace name or id and obj_name_or_id is the object name
           or id file_path              -  Source: file with the path of the
           sam or bam file to be uploaded read_library_ref       -  workspace
           object ref of the read sample used to make the alignment file
           condition              - assembly_or_genome_ref -  workspace
           object ref of assembly or genome annotation that was used to build
           the alignment *) -> structure: parameter "destination_ref" of
           String, parameter "file_path" of String, parameter "condition" of
           String, parameter "assembly_or_genome_ref" of String, parameter
           "read_library_ref" of String, parameter "aligned_using" of String,
           parameter "aligner_version" of String, parameter "aligner_opts" of
           mapping from String to String, parameter "replicate_id" of String,
           parameter "platform" of String, parameter "bowtie2_index" of type
           "ws_bowtieIndex_id", parameter "sampleset_ref" of type
           "ws_Sampleset_ref", parameter "mapped_sample_id" of mapping from
           String to mapping from String to String, parameter "validate" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "ignore" of list of String
        :returns: instance of type "UploadAlignmentOutput" (*  Output from
           uploading a reads alignment  *) -> structure: parameter "obj_ref"
           of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_alignment

        self.log('Starting upload Reads Alignment, parsing parameters ')
        pprint(params)

        ws_name_id, obj_name_id, file_path = self._proc_upload_alignment_params(ctx, params)

        dir, file_name, file_base, file_ext = self._get_file_path_info(file_path)

        # validate input file
        if 'validate' in params and params['validate'] is True:
            if self._validate(params) == 1:
                raise Exception('{0} failed validation'.format(file_path))

        bam_file = file_path
        if file_ext.lower() == '.sam':
            bam_file = os.path.join(dir, file_base + '_sorted.bam')
            self.samtools.convert_sam_to_sorted_bam(file_name, dir, bam_file)

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        uploaded_file = dfu.file_to_shock({'file_path': bam_file,
                                           'make_handle': 1
                                           })

        file_handle = uploaded_file['handle']
        file_size = uploaded_file['size']

        ###  gets the required parameters for workspace object

        aligner_stats = self._get_aligner_stats(file_path)

        aligner_data = {
                         'file': file_handle,
                         'size': file_size,
                         'condition': params.get(self.PARAM_IN_CONDITION),
                         'read_sample_id': params.get(self.PARAM_IN_READ_LIB_REF),
                         'genome_id': params.get(self.PARAM_IN_ASM_GEN_REF),
                         'aligner_stats': aligner_stats
                        }

        aligner_data['library_type'] = self._get_read_lib_type(ctx, params.get(self.PARAM_IN_READ_LIB_REF))

        optional_params = [ self.PARAM_IN_ALIGNED_USING,
                            self.PARAM_IN_ALIGNER_VER,
                            self.PARAM_IN_ALIGNER_OPTS,
                            self.PARAM_IN_REPLICATE_ID,
                            self.PARAM_IN_PLATFORM,
                            self.PARAM_IN_BOWTIE2_INDEX,
                            self.PARAM_IN_SAMPLESET_REF,
                            self.PARAM_IN_MAPPED_SAMPLE_ID ]

        for opt_param in optional_params:
            if opt_param in params and params[opt_param] is not None:
                aligner_data[opt_param] = params[opt_param]


        res = dfu.save_objects(
                {"id": ws_name_id,
                 "objects": [{
                     "type": "KBaseRNASeq.RNASeqAlignment",
                     "data": aligner_data,
                     "name": obj_name_id}
                 ]})[0]

        self.log('save complete')

        returnVal = {'obj_ref': str(res[6]) + '/' + str(res[0]) + '/' + str(res[4])}

        print('Uploaded object: ')
        print(returnVal)

        #END upload_alignment

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_alignment return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def download_alignment(self, ctx, params):
        """
        Downloads alignment files in .bam, .sam and .bai formats. Also downloads alignment stats *
        :param params: instance of type "DownloadAlignmentParams" (* Required
           input parameters for downloading a reads alignment string
           source_ref -  object reference of alignment source. The object ref
           is 'ws_name_or_id/obj_name_or_id' where ws_name_or_id is the
           workspace name or id and obj_name_or_id is the object name or id
           *) -> structure: parameter "source_ref" of String, parameter
           "downloadBAM" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "downloadSAM" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "downloadBAI" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "validate" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "ignore" of list of String
        :returns: instance of type "DownloadAlignmentOutput" (*  The output
           of the download method.  *) -> structure: parameter "ws_id" of
           String, parameter "bam_file" of String, parameter "sam_file" of
           String, parameter "bai_file" of String, parameter "stats" of type
           "AlignmentStats" (* @optional singletons multiple_alignments,
           properly_paired, alignment_rate, unmapped_reads, mapped_sections
           total_reads, mapped_reads *) -> structure: parameter
           "properly_paired" of Long, parameter "multiple_alignments" of
           Long, parameter "singletons" of Long, parameter "alignment_rate"
           of Double, parameter "unmapped_reads" of Long, parameter
           "mapped_reads" of Long, parameter "total_reads" of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN download_alignment

        self.log('Running download_alignment with params:\n' +
                 pformat(params))

        inref = params.get(self.PARAM_IN_SRC_REF)
        if not inref:
            raise ValueError(self.PARAM_IN_SRC_REF + ' parameter is required')

        info = self._get_ws_info(inref)

        obj_ref = str(info[6]) + '/' + str(info[0])

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        try:
            alignment = dfu.get_objects({'object_refs': [obj_ref]})['data']
        except DFUError as e:
            self.log('Logging stacktrace from workspace exception:\n' + e.data)
            raise

        # set the output dir
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'download_' + str(timestamp))
        os.mkdir(output_dir)

        file_ret = dfu.shock_to_file({
                                    'shock_id': alignment[0]['data']['file']['id'],
                                    'file_path': output_dir
                                    })

        bam_file = alignment[0]['data']['file']['file_name']

        # validate the downloaded bam file
        if 'validate' in params and params['validate'] is True:
            params['file_path'] = bam_file
            if self._validate(params) == 1:
                raise Exception('{0} failed validation'.format(bam_file))

        print(bam_file)

        dir, file_name, file_base, file_ext = self._get_file_path_info(bam_file)

        returnVal = {'ws_id': info[6]}

        if (params.get('downloadBAM', True)):
            bam_file_path = os.path.join(output_dir, bam_file)
            if os.path.isfile(bam_file_path):
                returnVal['bam_file'] = bam_file_path
            else:
                raise ValueError('Error downloading ' + bam_file)

        if (params.get('downloadBAI', False)):
            bai_file = file_base + '.bai'
            bai_file_path = os.path.join(output_dir, bai_file)
            self.samtools.create_bai_from_bam(bam_file, output_dir)
            if os.path.isfile(bai_file_path):
                returnVal['bai_file'] = bai_file_path
            else:
                raise ValueError('Error downloading ' + bai_file)

        if (params.get('downloadSAM', False)):
            file_base = file_base.replace('_sorted', '')
            sam_file = file_base + '.sam'
            self.samtools.convert_bam_to_sam(bam_file, output_dir, sam_file)
            sam_file_path = os.path.join(output_dir, sam_file)
            if os.path.isfile(sam_file_path):
                returnVal['sam_file'] = sam_file_path
            else:
                raise ValueError('Error downloading ' + sam_file)

        if len(returnVal) == 1:
            raise ValueError('No files were requested to be downloaded')

        #END download_alignment

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method download_alignment return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def export_alignment(self, ctx, params):
        """
        Wrapper function for use by in-narrative downloaders to download alignments from shock *
        :param params: instance of type "ExportParams" (* Required input
           parameters for exporting a reads alignment string source_ref - 
           object reference of alignment source. The object ref is
           'ws_name_or_id/obj_name_or_id' where ws_name_or_id is the
           workspace name or id and obj_name_or_id is the object name or id
           *) -> structure: parameter "source_ref" of String, parameter
           "exportBAM" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "exportSAM" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "exportBAI" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "validate" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "ignore" of list of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_alignment

        inref = params.get(self.PARAM_IN_SRC_REF)
        if not inref:
            raise ValueError(self.PARAM_IN_SRC_REF + ' parameter is required')

        info = self._get_ws_info(inref)

        download_params = {}
        for key, val in params.iteritems():
            download_params[key.replace('export', 'download')] = val

        files = self.download_alignment(ctx, download_params)[0]

        # create the output directory and move the file there
        tempdir = tempfile.mkdtemp(dir=self.scratch)
        export_dir = os.path.join(tempdir, info[1])
        os.makedirs(export_dir)

        bamFile = files.get('bam_file')
        if bamFile:
            shutil.move(bamFile, os.path.join(export_dir, os.path.basename(bamFile)))
        samFile = files.get('sam_file')
        if samFile:
            shutil.move(samFile, os.path.join(export_dir, os.path.basename(samFile)))
        baiFile = files.get('bai_file')
        if baiFile:
            shutil.move(baiFile, os.path.join(export_dir, os.path.basename(baiFile)))

        # package and load to shock
        dfu = DataFileUtil(self.callback_url)
        ret = dfu.package_for_download({'file_path': export_dir,
                                        'ws_refs': [inref]
                                        })

        output = {'shock_id': ret['shock_id']}

        #END export_alignment

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_alignment return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
