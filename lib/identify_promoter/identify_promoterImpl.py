# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
from Bio import SeqIO
from pprint import pprint, pformat
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from KBaseReport.KBaseReportClient import KBaseReport
from DataFileUtil.DataFileUtilClient import DataFileUtil
#END_HEADER


class identify_promoter:
    '''
    Module Name:
    identify_promoter

    Module Description:
    This module has methods for promoter discovery.
get_promoter_for_gene retrieves promoter sequence for a gene
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/arwyer/identify_promoter.git"
    GIT_COMMIT_HASH = "421f8f35d1f7e225b22dded28f8005fbcb0afd8a"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        #END_CONSTRUCTOR
        pass


    def get_promoter_for_gene(self, ctx, params):
        """
        :param params: instance of type "get_promoter_for_gene_input" (Genome
           is a KBase genome Featureset is a KBase featureset Promoter_length
           is the length of promoter requested for all genes) -> structure:
           parameter "genome_ref" of String, parameter "featureSet_ref" of
           String, parameter "promoter_length" of Long
        :returns: instance of type "get_promoter_for_gene_output_params" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN get_promoter_for_gene
        #code goes here
        dfu = DataFileUtil(self.callback_url)
        objectRefs = {'object_refs':[params['Genome'],params['featureSet']]}
        objects = dfu.get_objects(objectRefs)
        genome = objects['data'][0]['data']
        featureSet = objects['data'][1]['data']
        assembly_ref = {'object_refs':[genome['assembly_ref']]}
        assembly = dfu.get_objects(assembly_ref)['data'][0]['data']
        with open('/kb/module/work/genome.json','w') as f:
            json.dump(genome,f)
        with open('/kb/module/work/featureSet.json','w') as f:
            json.dump(featureSet,f)
        with open('/kb/module/work/asssembly.json','w') as f:
            json.dump(assembly,f)
        stfp = {'handle_id':assembly['fasta_handle_ref'],'file_path':'/kb/module/work/fasta_file'}
        stfo = dfu.shock_to_file(stfp)
        pprint(stfo)

        #objects list of Genome and featureSet

        #pprint(objects)
        #END get_promoter_for_gene

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method get_promoter_for_gene return value ' +
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
