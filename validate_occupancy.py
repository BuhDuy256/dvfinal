import pandas as pd
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CSV_PATH = "data/cleaned_calendar.csv"

print("Loading data...")
df = pd.read_csv(CSV_PATH, usecols=["year", "month", "is_booked"])
df["is_booked"] = pd.to_numeric(df["is_booked"], errors="coerce")

print(f"Total rows loaded: {len(df):,}\n")

# ── 1. Pivot: occ_rate by year × month ──────────────────────────────────────
print("=" * 70)
print("TABLE 1 — Occupancy Rate (%) by Year × Month")
print("=" * 70)

by_year_month = (
    df.groupby(["year", "month"])["is_booked"]
    .agg(occ_rate="mean", n_records="count")
    .reset_index()
)
by_year_month["occ_rate_pct"] = (by_year_month["occ_rate"] * 100).round(2)

pivot = by_year_month.pivot(index="year", columns="month", values="occ_rate_pct")
pivot.columns = [f"M{int(c):02d}" for c in pivot.columns]
print(pivot.to_string())

# ── 2. All-years aggregate by month ─────────────────────────────────────────
print("\n" + "=" * 70)
print("TABLE 2 — Average Occupancy Rate (%) across All Years by Month")
print("(This is what Chart 8.1 Phương án B shows)")
print("=" * 70)

by_month = (
    df.groupby("month")["is_booked"]
    .agg(occ_rate="mean", n_records="count")
    .reset_index()
)
by_month["occ_rate_pct"] = (by_month["occ_rate"] * 100).round(2)
by_month.columns = ["Month", "Occ Rate (raw)", "N Records", "Occ Rate (%)"]
print(by_month.to_string(index=False))

# ── 3. Record count by year × month (check imbalance) ───────────────────────
print("\n" + "=" * 70)
print("TABLE 3 — Record Count by Year × Month (check data imbalance)")
print("=" * 70)

pivot_count = by_year_month.pivot(index="year", columns="month", values="n_records")
pivot_count.columns = [f"M{int(c):02d}" for c in pivot_count.columns]
print(pivot_count.fillna(0).astype(int).to_string())

# ── 4. November deep-dive ────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("TABLE 4 — November Deep-Dive (is_booked distribution per year)")
print("=" * 70)

nov = df[df["month"] == 11].copy()
nov_summary = (
    nov.groupby("year")["is_booked"]
    .agg(
        n_records="count",
        n_booked="sum",
        occ_rate_pct=lambda x: round(x.mean() * 100, 2),
    )
    .reset_index()
)
print(nov_summary.to_string(index=False))

# ── 5. Spike check: Nov vs Aug (peak summer) ────────────────────────────────
print("\n" + "=" * 70)
print("TABLE 5 — Month Ranking by Avg Occupancy Rate (all years)")
print("=" * 70)

ranked = by_month[["Month", "Occ Rate (%)"]].sort_values("Occ Rate (%)", ascending=False)
ranked.insert(0, "Rank", range(1, len(ranked) + 1))
print(ranked.to_string(index=False))

# ── 6. Quick flag ────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70)

nov_rate = by_month.loc[by_month["Month"] == 11, "Occ Rate (%)"].values[0]
aug_rate = by_month.loc[by_month["Month"] == 8, "Occ Rate (%)"].values[0]
print(f"  November avg occ rate : {nov_rate:.2f}%")
print(f"  August   avg occ rate : {aug_rate:.2f}%")
print(f"  Nov > Aug             : {nov_rate > aug_rate}")

years_in_nov = nov_summary["year"].tolist()
years_in_data = sorted(df["year"].unique().tolist())
print(f"\n  Years in dataset      : {years_in_data}")
print(f"  Years with Nov data   : {years_in_nov}")

# Check if spike is driven by 1 year
max_nov_year = nov_summary.loc[nov_summary["occ_rate_pct"].idxmax()]
print(f"\n  Highest Nov rate year : {int(max_nov_year['year'])} "
      f"({max_nov_year['occ_rate_pct']:.2f}%, n={int(max_nov_year['n_records']):,})")

if nov_rate > aug_rate:
    print("\n  >> November spike CONFIRMED in all-years aggregate.")
    print("     Check TABLE 1 to see if spike comes from 1 specific year.")
else:
    print("\n  >> November spike NOT found — likely was Year 2026 artifact.")
