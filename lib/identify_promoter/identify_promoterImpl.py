# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
from Bio import SeqIO
from pprint import pprint, pformat
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from KBaseReport.KBaseReportClient import KBaseReport
from DataFileUtil.DataFileUtilClient import DataFileUtil
import subprocess
import os
import re
from pprint import pprint, pformat
from datetime import datetime
import uuid
import identify_promoter.Utils.GibbsUtil as GU
import identify_promoter.Utils.HomerUtil as HU
import subprocess
from biokbase.workspace.client import Workspace
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from pyseqlogo.pyseqlogo import draw_logo, setup_axis

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
    GIT_COMMIT_HASH = "1f94c5754e7279926790c8c95efcb9c1cc3a8c47"

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


    def find_motifs(self, ctx, params):
        """
        :param params: instance of type "get_promoter_for_gene_input" (Genome
           is a KBase genome Featureset is a KBase featureset Promoter_length
           is the length of promoter requested for all genes) -> structure:
           parameter "workspace_name" of String, parameter "genome_ref" of
           String, parameter "featureSet_ref" of String, parameter
           "promoter_length" of Long
        :returns: instance of type "get_promoter_for_gene_output_params" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN find_motifs

        #TODO: have these guys return output paths
        promoterFastaFilePath = self.get_promoter_for_gene(ctx,params)[0]
        gibbsCommand = GU.build_gibbs_command(promoterFastaFilePath)
        GU.run_gibbs_command(gibbsCommand)
        homerMotifCommand = HU.build_homer_motif_command(promoterFastaFilePath)
        homerLocationCommand = HU.build_homer_location_command(promoterFastaFilePath)
        os.mkdir(self.shared_folder+'/homer_out')
        HU.run_homer_command(homerMotifCommand)
        HU.run_homer_command(homerLocationCommand)
        GU.parse_gibbs_output()
        HU.parse_homer_output()
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        timestamp = str(timestamp)
        htmlDir = self.shared_folder + '/html' +  timestamp
        os.mkdir(htmlDir)
        subprocess.call(['python3','/kb/module/lib/identify_promoter/Utils/makeReport.py',self.shared_folder + '/gibbs.json',htmlDir + '/gibbs.html'])
        subprocess.call(['python3','/kb/module/lib/identify_promoter/Utils/makeReport.py',self.shared_folder + '/homer_out/homer.json',htmlDir + '/homer.html'])


        #What needs to happen here:
        #call makeLogo for each of the json outputs(capture these from somewhere)
        dfu = DataFileUtil(self.callback_url)
        parsed = ['gibbs.html','homer.html']
        indexHtmlStr = '<html>'
        #use js to load the page content
        for p in parsed:
            indexHtmlStr += '<head><script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script> <script> $(function(){$("#' + p.replace('.html','_content')  + '").load("' + p + '"); });</script> '
        indexHtmlStr += """<style>
            body {font-family: Arial;}

            /* Style the tab */
            .tab {
            overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    display: none;
    padding: 6px 12px;
    border: 1px solid #ccc;
    border-top: none;
}
</style></head> """
        indexHtmlStr += '<body>'
        #adding tabs
        indexHtmlStr += '<div class="tab">\n'
        for p in parsed:
            indexHtmlStr += '<button class="tablinks" onclick="openReport(event, \'' +p.replace('.html','_content') +'\')">' + p.replace('.html','') + '</button>'
        indexHtmlStr += '</div>'
        for p in parsed:
            indexHtmlStr += '<div id="' + p.replace('.html','_content') +'" class="tabcontent"></div>'
        indexHtmlStr += """<script>
function openReport(evt, reportName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(reportName).style.display = "block";
    evt.currentTarget.className += " active";
}
</script>"""

        #for p in parsed:
        #    indexHtmlStr += '<a href="' + p + '">' + p.replace('.html','') +' Output</a>\n'
        #indexHtmlStr += '</body></html>'
        with open(htmlDir+  '/index.html','w') as html_handle:
            html_handle.write(str(indexHtmlStr))

        #plt.rcParams['figure.dpi'] = 300


        #htmlFiles = ['index.html','gibbs.html','homer.html']
        #shockParamsList = []
        #for f in htmlFiles:
        #    shockParamsList.append({'file_path': htmlDir + f ,'make_handle': 0, 'pack': 'zip'})

        try:
            html_upload_ret = dfu.file_to_shock({'file_path': htmlDir ,'make_handle': 0, 'pack': 'zip'})
        except:
            raise ValueError ('error uploading HTML file to shock')

        reportName = 'identify_promoter_report_'+str(uuid.uuid4())

        reportObj = {'objects_created': [],
                     'message': '',
                     'direct_html': None,
                     'direct_html_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'html_window_height': 220,
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # attach to report obj
        #reportObj['direct_html'] = None
        reportObj['direct_html'] = ''
        reportObj['direct_html_link_index'] = 0
        reportObj['html_links'] = [{'shock_id': html_upload_ret['shock_id'],
                                    #'name': 'promoter_download.zip',
                                    'name': 'index.html',
                                    'label': 'Save promoter_download.zip'
                                    }
                                   ]


        report = KBaseReport(self.callback_url, token=ctx['token'])
        #report_info = report.create({'report':reportObj, 'workspace_name':input_params['input_ws']})
        report_info = report.create_extended_report(reportObj)
        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }


        #END find_motifs

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method find_motifs return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def get_promoter_for_gene(self, ctx, params):
        """
        :param params: instance of type "get_promoter_for_gene_input" (Genome
           is a KBase genome Featureset is a KBase featureset Promoter_length
           is the length of promoter requested for all genes) -> structure:
           parameter "workspace_name" of String, parameter "genome_ref" of
           String, parameter "featureSet_ref" of String, parameter
           "promoter_length" of Long
        :returns: instance of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN get_promoter_for_gene
        #code goes here
        dfu = DataFileUtil(self.callback_url)
        #objectRefs = {'object_refs':[params['genome_ref'],params['featureSet_ref']]}
        objectRefs = {'object_refs':[params['featureSet_ref']]}
        ws = Workspace('https://appdev.kbase.us/services/ws')
        ws_name = params['workspace_name']
        subset = ws.get_object_subset([{
                                     'included':['/features/[*]/location', '/features/[*]/id','/assembly_ref'],
'ref':params['genome_ref']}])
        features = subset[0]['data']['features']
        aref = subset[0]['data']['assembly_ref']
        objects = dfu.get_objects(objectRefs)
        #genome = objects['data'][0]['data']
        #featureSet = objects['data'][1]['data']
        featureSet = objects['data'][0]['data']
        assembly_ref = {'ref': aref}
        #print assembly_ref
        #with open(self.shared_folder + '/genome.json','w') as f:
        #    json.dump(genome,f)
        #with open(self.shared_folder + '/featureSet.json','w') as f:
        #    json.dump(featureSet,f)
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
        prom= ""
        featureFound = False
        for feature in featureSet['elements']:
            #print(feature)
            #print(featureSet['elements'][feature])
            featureFound = False
            for f in features:
                #print f['id']
                #print feature
                if f['id'] == feature:
                    attributes = f['location'][0]
                    featureFound = True
                    #print('found match ' + feature)
                    #print(f['location'])
                    break
            if featureFound:
                for record in SeqIO.parse(fasta_file['path'], 'fasta'):
                #for record in SeqIO.parse('/kb/module/work/Gmax_189_genome_assembly.fa', 'fasta'):
                #print(record.id)
                #print(attributes[0])
                    if record.id == attributes[0]:
                        #print('adding to prom string')
                    #print(attributes[0])
                        if attributes[2] == '+':
                            #print('1')
                        #might need to offset by 1?
                            end = attributes[1]
                            start = end - params['promoter_length']
                            if end < 0:
                                end = 0
                            promoter = record.seq[start:end].upper()
                            prom += ">" + feature + "\n"
                            prom += promoter + "\n"


                        elif attributes[2] == '-':
                            #print('2')
                            start = attributes[1]
                            end = start + params['promoter_length']
                            if end > len(record.seq) - 1:
                                end = len(record.seq) - 1
                            promoter = record.seq[start:end].upper()
                            complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
                            promoter = ''.join([complement[base] for base in promoter[::-1]])
                            prom += ">" + feature + "\n"
                            prom += promoter + "\n"


                        else:
                            print('Error on orientation')
            else:
                print('Could not find feature ' + feature + 'in genome')
        promOutputPath = '/kb/module/work/tmp/promFile.fa'
        #print('prom string\n' + str(prom))
        with open(promOutputPath,'w') as promFile:
            promFile.write(str(prom))


        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        html_output_dir = os.path.join(self.shared_folder,'output_html.'+str(timestamp))
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)
        html_file = 'promoter.html'
        output_html_file_path = os.path.join(html_output_dir, html_file);


        html_report_lines = '<html><body>'
        html_report_lines += '<pre>' + prom + '</pre>'
        html_report_lines += '</body></html>'

        with open (output_html_file_path, 'w', 0) as html_handle:
            html_handle.write(str(html_report_lines))

        try:
            html_upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
            #html_upload_ret = dfu.file_to_shock({'file_path': output_html_file_path,
                                                 #'make_handle': 0})
                                                 'make_handle': 0,
                                                 'pack': 'zip'})
        except:
            raise ValueError ('error uploading HTML file to shock')

        reportName = 'identify_promoter_report_'+str(uuid.uuid4())

        reportObj = {'objects_created': [],
                     'message': '',
                     'direct_html': None,
                     'direct_html_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'html_window_height': 220,
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # attach to report obj
        #reportObj['direct_html'] = None
        reportObj['direct_html'] = ''
        reportObj['direct_html_link_index'] = 0
        reportObj['html_links'] = [{'shock_id': html_upload_ret['shock_id'],
                                    'name': html_file,
                                    'label': 'View'
                                    }
                                   ]

        report = KBaseReport(self.callback_url, token=ctx['token'])
        #report_info = report.create({'report':reportObj, 'workspace_name':input_params['input_ws']})
        report_info = report.create_extended_report(reportObj)
        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        #changing output to be path string
        #TODO: get rid of this html maybe and move into find_motifs
        output = promOutputPath

        #iterate over records in fasta
        #for record in SeqIO.parse(fasta_file['path'], 'fasta'):


        #objects list of Genome and featureSet

        #pprint(objects)
        #END get_promoter_for_gene

        # At some point might do deeper type checking...
        if not isinstance(output, basestring):
            raise ValueError('Method get_promoter_for_gene return value ' +
                             'output is not type basestring as required.')
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
