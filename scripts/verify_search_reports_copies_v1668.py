"""Explicit copy/cache successor for revised11-report payload1666."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/verify_search_reports_copies_v1664.py').read_text(encoding='utf-8')
    source=source.replace('work/analysis/search_reports_payload_v1661','work/analysis/search_reports_payload_v1666').replace('work/analysis/search_reports_copies_v1664','work/analysis/search_reports_copies_v1668')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
