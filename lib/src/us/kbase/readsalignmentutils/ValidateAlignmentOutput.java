
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
 * <p>Original spec-file type: ValidateAlignmentOutput</p>
 * <pre>
 * * Results from validate alignment *
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "validated"
})
public class ValidateAlignmentOutput {

    @JsonProperty("validated")
    private Long validated;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("validated")
    public Long getValidated() {
        return validated;
    }

    @JsonProperty("validated")
    public void setValidated(Long validated) {
        this.validated = validated;
    }

    public ValidateAlignmentOutput withValidated(Long validated) {
        this.validated = validated;
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
        return ((((("ValidateAlignmentOutput"+" [validated=")+ validated)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
