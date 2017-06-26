
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
 * <p>Original spec-file type: ExportParams</p>
 * <pre>
 * *
 * Required input parameters for exporting a reads alignment
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
    "exportSAM",
    "exportBAI",
    "validate",
    "ignore"
})
public class ExportParams {

    @JsonProperty("source_ref")
    private java.lang.String sourceRef;
    @JsonProperty("exportSAM")
    private Long exportSAM;
    @JsonProperty("exportBAI")
    private Long exportBAI;
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

    public ExportParams withSourceRef(java.lang.String sourceRef) {
        this.sourceRef = sourceRef;
        return this;
    }

    @JsonProperty("exportSAM")
    public Long getExportSAM() {
        return exportSAM;
    }

    @JsonProperty("exportSAM")
    public void setExportSAM(Long exportSAM) {
        this.exportSAM = exportSAM;
    }

    public ExportParams withExportSAM(Long exportSAM) {
        this.exportSAM = exportSAM;
        return this;
    }

    @JsonProperty("exportBAI")
    public Long getExportBAI() {
        return exportBAI;
    }

    @JsonProperty("exportBAI")
    public void setExportBAI(Long exportBAI) {
        this.exportBAI = exportBAI;
    }

    public ExportParams withExportBAI(Long exportBAI) {
        this.exportBAI = exportBAI;
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

    public ExportParams withValidate(Long validate) {
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

    public ExportParams withIgnore(List<String> ignore) {
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
        return ((((((((((((("ExportParams"+" [sourceRef=")+ sourceRef)+", exportSAM=")+ exportSAM)+", exportBAI=")+ exportBAI)+", validate=")+ validate)+", ignore=")+ ignore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
