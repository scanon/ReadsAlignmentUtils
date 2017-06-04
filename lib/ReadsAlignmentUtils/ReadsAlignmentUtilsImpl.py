# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import re
import time
import logging
from pprint import pprint
from pprint import pformat

from core import script_utils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DataFileUtil.baseclient import ServerError as DFUError
from ReadsAlignmentUtils.core.sam_tools import SamTools

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
    GIT_URL = "git@github.com:arfathpasha/ReadsAlignmentUtils.git"
    GIT_COMMIT_HASH = "8ecbd3a2803b809b8b585a33d88099dc25df22fa"

    #BEGIN_CLASS_HEADER

    PARAM_IN_WS = 'ws_id_or_name'
    PARAM_IN_OBJ = 'obj_id_or_name'
    PARAM_IN_FILE = 'file_path'
    PARAM_IN_LIB_TYPE = 'library_type'
    PARAM_IN_CONDITION = 'condition'
    PARAM_IN_SAMPLE_ID = 'read_sample_id'
    PARAM_IN_GENOME_ID = 'genome_id'
    PARAM_IN_ALIGNED_USING = 'aligned_using'
    PARAM_IN_ALIGNER_VER = 'aligner_version'

    INVALID_WS_OBJ_NAME_RE = re.compile('[^\\w\\|._-]')
    INVALID_WS_NAME_RE = re.compile('[^\\w:._-]')


    def log(self, message, prefix_newline=False):
        print(('\n' if prefix_newline else '') +
              str(time.time()) + ': ' + message)


    def _get_file_path_info(self, file_path):

        ### returns the dir name, file base name and extension

        dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)

        return dir, file_name, file_base, file_ext


    def _check_required_param(self, in_params, param_list):

       ###  Checks if each of the params in the list are in the input params

       for param in param_list:
            if (param not in in_params or not in_params[param]):
                raise ValueError(param + ' parameter is required')


    def _proc_ws_obj_params(self, ctx, params):

        ###  Checks the validity of workspace and object params and return them

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        if isinstance(params[self.PARAM_IN_WS], int):
            ws_name_id = params[self.PARAM_IN_WS]
            # check if ws id is a valid one
        else:
            try:
                ws_name_id = dfu.ws_name_to_id(params[self.PARAM_IN_WS])
            except DFUError as se:
                prefix = se.message.split('.')[0]
                raise ValueError(prefix)

        self.log('Obtained workspace name/id ' + str(ws_name_id))

        # if already created
        # presence of this object id or name in the workspace is checked later

        obj_name_id = params[self.PARAM_IN_OBJ]

        return ws_name_id, obj_name_id


    def _proc_upload_alignment_params(self, ctx, params):

        ###  Checks the presence and validity of upload alignment params

        self._check_required_param(params, [self.PARAM_IN_WS,
                                            self.PARAM_IN_OBJ,
                                            self.PARAM_IN_FILE,
                                            self.PARAM_IN_LIB_TYPE,
                                            self.PARAM_IN_CONDITION,
                                            self.PARAM_IN_SAMPLE_ID,
                                            self.PARAM_IN_GENOME_ID
                                            ])

        ws_name_id, obj_name_id = self._proc_ws_obj_params(ctx, params)

        file_path = params.get(self.PARAM_IN_FILE)

        if not (os.path.isfile(file_path)):
            raise ValueError('File does not exist: ' + file_path)

        return ws_name_id, obj_name_id, file_path


    def _proc_download_alignment_params(self, ctx, params):

        ###  Checks the presence and validity of download alignment params

        self._check_required_param(params, [self.PARAM_IN_WS,
                                            self.PARAM_IN_OBJ])

        return self._proc_ws_obj_params(ctx, params)


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
           input parameters for uploading a reads alignment ws_id_or_name  - 
           Destination: A numeric value is interpreted as an id and an
           alpha-numeric value is interpreted as a name obj_id_or_name - 
           Destination: A numeric value is interpreted as an id and an
           alpha-numeric value as a name and with '/' as obj ref file_path   
           -  Source: file with the path of the sam or bam file to be
           uploaded library_type   - ‘single_end’ or ‘paired_end’ condition  
           - genome_id      -  workspace id of genome annotation that was
           used to build the alignment read_sample_id -  workspace id of read
           sample used to make the alignment file *) -> structure: parameter
           "ws_id_or_name" of String, parameter "obj_id_or_name" of String,
           parameter "file_path" of String, parameter "library_type" of
           String, parameter "condition" of String, parameter "genome_id" of
           String, parameter "read_sample_id" of String, parameter
           "aligned_using" of String, parameter "aligner_version" of String,
           parameter "aligner_opts" of mapping from String to String,
           parameter "replicate_id" of String, parameter "platform" of
           String, parameter "bowtie2_index" of type "ws_bowtieIndex_id",
           parameter "sampleset_id" of type "ws_Sampleset_id", parameter
           "mapped_sample_id" of mapping from String to mapping from String
           to String, parameter "validate" of type "boolean" (A boolean - 0
           for false, 1 for true. @range (0, 1)), parameter "ignore" of list
           of String
        :returns: instance of type "UploadAlignmentOutput" (*  Output from
           uploading a reads alignment  *) -> structure: parameter "obj_ref"
           of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_alignment

        self.log('Starting upload Reads Alignment, parsing parameters')
        ws_name_id, obj_name_id, file_path = self._proc_upload_alignment_params(ctx, params)

        dir, file_name, file_base, file_ext = self._get_file_path_info(file_path)

        # validate input file
        if 'validate' in params and params['validate'] is True:
            if self._validate(params) == 1:
                raise Exception('{0} failed validation'.format(file_path))

        # more file type and error checking - TO DO

        bam_file = file_path
        if file_ext.lower() == '.sam':
            # checks error from samtools - TO DO
            self.samtools.convert_sam_to_sorted_bam(file_name, dir)
            bam_file = os.path.join(dir, file_base + '.bam')

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        uploaded_file = dfu.file_to_shock({'file_path': bam_file,
                                           'make_handle': 1
                                           })

        file_handle = uploaded_file['handle']
        file_size = uploaded_file['size']

        aligner_stats = self._get_aligner_stats(file_path)

        #  TO_DO:  whether and how to push these into provenance

        aligner_data = {'file': file_handle,
                       'size': file_size,
                       'aligned_using': params.get(self.PARAM_IN_ALIGNED_USING, 'None'),
                       'aligner_version': params.get(self.PARAM_IN_ALIGNER_VER, 'None'),
                       'library_type': params.get(self.PARAM_IN_LIB_TYPE),
                       'condition': params.get(self.PARAM_IN_CONDITION),
                       'read_sample_id': params.get(self.PARAM_IN_SAMPLE_ID),
                       'genome_id': params.get(self.PARAM_IN_GENOME_ID),
                       'alignment_stats': aligner_stats
                      }
        try:

            res = dfu.save_objects(
                {"id": ws_name_id,
                 "objects": [{
                     "type": "KBaseRNASeq.RNASeqAlignment",
                     "data": aligner_data,
                     "name": obj_name_id}
                 ]})[0]

        except Exception, e:
            self.log("Failed to save alignment to workspace")
            raise Exception(e)

        self.log('save complete')

        print("============== SAVE OBJECTS OUTPUT ===================")
        pprint(res)
        print("======================================================\n")

        returnVal = {'obj_ref': str(res[6]) + '/' + str(res[0]) + '/' + str(res[4])}

        print("uploaded object:")
        print(returnVal)

        #END upload_alignment

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_alignment return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def export_alignment(self, ctx, params):
        """
        Wrapper function for use by in-narrative downloaders to download alignments from shock *
        :param params: instance of type "ExportParams" -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_alignment

        #  TO DO

        #END export_alignment

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_alignment return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def download_alignment(self, ctx, params):
        """
        Downloads alignment files in .bam, .sam and .bai formats. Also downloads alignment stats *
        :param params: instance of type "DownloadAlignmentParams" (* Required
           input parameters for downloading a reads alignment ws_id_or_name 
           -  Destination: A numeric value is interpreted as an id and an
           alpha-numeric value is interpreted as a name obj_id_or_name - 
           Destination: A numeric value is interpreted as an id and an
           alpha-numeric value as a name and with '/' as obj ref *) ->
           structure: parameter "ws_id_or_name" of String, parameter
           "obj_id_or_name" of String, parameter "downloadBAM" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "downloadSAM" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "downloadBAI" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "validate" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1)), parameter "ignore" of list of String
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

        ws_name_id, obj_name_id = self._proc_download_alignment_params(ctx, params)

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        obj_ref = obj_name_id if '/' in obj_name_id else \
                    (str(ws_name_id) + '/' + str(obj_name_id))

        try:
            alignment = dfu.get_objects({'object_refs': [obj_ref]})['data']
        except DFUError as e:
            self.log('Logging stacktrace from workspace exception:\n' + e.data)
            raise

        print("=========== Alignment ===============")
        pprint(alignment)
        print("=====================================")

        ## check error from shock_to_file: to do

        output_dir = self.scratch

        file_ret = dfu.shock_to_file({
                                    'shock_id': alignment[0]['data']['file']['id'],
                                    'file_path': output_dir
                                    })

        ## make sure the output file is present: to do

        bam_file = alignment[0]['data']['file']['file_name']

        print(bam_file)

        dir, file_name, file_base, file_ext = self._get_file_path_info(bam_file)

        ## check flags in input param to see which files need to be created - TO DO

        ## check error from samtools - TO DO
        # self.samtools.convert_bam_to_sam(bam_file, self.scratch)
        sam_file = file_base + '.sam'

        # check error from samtools - TO DO
        bai_file = file_base + '.bai'
        self.samtools.create_bai_from_bam(bam_file, self.scratch)

        returnVal = {'ws_id': ws_name_id,
                     'bam_file': os.path.join(output_dir, bam_file),
                     'bai_file': os.path.join(output_dir, bai_file)
                    }

        #END download_alignment

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method download_alignment return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
