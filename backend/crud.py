import models
import schemas

def upsert_reported_ages(ages_data: schemas.ReportedAgesSchema):
    models.ReportedAges.insert(**ages_data.dict()).on_conflict(
        conflict_target=[models.ReportedAges.sample],
        update=ages_data.dict()
    ).execute()

def upsert_bs_rate(bs_rate_data: schemas.BsRateSchema):
    models.BsRate.insert(**bs_rate_data.dict()).on_conflict(
        conflict_target=[models.BsRate.sample],
        update=bs_rate_data.dict()
    ).execute()

def upsert_coverage(coverage_data: schemas.CoverageSchema):
    models.Coverage.insert(**coverage_data.dict()).on_conflict(
        conflict_target=[models.Coverage.sample],
        update=coverage_data.dict()
    ).execute()

def upsert_fastp(fastp_data: schemas.FastpSchema):
    models.Fastp.insert(**fastp_data.dict()).on_conflict(
        conflict_target=[models.Fastp.sample],
        update=fastp_data.dict()
    ).execute()

def upsert_markdup(markdup_data: schemas.MarkdupSchema):
    models.Markdup.insert(**markdup_data.dict()).on_conflict(
        conflict_target=[models.Markdup.sample],
        update=markdup_data.dict()
    ).execute()

def upsert_picard_alignment_summary(picard_alignment_summary_data: schemas.PicardAlignmentSummarySchema):
    models.PicardAlignmentSummary.insert(**picard_alignment_summary_data.dict()).on_conflict(
        conflict_target=[models.PicardAlignmentSummary.sample],
        update=picard_alignment_summary_data.dict()
    ).execute()

def upsert_picard_gc_bias(picard_gc_bias_data: schemas.PicardGcBiasSchema):
    models.PicardGcBias.insert(**picard_gc_bias_data.dict()).on_conflict(
        conflict_target=[models.PicardGcBias.sample],
        update=picard_gc_bias_data.dict()
    ).execute()

def upsert_picard_gc_bias_summary(picard_gc_bias_summary_data: schemas.PicardGcBiasSummarySchema):
    models.PicardGcBiasSummary.insert(**picard_gc_bias_summary_data.dict()).on_conflict(
        conflict_target=[models.PicardGcBiasSummary.sample],
        update=picard_gc_bias_summary_data.dict()
    ).execute()

def upsert_picard_hs(picard_hs_data: schemas.PicardHsSchema):
    models.PicardHs.insert(**picard_hs_data.dict()).on_conflict(
        conflict_target=[models.PicardHs.sample],
        update=picard_hs_data.dict()
    ).execute()

def upsert_picard_insert_size(picard_insert_size_data: schemas.PicardInsertSizeSchema):
    models.PicardInsertSize.insert(**picard_insert_size_data.dict()).on_conflict(
        conflict_target=[models.PicardInsertSize.sample],
        update=picard_insert_size_data.dict()
    ).execute()

def upsert_picard_quality_yield(picard_quality_yield_data: schemas.PicardQualityYieldSchema):
    models.PicardQualityYield.insert(**picard_quality_yield_data.dict()).on_conflict(
        conflict_target=[models.PicardQualityYield.sample],
        update=picard_quality_yield_data.dict()
    ).execute()

def upsert_screen(screen_data: schemas.ScreenSchema):
    models.Screen.insert(**screen_data.dict()).on_conflict(
        conflict_target=[models.Screen.sample],
        update=screen_data.dict()
    ).execute()

def get_data_by_samples(samples: list[str]):
    reported_ages = models.ReportedAges.select().where(models.ReportedAges.sample.in_(samples))
    bs_rate = models.BsRate.select().where(models.BsRate.sample.in_(samples))
    coverage = models.Coverage.select().where(models.Coverage.sample.in_(samples))
    fastp = models.Fastp.select().where(models.Fastp.sample.in_(samples))
    markdup = models.Markdup.select().where(models.Markdup.sample.in_(samples))
    picard_alignment_summary = models.PicardAlignmentSummary.select().where(models.PicardAlignmentSummary.sample.in_(samples))
    picard_gc_bias = models.PicardGcBias.select().where(models.PicardGcBias.sample.in_(samples))
    picard_gc_bias_summary = models.PicardGcBiasSummary.select().where(models.PicardGcBiasSummary.sample.in_(samples))
    picard_hs = models.PicardHs.select().where(models.PicardHs.sample.in_(samples))
    picard_insert_size = models.PicardInsertSize.select().where(models.PicardInsertSize.sample.in_(samples))
    picard_quality_yield = models.PicardQualityYield.select().where(models.PicardQualityYield.sample.in_(samples))
    screen = models.Screen.select().where(models.Screen.sample.in_(samples))
    
    return {
        "ReportedAges": list(reported_ages),
        "BsRate": list(bs_rate),
        "Coverage": list(coverage),
        "Fastp": list(fastp),
        "Markdup": list(markdup),
        "PicardAlignmentSummary": list(picard_alignment_summary),
        "PicardGcBias": list(picard_gc_bias),
        "PicardGcBiasSummary": list(picard_gc_bias_summary),
        "PicardHs": list(picard_hs),
        "PicardInsertSize": list(picard_insert_size),
        "PicardQualityYield": list(picard_quality_yield),
        "Screen": list(screen)
    }

def get_filtered_data(filters: schemas.FilterSchema):
    query = models.BsRate.select(models.BsRate.sample)

    field_to_model = {
        "lambda_dna_conversion_rate": models.BsRate,
        "pct_selected_bases": models.PicardHs,
        "fold_80_base_penalty": models.PicardHs,
        "percent_duplication": models.Markdup,
    }

    joined_models = set([models.BsRate])

    for field_name, (operator, value) in filters.filters.items():
        model = field_to_model.get(field_name)
        if model and model not in joined_models:
            query = query.join(model, on=(models.BsRate.sample == model.sample))
            joined_models.add(model)

        if hasattr(model, field_name):
            field = getattr(model, field_name)
            if operator == ">=":
                query = query.where(field >= value)
            elif operator == "<=":
                query = query.where(field <= value)
            elif operator == ">":
                query = query.where(field > value)
            elif operator == "<":
                query = query.where(field < value)
            elif operator == "==":
                query = query.where(field == value)

    samples = [item.sample for item in query]
    return get_data_by_samples(samples)
