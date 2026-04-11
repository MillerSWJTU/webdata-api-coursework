"""
Data processing script: clean and sample raw Kaggle CSVs into SQLite-ready files.

Outputs (in /data):
  books_cleaned.csv   – 5000 representative books
  reviews_cleaned.csv – up to 5 reviews per kept book, max 30000 rows total
"""
import csv
import os
import ast
import pathlib
from collections import defaultdict

# ── paths ──────────────────────────────────────────────────────────────────────
BASE = pathlib.Path(__file__).parent.parent
SRC_BOOKS   = BASE / "archive" / "books_data.csv"
SRC_REVIEWS = BASE / "archive" / "Books_rating.csv"
OUT_DIR     = BASE / "data"
OUT_DIR.mkdir(exist_ok=True)
OUT_BOOKS   = OUT_DIR / "books_cleaned.csv"
OUT_REVIEWS = OUT_DIR / "reviews_cleaned.csv"

# ── Step 1: clean books ────────────────────────────────────────────────────────
print("Processing books_data.csv ...")

def flatten_list_str(raw: str, max_len: int = 200) -> str:
    """Convert "['A', 'B']" string to 'A, B'."""
    raw = raw.strip()
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return ", ".join(str(x) for x in parsed)[:max_len]
    except Exception:
        pass
    return raw.strip("[]'\"")[:max_len]

kept_books = []
kept_titles = set()
skipped = 0

with open(SRC_BOOKS, encoding="utf-8", errors="replace") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        title = row.get("Title", "").strip()
        if not title:
            skipped += 1
            continue
        if title in kept_titles:   # deduplicate
            continue
        kept_books.append({
            "title":          title,
            "description":    row.get("description", "").strip()[:500],
            "authors":        flatten_list_str(row.get("authors", "")),
            "publisher":      row.get("publisher", "").strip()[:100],
            "published_date": row.get("publishedDate", "").strip()[:20],
            "categories":     flatten_list_str(row.get("categories", ""), 100),
            "ratings_count":  row.get("ratingsCount", "").strip() or "0",
        })
        kept_titles.add(title)
        if len(kept_books) >= 5000:
            break

with open(OUT_BOOKS, "w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(kept_books[0].keys()))
    writer.writeheader()
    writer.writerows(kept_books)

print(f"  books_cleaned.csv : {len(kept_books)} rows | "
      f"{round(OUT_BOOKS.stat().st_size/1024, 1)} KB | {skipped} skipped")

# ── Step 2: sample reviews ─────────────────────────────────────────────────────
print("Processing Books_rating.csv (this may take a minute) ...")

MAX_REVIEWS_PER_BOOK = 5
MAX_TOTAL_REVIEWS    = 30000

review_counter = defaultdict(int)
reviews_kept   = []

with open(SRC_REVIEWS, encoding="utf-8", errors="replace") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        title = row.get("Title", "").strip()
        if title not in kept_titles:
            continue
        if review_counter[title] >= MAX_REVIEWS_PER_BOOK:
            continue
        score_raw = row.get("review/score", "").strip()
        try:
            score = float(score_raw)
        except ValueError:
            continue
        reviews_kept.append({
            "book_title":   title,
            "user_id":      row.get("User_id", "").strip()[:50],
            "profile_name": row.get("profileName", "").strip()[:100],
            "score":        score,
            "summary":      row.get("review/summary", "").strip()[:200],
            "review_text":  row.get("review/text", "").strip()[:1000],
            "review_time":  row.get("review/time", "").strip(),
        })
        review_counter[title] += 1
        if len(reviews_kept) >= MAX_TOTAL_REVIEWS:
            break

with open(OUT_REVIEWS, "w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(reviews_kept[0].keys()))
    writer.writeheader()
    writer.writerows(reviews_kept)

books_with_reviews = len(review_counter)
print(f"  reviews_cleaned.csv: {len(reviews_kept)} rows | "
      f"{round(OUT_REVIEWS.stat().st_size/1024/1024, 2)} MB | "
      f"{books_with_reviews} books covered")

print("\nDone. Files written to /data/")
