
package us.kbase.identifypromoter;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: get_promoter_for_gene_input</p>
 * <pre>
 * Genome is a KBase genome
 * Featureset is a KBase featureset
 * Promoter_length is the length of promoter requested for all genes
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "genome_ref",
    "featureSet_ref",
    "promoter_length"
})
public class GetPromoterForGeneInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("genome_ref")
    private String genomeRef;
    @JsonProperty("featureSet_ref")
    private String featureSetRef;
    @JsonProperty("promoter_length")
    private Long promoterLength;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public GetPromoterForGeneInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("genome_ref")
    public String getGenomeRef() {
        return genomeRef;
    }

    @JsonProperty("genome_ref")
    public void setGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
    }

    public GetPromoterForGeneInput withGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
        return this;
    }

    @JsonProperty("featureSet_ref")
    public String getFeatureSetRef() {
        return featureSetRef;
    }

    @JsonProperty("featureSet_ref")
    public void setFeatureSetRef(String featureSetRef) {
        this.featureSetRef = featureSetRef;
    }

    public GetPromoterForGeneInput withFeatureSetRef(String featureSetRef) {
        this.featureSetRef = featureSetRef;
        return this;
    }

    @JsonProperty("promoter_length")
    public Long getPromoterLength() {
        return promoterLength;
    }

    @JsonProperty("promoter_length")
    public void setPromoterLength(Long promoterLength) {
        this.promoterLength = promoterLength;
    }

    public GetPromoterForGeneInput withPromoterLength(Long promoterLength) {
        this.promoterLength = promoterLength;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("GetPromoterForGeneInput"+" [workspaceName=")+ workspaceName)+", genomeRef=")+ genomeRef)+", featureSetRef=")+ featureSetRef)+", promoterLength=")+ promoterLength)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
