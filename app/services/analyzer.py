"""Numeric, categorical, and conditional business analysis."""

from __future__ import annotations

import pandas as pd

from app.schemas.analysis import (
    AnalysisResponse,
    BusinessAnalysis,
    CategoricalStats,
    CategoryFrequency,
    NumericStats,
)
from app.utils.helpers import is_numeric_series, safe_percentage


def _numeric_stats(series: pd.Series) -> NumericStats:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return NumericStats(count=0)
    return NumericStats(
        count=int(numeric.count()),
        mean=float(round(numeric.mean(), 4)),
        median=float(round(numeric.median(), 4)),
        min=float(numeric.min()),
        max=float(numeric.max()),
        std=float(round(numeric.std(ddof=1), 4)) if len(numeric) > 1 else 0.0,
        p25=float(round(numeric.quantile(0.25), 4)),
        p50=float(round(numeric.quantile(0.50), 4)),
        p75=float(round(numeric.quantile(0.75), 4)),
    )


def _categorical_stats(series: pd.Series, top_n: int = 10) -> CategoricalStats:
    cleaned = series.dropna().astype(str)
    total = max(len(cleaned), 1)
    counts = cleaned.value_counts().head(top_n)
    top = [
        CategoryFrequency(value=str(idx), count=int(cnt), percentage=safe_percentage(int(cnt), total))
        for idx, cnt in counts.items()
    ]
    return CategoricalStats(unique_count=int(cleaned.nunique()), top_categories=top)


def _business_analysis(df: pd.DataFrame) -> BusinessAnalysis | None:
    cols = {str(c).strip().lower(): c for c in df.columns}
    sales_col = cols.get("total_sales") or cols.get("sales") or cols.get("amount")
    product_col = cols.get("product") or cols.get("product_name")
    customer_col = cols.get("customer_id") or cols.get("customer") or cols.get("name")
    region_col = cols.get("region") or cols.get("city")
    date_col = cols.get("date") or cols.get("order_date")

    if not any([sales_col, product_col, customer_col, region_col]):
        return None

    business = BusinessAnalysis()

    if sales_col is not None:
        sales = pd.to_numeric(df[sales_col], errors="coerce")
        business.total_sales = float(round(sales.sum(skipna=True), 2))
        business.average_sales = float(round(sales.mean(skipna=True), 2)) if sales.notna().any() else None

    if product_col is not None:
        business.top_products = _categorical_stats(df[product_col], top_n=5).top_categories

    if customer_col is not None and sales_col is not None:
        grouped = (
            df.assign(_sales=pd.to_numeric(df[sales_col], errors="coerce"))
            .groupby(df[customer_col].astype(str))["_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        total = float(grouped.sum()) or 1.0
        business.top_customers = [
            CategoryFrequency(
                value=str(idx),
                count=int(round(val)),
                percentage=safe_percentage(float(val), total),
            )
            for idx, val in grouped.items()
        ]

    if region_col is not None and sales_col is not None:
        grouped = (
            df.assign(_sales=pd.to_numeric(df[sales_col], errors="coerce"))
            .groupby(df[region_col].astype(str))["_sales"]
            .sum()
            .sort_values(ascending=False)
        )
        total = float(grouped.sum()) or 1.0
        business.sales_by_region = [
            CategoryFrequency(
                value=str(idx),
                count=int(round(val)),
                percentage=safe_percentage(float(val), total),
            )
            for idx, val in grouped.items()
        ]

    if date_col is not None and sales_col is not None:
        dates = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        tmp = pd.DataFrame(
            {
                "month": dates.dt.to_period("M").astype(str),
                "sales": pd.to_numeric(df[sales_col], errors="coerce"),
            }
        ).dropna()
        if not tmp.empty:
            monthly = tmp.groupby("month")["sales"].sum().reset_index()
            business.monthly_sales = [
                {"month": row["month"], "total_sales": float(round(row["sales"], 2))}
                for _, row in monthly.iterrows()
            ]

    return business


def analyze_dataframe(df: pd.DataFrame, dataset_id: int) -> AnalysisResponse:
    numeric: dict[str, NumericStats] = {}
    categorical: dict[str, CategoricalStats] = {}

    for column in df.columns:
        series = df[column]
        if is_numeric_series(series):
            numeric[str(column)] = _numeric_stats(series)
        else:
            categorical[str(column)] = _categorical_stats(series)

    return AnalysisResponse(
        dataset_id=dataset_id,
        rows=int(len(df)),
        columns=int(df.shape[1]),
        numeric=numeric,
        categorical=categorical,
        business=_business_analysis(df),
    )
