import html, math

rows=[l.rstrip("\n").split("\t") for l in open("roster.tsv") if l.strip()]

SECTOR_ORDER=["Food & beverage","Food trade","Consumer retail","Built environment",
              "Professional services","Sports & leisure","Industrial trade","Other services"]

def money(lo,hi):
    def f(v):
        v=float(v)
        if v>=1: return ("$%gM"%v)
        return "$%gK"%(v*1000)
    return f(lo) if lo==hi else "%s–%s"%(f(lo),f(hi))

# ---------- table ----------
trs=[]
for st,name,lo,hi,tier,sector,note,xb in rows:
    dup = "DUPLICATE" in note
    lof,hif=float(lo),float(hi)
    width = 0 if hif==0 else max(3, round(100*math.sqrt(hif)/math.sqrt(80)))
    stat_cls = "ex" if st.startswith("Existing") and "Dormant" not in st else ("dor" if "Dormant" in st else "pro")
    tier_cls = tier.lower() if tier!="NA" else "na"
    trs.append(
      '<tr data-tier="%s" data-status="%s" data-xb="%s"%s>'
      '<td class="c-name"><span class="nm">%s</span>%s<span class="sec">%s</span></td>'
      '<td class="c-stat"><span class="chip %s">%s</span></td>'
      '<td class="c-tier"><span class="tierbadge %s">%s</span></td>'
      '<td class="c-turn"><span class="num">%s</span>'
      '<span class="bar"><i style="width:%d%%"></i></span></td>'
      '<td class="c-xb">%s</td>'
      '<td class="c-note">%s</td></tr>' % (
        tier_cls, stat_cls, xb.lower(),
        ' class="isdup"' if dup else '',
        html.escape(name),
        ' <span class="duptag">duplicate</span>' if dup else '',
        html.escape(sector),
        stat_cls, html.escape(st.replace(" (Dormant)"," · dormant")),
        tier_cls, tier if tier!="NA" else "—",
        money(lof,hif) if hif>0 else "—", width,
        '<span class="xbyes" title="Documented cross-border trade">●</span>' if xb=="Y" else '<span class="xbno">–</span>',
        html.escape(note)))
TABLE="\n".join(trs)

# ---------- sector bars ----------
comm=[r for r in rows if r[4]!="NA"]
counts={s:sum(1 for r in comm if r[5]==s) for s in SECTOR_ORDER}
mx=max(counts.values())
SECTORS="\n".join(
  '<li><span class="s-name">%s</span><span class="s-bar"><i style="width:%d%%"></i></span>'
  '<span class="s-n">%d</span></li>'%(html.escape(s),round(100*counts[s]/mx),counts[s])
  for s in SECTOR_ORDER)

# ---------- programme ----------
PROG=[
 ("13 Jul","done","‘Dear You’ Movie Client Screening",
  "<b>Golden Village, Suntec City</b> — Monday 13 July 2026, billed on the standee as a client appreciation evening hosted by WorldFirst. The film took RMB 1.8bn and sold out its Singapore run in two hours. Its subject is <b>qiaopi</b> — the remittance letters overseas Chinese sent home. Cross-border payments, a century early. Two group photos received: around two dozen guests at the standee in the foyer, and a full hall of more than a hundred behind the “Road to WorldFirst” banner.",
  None),
 ("22 Jul","done","WorldFirst × Bosses United Friendly Match",
  "Played at SAFRA under floodlights. <b>WorldFirst fielded its own XI</b> in red FBT kit — fifteen in the squad photo — against Bosses United in yellow and blue. Photos show the handshake line, a defensive wall at a free kick, and a combined group shot of roughly forty people. Covered by three photographers: Jason (@lightstoriesbyj), Shan (@art.of.shan) and Victor (@victor.chick), with 71 frames confirmed in the two Drive galleries.",
  "Date to settle — your latest note says 21 Jul; both photographers’ folders and all 71 filenames say 22 Jul."),
 ("7 Aug","done","Partnership Agreement Signing Ceremony",
  "<b>Wheeler’s Estate.</b> Billed on screen as the <b>Official Partnership Launch</b>, with a formal <b>Partnership Agreement Signing Ceremony</b> — signed folders, a Bosses United pennant and match ball exchanged for a WorldFirst gift box, and a celadon figurine presented. Group photo of roughly seventy guests. The <b>Bosses United team bus</b> was also unveiled, carrying the WorldFirst lockup and a wall of member-company logos. <b>Minister of State Dinesh Vasu Dash attended</b> and received the figurine — confirmed, this is his second appearance with WorldFirst in three weeks by 26 Aug.",
  None),
 ("21 Aug","done","Bosses United Interview Series",
  "Member interviews captured two days ago. <b>Ten interviews in total</b>, shot as a professional multi-cam production &mdash; an interviewer paired with a business owner (one segment ran three-up), filmed on synced cameras with a WorldFirst-branded red bottle as the on-camera talent gift. This is the content engine behind the partnership: named founders telling their own growth stories on video, not just photos. <b>Eight of the ten confirmed</b> from behind-the-scenes monitor shots; the remaining two took place but weren&rsquo;t photographed.",
  "The finished footage and every interviewee&rsquo;s name &mdash; nobody in the monitor shots is identified yet."),
 ("26 Aug","now","Congress Cup Opening Ceremony",
  "Graced by Minister of State Dinesh Vasu Dash. Token of appreciation presentation. Six markets represented on the ground: Singapore, Malaysia, Thailand, Japan, Korea and Hong Kong. <b>This is the briefing.</b>",
  None),
 ("28 Aug","next","WorldFirst × Bosses United Exhibition Match",
  "WorldFirst versus Singapore Xin Hua Sports Club. We have a working XI already — the 22 July squad photo is effectively the team sheet.",
  None),
 ("30 Aug","next","Congress Cup Closing Ceremony",
  "Winners’ presentation, with the trophy presented to WorldFirst. The natural place to announce the Q4 clinics while the room is still together.",
  None),
 ("Oct–Dec","next","WorldFirst Topical Clinics with Curated Bosses",
  "One session a month, capped at 20 people each — three sessions, up to 60 curated seats. This is where the relationship converts: small rooms, named attendees, real treasury and FX problems.",
  None),
]
PLABEL={"done":"Completed","now":"Next · 3 days","next":"Upcoming"}
prog=[]
for d,state,title,body,ask in PROG:
    prog.append(
      '<article class="ev %s">'
      '<div class="ev-rail"><span class="ev-date">%s</span>'
      '<span class="ev-state">%s</span></div>'
      '<div class="ev-body"><h3>%s</h3><p>%s</p>%s</div></article>'%(
        state,d,PLABEL[state],html.escape(title),body,
        '<p class="ev-ask"><span class="tag gap">Need from you</span> %s</p>'%html.escape(ask) if ask else ''))
PROGRAMME="\n".join(prog)

MARKETS=[("SG","Singapore","Host market · all 44 member companies"),
         ("MY","Malaysia","TEHC exports here; nearest trade corridor"),
         ("TH","Thailand","D Wall recruits here; 2023 Bangkok tour"),
         ("JP","Japan","Bencoolen’s Andersen’s franchise; Honda link"),
         ("KR","Korea","New corridor — no existing member link found"),
         ("HK","Hong Kong","HKAFA MOU + Bosses United Hong Kong chapter")]
MK="\n".join('<li><span class="mk-code">%s</span><span class="mk-name">%s</span>'
             '<span class="mk-note">%s</span></li>'%(c,n,html.escape(t)) for c,n,t in MARKETS)

css=open("style.css").read()
body=open("body.html").read()
body=(body.replace("<!--TABLE-->",TABLE).replace("<!--SECTORS-->",SECTORS)
          .replace("<!--PROGRAMME-->",PROGRAMME).replace("<!--MARKETS-->",MK))
out=open("head.html").read()+"<style>\n"+css+"\n</style>\n"+body
open("bosses-united.html","w").write(out)
print("wrote bosses-united.html  %.1f KB"%(len(out)/1024))
print("table rows:",len(trs),"| sectors:",counts)
