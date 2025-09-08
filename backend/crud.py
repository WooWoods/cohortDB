import models
import schemas
from playhouse.shortcuts import model_to_dict
from typing import Optional
from peewee import Expression
import operator

def create_user(user: schemas.UserCreate, hashed_password: str) -> models.User:
    """
    Creates a new user in the database.
    """
    new_user = models.User.create(
        username=user.username,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    return new_user

def get_user_by_username(username: str) -> Optional[models.User]:
    """
    Retrieves a user by their username.
    """
    return models.User.get_or_none(models.User.username == username)

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

import re

def get_samples_by_search_term(search_term: str) -> list[str]:
    if search_term.endswith("*"):
        # This is a prefix search
        prefix = search_term[:-1].strip() # Remove the trailing '*'
        
        # Remove "CAP\d+WGS_" or "CAP\d+_" prefix from the search term if present
        cleaned_prefix = re.sub(r"CAP\d+(WGS_|_)", "", prefix)
        
        # Ensure the search term starts with "MO" or "MS"
        if not cleaned_prefix.startswith(("MO", "MS")):
            return []
        
        # Construct a LIKE query for the relevant part of the sample name
        like_pattern = f"%{cleaned_prefix}%"
        
        # Search across all models for samples matching the pattern
        # We need to get distinct samples from one of the tables, e.g., ReportedAges
        samples = models.ReportedAges.select(models.ReportedAges.sample).where(
            models.ReportedAges.sample.ilike(like_pattern)
        ).distinct()
        return [s.sample for s in samples]
    else:
        # Exact match search
        return [search_term]

def get_data_by_samples(samples: list[str]):
    if not samples:
        return {
            "ReportedAges": [], "BsRate": [], "Coverage": [], "Fastp": [],
            "Markdup": [], "PicardAlignmentSummary": [], "PicardGcBias": [],
            "PicardGcBiasSummary": [], "PicardHs": [], "PicardInsertSize": [],
            "PicardQualityYield": [], "Screen": []
        }

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
        "ReportedAges": [model_to_dict(r) for r in reported_ages],
        "BsRate": [model_to_dict(b) for b in bs_rate],
        "Coverage": [model_to_dict(c) for c in coverage],
        "Fastp": [model_to_dict(f) for f in fastp],
        "Markdup": [model_to_dict(m) for m in markdup],
        "PicardAlignmentSummary": [model_to_dict(p) for p in picard_alignment_summary],
        "PicardGcBias": [model_to_dict(p) for p in picard_gc_bias],
        "PicardGcBiasSummary": [model_to_dict(p) for p in picard_gc_bias_summary],
        "PicardHs": [model_to_dict(p) for p in picard_hs],
        "PicardInsertSize": [model_to_dict(p) for p in picard_insert_size],
        "PicardQualityYield": [model_to_dict(p) for p in picard_quality_yield],
        "Screen": [model_to_dict(s) for s in screen]
    }

def get_filtered_data(filters: schemas.FilterSchema):
    base_model = models.ReportedAges
    query = base_model.select(base_model.sample)

    field_to_model = {
        "age": models.ReportedAges,
        "total_bases": models.Fastp,
        "puc19vector": models.BsRate,
        "lambda_dna_conversion_rate": models.BsRate,
        "human": models.Screen,
        "lambda_dna": models.Screen,
        "pUC19": models.Screen,
        "q30_rate": models.Fastp,
        "mean_insert_size": models.PicardInsertSize,
        "percent_duplication": models.Markdup,
        "pct_selected_bases": models.PicardHs,
        "fold_enrichment": models.PicardHs,
        "zero_cvg_targets_pct": models.PicardHs,
        "mean_target_coverage": models.PicardHs,
        "pct_exc_dupe": models.PicardHs,
        "pct_exc_off_target": models.PicardHs,
        "fold_80_base_penalty": models.PicardHs,
        "pct_target_bases_10x": models.PicardHs,
        "pct_target_bases_20x": models.PicardHs,
        "pct_target_bases_30x": models.PicardHs,
    }

    joined_models = {base_model}
    expressions = []

    for f in filters.filters:
        model = field_to_model.get(f.field)
        if not model:
            continue

        if model not in joined_models:
            query = query.join(model, on=(base_model.sample == model.sample))
            joined_models.add(model)

        field = getattr(model, f.field)
        op_map = {
            ">=": operator.ge,
            "<=": operator.le,
            ">": operator.gt,
            "<": operator.lt,
            "==": operator.eq,
        }
        expressions.append(op_map[f.operator](field, f.value))

    if not expressions:
        return get_data_by_samples([])

    final_expression = expressions[0]
    for i, op in enumerate(filters.logical_operators):
        if op == "and":
            final_expression &= expressions[i + 1]
        elif op == "or":
            final_expression |= expressions[i + 1]

    query = query.where(final_expression)
    samples = [item.sample for item in query]
    return get_data_by_samples(samples)

def get_initial_data(offset: int = 0, limit: int = 20):
    samples = [item.sample for item in models.ReportedAges.select(models.ReportedAges.sample).offset(offset).limit(limit)]
    return get_data_by_samples(samples)

def get_total_data_count():
    return models.ReportedAges.select().count()
