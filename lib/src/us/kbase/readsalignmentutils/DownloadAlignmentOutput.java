
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
    "destination_dir",
    "stats"
})
public class DownloadAlignmentOutput {

    @JsonProperty("ws_id")
    private String wsId;
    @JsonProperty("destination_dir")
    private String destinationDir;
    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * 
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

    @JsonProperty("destination_dir")
    public String getDestinationDir() {
        return destinationDir;
    }

    @JsonProperty("destination_dir")
    public void setDestinationDir(String destinationDir) {
        this.destinationDir = destinationDir;
    }

    public DownloadAlignmentOutput withDestinationDir(String destinationDir) {
        this.destinationDir = destinationDir;
        return this;
    }

    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * 
     * 
     */
    @JsonProperty("stats")
    public AlignmentStats getStats() {
        return stats;
    }

    /**
     * <p>Original spec-file type: AlignmentStats</p>
     * 
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
        return ((((((((("DownloadAlignmentOutput"+" [wsId=")+ wsId)+", destinationDir=")+ destinationDir)+", stats=")+ stats)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
