"""Trace Follower's F and Diogo's source de component without changing ROM bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/propose_editorial_name_fields.py').read_text(encoding='utf-8'),{
    "ROOT=Path('work/analysis/Hodram_B91_B110_name_fields_20261101')":"ROOT=Path('work/analysis/Hodram_B111_B130_name_fields_20261101')",
    "Hodram_B81_B89_release_verified_20261101":"Hodram_B91_B110_release_verified_20261101",
    "SOURCE=Path('work/analysis/Hodram_B91_B110_clean_20261101/clean_name_fields.json')":"SOURCE=Path('work/analysis/Hodram_B111_B130_clean_20261101/clean_name_fields.json')",
    "(20,0,'Ｆernando','Fernando'":"(178,0,'Ｆollower','Follower'",
    "Retain the already established Fernando Dias spelling;normalize only the mismatched full-width initial F.":
        "Retain Follower for source信徒 in the complete sect exchange; normalize only its mismatched full-width F. Do not add a rank, plural group identity or pejorative.",
    "(22,8,'ダ','da'":"(43,8,'デ','de'",
    "Render the explicit source name componentダ as da,retaining Samwell andKhan. It is part of the full name,not a new title,rank,nationality orbiography;progressive Samwell Khan is unchanged.":
        "Render the explicit source componentデ as de in Diogo de Escante. Preserve progressive Diogo Escante and the source full name; infer no noble rank, nationality or additional biography. Shared owners remain a blocking ownership review until individually bound.",
})
exec(compile(source,__file__+'::source-owned-current-name-proposals-only','exec'),globals())
