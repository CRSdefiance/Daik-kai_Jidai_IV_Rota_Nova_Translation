"""Resolve proven native stat/room terms; leave three concrete control bindings open."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')

def plain(text):
    return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]',r'\1',text).split())

if __name__ == '__main__':
    prior_path = ROOT/'whole_article_comparisons_provisional_v1.json'
    binding_path = ROOT/'native_roles_rooms_andskills_v1.json'
    output = ROOT/'whole_article_comparisons_v2.json'
    assert not output.exists()
    prior, binding = map(load,[prior_path,binding_path])
    assert prior['current_ROM_sha256'] == binding['current_ROM_sha256']
    assert len(binding['native_roles']) == 16 and len(binding['stored_room_skill_andcommand_labels']) == 35
    records = deepcopy(prior['records'])
    for row in records:
        n = row['topic_id']
        old = row['english']
        if n == 110:
            row['english'] = "These are the rooms and stations where officers perform their assigned jobs. See [[111|Cabin]], [[112|Lounge]], [[113|Lumber Room]], [[114|Sickbay]], [[115|Galley]], [[116|Nursery]], [[117|Chapel]], [[118|Tactics Room]], [[119|Purser's Office]], [[120|Captain's Cabin]], [[121|First Mate's Office]], [[122|Helm]], [[123|Survey Room]], [[124|Lookout]], [[125|Mast]] and [[126|Deck]]."
            row['finding'] = 'Use recognizable native room labels, including Lounge, Sickbay, Nursery and Tactics. Rooms and stations naturally includes the mast, helm, lookout and deck. Descriptive Office/Cabin/Room words preserve context rather than mechanically copying every abbreviated label.'
        elif n in [116,117,118,121,126]:
            before,after = {116:('Vigor','Health'),117:('Speech','Social'),118:('Guile','Tactics'),121:('Speech','Social'),126:('Vigor','Health')}[n]
            assert before in row['english']
            row['english'] = row['english'].replace(before,after)
            row['finding'] = row['finding'] + ' Correct '+before+' to native '+after+' for the exact clean Japanese stat; preserve its numeric threshold and effects.'
        if row['english'] != old:
            row['decision'] = 'revision'
            row['retention_reason'] = None
        # Full English room descriptions may expand the short labels. These
        # titles specifically benefit from matching the displayed room name.
        heading = {105:'Deck View',106:'Personnel',114:'Sickbay',116:'Nursery',118:'Tactics Room',122:'Helm',124:'Lookout',125:'Mast',128:'Quarters',129:'Battery'}.get(n)
        if heading:
            row['heading'] = heading
            row['heading_localization_reason'] = 'Use the source-bound native room/consumer name; a descriptive room title is distinct from a body-wording retention.'
        row['localization_note'] = row['finding']
        pending = n in [103,104,106]
        row['review']['localization'] = not pending
        row['native_term_orcontrol_binding_pending'] = pending
        row['native_terms_andcontrols_binding_pending'] = pending
        row['native_binding'] = str(binding_path)
        row['native_binding_sha256'] = sha(binding_path.read_bytes())
        row['provisional_decision_may_change_after_binding'] = pending
        assert [int(t) for t in re.findall(r'\[\[(\d+)\|',row['english'])] == row['original_link_IDs']
        if row['decision'] == 'retention':
            assert plain(row['english']) == plain(row['current_English'].split('\n',1)[1])
            row['localization_note'] += ' Native role/skill terms match; fuller room descriptions are natural contextual expansions of the short UI labels.'
        assert row['english'].isascii() and '\n' not in row['english'] and '  ' not in row['english']
    assert sum(r['decision']=='revision' for r in records) == 12
    assert sum(all(r['review'][g] for g in ['source','context','localization','naturalness']) for r in records) == 27
    save(output,dict(format='dk4-help103-132-contextual-comparisons-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=records,records_count=30,proposed_revisions=12,justified_retentions=18,first_four_gates_passed=27,
        pending_localization_binding_topic_IDs=[103,104,106],all_fifth_gates_pending=True,
        current_ROM=prior['current_ROM'],current_ROM_sha256=prior['current_ROM_sha256'],
        source_draft=prior['source_draft'],source_draft_sha256=prior['source_draft_sha256'],
        current_packet=prior['current_packet'],current_packet_sha256=prior['current_packet_sha256'],
        prior_comparisons=str(prior_path),prior_comparisons_sha256=sha(prior_path.read_bytes()),
        native_binding=str(binding_path),native_binding_sha256=sha(binding_path.read_bytes()),
        all18_retained_bodies_word_exact_with_titles_reviewed_separately=True,
        all_text_formatting_representative_Help_display_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('30 contextual decisions:12 revisions/18 exact-body retentions;27 four-gate passes,103/104/106 control bindings and all display remain.')
