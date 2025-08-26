import pandas as pd
from io import BytesIO
import crud
import schemas

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
            "sample": row["Sample"],
            "gender": row["gender"],
            "age": row["age"],
            "sample_date": row["sampleDate"],
            "menopausal_status": row["menopausalStatus"],
            "ptid": row["ptid"],
            "esti_gender": row["esti_gender"],
            "cfdna": row["cfdna"],
            "wbc": row["WBC"],
            "colon": row["colon"],
            "liver": row["liver"],
            "ovary": row["ovary"],
            "pancreas": row["pancreas"],
            "prostate": row["prostate"],
            "small_intestine": row["small_intestine"],
            "spleen": row["spleen"],
            "stomach": row["stomach"],
            "adj_ovary_menopause": row["adjOvary(menopause)"],
            "adj_ovary_no_menopause": row["adjOvary(noMenopause)"]
        }
        ages_schema = schemas.ReportedAgesSchema(**row_data)
        crud.upsert_reported_ages(ages_schema)

def process_qc_file(qc_file):
    # Process qc file
    xls = pd.ExcelFile(qc_file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        if sheet_name == "bsrate":
            for _, row in df.iterrows():
                row_data = {
                    "sample": row["Sample"],
                    "puc19vector": row["pUC19vector"],
                    "lambda_dna_conversion_rate": row["¦Ë-DNA(ConversionRate)"]
                }
                bs_rate_schema = schemas.BsRateSchema(**row_data)
                crud.upsert_bs_rate(bs_rate_schema)
        elif sheet_name == "coverage":
            for _, row in df.iterrows():
                row_data = {
                    "sample": row["Sample"],
                    "pct_v2_sites_5x": row["PCT_V2_sites_5X"],
                    "pct_v2_sites_15x": row["PCT_V2_sites_15X"],
                    "pct_v2_sites_20x": row["PCT_V2_sites_20X"],
                    "pct_pcages_sites_5x": row["PCT_PCages_sites_5X"],
                    "pct_pcages_sites_15x": row["PCT_PCages_sites_15X"],
                    "pct_pcages_sites_20x": row["PCT_PCages_sites_20X"],
                    "pct_horvath_sites_5x": row["PCT_horvath_sites_5X"],
                    "pct_horvath_sites_15x": row["PCT_horvath_sites_15X"],
                    "pct_horvath_sites_20x": row["PCT_horvath_sites_20X"],
                    "pct_skinblood_sites_5x": row["PCT_skinblood_sites_5X"],
                    "pct_skinblood_sites_15x": row["PCT_skinblood_sites_15X"],
                    "pct_skinblood_sites_20x": row["PCT_skinblood_sites_20X"]
                }
                coverage_schema = schemas.CoverageSchema(**row_data)
                crud.upsert_coverage(coverage_schema)
        elif sheet_name == "fastp":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                fastp_schema = schemas.FastpSchema(**row_data)
                crud.upsert_fastp(fastp_schema)
        elif sheet_name == "markdup":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                markdup_schema = schemas.MarkdupSchema(**row_data)
                crud.upsert_markdup(markdup_schema)
        elif sheet_name == "picard.alignmentSummary":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_alignment_summary_schema = schemas.PicardAlignmentSummarySchema(**row_data)
                crud.upsert_picard_alignment_summary(picard_alignment_summary_schema)
        elif sheet_name == "picard.gcBias":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_gc_bias_schema = schemas.PicardGcBiasSchema(**row_data)
                crud.upsert_picard_gc_bias(picard_gc_bias_schema)
        elif sheet_name == "picard.gcBiasSummary":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_gc_bias_summary_schema = schemas.PicardGcBiasSummarySchema(**row_data)
                crud.upsert_picard_gc_bias_summary(picard_gc_bias_summary_schema)
        elif sheet_name == "picard.hs":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_hs_schema = schemas.PicardHsSchema(**row_data)
                crud.upsert_picard_hs(picard_hs_schema)
        elif sheet_name == "picard.insertSize":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_insert_size_schema = schemas.PicardInsertSizeSchema(**row_data)
                crud.upsert_picard_insert_size(picard_insert_size_schema)
        elif sheet_name == "picard.qualityYield":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                picard_quality_yield_schema = schemas.PicardQualityYieldSchema(**row_data)
                crud.upsert_picard_quality_yield(picard_quality_yield_schema)
        elif sheet_name == "screen":
            for _, row in df.iterrows():
                row_data = row.to_dict()
                row_data['sample'] = row_data.pop('Sample')
                screen_schema = schemas.ScreenSchema(**row_data)
                crud.upsert_screen(screen_schema)

def generate_excel_file(samples: list[str]):
    data = crud.get_data_by_samples(samples)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for table_name, records in data.items():
            if records:
                df = pd.DataFrame([record.__data__ for record in records])
                df.to_excel(writer, sheet_name=table_name, index=False)
    
    output.seek(0)
    return output
