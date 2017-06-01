# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import re
import time
from pprint import pprint
from pprint import pformat

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
    GIT_URL = "https://github.com/ugswork/ReadsAlignmentUtils.git"
    GIT_COMMIT_HASH = "bef0d1fb61a7eca8167adcb8ab0c5374c300579d"

    #BEGIN_CLASS_HEADER

    PARAM_IN_WS = 'ws_id_or_name'
    PARAM_IN_OBJ = 'obj_id_or_name'
    PARAM_IN_FILE = 'file_path'

    INVALID_WS_OBJ_NAME_RE = re.compile('[^\\w\\|._-]')
    INVALID_WS_NAME_RE = re.compile('[^\\w:._-]')

    def log(self, message, prefix_newline=False):
        print(('\n' if prefix_newline else '') +
              str(time.time()) + ': ' + message)


    def _check_required_param(self, in_params, param):
        if (param not in in_params or not in_params[param]):
            raise ValueError(param + ' parameter is required')


    def _proc_ws_obj_params(self, ctx, params):

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

        # TO DO:  add all required params

        self._check_required_param(params, self.PARAM_IN_WS)
        self._check_required_param(params, self.PARAM_IN_OBJ)
        self._check_required_param(params, self.PARAM_IN_FILE)

        ws_name_id, obj_name_id = self._proc_ws_obj_params(ctx, params)

        file_path = params.get(self.PARAM_IN_FILE)

        if not (os.path.isfile(file_path)):
            raise ValueError('File does not exist: ' + file_path)

        return ws_name_id, obj_name_id, file_path


    def _proc_download_alignment_params(self, ctx, params):

        self._check_required_param(params, self.PARAM_IN_WS)
        self._check_required_param(params, self.PARAM_IN_OBJ)

        return self._proc_ws_obj_params(ctx, params)


    def _get_aligner_stats(self, file):
        return self.samtools.get_stats(file)


    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.samtools = SamTools(config)
        #END_CONSTRUCTOR
        pass

    def validate_alignment(self, ctx, params):
        """
        :param params: instance of type "ValidateAlignmentParams" (* Input
           parameters for validating a reads alignment *) -> structure:
           parameter "file_path" of String
        :returns: instance of type "ValidateAlignmentOutput" (* Results from
           validate alignment *) -> structure: parameter "validated" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN validate_alignment
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
        :param params: instance of type "UploadAlignmentParams" (* Input
           parameters for uploading a reads alignment *) -> structure:
           parameter "aligned_using" of String, parameter "aligner_version"
           of String, parameter "library_type" of String, parameter
           "read_sample_id" of String, parameter "replicate_id" of String,
           parameter "condition" of String, parameter "platform" of String,
           parameter "genome_id" of String, parameter "file_path" of String,
           parameter "ws_id_or_name" of String, parameter "name" of String
        :returns: instance of type "UploadAlignmentOutput" (*  Output report
           from uploading a reads alignment  *) -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_alignment

        self.log('Starting upload Reads Alignment, parsing parameters')
        ws_name_id, obj_name_id, file_path = self._proc_upload_alignment_params(ctx, params)

        # validate input sam/bam file

        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        uploaded_file = dfu.file_to_shock({'file_path': file_path,
                                           'make_handle': 1
                                           })

        file_handle = uploaded_file['handle']
        file_size = uploaded_file['size']

        print("\nUploaded file ===================")
        pprint(uploaded_file)
        print("====================\n")

        aligner_stats = self._get_aligner_stats(file_path)

        # the following parameters are required to be provided for
        # the workspace object validation
        #  TO DO:  need to get these from input parameters
        #  TO_DO:  how to push these into provenance

        aligner_data = {'file': file_handle,
                       'size': file_size,
                       #'aligned_using': 'update this',
                       #'aligner_version': 'update this',
                       'library_type': 'update this',
                       'condition': 'update this',
                       'read_sample_id': '2300',
                       'genome_id': '3400',
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

        print("\nSAVE OBJECTS OUTPUT ===================")
        pprint(res)
        print("====================\n")

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
        Downloads .bam and .bai files along with alignment stats *
        :param params: instance of type "DownloadAlignmentParams" ->
           structure: parameter "ws_id_or_name" of String, parameter "name"
           of String, parameter "downloadBAM" of type "boolean" (A boolean -
           0 for false, 1 for true. @range (0, 1)), parameter "downloadSAM"
           of type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "downloadBAI" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1))
        :returns: instance of type "DownloadAlignmentOutput" (*  The output
           of the download method.  *) -> structure: parameter "ws_id" of
           String, parameter "bam_file" of String, parameter "bai_file" of
           String, parameter "stats" of type "AlignmentStats" (* @optional
           singletons multiple_alignments, properly_paired, alignment_rate,
           unmapped_reads, mapped_sections total_reads, mapped_reads *) ->
           structure: parameter "properly_paired" of Long, parameter
           "multiple_alignments" of Long, parameter "singletons" of Long,
           parameter "alignment_rate" of Double, parameter "unmapped_reads"
           of Long, parameter "mapped_reads" of Long, parameter "total_reads"
           of Long
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

        # call get_object_info_new ??

        try:
            alignment = dfu.get_objects({'object_refs': [obj_ref]})['data']
        except DFUError as e:
            self.log('Logging stacktrace from workspace exception:\n' + e.data)
            raise

        print("Alignment ===============")
        pprint(alignment)
        print("=================")

        downloaded_file = alignment[0]['data']['file']['file_name']
        print(downloaded_file)

        file_name, file_ext = os.path.splitext(downloaded_file)
        bam_file = ''

        if file_ext.lower() == '.sam':
            sam_file = downloaded_file
            bam_file = file_name + '.bam'
            self.samtools.convert_sam_to_sorted_bam(sam_file, self.scratch,
                                                        bam_file)

        elif file_ext.lower() == '.bam':
            bam_file = downloaded_file

        else:
            raise ValueError("File not of type .sam or .bam")

        bai_file = file_name + '.bai'
        self.samtools.create_bai_from_bam(bam_file, self.scratch, bai_file)

        returnVal = {'ws_id':ws_name_id,
                     'bam_file': bam_file,
                     'bai_file': bai_file
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
