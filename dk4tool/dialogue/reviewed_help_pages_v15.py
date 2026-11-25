"""Keep v14 page bytes while guarding the resolved current controls, labels and numerical boundaries."""
from dk4tool.dialogue import reviewed_help_pages_v14 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
    "        title,english=row['heading'],row['english']":
    """        title,english=row['heading'],row['english']
        resolved={133:['Sailing 80','Observe 70','Vigor 30','Survey 120','Sailing 60','Command 30','Speech 100','Swords 90','Aim 90','Survey 130','Observe 150','Aim 70','Vigor 130','Speech 160','Guile 120','Finance 100'],
            138:['press Y to equip or use'],139:['Left or Right','press Y for Auto','Flagship gives priority','Even assigns the same percentage','Minimum assigns only'],
            148:['Trade House'],152:['Products'],189:['Coerce'],191:['Trade House'],194:['Products','Trade House','five specialties'],
            201:['exceeds 500 percent']}
        if topic in resolved and any(term not in english for term in resolved[topic]):
            raise ValueError('Resolved current Help control,active label orsource numerical boundary differs')
        if topic==194 and title!='Products (Raw Materials)':raise ValueError('Bound Product heading differs')
        if topic in [133,168,170,175,177] and any(term in english for term in ['Health 30','Health 130','Social','Tactics 120','HP and Health']):
            raise ValueError('Inactive skill labels must not replace active Vigor,Speech,Guile')""",
})
env={**previous.plan_articles.__globals__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-native-pages-with-confirmed-control-term-andthreshold-contracts','exec'),env)
plan_articles=env['plan_articles']
