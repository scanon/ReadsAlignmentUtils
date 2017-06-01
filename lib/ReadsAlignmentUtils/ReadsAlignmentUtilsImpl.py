# -*- coding: utf-8 -*-
#BEGIN_HEADER
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
    GIT_COMMIT_HASH = "7daeb26ba8f92cb0a79d2e7e7c6d8240a43a60d2"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
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
