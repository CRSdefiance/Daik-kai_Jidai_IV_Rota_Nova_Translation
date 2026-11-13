"""Join exact scoped name evidence,bind six native roles,andstage two unlocalized-particle findings."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/analysis/Rafael351_identity_qualification_v1_20261105')
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
FRESH = Path('work/analysis/Rafael351_scoped_names_v1_20261105/names.json')
DYNAMIC = FRESH.with_name('dynamic_roles.json')
PRIORS = [Path('work/analysis')/name/file for name,file in [
    ('Rafael241_names_terms_20261105','names_terms_roles_andconsumer_dependency_qualification_v1.json'),
    ('Rafael261_names_terms_20261105','names_macros_andconsumer_dependency_qualification_v1.json')]]
REASONS = {
0:'Retain approved Rafael Castor andcaptain0. Hiscare forClau andrespect forJulio donotcreate family relationships.',
3:'Retain approved Maria Li,withMaria Huamei Li inthe fullcatalogue. Herbandit confrontation preserves the source’s political/cultural context withoutnewrank oridentity.',
4:'Retain Janus Pasar andhis measured explanatory voice;no newprofessional title isadded.',
5:'Retain Claudio Manaus andthe explicit Clau nickname whereitappears inthe Japanese. Preserve fullClaudio inArcadius’s alarm.',
6:'Retain Julio Erneco. HeisCristina’s grandfather andRafael’s mentor;my boy hereisan idiomatic familiar address,nota statement offatherhood.',
8:'Retain Arcadius Eudoxios andthe distinct fullcatalogue Eirene component. The source’s private gender-reveal asides arepreserved withouta newpublic identity announcement.',
10:'Retain Xien Yan asthe established phonetic adaptation;the rebuke tobandits needsno invented officer rank.',
19:'Retain Carlo Sinat asthe established readable adaptation ofカルロ・シナート;his artifact knowledge doesnotjustify adding a scholar title.',
20:'Retain Gerhard Almsfeld fromthe exact earlier scoped proof;the rough battle response addsno nationality orrank.',
25:'Retain Yifa Sol asthe established phonetic name;the short battle reassurance addsno unspoken relationship.',
26:'Retain Haldin Mayer fromthe exact earlier scoped proof. Theflirtation advice isa character’s joking justification,notan invented biography orrelationship.',
30:'Retain Dinis Albuquerque inthe progressive header. Hisfullcatalogue particle remains Japanese andneedsa scoped de correction.',
31:'Retain Pedro Valdes andfullPedro de Valdes;the body’s Valdes address correctlyuses hisfamily name. No title isadded.',
48:'Retain Simon Linares andthe source-defined enemy battle perspective withouta newrank label.',
49:'Retain Alonso Rosa andfullAlonso de Rosa. The formation order doesnotcreate anextra military title.',
59:'Retain Garcia Oviedo inthe progressive header. Hisfullcatalogue particle remains Japanese andneedsa scoped de correction.',
151:'Retain Sailor forordinary public dialogue andfallback headers. Do notexpose unused Retainer metadata orassign everydynamic role a fixed person.',
163:'Retain Boy for男の子. Hisrelationship withthe grandfather isexplicit inthe exchange,butthe label needsno invented age orfamily name.',
170:'Retain Mysterious Old Man for謎の老人. Thisisanatural RPG role preserving the source’s deliberate unknown identity;do notlabel himRafael’s grandfather.',
179:'Retain Villager for村民. Offering theknife andspeaking forthe tribe doesnotestablish Chief,Priest oranother rank.',
180:'Retain Bandit for野盗. Thevillage grievance doesnotjustify adding Leader,ethnicity ormilitary rank.',
198:'Retain Benazir forベナジール. Reciprocating a gift witha landmark tip doesnotestablish a romance ornewnationality.',
}


def string(raw,pointer):
    if not pointer:return b''
    at = pointer-BASE
    assert 0 <= at < len(raw)
    return raw[at:raw.index(0,at)]


if __name__ == '__main__':
    assert not ROOT.exists()
    current,fresh,dynamic = map(load,[CURRENT,FRESH,DYNAMIC])
    ctx = RegisteredRuntime(current['runtime']['release_proof'],current['runtime']['startup_proof'],captain=0)
    assert current['runtime'] == fresh['runtime'] == dynamic['runtime'] == ctx.receipt()
    priors = [(path,load(path)) for path in PRIORS]
    for path,prior in priors:
        previous = RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=0)
        assert ctx.arm == previous.arm and ctx.common == previous.common and ctx.actor_root == previous.actor_root
        assert ctx.actor_bytes == previous.actor_bytes and ctx.image.read_file('/GRP/KANJI.FNT') == previous.image.read_file('/GRP/KANJI.FNT')
    actors = sorted({r['source_selector'] for g in current['groups'] for r in g['records'] if r['source_selector'] < 207})
    assert actors == sorted(REASONS) and len(actors) == 22
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    a,b = [struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [jp,ctx.arm]]
    bindings = []; names = []
    for actor in actors:
        fields = []
        for column in [0,4,8]:
            source_at,at = a+32*actor+column,b+32*actor+column
            sp,cp = struct.unpack_from('<I',jp,source_at)[0],struct.unpack_from('<I',ctx.arm,at)[0]
            sr,cr = string(jp,sp),string(ctx.raw,cp)
            fields.append(dict(column=column,source=dict(field_offset=source_at,pointer=sp,hex=sr.hex(),text=sr.decode('cp932')),
                current=dict(field_offset=at,pointer=cp,hex=cr.hex(),text=cr.decode('cp932'))))
        if actor in fresh['actors']:
            source_forms = [r for r in fresh['clean_names']['rows'] if r['actor_ID'] == actor]
            forms = [r for r in fresh['current_names']['rows'] if r['actor_ID'] == actor]
            proof = FRESH;mode = 'fresh exact-current intrinsic getters;newly scoped orolder complete ARM9 dependency differs'
        else:
            proof,prior = next((p,d) for p,d in priors if actor in d['actors'])
            entry = next(r for r in prior['name_bindings'] if r['actor_ID'] == actor)
            assert fields == entry['source_andcurrent_fields']
            source_forms,forms = entry['clean_consumers'],entry['current_consumers']
            mode = 'exact full ARM9/COMMON/font/actor-array/individual-field reuse;no newgetter run'
        assert len(forms) == 2 and {r['consumer'] for r in forms} == {'progressive-nameplate','full-catalogue'}
        public = next(r for r in forms if r['consumer'] == 'progressive-nameplate')
        assert public['text'].isascii()
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,clean_consumers=source_forms,
            native_proof=str(proof),native_proof_sha256=sha(proof.read_bytes()),qualification=mode))
        names.append(dict(id=f'ACTOR{actor}_RAFAEL121_140_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=public['text'],speaker=public['text'],source_meaning='Source-defined proper name orpublic role fromthe exact fields/native consumers.',
            context='Complete reviewed SC0 B121–B140 exchanges;onlythe visible consumer andsupported identities arecovered.',
            decision='retention',finding=REASONS[actor],retention_reason=REASONS[actor],localization_note=REASONS[actor],
            source_reference=dict(actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=public['text_hex'],native_proof=str(proof),native_proof_sha256=sha(proof.read_bytes())),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    role_rows = dynamic['native_roles']['rows']
    assert [r['source_selector'] for r in role_rows] == [207,208,209,214,215,220]
    assert len(dynamic['source_records']) == 37 and dynamic['native_roles']['all_actor_role_RNG_and_unowned4MiB_exact']
    assert role_rows[0]['resolved_actor_ID'] == 0 and all(r['resolved_actor_ID'] == 151 for r in role_rows[1:])
    donor = next(r for r in bindings if r['actor_ID'] == 31)['source_andcurrent_fields'][1]['current']
    assert donor['text'] == 'de' and bytes.fromhex(donor['hex']) == b'de'
    particle_changes = []
    for actor,wanted in [(30,'Dinis de Albuquerque'),(59,'Garcia de Oviedo')]:
        binding = next(r for r in bindings if r['actor_ID'] == actor)
        field = binding['source_andcurrent_fields'][1]
        assert field['source']['text'] == field['current']['text'] == 'デ'
        actual = next(r for r in binding['current_consumers'] if r['consumer'] == 'full-catalogue')['text']
        assert actual.replace('デ','de') == wanted
        at = field['current']['field_offset'];raw = ctx.arm[at:at+4]
        assert struct.unpack('<I',raw)[0] == field['current']['pointer']
        particle_changes.append(dict(actor_ID=actor,current_full_name=actual,reviewed_full_name=wanted,
            source_reference=field['source'],current_reference=field['current'],
            proposed_pointer_field_offset=at,current_field_hex=raw.hex(),proposed_field_hex=struct.pack('<I',donor['pointer']).hex(),
            existing_readonly_de_pointer=donor['pointer'],existing_de_bytes_hex='6465',
            never_rewrite_the_shared_Japanese_string_globally=True,
            proposal_only_not_a_ROM_orfield_write=True,native_target_display_stored_actual_andregistered_work_pending=True))
    ROOT.mkdir(parents=True)
    name_path = Path('translations/rafael_B121_B140_scoped_names_review_v1.json');assert not name_path.exists()
    save(name_path,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],records=names,
        public_name_retentions=22,public_name_changes=0,all22_name_formatting_gates_pending=True,
        two_full_catalogue_particle_corrections_required=particle_changes,
        ordinary_progressive_headers_do_not_contain_the_two_bad_particles=True,
        global_207_name_andfullcatalogue_UI_review_still_open=True,new_credit=0,guide_photos=False))
    save(ROOT/'qualified_names_roles_andparticle_findings.json',dict(runtime=ctx.receipt(),actors=actors,name_bindings=bindings,
        fresh_actors=fresh['actors'],qualified_reused_actors=sorted(set(actors)-set(fresh['actors'])),
        scoped_name_review=str(name_path),scoped_name_review_sha256=sha(name_path.read_bytes()),
        dynamic_role_proof=str(DYNAMIC),dynamic_role_proof_sha256=sha(DYNAMIC.read_bytes()),dynamic_roles=role_rows,
        no_static_lookup_of_selectors207_through223=True,no_original_conditional_role_assignment_orUI_visit_claim=True,
        two_unlocalized_full_name_particles=particle_changes,no_RAM_ROM_field_orregistry_mutation=True,
        no_formatting_orcompletion_credit=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,FRESH,DYNAMIC,*PRIORS,name_path,Path(__file__)]}))
    print('22 scoped publicnames retained:14 fresh/eight exact reuses;six native roles/37 source entries bound. Two fullcatalogue Japanese particles needscoped de corrections;proposal only,no ROM change orcredit.')
