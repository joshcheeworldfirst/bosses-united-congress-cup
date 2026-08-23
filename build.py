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
 ("13 Jul","done","‘Dear You’ client screening",
  "Golden Village Suntec City — 100+ clients behind the “Road to WorldFirst” banner. The film’s subject is <b>qiaopi</b>: remittance letters home. Cross-border payments, a century early.",None),
 ("22 Jul","done","Friendly match",
  "SAFRA, under floodlights — a WorldFirst XI in red against Bosses United, covered by three photographers.",None),
 ("7 Aug","done","Partnership signing",
  "Wheeler’s Estate — agreement signed, team bus unveiled, MOS Dinesh Vasu Dash in attendance.",None),
 ("21 Aug","done","Interview series",
  "Ten founders filmed telling their growth stories — the content engine behind the partnership.",None),
 ("26 Aug","now","Congress Cup Opening Ceremony",
  "<b>Pan Pacific Singapore, report 5:15pm.</b> MOS Dinesh Vasu Dash; token of appreciation; six markets in the room.",None),
 ("28 Aug","next","Exhibition match",
  "WorldFirst vs Singapore Xin Hua Sports Club.",None),
 ("30 Aug","next","Closing ceremony",
  "Winners’ presentation; trophy presented to WorldFirst.",None),
 ("Oct–Dec","next","Topical clinics",
  "Monthly, 20 curated seats each — where the relationship converts.",None),
]
PLABEL={"done":"Done","now":"The event","next":"Upcoming"}
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

MARKETS=[("SG","Singapore","Host — all local members"),
         ("MY","Malaysia","Member export corridor"),
         ("TH","Thailand","2023 tour; recruitment corridor"),
         ("JP","Japan","Franchise link; Honda meeting"),
         ("KR","Korea","New corridor"),
         ("HK","Hong Kong","HKAFA MOU + HK chapter")]
MK="\n".join('<li><span class="mk-code">%s</span><span class="mk-name">%s</span>'
             '<span class="mk-note">%s</span></li>'%(c,n,html.escape(t)) for c,n,t in MARKETS)

css=open("style.css").read()
body=open("body.html").read()
body=(body.replace("<!--SECTORS-->",SECTORS)
          .replace("<!--PROGRAMME-->",PROGRAMME).replace("<!--MARKETS-->",MK))
out=open("head.html").read()+"<style>\n"+css+"\n</style>\n"+body
open("bosses-united.html","w").write(out)
print("wrote bosses-united.html  %.1f KB"%(len(out)/1024))
print("sectors:",counts)
