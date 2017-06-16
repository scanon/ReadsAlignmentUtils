
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
 * <p>Original spec-file type: UploadAlignmentParams</p>
 * <pre>
 * *
 * Required input parameters for uploading a reads alignment
 *   string destination_ref -  object reference of alignment destination. The
 *                             object ref is 'ws_name_or_id/obj_name_or_id'
 *                             where ws_name_or_id is the workspace name or id
 *                             and obj_name_or_id is the object name or id
 *   file_path              -  Source: file with the path of the sam or bam file to be uploaded
 *   read_library_ref       -  workspace object ref of the read sample used to make
 *                             the alignment file
 *   condition              -
 *   assembly_or_genome_ref -  workspace object ref of genome assembly or genome object that was
 *                             used to build the alignment
 *     *
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "destination_ref",
    "file_path",
    "condition",
    "assembly_or_genome_ref",
    "read_library_ref",
    "aligned_using",
    "aligner_version",
    "aligner_opts",
    "replicate_id",
    "platform",
    "bowtie2_index",
    "sampleset_ref",
    "mapped_sample_id",
    "validate",
    "ignore"
})
public class UploadAlignmentParams {

    @JsonProperty("destination_ref")
    private java.lang.String destinationRef;
    @JsonProperty("file_path")
    private java.lang.String filePath;
    @JsonProperty("condition")
    private java.lang.String condition;
    @JsonProperty("assembly_or_genome_ref")
    private java.lang.String assemblyOrGenomeRef;
    @JsonProperty("read_library_ref")
    private java.lang.String readLibraryRef;
    @JsonProperty("aligned_using")
    private java.lang.String alignedUsing;
    @JsonProperty("aligner_version")
    private java.lang.String alignerVersion;
    @JsonProperty("aligner_opts")
    private Map<String, String> alignerOpts;
    @JsonProperty("replicate_id")
    private java.lang.String replicateId;
    @JsonProperty("platform")
    private java.lang.String platform;
    @JsonProperty("bowtie2_index")
    private java.lang.String bowtie2Index;
    @JsonProperty("sampleset_ref")
    private java.lang.String samplesetRef;
    @JsonProperty("mapped_sample_id")
    private Map<String, Map<String, String>> mappedSampleId;
    @JsonProperty("validate")
    private Long validate;
    @JsonProperty("ignore")
    private List<String> ignore;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("destination_ref")
    public java.lang.String getDestinationRef() {
        return destinationRef;
    }

    @JsonProperty("destination_ref")
    public void setDestinationRef(java.lang.String destinationRef) {
        this.destinationRef = destinationRef;
    }

    public UploadAlignmentParams withDestinationRef(java.lang.String destinationRef) {
        this.destinationRef = destinationRef;
        return this;
    }

    @JsonProperty("file_path")
    public java.lang.String getFilePath() {
        return filePath;
    }

    @JsonProperty("file_path")
    public void setFilePath(java.lang.String filePath) {
        this.filePath = filePath;
    }

    public UploadAlignmentParams withFilePath(java.lang.String filePath) {
        this.filePath = filePath;
        return this;
    }

    @JsonProperty("condition")
    public java.lang.String getCondition() {
        return condition;
    }

    @JsonProperty("condition")
    public void setCondition(java.lang.String condition) {
        this.condition = condition;
    }

    public UploadAlignmentParams withCondition(java.lang.String condition) {
        this.condition = condition;
        return this;
    }

    @JsonProperty("assembly_or_genome_ref")
    public java.lang.String getAssemblyOrGenomeRef() {
        return assemblyOrGenomeRef;
    }

    @JsonProperty("assembly_or_genome_ref")
    public void setAssemblyOrGenomeRef(java.lang.String assemblyOrGenomeRef) {
        this.assemblyOrGenomeRef = assemblyOrGenomeRef;
    }

    public UploadAlignmentParams withAssemblyOrGenomeRef(java.lang.String assemblyOrGenomeRef) {
        this.assemblyOrGenomeRef = assemblyOrGenomeRef;
        return this;
    }

    @JsonProperty("read_library_ref")
    public java.lang.String getReadLibraryRef() {
        return readLibraryRef;
    }

    @JsonProperty("read_library_ref")
    public void setReadLibraryRef(java.lang.String readLibraryRef) {
        this.readLibraryRef = readLibraryRef;
    }

    public UploadAlignmentParams withReadLibraryRef(java.lang.String readLibraryRef) {
        this.readLibraryRef = readLibraryRef;
        return this;
    }

    @JsonProperty("aligned_using")
    public java.lang.String getAlignedUsing() {
        return alignedUsing;
    }

    @JsonProperty("aligned_using")
    public void setAlignedUsing(java.lang.String alignedUsing) {
        this.alignedUsing = alignedUsing;
    }

    public UploadAlignmentParams withAlignedUsing(java.lang.String alignedUsing) {
        this.alignedUsing = alignedUsing;
        return this;
    }

    @JsonProperty("aligner_version")
    public java.lang.String getAlignerVersion() {
        return alignerVersion;
    }

    @JsonProperty("aligner_version")
    public void setAlignerVersion(java.lang.String alignerVersion) {
        this.alignerVersion = alignerVersion;
    }

    public UploadAlignmentParams withAlignerVersion(java.lang.String alignerVersion) {
        this.alignerVersion = alignerVersion;
        return this;
    }

    @JsonProperty("aligner_opts")
    public Map<String, String> getAlignerOpts() {
        return alignerOpts;
    }

    @JsonProperty("aligner_opts")
    public void setAlignerOpts(Map<String, String> alignerOpts) {
        this.alignerOpts = alignerOpts;
    }

    public UploadAlignmentParams withAlignerOpts(Map<String, String> alignerOpts) {
        this.alignerOpts = alignerOpts;
        return this;
    }

    @JsonProperty("replicate_id")
    public java.lang.String getReplicateId() {
        return replicateId;
    }

    @JsonProperty("replicate_id")
    public void setReplicateId(java.lang.String replicateId) {
        this.replicateId = replicateId;
    }

    public UploadAlignmentParams withReplicateId(java.lang.String replicateId) {
        this.replicateId = replicateId;
        return this;
    }

    @JsonProperty("platform")
    public java.lang.String getPlatform() {
        return platform;
    }

    @JsonProperty("platform")
    public void setPlatform(java.lang.String platform) {
        this.platform = platform;
    }

    public UploadAlignmentParams withPlatform(java.lang.String platform) {
        this.platform = platform;
        return this;
    }

    @JsonProperty("bowtie2_index")
    public java.lang.String getBowtie2Index() {
        return bowtie2Index;
    }

    @JsonProperty("bowtie2_index")
    public void setBowtie2Index(java.lang.String bowtie2Index) {
        this.bowtie2Index = bowtie2Index;
    }

    public UploadAlignmentParams withBowtie2Index(java.lang.String bowtie2Index) {
        this.bowtie2Index = bowtie2Index;
        return this;
    }

    @JsonProperty("sampleset_ref")
    public java.lang.String getSamplesetRef() {
        return samplesetRef;
    }

    @JsonProperty("sampleset_ref")
    public void setSamplesetRef(java.lang.String samplesetRef) {
        this.samplesetRef = samplesetRef;
    }

    public UploadAlignmentParams withSamplesetRef(java.lang.String samplesetRef) {
        this.samplesetRef = samplesetRef;
        return this;
    }

    @JsonProperty("mapped_sample_id")
    public Map<String, Map<String, String>> getMappedSampleId() {
        return mappedSampleId;
    }

    @JsonProperty("mapped_sample_id")
    public void setMappedSampleId(Map<String, Map<String, String>> mappedSampleId) {
        this.mappedSampleId = mappedSampleId;
    }

    public UploadAlignmentParams withMappedSampleId(Map<String, Map<String, String>> mappedSampleId) {
        this.mappedSampleId = mappedSampleId;
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

    public UploadAlignmentParams withValidate(Long validate) {
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

    public UploadAlignmentParams withIgnore(List<String> ignore) {
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
        return ((((((((((((((((((((((((((((((((("UploadAlignmentParams"+" [destinationRef=")+ destinationRef)+", filePath=")+ filePath)+", condition=")+ condition)+", assemblyOrGenomeRef=")+ assemblyOrGenomeRef)+", readLibraryRef=")+ readLibraryRef)+", alignedUsing=")+ alignedUsing)+", alignerVersion=")+ alignerVersion)+", alignerOpts=")+ alignerOpts)+", replicateId=")+ replicateId)+", platform=")+ platform)+", bowtie2Index=")+ bowtie2Index)+", samplesetRef=")+ samplesetRef)+", mappedSampleId=")+ mappedSampleId)+", validate=")+ validate)+", ignore=")+ ignore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
