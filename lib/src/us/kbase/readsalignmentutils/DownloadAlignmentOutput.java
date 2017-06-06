
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
 * <p>Original spec-file type: DownloadAlignmentOutput</p>
 * <pre>
 * *  The output of the download method.  *
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_id",
    "bam_file",
    "sam_file",
    "bai_file",
    "stats"
})
public class DownloadAlignmentOutput {

    @JsonProperty("ws_id")
    private String wsId;
    @JsonProperty("bam_file")
    private String bamFile;
    @JsonProperty("sam_file")
    private String samFile;
    @JsonProperty("bai_file")
    private String baiFile;
    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * <pre>
     * * @optional singletons multiple_alignments, properly_paired,
     * alignment_rate, unmapped_reads, mapped_sections total_reads,
     * mapped_reads
     *     *
     * </pre>
     * 
     */
    @JsonProperty("stats")
    private AlignmentStats stats;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ws_id")
    public String getWsId() {
        return wsId;
    }

    @JsonProperty("ws_id")
    public void setWsId(String wsId) {
        this.wsId = wsId;
    }

    public DownloadAlignmentOutput withWsId(String wsId) {
        this.wsId = wsId;
        return this;
    }

    @JsonProperty("bam_file")
    public String getBamFile() {
        return bamFile;
    }

    @JsonProperty("bam_file")
    public void setBamFile(String bamFile) {
        this.bamFile = bamFile;
    }

    public DownloadAlignmentOutput withBamFile(String bamFile) {
        this.bamFile = bamFile;
        return this;
    }

    @JsonProperty("sam_file")
    public String getSamFile() {
        return samFile;
    }

    @JsonProperty("sam_file")
    public void setSamFile(String samFile) {
        this.samFile = samFile;
    }

    public DownloadAlignmentOutput withSamFile(String samFile) {
        this.samFile = samFile;
        return this;
    }

    @JsonProperty("bai_file")
    public String getBaiFile() {
        return baiFile;
    }

    @JsonProperty("bai_file")
    public void setBaiFile(String baiFile) {
        this.baiFile = baiFile;
    }

    public DownloadAlignmentOutput withBaiFile(String baiFile) {
        this.baiFile = baiFile;
        return this;
    }

    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * <pre>
     * * @optional singletons multiple_alignments, properly_paired,
     * alignment_rate, unmapped_reads, mapped_sections total_reads,
     * mapped_reads
     *     *
     * </pre>
     * 
     */
    @JsonProperty("stats")
    public AlignmentStats getStats() {
        return stats;
    }

    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * <pre>
     * * @optional singletons multiple_alignments, properly_paired,
     * alignment_rate, unmapped_reads, mapped_sections total_reads,
     * mapped_reads
     *     *
     * </pre>
     * 
     */
    @JsonProperty("stats")
    public void setStats(AlignmentStats stats) {
        this.stats = stats;
    }

    public DownloadAlignmentOutput withStats(AlignmentStats stats) {
        this.stats = stats;
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
        return ((((((((((((("DownloadAlignmentOutput"+" [wsId=")+ wsId)+", bamFile=")+ bamFile)+", samFile=")+ samFile)+", baiFile=")+ baiFile)+", stats=")+ stats)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
