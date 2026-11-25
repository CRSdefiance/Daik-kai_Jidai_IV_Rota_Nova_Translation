"""Explicit prior-direct-speech successor for final reviewed11-report payload."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/verify_search_reports_escape_v1669.py').read_text(encoding='utf-8')
    source=source.replace('work/analysis/search_reports_payload_v1666','work/analysis/search_reports_payload_v1670').replace('work/analysis/search_reports_escape_v1669','work/analysis/search_reports_escape_v1673')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
