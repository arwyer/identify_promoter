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
        assembly_ref = {'ref': genome['assembly_ref']}
        with open('/kb/module/work/genome.json','w') as f:
            json.dump(genome,f)
        with open('/kb/module/work/featureSet.json','w') as f:
            json.dump(featureSet,f)
        #with open('/kb/module/work/asssembly.json','w') as f:
        #    json.dump(assembly,f)
        print('Downloading Assembly data as a Fasta file.')
        assemblyUtil = AssemblyUtil(self.callback_url)
        fasta_file = assemblyUtil.get_assembly_as_fasta(assembly_ref)
        #pprint(fasta_file)
        #loop over featureSet
        #find matching feature in genome
        #get record, start, orientation, length
        #TODO: add some error checking logic to the bounds of the promoter
        for feature in featureSet['elements']:
            #print(feature)
            #print(featureSet['elements'][feature])
            for f in genome['features']:
                if f['id'] == feature:
                    attributes = f['location'][0]
                    #print(f['location'])
                    break
            for record in SeqIO.parse(fasta_file['path'], 'fasta'):
                #print(record.id)
                #print(attributes[0])
                if record.id == attributes[0]:
                    #print(attributes[0])
                    if attributes[2] == '+':
                        #might need to offset by 1?
                        end = attributes[1]
                        start = end - params['promoter_length']
                        if end < 0:
                            end = 0
                        promoter = record.seq[start:end].upper()
                    elif attributes[2] == '-':
                        start = attributes[1]
                        end = start + params['promoter_length']
                        if end > len(record.seq) - 1:
                            end = len(record.seq) - 1
                        promoter = record.seq[start:end].upper()
                        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
                        promoter = ''.join([complement[base] for base in promoter[::-1]])
                    else:
                        print('Error on orientation')
                    print('>'+feature)
                    print(promoter)
                    break



        #iterate over records in fasta
        #for record in SeqIO.parse(fasta_file['path'], 'fasta'):


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
