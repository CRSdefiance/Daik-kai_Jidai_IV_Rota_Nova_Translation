"""Source-reviewed prose and native compact-name supplement; formatting still open."""
from copy import deepcopy
from pathlib import Path
import struct
import unicodedata
from collections import Counter
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_declaration_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1023')
MANUSCRIPT=Path('translations/reinforcement_sniping_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v997_candidate.nds')
SOURCE=Path('work/analysis/reinforcement_sniping_v1022b/source_context_packet.json')
TEXT={
1911:"Admiral! It looks like a fleet from %s will help us!",
1912:"Admiral! A fleet from %s is coming to help us!",
1913:"Admiral! Looks like a fleet from %s is joining our side!",
1914:"Admiral! It seems a fleet from %s will lend us a hand!",
1915:"I hear a fleet from %s will fight alongside us too!",
1916:"Admiral! It seems a fleet from %s is coming to our aid!",
1917:"It looks like %s's nearby fleet will provide covering fire!",
1918:"Admiral! It looks like %s's nearby fleet will provide covering fire!",
1919:"%s's nearby fleet will lend us a hand!",
1920:"I hear %s's nearby fleet will provide covering fire! What a relief!",
1921:"It looks like %s's nearby fleet will help us too!",
1922:"I hear %s's nearby fleet will lend us a hand!",
1923:"It seems %s's nearby fleet will join our side too!",
1924:"Admiral, we've shot the enemy admiral! Victory is ours!",
1925:"Yes! We shot the enemy admiral! We won!",
1926:"We shot the enemy admiral! Victory is ours!",
1927:"A direct hit on the enemy admiral! We won!",
1928:"Admiral, we shot their admiral! We've won!",
1929:"Our shot hit the enemy admiral! Hooray! We won!",
1930:"We've shot the enemy admiral! Victory is ours!"}
GLOSS={
1911:'The speaker politely tells the admiral that a fleet belonging to the named faction apparently will assist our side.',
1912:'The speaker tells the admiral in a casual,upbeat voice that the named faction fleet will give us a hand.',
1913:'The speaker reports to the admiral that the named faction fleet appears to be joining our side,with a firm informal tone.',
1914:'An older speaker tells the admiral that the named faction fleet apparently will cooperate with us.',
1915:'The youthful speaker says they hear that the named faction fleet will also fight alongside us.',
1916:'A politely emphatic older speaker reports to the admiral that the named faction fleet appears to be helping our side.',
1917:'The speaker says a nearby fleet under the named commander apparently will give us covering fire.',
1918:'The speaker formally reports to the admiral that a nearby fleet under the named commander appears to be providing covering fire.',
1919:'The upbeat speaker says the nearby fleet under the named commander will give us a hand.',
1920:'The speaker hears that a nearby fleet under the named commander will provide covering fire,and expresses relief.',
1921:'An older speaker says the named commanders nearby fleet also appears to be helping us.',
1922:'The youthful speaker says they hear that the named commanders nearby fleet will help us.',
1923:'A politely emphatic older speaker says the named commanders nearby fleet also seems to be joining our side.',
1924:'The Lookout politely tells the admiral that the enemy admiral has been successfully shot,and declares our victory.',
1925:'The excited Lookout celebrates successfully shooting the enemy admiral and emphatically says we have won.',
1926:'A confident feminine-voiced Lookout reports a successful shot at the enemy admiral and declares our victory.',
1927:'A rough,terse Lookout announces a successful hit on the enemy admiral and says we have won.',
1928:'An older Lookout addresses the admiral,reports a successful shot at the enemy admiral,and declares our victory.',
1929:'The childlike Lookout says a bullet hit the enemy admiral,cheers,and celebrates our victory.',
1930:'A politely emphatic older Lookout reports shooting the enemy admiral and declares our victory.'}


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists();ROOT.mkdir(parents=True)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1199
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    context=read(SOURCE)
    assert len(context['all624_actor_voice_selections'])==624 and len(context['all24_original_role_wrapper_cases'])==24
    assert len(context['all_original_reinforcement_argument_fragments'])==40
    assert len(context['all_original_covering_fire_argument_fragments'])==57
    rom,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    old=current_entries(common,arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    raw=Path(context['source_snapshot']['path']).read_bytes();cpu,get=get_machine(arm,raw)
    actors=get(0xCB184);hero=get(0x7F244);names=[]
    for actor in range(208):
        obj=actors+0x19E4 if actor==hero else actors+4+actor*32
        vt=struct.unpack('<I',cpu.mem_read(obj,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
        at=get(getter-0x02000000,obj);value=bytes(cpu.mem_read(at,256)).split(b'\0')[0]
        assert value and b'\n' not in value and b'%' not in value
        names.append({'actor_ID':actor,'name_hex':value.hex(),'native_compact_label':value.decode('cp932'),
            'normalized_for_documentation_only':unicodedata.normalize('NFKC',value.decode('cp932')),
            'native_getter':getter,'current_player_captain':actor==hero,
            'regular_officer_ID_for_additional_captain_format_cases':actor<28})
    assert names[hero]['name_hex']==b'Hodram'.hex()
    assert bytes.fromhex(names[20]['name_hex']).startswith(bytes.fromhex('8265'))
    supplement=ROOT/'compact_name_and_source_meaning_supplement.json'
    save(supplement,{'source_context':str(SOURCE),'source_context_sha256':sha(SOURCE.read_bytes()),
        'source_context_wording_erratum':'The covering-fire native getter returns a compact commander label/given name,such as Hodram,not the full name plaque Hodram Joakim Bergstrom. The earlier packet field named full_name is superseded by this exact byte catalog;all57 original argument-fragment results remain valid.',
        'all208_native_compact_actor_labels':names,
        'full_width_F_leading_labels_preserved_as_exact_CP932_bytes':[n for n in names if not bytes.fromhex(n['name_hex']).isascii()],
        'regular_officer_0_27_catalog_is_format_stress_not_earned_captain_appointments':True,
        'all57_fleet_labels_include_nonplayer_fleets_for_format_stress_only_covering_fire_source_requires_other_player_fleet':True,
        'reinforcement_percent_s_is_complete_faction_label':True,
        'covering_fire_percent_s_is_compact_commander_label':True,
        'retain_explicit_covering_fire_in1917_1918_1920':True,
        'shot_reports_do_not_add_death_or_new_kind_of_battle_reward':True,
        'all_names_bytes_and_source_runtime_unchanged':True})
    records=[]
    for n in range(1911,1931):
        family='reinforcement' if n<1917 else 'covering_fire' if n<1924 else 'admiral_shot'
        role=context['tables'][family]['speaker_role'];ids=context['tables'][family]['voice_IDs']
        voices=[v for v,i in enumerate(ids) if (ids[0] if i==-1 else i)==n]
        actor_ids=[{0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:19}[v] for v in voices]
        previous=unicodedata.normalize('NFKC',old[n].text.decode('cp932'))
        retain=TEXT[n]==' '.join(previous.split())
        assert retain==(n in (1921,1922,1923,1924))
        note=('Use a fleet from the complete faction label,rather than treating that label as a persons name. Preserve the announcement and source voice;no fleet is invented or spawned by translation.' if family=='reinforcement' else
            'Preserve the compact commander label supplied by the original native getter. Use its possessive for natural English. Keep nearby and any report/hearsay/relief/also cue. Where the source says covering fire,retain that explicit action;other assistance variants do not gain it.' if family=='covering_fire' else
            'Use complete natural sentences matching the Lookouts successful-shot and victory announcement. A hit or shot does not assert that the enemy admiral died. Preserve the speakers excitement,formality and address without adding an event or reward.')
        if retain:note+=' The current normalized English wording already preserves those facts and reads naturally;retain the wording while removing only legacy encoding/layout debt through the mapped compiler.'
        scene=('Original775EC/778D4 announcement follows the separately selected614-621 fleet-sighting/battle-preparation notice. The helper picks an existing supporting faction fleet and supplies the supporting faction objects virtual-name label.' if family=='reinforcement' else
            'Original70E4C announces nearby support after the original70BF8 scan finds another valid player-faction fleet and original2CE90 admits it. Fleet3697C returns its commander object;virtual20 supplies the compact commander label.' if family=='covering_fire' else
            'Original73BA0 announces a successful Lookout shot at the enemy flagship. The original branch uses role7 stat6 above150 and its own RNG2000 comparison,before original capture/battle-resolution calls. No outcome is assigned by this review.')
        records.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':family,'consumer':'native-speech-announcement',
            'speaker':('Player First Mate' if role==1 else 'Player Lookout')+' or original native fallback; voice classes '+','.join(map(str,voices)),
            'source_speaker_role':role,'source_voice_classes_including_native_fallback':voices,'representative_actor_IDs':actor_ids,
            'context':scene+' Voice-table entries are independent alternatives,not sequential dialogue. Preserve the real current captain and actor identities. Actual scene activation and outcome verification remain pending.',
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'canonical_source_hex':accepted[n].text.hex(),'current_reference':reference(old[n]),'current_text_hex':old[n].text.hex(),
            'current_English':old[n].text.decode('cp932'),'source_meaning':GLOSS[n],'english':TEXT[n],
            'localization_note':note,'editorial_decision':'retain' if retain else 'revise',
            'native_argument_count':int(n<1924),'native_argument_kind':'complete-faction-label' if family=='reinforcement' else 'compact-commander-label' if family=='covering_fire' else None,
            'source_native_macros':[], 'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert Counter(r['editorial_decision'] for r in records)=={'revise':16,'retain':4}
    document={'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'reinforcement-sniping-native-post-expansion-35x4-v1',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'20-source-context-prose-reviewed-format-runtime-native-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),
        'native_context_proof':str(SOURCE),'native_context_proof_sha256':sha(SOURCE.read_bytes()),
        'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':records}
    save(MANUSCRIPT,document)
    save(ROOT/'editorial_ledger_before_prose.json',ledger)
    ledger['records_with_source_and_prose_pass']+=20;ledger['records_with_source_prose_drafts']+=20
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=20
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*range(1911,1931)]
    ledger['active_source_prose_drafts']['native_message_IDs']=deepcopy(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['active_source_prose_drafts']['manuscripts'].append(str(MANUSCRIPT))
    ledger['active_source_prose_drafts']['status']='three-older-context-pending-and20-reinforcement-covering-fire-shot-prose-native-actual-pending'
    ledger['reinforcement_sniping_v1023']={'native_message_IDs':list(range(1911,1931)),
        'manuscript':str(MANUSCRIPT),'source_context':str(SOURCE),'name_supplement':str(supplement),
        'source_prose_reviews_added':20,'completed_entries_added':0,'revisions':16,'retained_wordings':4}
    checkpoint=('V1023 reviews20 reinforcement,covering-fire and Lookout-shot announcements1911-1930:16 proposed revisions,4 retained wordings.624 original voice selections,24 role wrappers,40 faction-argument fragments and57 compact-commander argument fragments bind the three source families. Reinforcement uses complete faction labels;covering fire uses compact commander names,with exact protected leading-F bytes retained. Explicit covering fire and successful-shot/victory meaning are restored without adding deaths. Formatting/runtime/copy/registered integration/actual gates remain pending;no completed credit. V997 stays current;1196 complete,1219 source/prose. Full editorial and separate graphics goals remain open.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1023-reinforcement-sniping-source-prose',
        'proof':str(SOURCE),'manuscript':str(MANUSCRIPT),'source_prose_reviews_added':20,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:22 battle-declaration entries completed with actual scenes and exact patch',
        'this_goal_turn_classification':'progress:three original speaker/name consumers mapped and20 source-prose reviews recorded',
        'full_goal_complete':False})
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    save(ledger_path,ledger)
    doc_path=Path('docs/reinforcement_sniping_v1023_source_prose.md');assert not doc_path.exists()
    doc_path.write_text('# V1023: reinforcement,covering-fire and shot announcements\n\n'+checkpoint+'\n\nThe source fragment tests bridge only message loading and popup boundaries. They prove roles,voice selection and exact arguments;they do not prove entire eligibility branches or actual gameplay. The compact-name supplement corrects the initial full-name label:the current captain getter returns Hodram,and other captains likewise use compact labels. All raw bytes are preserved,including leading fullwidth Latin F in Fernando/Fernan and three noncaptain stress labels. The native source filters covering-fire support to another player-faction fleet;nonplayer labels in the broad57-name catalog are format stress,not claimed valid own-fleet appointments.\n\nNo ROM,patch,registry,actor identity or original save changes. Next:compile one paragraph before native expansion,review native line boundaries and full glyphs for faction/commander names,then register and verify actual scenes. The three older750-752 drafts and the wider shared/route/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain unfinished.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1023: reinforcement and shot source/prose review\n\n'+checkpoint+' See [V1023 review](reinforcement_sniping_v1023_source_prose.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V1023 Reinforcement and shot source prose');assert not archive.exists();files=[]
    for p in (SOURCE,SOURCE.parent/'original_source_fragments.json',supplement,MANUSCRIPT,ledger_path,doc_path,Path(__file__),
              Path('scripts/research_reinforcement_sniping_v1022b.py')):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert p.read_bytes()==target.read_bytes();files.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':files,'all_hashes_verified':True,'no_ROM_or_save_duplicated':True})
    print('20 source/prose reviews:16 revisions4 retained.1219 source/prose;1196 complete unchanged. Native formatting/integration/actual remain.',flush=True)


if __name__=='__main__':main()
