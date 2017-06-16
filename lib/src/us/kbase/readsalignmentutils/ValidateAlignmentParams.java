
package us.kbase.readsalignmentutils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ValidateAlignmentParams</p>
 * <pre>
 * * Input parameters for validating a reads alignment. For validation errors to ignore,
 * see http://broadinstitute.github.io/picard/command-line-overview.html#ValidateSamFile
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "file_path",
    "ignore"
})
public class ValidateAlignmentParams {

    @JsonProperty("file_path")
    private java.lang.String filePath;
    @JsonProperty("ignore")
    private List<String> ignore;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("file_path")
    public java.lang.String getFilePath() {
        return filePath;
    }

    @JsonProperty("file_path")
    public void setFilePath(java.lang.String filePath) {
        this.filePath = filePath;
    }

    public ValidateAlignmentParams withFilePath(java.lang.String filePath) {
        this.filePath = filePath;
        return this;
    }

    @JsonProperty("ignore")
    public List<String> getIgnore() {
        return ignore;
    }

    @JsonProperty("ignore")
    public void setIgnore(List<String> ignore) {
        this.ignore = ignore;
    }

    public ValidateAlignmentParams withIgnore(List<String> ignore) {
        this.ignore = ignore;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((("ValidateAlignmentParams"+" [filePath=")+ filePath)+", ignore=")+ ignore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
