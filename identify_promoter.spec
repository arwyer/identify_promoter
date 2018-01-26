/*
This module has methods for promoter discovery.
get_promoter_for_gene retrieves promoter sequence for a gene

*/

module identify_promoter {

/*
 Genome is a KBase genome
 Featureset is a KBase featureset
 Promoter_length is the length of promoter requested for all genes
*/


typedef structure {
    string Genome;
    string featureSet;
    int promoter_length;
} get_promoter_for_gene_input;

typedef structure {
 string report_name;
 string report_ref;
} get_promoter_for_gene_output_params;


funcdef get_promoter_for_gene(get_promoter_for_gene_input params)
      returns (get_promoter_for_gene_output_params output)
      authentication required;



};

