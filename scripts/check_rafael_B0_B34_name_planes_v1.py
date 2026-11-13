"""Check the 39 unchanged progressive labels separately from full-name repairs."""
import sys
from scripts import check_rafael_B301_B320_name_planes_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B0_B34_v1 import IDENTITY as BINDINGS_PATH
from scripts.qualify_rafael_B0_B34_names_v1 import LABELS
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT as BASE_ROOT
from scripts.source_locked_derivation_v5118 import checked_text


NAMES=BASE_ROOT/'progressive_name_decisions_v1.json'
RETAINED=BASE_ROOT/'retained_name_planes_v2/native_name_planes.json'
TEMPLATE=previous.TEMPLATE
source=checked_text(previous.source,{
    "len(doc['records'])==len(bound['name_bindings'])==19":"len(doc['records'])==len(bound['name_bindings'])==39",
    "len(doc['records'])==19":"len(doc['records'])==39",
})


def prepare():
    assert not NAMES.exists()
    labels=load(LABELS)
    assert len(labels['records'])==39
    rows=[]
    for row in labels['records']:
        text=row['approved_forms']['progressive-nameplate']
        before=next(c['text'] for c in row['current_consumers'] if c['consumer']=='progressive-nameplate')
        assert text==before
        rows.append({**row,'english':text,'decision':'retention','consumer_scope':'progressive-nameplate-only',
            'full_catalogue_decision':row['decision'],
            'source_reference':[f['source'] for f in row['source_andcurrent_fields']],
            'current_reference':[f['current'] for f in row['source_andcurrent_fields']]})
    save(NAMES,{**labels,'records':rows,'all_progressive_forms_retained_full_name_repairs_separate':True})


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        assert not sys.argv[1:]
        exec(compile(source,__file__+'::same-native-style11-consumers','exec'),globals())
