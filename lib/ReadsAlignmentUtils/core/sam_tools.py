from script_utils import log as log
from script_utils import whereis
from subprocess import Popen, PIPE
import os
import logging


class SamTools:
    """
    This class wraps functions from samtools. 
    
    The functions in this class pivot around the bam format. i.e if the user has
    a sam file, it is expected that the user will first convert the file to 
    a bam format before performing any other operation from this class on the file.
    """

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        pass

    def _prepare_paths(self, ifile, ipath, ofile, opath, iext, oext):
        '''
        setup input and output file paths and extensions 
        '''
        if ipath is None: ipath = ''
        if opath is None: opath = ipath
        if ofile is None:
            if ifile[-4:] == iext:
                ofile = ifile[:-4]+oext
            else:
                ofile = ifile + oext
        ifile = os.path.join(ipath, ifile)
        ofile = os.path.join(opath, ofile)

        return ifile, ofile

    def _check_prog(self):
        '''
        Check if samtools is present in the env 
        '''
        progPath = whereis('samtools')
        if not progPath:
            raise RuntimeError(None, '{0} command not found in your PATH '
                                     'environmental variable. {1}'.format(
                'samtools', os.environ.get('PATH', '')))


    def convert_sam_to_sorted_bam(self, ifile,ipath=None, ofile=None, opath=None):
        """
        Converts the specified sam file to a sorted bam file.
        
        throws exceptions if input file is missing, invalid or if the output file could 
        not be written to disk
    
        :param ifile: sam file name
        :param ipath: path to sam file. If None, ipath is set to current path
        :param ofile: sorted bam file name. If None, ifile name is used with the
        extension '.sam' (if any) replaced with '.bam'
        :param opath: path to sorted bam file. If None, ipath will be used
    
        :returns 0 if successful, else 1            
        """
        # prepare input and output file paths
        ifile, ofile = self._prepare_paths(ifile, ipath, ofile, opath, '.sam', '.bam')


        # check if input file exists
        if not os.path.exists(ifile):
            raise RuntimeError(None, 'Input sam file does not exist: '+str(ifile))

        # validate input sam file TODO

        # convert
        self._check_prog()

        # samtools view -bS ifile | samtools sort -l 9 -O BAM > ofile
        try:
            sort = Popen('samtools sort -l 9 -O BAM > {0}'.format(ofile), shell=True, stdin=PIPE, stdout=PIPE)
            view = Popen('samtools view -bS {0}'.format(ifile), shell=True, stdout=sort.stdin)
            result, stderr = sort.communicate()  # samtools always returns success
            view.wait()
        except:
            raise RuntimeError(None, 'failed to convert {0} to {1}'.format(ifile, ofile))

        return 0


    def convert_bam_to_sam(self, ifile, ipath=None, ofile=None, opath=None):
        """
        Converts the specified bam file to a sam file.

        throws exceptions if input file is missing, invalid or if the output file could 
        not be written to disk

        :param ifile: bam file name
        :param ipath: path to bam file. If None, ipath is set to current path
        :param ofile: sam file name. If None, ifile name is used with the
        extension '.bam' (if any) replaced with '.sam'
        :param opath: path to sam file. If None, ipath will be used

        :returns 0 if successful, else 1            
        """
        # prepare input and output file paths
        ifile, ofile = self._prepare_paths(ifile, ipath, ofile, opath, '.sam', '.bam')


        # check if input file exists
        if not os.path.exists(ifile):
            raise RuntimeError(None, 'Input bam file does not exist: '+str(ifile))

        # validate input sam file TODO

        # convert
        self._check_prog()

        # samtools view -h ifile > ofile
        try:
            convert = Popen('samtools view -h {0} > {1}'.format(ifile, ofile), shell=True, stdin=PIPE, stdout=PIPE)
        except:
            raise RuntimeError(None, 'failed to convert {0} to {1}'.format(ifile, ofile))

        return 0


    def create_bai_from_bam(self, ifile, ipath=None, ofile=None, opath=None):
        """
        creates a bai file from a bam file

        throws exceptions if input file is missing, invalid or if the output file could 
        not be written to disk

        :param ifile: bam file name
        :param ipath: path to bam file. If None, ipath is set to current path
        :param ofile: bai file name. If None, ifile name is used with the
        extension '.bam' (if any) replaced with '.bai'
        :param opath: path to bai file. If None, ipath will be used

        :returns 0 if successful, else 1            
        """
        # prepare input and output file paths
        ifile, ofile = self._prepare_paths(ifile, ipath, ofile, opath, '.bam',
                                           '.bai')

        # check if input file exists
        if not os.path.exists(ifile):
            raise RuntimeError(None,
                               'Input bam file does not exist: ' + str(ifile))

        # validate input sam file TODO

        # convert
        self._check_prog()

        #  samtools index ifile ofile
        try:
            create = Popen('samtools index {0} {1}'.format(ifile, ofile),
                            shell=True, stdin=PIPE, stdout=PIPE)
        except:
            raise RuntimeError(None,
                               'failed to convert {0} to {1}'.format(ifile,
                                                                     ofile))

        return 0




    '''
    Generate simple statistics from a BAM file. This tool calculates statistics 
    from a BAM file. The statistics collected include counts of aligned and unaligned 
    reads as well as all records with no start coordinate. The input to the tool 
    is the BAM file name but it must be accompanied by a corresponding index file.
    '''
    def get_stats(self):
        # samtools flagstat work/accepted_hits_sorted.bam
        pass
