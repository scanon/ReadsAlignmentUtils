
package us.kbase.readsalignmentutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: AlignmentStats</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "properly_paired",
    "multiple_alignments",
    "singletons",
    "alignment_rate",
    "unmapped_reads",
    "mapped_reads",
    "total_reads"
})
public class AlignmentStats {

    @JsonProperty("properly_paired")
    private Long properlyPaired;
    @JsonProperty("multiple_alignments")
    private Long multipleAlignments;
    @JsonProperty("singletons")
    private Long singletons;
    @JsonProperty("alignment_rate")
    private Double alignmentRate;
    @JsonProperty("unmapped_reads")
    private Long unmappedReads;
    @JsonProperty("mapped_reads")
    private Long mappedReads;
    @JsonProperty("total_reads")
    private Long totalReads;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("properly_paired")
    public Long getProperlyPaired() {
        return properlyPaired;
    }

    @JsonProperty("properly_paired")
    public void setProperlyPaired(Long properlyPaired) {
        this.properlyPaired = properlyPaired;
    }

    public AlignmentStats withProperlyPaired(Long properlyPaired) {
        this.properlyPaired = properlyPaired;
        return this;
    }

    @JsonProperty("multiple_alignments")
    public Long getMultipleAlignments() {
        return multipleAlignments;
    }

    @JsonProperty("multiple_alignments")
    public void setMultipleAlignments(Long multipleAlignments) {
        this.multipleAlignments = multipleAlignments;
    }

    public AlignmentStats withMultipleAlignments(Long multipleAlignments) {
        this.multipleAlignments = multipleAlignments;
        return this;
    }

    @JsonProperty("singletons")
    public Long getSingletons() {
        return singletons;
    }

    @JsonProperty("singletons")
    public void setSingletons(Long singletons) {
        this.singletons = singletons;
    }

    public AlignmentStats withSingletons(Long singletons) {
        this.singletons = singletons;
        return this;
    }

    @JsonProperty("alignment_rate")
    public Double getAlignmentRate() {
        return alignmentRate;
    }

    @JsonProperty("alignment_rate")
    public void setAlignmentRate(Double alignmentRate) {
        this.alignmentRate = alignmentRate;
    }

    public AlignmentStats withAlignmentRate(Double alignmentRate) {
        this.alignmentRate = alignmentRate;
        return this;
    }

    @JsonProperty("unmapped_reads")
    public Long getUnmappedReads() {
        return unmappedReads;
    }

    @JsonProperty("unmapped_reads")
    public void setUnmappedReads(Long unmappedReads) {
        this.unmappedReads = unmappedReads;
    }

    public AlignmentStats withUnmappedReads(Long unmappedReads) {
        this.unmappedReads = unmappedReads;
        return this;
    }

    @JsonProperty("mapped_reads")
    public Long getMappedReads() {
        return mappedReads;
    }

    @JsonProperty("mapped_reads")
    public void setMappedReads(Long mappedReads) {
        this.mappedReads = mappedReads;
    }

    public AlignmentStats withMappedReads(Long mappedReads) {
        this.mappedReads = mappedReads;
        return this;
    }

    @JsonProperty("total_reads")
    public Long getTotalReads() {
        return totalReads;
    }

    @JsonProperty("total_reads")
    public void setTotalReads(Long totalReads) {
        this.totalReads = totalReads;
    }

    public AlignmentStats withTotalReads(Long totalReads) {
        this.totalReads = totalReads;
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
        return ((((((((((((((((("AlignmentStats"+" [properlyPaired=")+ properlyPaired)+", multipleAlignments=")+ multipleAlignments)+", singletons=")+ singletons)+", alignmentRate=")+ alignmentRate)+", unmappedReads=")+ unmappedReads)+", mappedReads=")+ mappedReads)+", totalReads=")+ totalReads)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
