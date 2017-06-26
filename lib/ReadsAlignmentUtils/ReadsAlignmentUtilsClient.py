# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class ReadsAlignmentUtils(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def validate_alignment(self, params, context=None):
        """
        :param params: instance of type "ValidateAlignmentParams" (* Input
           parameters for validating a reads alignment. For validation errors
           to ignore, see
           http://broadinstitute.github.io/picard/command-line-overview.html#V
           alidateSamFile) -> structure: parameter "file_path" of String,
           parameter "ignore" of list of String
        :returns: instance of type "ValidateAlignmentOutput" (* Results from
           validate alignment *) -> structure: parameter "validated" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        """
        return self._client.call_method(
            'ReadsAlignmentUtils.validate_alignment',
            [params], self._service_ver, context)

    def upload_alignment(self, params, context=None):
        """
        Validates and uploads the reads alignment  *
        :param params: instance of type "UploadAlignmentParams" (* Required
           input parameters for uploading a reads alignment string
           destination_ref -  object reference of alignment destination. The
           object ref is 'ws_name_or_id/obj_name_or_id' where ws_name_or_id
           is the workspace name or id and obj_name_or_id is the object name
           or id file_path              -  File with the path of the sam or
           bam file to be uploaded. If a sam file is provided, it will be
           converted to the sorted bam format before being saved
           read_library_ref       -  workspace object ref of the read sample
           used to make the alignment file condition              -
           assembly_or_genome_ref -  workspace object ref of genome assembly
           or genome object that was used to build the alignment *) ->
           structure: parameter "destination_ref" of String, parameter
           "file_path" of String, parameter "read_library_ref" of String,
           parameter "condition" of String, parameter
           "assembly_or_genome_ref" of String, parameter "aligned_using" of
           String, parameter "aligner_version" of String, parameter
           "aligner_opts" of mapping from String to String, parameter
           "replicate_id" of String, parameter "platform" of String,
           parameter "bowtie2_index" of type "ws_bowtieIndex_id", parameter
           "sampleset_ref" of type "ws_Sampleset_ref", parameter
           "mapped_sample_id" of mapping from String to mapping from String
           to String, parameter "validate" of type "boolean" (A boolean - 0
           for false, 1 for true. @range (0, 1)), parameter "ignore" of list
           of String
        :returns: instance of type "UploadAlignmentOutput" (*  Output from
           uploading a reads alignment  *) -> structure: parameter "obj_ref"
           of String
        """
        return self._client.call_method(
            'ReadsAlignmentUtils.upload_alignment',
            [params], self._service_ver, context)

    def download_alignment(self, params, context=None):
        """
        Downloads alignment files in .bam, .sam and .bai formats. Also downloads alignment stats *
        :param params: instance of type "DownloadAlignmentParams" (* Required
           input parameters for downloading a reads alignment string
           source_ref -  object reference of alignment source. The object ref
           is 'ws_name_or_id/obj_name_or_id' where ws_name_or_id is the
           workspace name or id and obj_name_or_id is the object name or id
           *) -> structure: parameter "source_ref" of String, parameter
           "downloadSAM" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "downloadBAI" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "validate" of type "boolean" (A boolean - 0 for false, 1 for true.
           @range (0, 1)), parameter "ignore" of list of String
        :returns: instance of type "DownloadAlignmentOutput" (*  The output
           of the download method.  *) -> structure: parameter "ws_id" of
           String, parameter "destination_dir" of String, parameter "stats"
           of type "AlignmentStats" -> structure: parameter "properly_paired"
           of Long, parameter "multiple_alignments" of Long, parameter
           "singletons" of Long, parameter "alignment_rate" of Double,
           parameter "unmapped_reads" of Long, parameter "mapped_reads" of
           Long, parameter "total_reads" of Long
        """
        return self._client.call_method(
            'ReadsAlignmentUtils.download_alignment',
            [params], self._service_ver, context)

    def export_alignment(self, params, context=None):
        """
        Wrapper function for use by in-narrative downloaders to download alignments from shock *
        :param params: instance of type "ExportParams" (* Required input
           parameters for exporting a reads alignment string source_ref - 
           object reference of alignment source. The object ref is
           'ws_name_or_id/obj_name_or_id' where ws_name_or_id is the
           workspace name or id and obj_name_or_id is the object name or id
           *) -> structure: parameter "source_ref" of String, parameter
           "exportSAM" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "exportBAI" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "validate" of type "boolean" (A boolean - 0 for false, 1 for true.
           @range (0, 1)), parameter "ignore" of list of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        return self._client.call_method(
            'ReadsAlignmentUtils.export_alignment',
            [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('ReadsAlignmentUtils.status',
                                        [], self._service_ver, context)
