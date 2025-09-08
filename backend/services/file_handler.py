import pandas as pd
from io import BytesIO
import crud
import schemas
import math
from typing import Type, Any, Optional
from pydantic import BaseModel
import re

def replace_nan_with_none(data: dict) -> dict:
    """
    Replaces NaN values in a dictionary with None.
    """
    return {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in data.items()}

def normalize_keys_to_snake_case(data: dict) -> dict:
    """
    Converts dictionary keys to snake_case.
    Handles keys that might be in UPPERCASE_WITH_UNDERSCORES or PascalCase.
    """
    normalized_data = {}
    for key, value in data.items():
        # First, handle the 'X' suffix specifically for numeric contexts (e.g., 1X, 10X)
        # Convert '1X' to '1x' directly, without adding an underscore
        temp_key = re.sub(r'(\d+)X', r'\1x', key)

        # Determine if the key is predominantly ALL_CAPS_WITH_UNDERSCORES
        # A simple heuristic: if it contains only uppercase letters, digits, and underscores
        if re.fullmatch(r'[A-Z0-9_]+', temp_key):
            snake_case_key = temp_key.lower()
        else:
            # Otherwise, assume it's PascalCase or camelCase and convert
            s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', temp_key)
            snake_case_key = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        # Clean up any multiple underscores that might have been introduced
        snake_case_key = re.sub(r'_{2,}', '_', snake_case_key)
        
        # Remove leading/trailing underscores
        snake_case_key = snake_case_key.strip('_')

        normalized_data[snake_case_key] = value
    return normalized_data


def convert_numeric_fields(row_data: dict, schema_class: Type[BaseModel]) -> dict:
    """
    Converts fields in row_data to int or float based on schema_class annotations.
    Handles cases where numeric data might be read as strings from Excel.
    """
    converted_data = row_data.copy()
    for field_name, field_info in schema_class.model_fields.items():
        if field_name in converted_data and converted_data[field_name] is not None:
            value = converted_data[field_name]
            # Check if the field is Optional[int] or Optional[float]
            if field_info.annotation == Optional[int] or field_info.annotation == int:
                try:
                    converted_data[field_name] = int(value)
                except (ValueError, TypeError):
                    converted_data[field_name] = None
            elif field_info.annotation == Optional[float] or field_info.annotation == float:
                try:
                    converted_data[field_name] = float(value)
                except (ValueError, TypeError):
                    converted_data[field_name] = None
    return converted_data


def process_uploaded_file(file):
    if file.filename.endswith('.csv'):
        process_ages_file(file.file)
    elif file.filename.endswith('.xlsx'):
        process_qc_file(file.file)
    else:
        raise ValueError("Unsupported file type")

def process_ages_file(ages_file):
    # Process ages file
    ages_df = pd.read_csv(ages_file)
    for _, row in ages_df.iterrows():
        # Clean up column names
        row_data = {
            "sample": row.get("Sample"),
            "gender": row.get("gender"),
            "age": row.get("age"),
            "sample_date": row.get("sampleDate"),
            "menopausal_status": row.get("menopausalStatus"),
            "ptid": row.get("ptid"),
            "esti_gender": row.get("esti_gender"),
            "cfdna": row.get("cfdna"),
            "wbc": row.get("WBC"),
            "colon": row.get("colon"),
            "liver": row.get("liver"),
            "ovary": row.get("ovary"),
            "pancreas": row.get("pancreas"),
            "prostate": row.get("prostate"),
            "small_intestine": row.get("small_intestine"),
            "spleen": row.get("spleen"),
            "stomach": row.get("stomach"),
            "adj_ovary_menopause": row.get("adjOvary(menopause)"),
            "adj_ovary_no_menopause": row.get("adjOvary(noMenopause)")
        }
        cleaned_row_data = replace_nan_with_none(row_data)
        ages_schema = schemas.ReportedAgesSchema(**cleaned_row_data)
        crud.upsert_reported_ages(ages_schema)

def process_qc_file(qc_file):
    # Process qc file
    xls = pd.ExcelFile(qc_file)
    for sheet_name in xls.sheet_names:
        print(sheet_name)
        df = pd.read_excel(xls, sheet_name=sheet_name)
        if sheet_name == "bsrate":
            for _, row in df.iterrows():
                row_data = {
                    "sample": row.get("Sample"),
                    "puc19vector": row.get("pUC19vector"),
                    "lambda_dna_conversion_rate": row.get("λ-DNA(ConversionRate)")
                }
                cleaned_row_data = replace_nan_with_none(row_data)
                bs_rate_schema = schemas.BsRateSchema(**cleaned_row_data)
                crud.upsert_bs_rate(bs_rate_schema)
        elif sheet_name == "coverage":
            for _, row in df.iterrows():
                row_data = {
                    "sample": row.get("Sample"),
                    "pct_v2_sites_5x": row.get("PCT_V2_sites_5X"),
                    "pct_v2_sites_15x": row.get("PCT_V2_sites_15X"),
                    "pct_v2_sites_20x": row.get("PCT_V2_sites_20X"),
                    "pct_pcages_sites_5x": row.get("PCT_PCages_sites_5X"),
                    "pct_pcages_sites_15x": row.get("PCT_PCages_sites_15X"),
                    "pct_pcages_sites_20x": row.get("PCT_PCages_sites_20X"),
                    "pct_horvath_sites_5x": row.get("PCT_horvath_sites_5X"),
                    "pct_horvath_sites_15x": row.get("PCT_horvath_sites_15X"),
                    "pct_horvath_sites_20x": row.get("PCT_horvath_sites_20X"),
                    "pct_skinblood_sites_5x": row.get("PCT_skinblood_sites_5X"),
                    "pct_skinblood_sites_15x": row.get("PCT_skinblood_sites_15X"),
                    "pct_skinblood_sites_20x": row.get("PCT_skinblood_sites_20X")
                }
                cleaned_row_data = replace_nan_with_none(row_data)
                coverage_schema = schemas.CoverageSchema(**cleaned_row_data)
                crud.upsert_coverage(coverage_schema)
        elif sheet_name == "fastp":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                cleaned_row_data = replace_nan_with_none(row_data)
                fastp_schema = schemas.FastpSchema(**cleaned_row_data)
                crud.upsert_fastp(fastp_schema)
        elif sheet_name == "markdup.markdup.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.MarkdupSchema)
                markdup_schema = schemas.MarkdupSchema(**converted_row_data)
                crud.upsert_markdup(markdup_schema)
        elif sheet_name == "picard.alignmentSummary.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardAlignmentSummarySchema)
                picard_alignment_summary_schema = schemas.PicardAlignmentSummarySchema(**converted_row_data)
                crud.upsert_picard_alignment_summary(picard_alignment_summary_schema)
        elif sheet_name == "picard.gcBias.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardGcBiasSchema)
                picard_gc_bias_schema = schemas.PicardGcBiasSchema(**converted_row_data)
                crud.upsert_picard_gc_bias(picard_gc_bias_schema)
        elif sheet_name == "picard.gcBiasSummary.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardGcBiasSummarySchema)
                picard_gc_bias_summary_schema = schemas.PicardGcBiasSummarySchema(**converted_row_data)
                crud.upsert_picard_gc_bias_summary(picard_gc_bias_summary_schema)
        elif sheet_name == "picard.hs.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardHsSchema)
                print(converted_row_data)
                picard_hs_schema = schemas.PicardHsSchema(**converted_row_data)
                print(picard_hs_schema)
                crud.upsert_picard_hs(picard_hs_schema)
        elif sheet_name == "picard.insertSize.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardInsertSizeSchema)
                picard_insert_size_schema = schemas.PicardInsertSizeSchema(**converted_row_data)
                crud.upsert_picard_insert_size(picard_insert_size_schema)
        elif sheet_name == "picard.qualityYield.txt":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.PicardQualityYieldSchema)
                picard_quality_yield_schema = schemas.PicardQualityYieldSchema(**converted_row_data)
                crud.upsert_picard_quality_yield(picard_quality_yield_schema)
        elif sheet_name == "screen":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                
                # Prioritize 'Sample' (correct sample name) and remove 'SAMPLE' if it's empty
                if "SAMPLE" in row_data and (pd.isna(row_data["SAMPLE"]) or row_data["SAMPLE"] is None):
                    del row_data["SAMPLE"]
                
                row_data = normalize_keys_to_snake_case(row_data) # Normalize keys
                
                if 'dna' in row_data: # This check should happen after normalization
                    row_data['lambda_dna'] = row_data.pop('dna')
                cleaned_row_data = replace_nan_with_none(row_data)
                converted_row_data = convert_numeric_fields(cleaned_row_data, schemas.ScreenSchema)
                screen_schema = schemas.ScreenSchema(**converted_row_data)
                crud.upsert_screen(screen_schema)

def generate_excel_file(samples: list[str]):
    data = crud.get_data_by_samples(samples)

    DESIRED_COLUMNS = [
        "sample", "ptid", "gender", "esti_gender", "age", "total_bases",
        "puc19vector", "lambda_dna_conversion_rate", "human", "lambda_dna",
        "pUC19", "q30_rate", "mean_insert_size", "percent_duplication",
        "pct_selected_bases", "fold_enrichment", "zero_cvg_targets_pct",
        "mean_target_coverage", "pct_exc_dupe", "pct_exc_off_target",
        "fold_80_base_penalty", "pct_target_bases_10x",
        "pct_target_bases_20x", "pct_target_bases_30x",
    ]

    # Process data to create a combined view
    sample_map = {}
    for table_name, records in data.items():
        for record in records:
            sample_id = record.get("sample")
            if sample_id:
                if sample_id not in sample_map:
                    sample_map[sample_id] = {}
                sample_map[sample_id].update(record)

    combined_data = []
    # Use the original samples list to maintain order
    for sample_id in samples:
        if sample_id in sample_map:
            record = sample_map[sample_id]
            processed_record = {col: record.get(col) for col in DESIRED_COLUMNS}
            combined_data.append(processed_record)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write the combined sheet first
        if combined_data:
            combined_df = pd.DataFrame(combined_data)
            combined_df.to_excel(writer, sheet_name="Sheet1", index=False)

        # Write the raw data sheets
        for table_name, records in data.items():
            if records:
                df = pd.DataFrame(records)
                df.to_excel(writer, sheet_name=table_name, index=False)
    
    output.seek(0)
    return output
