"""Check comparison-stage logical prose; this does not approve native formatting."""
import argparse
import re
import unicodedata
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--reject-legacy-name',nargs='*',default=[])
    parser.add_argument('--allowed-non-ascii-id',nargs='*',default=[])
    args=parser.parse_args();assert not args.out.exists()
    doc=load(args.manuscript);errors=[];symbols=[]
    ids={r['id'] for r in doc['records']};assert len(ids)==len(doc['records'])
    assert set(args.allowed_non_ascii_id)<=ids
    for row in doc['records']:
        text=row['english'];ident=row['id']
        expected=row.get('source_macros',dict(FI=0,FA=0,FO=0))
        actual={m:len(re.findall(r'\{MACRO:'+m+r'\}',text)) for m in ['FI','FA','FO']}
        if expected!=actual:errors.append(dict(id=ident,kind='macro counts',expected=expected,actual=actual))
        if text.encode('cp932').decode('cp932')!=text or text!=text.strip() or any(x in text for x in ['\n','\t','  ','{LB','{ALIGN','{PAD}','%']):
            errors.append(dict(id=ident,kind='CP932 orlogical paragraph'))
        for name in args.reject_legacy_name:
            if re.search(r'\b'+re.escape(name)+r'\b',text,re.I):errors.append(dict(id=ident,kind='scoped legacy name',name=name))
        # Object phrases such as find this man are valid; only flag detached self-reference leads.
        if re.search(r'(?:^|[.!?]\s+)(?:this servant|this scholar|this man)\b',text,re.I):
            errors.append(dict(id=ident,kind='self-reference lead needs review'))
        if any(ord(c)>127 for c in text):
            source=unicodedata.normalize('NFKC',row['source_Japanese'])
            assert ident in args.allowed_non_ascii_id and unicodedata.normalize('NFKC',text)==source
            symbols.append(dict(id=ident,english=text,exact_NFKC_source_content=True))
    assert not errors,errors
    assert all(row['review']['formatting'] is False for row in doc['records'])
    save(args.out,dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
                       records=len(ids),macro_counts_CP932_logical_paragraphs_andscoped_name_checks_pass=True,
                       rejected_legacy_names=args.reject_legacy_name,intentional_source_symbol_records=symbols,
                       no_authored_wraps_alignment_padding_orliteral_percent_bytes=True,
                       all_five_gate_completions=0,native_formatting_visual_stored_gameplay_andrelease_pending=True,
                       new_credit=0,new_ROMs=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(records=len(ids),draft_consistency='pass',intentional_symbol_records=len(symbols),native_formatting_approvals=0,new_credit=0))
