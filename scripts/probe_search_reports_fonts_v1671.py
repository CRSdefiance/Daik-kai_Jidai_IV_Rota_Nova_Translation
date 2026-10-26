"""Successor:count-neutral loss label and explicit nonmultiples-of-five stress."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/probe_search_reports_fonts_v1667.py').read_text(encoding='utf-8')
    for a,b in [('work/analysis/search_reports_fonts_v1667','work/analysis/search_reports_fonts_v1671'),
                ('work/analysis/search_reports_payload_v1666','work/analysis/search_reports_payload_v1670'),
                ('translations/search_reports_editorial_manuscript_v2.json','translations/search_reports_editorial_manuscript_v3.json')]:
        assert source.count(a)==1;source=source.replace(a,b)
    old="0<=native['source_amounts'][0]<=4650 and 0<=native['source_amounts'][1]<=3875"
    assert source.count(old)==1
    source=source.replace(old,old+" and all(v%5==0 for v in native['source_amounts'])")
    source=source.replace('outside_original_quantity_bounds_CPU_stress_only','outside_original_quantity_domain_CPU_stress_only')
    source=source.replace('outside_source_bounds_stress_findings','outside_source_domain_stress_findings')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
