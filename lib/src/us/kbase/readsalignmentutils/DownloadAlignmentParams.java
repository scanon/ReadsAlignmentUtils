
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
 * <p>Original spec-file type: DownloadAlignmentParams</p>
 * <pre>
 * *
 * Required input parameters for downloading a reads alignment
 * string source_ref -  object reference of alignment source. The
 *                      object ref is 'ws_name_or_id/obj_name_or_id'
 *                      where ws_name_or_id is the workspace name or id
 *                      and obj_name_or_id is the object name or id
 *     *
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "source_ref",
    "downloadSAM",
    "downloadBAI",
    "validate",
    "ignore"
})
public class DownloadAlignmentParams {

    @JsonProperty("source_ref")
    private java.lang.String sourceRef;
    @JsonProperty("downloadSAM")
    private Long downloadSAM;
    @JsonProperty("downloadBAI")
    private Long downloadBAI;
    @JsonProperty("validate")
    private Long validate;
    @JsonProperty("ignore")
    private List<String> ignore;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("source_ref")
    public java.lang.String getSourceRef() {
        return sourceRef;
    }

    @JsonProperty("source_ref")
    public void setSourceRef(java.lang.String sourceRef) {
        this.sourceRef = sourceRef;
    }

    public DownloadAlignmentParams withSourceRef(java.lang.String sourceRef) {
        this.sourceRef = sourceRef;
        return this;
    }

    @JsonProperty("downloadSAM")
    public Long getDownloadSAM() {
        return downloadSAM;
    }

    @JsonProperty("downloadSAM")
    public void setDownloadSAM(Long downloadSAM) {
        this.downloadSAM = downloadSAM;
    }

    public DownloadAlignmentParams withDownloadSAM(Long downloadSAM) {
        this.downloadSAM = downloadSAM;
        return this;
    }

    @JsonProperty("downloadBAI")
    public Long getDownloadBAI() {
        return downloadBAI;
    }

    @JsonProperty("downloadBAI")
    public void setDownloadBAI(Long downloadBAI) {
        this.downloadBAI = downloadBAI;
    }

    public DownloadAlignmentParams withDownloadBAI(Long downloadBAI) {
        this.downloadBAI = downloadBAI;
        return this;
    }

    @JsonProperty("validate")
    public Long getValidate() {
        return validate;
    }

    @JsonProperty("validate")
    public void setValidate(Long validate) {
        this.validate = validate;
    }

    public DownloadAlignmentParams withValidate(Long validate) {
        this.validate = validate;
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

    public DownloadAlignmentParams withIgnore(List<String> ignore) {
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
        return ((((((((((((("DownloadAlignmentParams"+" [sourceRef=")+ sourceRef)+", downloadSAM=")+ downloadSAM)+", downloadBAI=")+ downloadBAI)+", validate=")+ validate)+", ignore=")+ ignore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
