"""Bind authored scoped layout preferences to complete source/current/prose hashes."""
import argparse
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','preferences','out']:ap.add_argument('--'+key,type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    doc,prefs=map(load,[args.manuscript,args.preferences]);rows={r['id']:r for r in doc['records']}
    for key,entry in prefs['records'].items():
        row=rows[key]
        assert entry['source_hex']==row['source_hex'] and entry['current_hex']==row['current_hex']
        assert entry['exact_logical_English']==row['editorial_logical_English']
        entry['bindings']={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}
        assert entry.get('reason') or entry.get('QA_line_ending_retention',{}).get('reason')
    prefs.update(preference_binding_only_no_new_layout_orapproval=True,
        binding_evidence={str(p):digest(p) for p in [args.manuscript,args.preferences,Path(__file__)]})
    save(args.out,prefs);print('Bound',len(prefs['records']),'preferences to exact source/current/logical prose; no text changes.')


if __name__=='__main__':main()
