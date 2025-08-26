from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Tuple

class FilterSchema(BaseModel):
    filters: Dict[str, Tuple[str, float]]

class ReportedAgesSchema(BaseModel):
    sample: str
    gender: Optional[str] = None
    age: Optional[int] = None
    sample_date: Optional[date] = None
    menopausal_status: Optional[str] = None
    ptid: Optional[str] = None
    esti_gender: Optional[str] = None
    cfdna: Optional[float] = None
    wbc: Optional[float] = None
    colon: Optional[float] = None
    liver: Optional[float] = None
    ovary: Optional[float] = None
    pancreas: Optional[float] = None
    prostate: Optional[float] = None
    small_intestine: Optional[float] = None
    spleen: Optional[float] = None
    stomach: Optional[float] = None
    adj_ovary_menopause: Optional[float] = None
    adj_ovary_no_menopause: Optional[float] = None

    class Config:
        from_attributes = True

class FastpSchema(BaseModel):
    sample: str
    total_reads: Optional[str] = None
    total_bases: Optional[str] = None
    q20_bases: Optional[str] = None
    q30_bases: Optional[str] = None
    q20_rate: Optional[str] = None
    q30_rate: Optional[str] = None
    read1_mean_length: Optional[str] = None
    read2_mean_length: Optional[str] = None
    gc_content: Optional[str] = None
    passed_filter_reads: Optional[int] = None
    corrected_reads: Optional[int] = None
    corrected_bases: Optional[int] = None
    low_quality_reads: Optional[int] = None
    too_many_N_reads: Optional[int] = None
    too_short_reads: Optional[int] = None
    too_long_reads: Optional[int] = None
    duplication_rate: Optional[float] = None
    adapter_trimmed_reads: Optional[int] = None
    adapter_trimmed_bases: Optional[int] = None
    read1_adapter_sequence: Optional[str] = None
    read2_adapter_sequence: Optional[str] = None
    total_polyx_trimmed_reads: Optional[int] = None
    polyx_trimmed_reads: Optional[str] = None
    total_polyx_trimmed_bases: Optional[int] = None
    polyx_trimmed_bases: Optional[str] = None
    read1_total_reads: Optional[str] = None
    read1_total_bases: Optional[str] = None
    read1_q20_bases: Optional[str] = None
    read1_q30_bases: Optional[str] = None
    read2_total_reads: Optional[str] = None
    read2_total_bases: Optional[str] = None
    read2_q20_bases: Optional[str] = None
    read2_q30_bases: Optional[str] = None

    class Config:
        from_attributes = True

class MarkdupSchema(BaseModel):
    sample: str
    total_read_pairs: Optional[int] = None
    read_pair_duplicates: Optional[int] = None
    percent_duplication: Optional[float] = None

    class Config:
        from_attributes = True

class PicardAlignmentSummarySchema(BaseModel):
    sample: str
    category: Optional[str] = None
    total_reads: Optional[int] = None
    pf_reads: Optional[int] = None
    pct_pf_reads: Optional[float] = None
    pf_noise_reads: Optional[int] = None
    pf_reads_aligned: Optional[int] = None
    pct_pf_reads_aligned: Optional[float] = None
    pf_aligned_bases: Optional[int] = None
    pf_hq_aligned_reads: Optional[int] = None
    pf_hq_aligned_bases: Optional[int] = None
    pf_hq_aligned_q20_bases: Optional[int] = None
    pf_hq_median_mismatches: Optional[float] = None
    pf_mismatch_rate: Optional[float] = None
    pf_hq_error_rate: Optional[float] = None
    pf_indel_rate: Optional[float] = None
    mean_read_length: Optional[float] = None
    sd_read_length: Optional[float] = None
    median_read_length: Optional[int] = None
    mad_read_length: Optional[int] = None
    min_read_length: Optional[int] = None
    max_read_length: Optional[int] = None
    mean_aligned_read_length: Optional[float] = None
    reads_aligned_in_pairs: Optional[int] = None
    pct_reads_aligned_in_pairs: Optional[float] = None
    pf_reads_improper_pairs: Optional[int] = None
    pct_pf_reads_improper_pairs: Optional[float] = None
    bad_cycles: Optional[int] = None
    strand_balance: Optional[float] = None
    pct_chimeras: Optional[float] = None
    pct_adapter: Optional[float] = None
    pct_softclip: Optional[float] = None
    pct_hardclip: Optional[float] = None
    avg_pos_3prime_softclip_length: Optional[float] = None
    library: Optional[str] = None
    read_group: Optional[str] = None

    class Config:
        from_attributes = True

class PicardGcBiasSchema(BaseModel):
    sample: str
    accumulation_level: Optional[float] = None
    reads_used: Optional[int] = None
    gc: Optional[int] = None
    windows: Optional[int] = None
    read_starts: Optional[int] = None
    mean_base_quality: Optional[float] = None
    normalized_coverage: Optional[float] = None
    error_bar_width: Optional[float] = None
    library: Optional[str] = None
    read_group: Optional[str] = None

    class Config:
        from_attributes = True

class PicardGcBiasSummarySchema(BaseModel):
    sample: str
    accumulation_level: Optional[float] = None
    reads_used: Optional[int] = None
    window_size: Optional[int] = None
    total_clusters: Optional[int] = None
    aligned_reads: Optional[int] = None
    at_dropout: Optional[float] = None
    gc_dropout: Optional[float] = None
    gc_nc_0_19: Optional[float] = None
    gc_nc_20_39: Optional[float] = None
    gc_nc_40_59: Optional[float] = None
    gc_nc_60_79: Optional[float] = None
    gc_nc_80_100: Optional[float] = None
    library: Optional[str] = None
    read_group: Optional[str] = None

    class Config:
        from_attributes = True

class PicardHsSchema(BaseModel):
    sample: str
    bait_set: Optional[str] = None
    bait_territory: Optional[int] = None
    bait_design_efficiency: Optional[float] = None
    on_bait_bases: Optional[int] = None
    near_bait_bases: Optional[int] = None
    off_bait_bases: Optional[int] = None
    pct_selected_bases: Optional[float] = None
    pct_off_bait: Optional[float] = None
    on_bait_vs_selected: Optional[float] = None
    mean_bait_coverage: Optional[float] = None
    pct_usable_bases_on_bait: Optional[float] = None
    pct_usable_bases_on_target: Optional[float] = None
    fold_enrichment: Optional[float] = None
    hs_library_size: Optional[int] = None
    hs_penalty_10x: Optional[float] = None
    hs_penalty_20x: Optional[float] = None
    hs_penalty_30x: Optional[float] = None
    hs_penalty_40x: Optional[float] = None
    hs_penalty_50x: Optional[float] = None
    hs_penalty_100x: Optional[float] = None
    target_territory: Optional[int] = None
    genome_size: Optional[int] = None
    total_reads: Optional[int] = None
    pf_reads: Optional[int] = None
    pf_bases: Optional[int] = None
    pf_unique_reads: Optional[int] = None
    pf_uq_reads_aligned: Optional[int] = None
    pf_bases_aligned: Optional[int] = None
    pf_uq_bases_aligned: Optional[int] = None
    on_target_bases: Optional[int] = None
    pct_pf_reads: Optional[float] = None
    pct_pf_uq_reads: Optional[float] = None
    pct_pf_uq_reads_aligned: Optional[float] = None
    mean_target_coverage: Optional[float] = None
    median_target_coverage: Optional[float] = None
    max_target_coverage: Optional[float] = None
    min_target_coverage: Optional[float] = None
    zero_cvg_targets_pct: Optional[float] = None
    pct_exc_dupe: Optional[float] = None
    pct_exc_adapter: Optional[float] = None
    pct_exc_mapq: Optional[float] = None
    pct_exc_baseq: Optional[float] = None
    pct_exc_overlap: Optional[float] = None
    pct_exc_off_target: Optional[float] = None
    fold_80_base_penalty: Optional[float] = None
    pct_target_bases_1x: Optional[float] = None
    pct_target_bases_2x: Optional[float] = None
    pct_target_bases_10x: Optional[float] = None
    pct_target_bases_20x: Optional[float] = None
    pct_target_bases_30x: Optional[float] = None
    pct_target_bases_40x: Optional[float] = None
    pct_target_bases_50x: Optional[float] = None
    pct_target_bases_100x: Optional[float] = None
    pct_target_bases_250x: Optional[float] = None
    pct_target_bases_500x: Optional[float] = None
    pct_target_bases_1000x: Optional[float] = None
    pct_target_bases_2500x: Optional[float] = None
    pct_target_bases_5000x: Optional[float] = None
    pct_target_bases_10000x: Optional[float] = None
    pct_target_bases_25000x: Optional[float] = None
    pct_target_bases_50000x: Optional[float] = None
    pct_target_bases_100000x: Optional[float] = None
    at_dropout: Optional[float] = None
    gc_dropout: Optional[float] = None
    het_snp_sensitivity: Optional[float] = None
    het_snp_q: Optional[float] = None
    library: Optional[str] = None
    read_group: Optional[str] = None

    class Config:
        from_attributes = True

class PicardInsertSizeSchema(BaseModel):
    sample: str
    median_insert_size: Optional[int] = None
    mode_insert_size: Optional[int] = None
    median_absolute_deviation: Optional[int] = None
    min_insert_size: Optional[int] = None
    max_insert_size: Optional[int] = None
    mean_insert_size: Optional[float] = None
    standard_deviation: Optional[float] = None
    read_pairs: Optional[int] = None
    pair_orientation: Optional[str] = None
    width_of_10_percent: Optional[int] = None
    width_of_20_percent: Optional[int] = None
    width_of_30_percent: Optional[int] = None
    width_of_40_percent: Optional[int] = None
    width_of_50_percent: Optional[int] = None
    width_of_60_percent: Optional[int] = None
    width_of_70_percent: Optional[int] = None
    width_of_80_percent: Optional[int] = None
    width_of_90_percent: Optional[int] = None
    width_of_95_percent: Optional[int] = None
    width_of_99_percent: Optional[int] = None
    library: Optional[str] = None
    read_group: Optional[str] = None

    class Config:
        from_attributes = True

class PicardQualityYieldSchema(BaseModel):
    sample: str
    total_reads: Optional[int] = None
    pf_reads: Optional[int] = None
    read_length: Optional[int] = None
    total_bases: Optional[int] = None
    pf_bases: Optional[int] = None
    q20_bases: Optional[int] = None
    pf_q20_bases: Optional[int] = None
    q30_bases: Optional[int] = None
    pf_q30_bases: Optional[int] = None
    q20_equivalent_yield: Optional[int] = None
    pf_q20_equivalent_yield: Optional[int] = None

    class Config:
        from_attributes = True

class ScreenSchema(BaseModel):
    sample: str
    human: Optional[float] = None
    dna: Optional[float] = None
    pUC19: Optional[float] = None
    human_unmap: Optional[float] = None

    class Config:
        from_attributes = True

class BsRateSchema(BaseModel):
    sample: str
    puc19vector: Optional[float] = None
    lambda_dna_conversion_rate: Optional[float] = None

    class Config:
        from_attributes = True

class CoverageSchema(BaseModel):
    sample: str
    pct_v2_sites_5x: Optional[float] = None
    pct_v2_sites_15x: Optional[float] = None
    pct_v2_sites_20x: Optional[float] = None
    pct_pcages_sites_5x: Optional[float] = None
    pct_pcages_sites_15x: Optional[float] = None
    pct_pcages_sites_20x: Optional[float] = None
    pct_horvath_sites_5x: Optional[float] = None
    pct_horvath_sites_15x: Optional[float] = None
    pct_horvath_sites_20x: Optional[float] = None
    pct_skinblood_sites_5x: Optional[float] = None
    pct_skinblood_sites_15x: Optional[float] = None
    pct_skinblood_sites_20x: Optional[float] = None
