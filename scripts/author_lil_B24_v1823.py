"""Natural faithful B24 successor prose; formatting/integration remain blocked."""
from copy import deepcopy
from pathlib import Path
import re
import unicodedata
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_prose_v1823')
OUT=Path('translations/lil_trade_routes_officers_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/lil_B24_source_v1822/B24_clean_current_native_source_and_town_predicates.json')
INVENTORY=Path('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
PROSE=[
 (9,'Camille encourages contracts with many towns;even a one percent stake in each allows the fleet to establish its own trade routes.',
  "Let's keep this up and sign contracts with more towns. Even a one percent share in each town will let us establish our own trade routes.",
  'Restore the explicit one percent minimum andper-town contracts. Use the word percent to avoid inventing a native printf argument;do not shorten for allocation.'),
 (12,'Lil asks about the trade routes Camille just mentioned.','Trade routes?',
  'Echo the immediately preceding term naturally;no new route mechanic is added.'),
 (16,'Camille confirms andsays those routes are especially useful if the fleet has a surveyor.',
  'Yes. With a surveyor aboard, those routes will really come in handy.',
  'Keep the conditional role-to-route benefit. Do not add an automatic travel instruction absent from this speech.'),
 (19,'Lil gives a brief,noncommittal acknowledgment.','Huh.',
  'Retain the existing brief thoughtful response. It follows her question andexplanation;it is not a demand for repetition ornew factual claim.'),
 (23,'With a surveyor needed,the fleet is short ofpeople;Camille says they should gather more companions who have experience at sea.',
  "If we're going to have a surveyor too, we'll need more people. We'd better find more companions with experience at sea.",
  'The fleet is understaffed;the surveyor does not personally require extra assistants. Keep companions broad here so Lils following misunderstanding about ordinary sailors remains natural.'),
 (26,'Lil suggests recruiting sailors at a tavern if they are short ofsailors.',
  "If we're short on sailors, can't we hire some at a tavern?",
  'Restore her practical question andconditional wording rather than issue a command to the player.'),
 (29,'Camille means the officers who command sailors;growing the fleet will require companions with diverse talents.',
  "I mean officers, the people who command the sailors. To build up our fleet, we'll need companions with all kinds of talents.",
  'Use officers for the party-member sense of航海士 andexplicitly preserve their command role. This explains the misunderstanding without inventing a relationship ornew rank.'),
 (32,'Lil asks how to find those companions.','How do we find them?',
  'Retain the method question;do not change it into only a location question.'),
 (36,'Camille says they must rely on luck,butmay find companions bysearching large cities.',
  "We'll have to rely on luck. We might find some in the bigger cities.",
  'Preserve chance andpossibility rather than promise recruitment oradd a search guarantee.'),
 (39,'Lil repeats the idea oflarge cities thoughtfully.','Big cities...',
  'Use the natural plural echo ofthe preceding generic city advice;keep the pause.'),
 (43,'Camille suggests going first to Mediterranean towns such as Genoa orIstanbul;hehas heard there are many seafarers in that region.',
  "Right. Let's head for a Mediterranean city first, like Genoa or Istanbul. I hear there are lots of seafarers around there.",
  'Restore the named Istanbul destination andhearsay. The Japanese says many seafarers,not specifically seasoned sailors;do not substitute Ottoman ports for the explicit city.'),
 (46,'Lil says signing contracts with towns along their route would accomplish two purposes at once.',
  'Then we can sign contracts with the towns along the way, too. Two birds with one stone!',
  'Use the natural English equivalent ofthe source idiom andpreserve contracts enroute as the second benefit.'),
 (49,'Camille praises Lil as expected andenthusiastically confirms she is exactly right.',
  "That's our {MACRO:FI}! Exactly!",
  'Preserve the genuine FI name macro andthe source approving praise. The source-bound current native macro resolves FI to Lil for this actual captain;do not hardcode her name.')]


def visible(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()


if __name__=='__main__':
    assert not ROOT.exists()and not OUT.exists();ROOT.mkdir(parents=True)
    packet=read(PACKET);prior=read(INVENTORY);assert len(packet['records'])==13
    assert[r['record_index']for r in packet['records']]==[p[0]for p in PROSE]
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');raw=Path(prior['historical_verified_snapshot']).read_bytes()
    assert sha(raw)==prior['snapshot_sha256'];cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=actors+0x19E4
    assert get(0x7F244)==2 and get(0x2434C,9)==9 and get(0x2434C,2)==2
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    rows=[];macro_cases=[];allocations=[];profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    try:
        for source,(index,meaning,english,note)in zip(packet['records'],PROSE,strict=True):
            row=deepcopy(source);prefix=int(row['source_presentation_prefix_hex'],16);actor_ID=get(0x2434C,prefix)
            actor=captain if actor_ID==2 else actors+4+actor_ID*32
            current=bytes.fromhex(row['current_text_hex'])[1:]
            cpu.mem_write(0x02660000-16,b'\xA5'*2080);cpu.mem_write(0x02660000,current+b'\0')
            guarded_input=bytes(cpu.mem_read(0x02660000-16,2080));cpu.mem_write(0x02662000-16,b'\xA5'*4128)
            call(cpu,0x242C8,(0x02662000,0x02660000,actor),instruction_limit=400000)
            output=bytes(cpu.mem_read(0x02662000,4096)).split(b'\0')[0]
            assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
            assert bytes(cpu.mem_read(0x02660000-16,2080))==guarded_input
            assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xA5'*16
            assert bytes(cpu.mem_read(0x02662000+len(output)+1,4095-len(output)))==b'\xA5'*(4095-len(output))
            assert ('FI'in row['source_Japanese'])==('{MACRO:FI}'in english)
            decision='retain-wording'if visible(english.replace('{MACRO:FI}','Lil'))==visible(output.decode('cp932'))else'revise'
            row.update(source_meaning=meaning,english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english+'{PAD}',
                editorial_decision=decision,localization_note=note,current_native_macro_English=output.decode('cp932'),
                current_native_macro_output_hex=output.hex(),macro_probe_actor_ID=actor_ID,
                current_native_macro_entire4MiB_ABI_and_input_output_guards_exact=True,
                context='Lil SC2 B24 trade-route andofficer discussion,13 linear native speech objects. The full clean andcurrent block andboth immediate spoken neighbors were reviewed. '
                    'Original event24/category5/action25 selects B24 andrequires completed120;original not-in-Bruges condition andCamille presence are mapped. '
                    'The extra context prefix andfull activation remain unverified. These are not yet revised actual displays.',
                review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False})
            rows.append(row);macro_cases.append({'id':row['id'],'actor_ID':actor_ID,'output_hex':output.hex(),
                'all4MiB_ABI_and_input_output_guards_preserved':True})
            try:
                encoded=encode_fixed_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
                allocations.append({'id':row['id'],'fixed_source_allocation_encodes':True,'padding_bytes':encoded.padding_bytes,
                    'formatted_markup':encoded.formatted_markup,'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message}for d in encoded.diagnostics]})
            except ValueError as error:allocations.append({'id':row['id'],'fixed_source_allocation_encodes':False,'error':str(error),
                'faithful_prose_preserved_no_shortening_or_guard_relaxation':True})
    finally:cpu.hook_del(hook)
    assert sum(r['editorial_decision']=='retain-wording'for r in rows)==1
    doc={'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-fixed-v1','dialogue_profile':profile.name,'file_path':'/data/SC2.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'13-source-context-prose-reviewed;native-format-reference-map-integration-andactual-pending',
        'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'approved_names':['Rafael','Joakim','Maria','Camille'],'records':rows,
        'scope':'Complete B24 linear speech inventory. Source/prose draft only;existing B22 profile is an allocation probe,not B24 display orrelease approval.'}
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'formatting'in str(error).lower();doc['release_validation_rejects_unapproved_formatting']=True
    else:raise AssertionError('Unreviewed formatting passed release validation')
    save(OUT,doc)
    save(ROOT/'native_macros_and_allocation_probe_NOT_display_approval.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_packet':str(PACKET),'source_packet_sha256':sha(PACKET.read_bytes()),'macro_cases':macro_cases,
        'FI_actual_default_name_expansion':'Lil','fixed_allocation_cases':allocations,
        'source_prose_records':13,'proposed_revisions':12,'retained_wordings':1,
        'fixed_encodes':sum(r['fixed_source_allocation_encodes']for r in allocations),
        'fixed_failures':sum(not r['fixed_source_allocation_encodes']for r in allocations),
        'no_ROM_registry_or_completed_editorial_credit':True,'native_font_actual_bounds_trigger_andscene_transition_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'source_prose_records':13,'proposed_revisions':12,'retained':1,
        'fixed_encodes':sum(r['fixed_source_allocation_encodes']for r in allocations),
        'fixed_failures':sum(not r['fixed_source_allocation_encodes']for r in allocations),
        'release_rejects_unreviewed_formatting':True,'completed_entries_added':0},flush=True)
