#!/usr/bin/env python3
"""Builds the whole website as plain static files in the repo root (GitHub Pages serves them as they are; see .nojekyll).

Sources:   _posts/*.md (blog posts), publications.md (research page), site-src/home-source.html (home page text + forest script)
Output:    index.html, blog/, publications/, art/, one folder per post, 404.html, assets/site/
Run:       python3 site-src/build.py      then commit and push
Preview:   python3 -m http.server 8000    (from the repo root) and open http://localhost:8000
"""
import hashlib, json, math, os, random, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
OUT = REPO
SITE = 'https://zhanqizhang66.github.io'
RESUME = '/Zhanqi%20Zhang%20CV_2026_sans_serif_0722.pdf'
GTAG = 'G-Y06S3E3WTE'
DESC = 'Victoria Zhang. Machine Learning Research Scientist · Ph.D., UC San Diego · Ex-Google & Meta. Representation · AI Agents · Reasoning · Adaptation.'
OGIMG = '/assets/img/og-card.png'


def read(p):
    return open(os.path.join(REPO, p), encoding='utf8').read()


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf8').write(text)


# ------------------------------------------------------------------ shared pieces
SRC = read('site-src/home-source.html')
BODY = SRC[SRC.index('<body>'):]
FOREST_JS = BODY[BODY.rindex('<script>') + 8:BODY.rindex('</script>')]
HOME_MAIN = BODY[BODY.index('<main>'):BODY.index('</main>') + 7]
HOME_SCRIPT = BODY[BODY.index('<script>window.WORK'):BODY.index('<div class="treepick"')]
BASE_CSS = SRC[SRC.index('<style>') + 7:SRC.index('</style>')]


def must(s, a, b):
    assert a in s, a[:60]
    return s.replace(a, b, 1)


# night and day share one definition with the theme; blossom is always "full"
FOREST_JS = must(FOREST_JS, "function isNight(){return hour>=20.4||hour<5.6;}", "function isNight(){return vzNight(hour);}")
FOREST_JS = must(FOREST_JS, "slider.value=hour;reset.hidden=preview==null;}", "slider.value=hour;reset.hidden=preview==null;vzApplyTheme(hour);}")
FOREST_JS = must(FOREST_JS, "+' · heard '+toks.length+' words about Victoria'", "")
FOREST_JS = must(FOREST_JS, "what:'bigram model, 1 word of context'", "what:'bigram model · remembers 1 word back, so it rambles'")
FOREST_JS = must(FOREST_JS, "what:'trigram model, 2 words of context'", "what:'trigram model · remembers 2 words back'")
FOREST_JS = must(FOREST_JS, "what:'4-gram model, 3 words of context'", "what:'4-gram model · remembers 3 words back, nearly quotes'")
FOREST_JS = must(FOREST_JS, "'Victoria is a Ph.D. candidate at UC San Diego.'", "'Victoria is an ML research scientist.',\n  'Victoria defended her Ph.D. at UC San Diego.'")
FOREST_JS = must(FOREST_JS, "try{bloomMode=localStorage.getItem('vz-bloom')||bloomMode;}catch(e){}", "")

# ---- small screens: there are no side lanes, so the trees lean in from the edges and the birds perch on the part that shows
FOREST_JS = must(FOREST_JS, "}else{tree(-10,H*.12,84);tree(W+10,H*.3,76);tree(-20,H*.78,92);tree(W+16,H*.9,84);}",
                 "}else{tree(0,H*.16,84);tree(W,H*.36,78);tree(-4,H*.62,90);tree(W+4,H*.86,84);}")
FOREST_JS = must(FOREST_JS, "tr.spots=[[0,0],[tr.r*.32,tr.r*.1],[-tr.r*.25,tr.r*.28],[tr.r*.05,-tr.r*.34],[-tr.r*.3,-tr.r*.15]];buildTree(tr);",
                 "tr.spots=[[0,0],[tr.r*.32,tr.r*.1],[-tr.r*.25,tr.r*.28],[tr.r*.05,-tr.r*.34],[-tr.r*.3,-tr.r*.15]];tr.px=tr.x;tr.py=tr.y;tr.pr=tr.r*.5;"
                 "if(!wide){tr.px=tr.x<W/2?15:W-15;tr.pr=10;tr.spots=[[0,0],[-3,-tr.r*.3],[3,-tr.r*.13],[-2,tr.r*.14],[2,tr.r*.3]].map(function(s){return [tr.px-tr.x+s[0],s[1]];});}buildTree(tr);")
FOREST_JS = must(FOREST_JS, "return tr.r>50&&tr.x>10&&tr.x<W-10&&tr.y>40&&tr.y<H-40;", "return tr.r>50&&tr.px>10&&tr.px<W-10&&tr.y>40&&tr.y<H-40;")
FOREST_JS = must(FOREST_JS, "if(Math.hypot(hx-tr.x,hy-tr.y)>tr.r*.5){ha=Math.atan2(tr.y-b.y,tr.x-b.x)+rnd(-.5,.5);", "if(Math.hypot(hx-tr.px,hy-tr.py)>tr.pr){ha=Math.atan2(tr.py-b.y,tr.px-b.x)+rnd(-.5,.5);")
FOREST_JS = must(FOREST_JS, "return {x:rt.x+k*15,y:rt.y+Math.abs(k)*3,tr:rt,night:true};", "return {x:(rt.px===rt.x?rt.x+k*15:(rt.px<W/2?34:W-34)+k*13),y:rt.py+Math.abs(k)*3,tr:rt,night:true};")
# a phone's address bar sliding away changes the height a little; keep the same forest and birds instead of starting over
FOREST_JS = must(FOREST_JS, "rz=setTimeout(function(){resize();makeTrees();makeBirds();settle();", "rz=setTimeout(function(){if(innerWidth===W&&Math.abs(innerHeight-H)<160){resize();if(reduce)frame();return;}resize();makeTrees();makeBirds();settle();")

HEAD_JS = """(function(){
  // Dark at night and bright by day, on San Diego time. The button overrides it for this visit.
  var root=document.documentElement,KEY='vz-theme';
  var fmt=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',hour:'numeric',minute:'2-digit',hourCycle:'h23'});
  function hourNow(){var p={};fmt.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value;});return (+p.hour%24)+(+p.minute)/60;}
  function manual(){try{return sessionStorage.getItem(KEY);}catch(e){return null;}}
  window.vzNight=function(h){return h>=19||h<6;};
  window.vzApplyTheme=function(h){root.setAttribute('data-theme',manual()||(vzNight(h)?'dark':'light'));};
  window.toggleTheme=function(){var next=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',next);try{sessionStorage.setItem(KEY,next);}catch(e){}};
  vzApplyTheme(hourNow());
})();"""

EXTRA_CSS = """
/* ---------- pages beyond the home page ---------- */
main img{max-width:100%}
.back{display:inline-block;font-size:14px;color:var(--muted);margin:10px 0 18px}
.pmeta{color:var(--muted);font-size:13.5px;margin:-22px 0 26px}
.pmeta .tg{display:inline-block;margin-right:8px}
.publication-row[id]{scroll-margin-top:84px}
:root{--col:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--col:#0d0f11}}
:root[data-theme="dark"]{--col:#0d0f11}
main.post{position:relative;max-width:800px;min-height:100vh;background:var(--col);padding:28px 48px 64px;border-left:1px solid var(--line);border-right:1px solid var(--line)}
@media (max-width:640px){main.post{padding:20px 20px 48px;border:0}}
.prose iframe{display:block;width:100%;border:1px solid var(--line);border-radius:12px;background:#fff}
.prose p.pdf{margin:18px 0 10px;font-weight:600;font-size:15px}
.publication-content a.code{display:block;width:fit-content;margin-top:8px;font-weight:600;font-size:14px}
.nw{white-space:nowrap}
.figsrc{font-size:12.5px;color:var(--muted);margin:8px 2px 0}
.pub-abstract details p{margin:0 0 10px}
.cover-img{width:100%;aspect-ratio:1200/630;object-fit:cover;border-radius:18px;border:1px solid var(--line);margin:0 0 36px;display:block}
:root[data-theme="dark"] .cover-img,:root[data-theme="dark"] .card img{filter:brightness(.86)}

/* post body */
.prose{font-size:16.5px;line-height:1.78}
.prose h2{font-size:25px;letter-spacing:-.02em;line-height:1.25;margin:46px 0 12px}
.prose h3{font-size:19px;letter-spacing:-.01em;margin:32px 0 8px}
.prose h4{font-size:16.5px;margin:24px 0 6px}
.prose p{margin:0 0 16px}
.prose ul,.prose ol{padding-left:22px;margin:0 0 16px}.prose li{margin:4px 0}
.prose img{border-radius:12px;margin:10px auto;display:block}
.prose blockquote{margin:20px 0;padding:2px 0 2px 18px;border-left:3px solid var(--link);color:var(--muted)}
.prose hr{border:0;border-top:1px solid var(--line);margin:36px 0}
.prose code{font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:.88em;background:var(--hl);padding:1px 5px;border-radius:5px}
.prose pre{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;overflow-x:auto;font-size:13.5px;line-height:1.6;margin:0 0 18px}
.prose pre code{background:none;padding:0;font-size:inherit}
.prose .tw{overflow-x:auto;margin:0 0 20px;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
.prose table{border-collapse:collapse;width:100%;font-size:14.5px;line-height:1.5}
.prose th,.prose td{padding:9px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.prose th{font-size:12.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:600}
.prose tr:last-child td{border-bottom:0}
.prose .box-note,.prose .box-warning,.prose .box-error,.prose .box-success{padding:12px 16px;border-radius:12px;background:var(--hl);border:1px solid var(--line)}
.prose mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden;padding:4px 0}
.pn{display:flex;justify-content:space-between;gap:20px;margin:56px 0 0;padding-top:20px;border-top:1px solid var(--line);font-size:14.5px}
.pn a{max-width:48%}.pn span{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}

/* share, likes and comments under a post */
.share{display:flex;align-items:center;gap:16px;margin:44px 0 0;padding-top:18px;border-top:1px solid var(--line);font-size:17px}
.share span{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.share a,.share button{color:var(--muted);background:none;border:0;padding:0;font-size:17px;cursor:pointer}
.share a:hover,.share button:hover,.share button.ok{color:var(--link);text-decoration:none}
.comments{margin:34px 0 0}.comments h3{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:600;margin:0 0 12px}
#disqus_thread{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 18px;min-height:80px}
.pn{margin-top:34px}
/* essay covers: photo above, abstract panel below */
.pae{display:block;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:#f4efe3;transition:transform .25s}
.pae img{display:block;width:100%;object-fit:cover;border:0 !important;border-radius:0 !important;margin:0 !important;transform:none !important}
.pae svg{display:block;width:100%;height:auto}
.card:hover .pae{transform:translateY(-3px)}
.pae-wrap{max-width:400px;margin:0 0 36px}
.grid.three{grid-template-columns:repeat(3,1fr);gap:26px 18px}
/* home */
.newsl .old{display:none}.newsl.all .old{display:grid}
.newsl .ln{padding:7px 0}
.after{margin:14px 0 0;font-size:14.5px}
/* blog index */
.filters{display:flex;gap:18px;margin:0 0 30px;font-size:14.5px}
.filters button{border:0;background:none;font:inherit;color:var(--muted);cursor:pointer;padding:0}
.filters button.on{color:var(--ink);text-decoration:underline;text-underline-offset:4px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px 22px}
.card{display:block;color:var(--ink)}.card:hover{text-decoration:none}
.card img{width:100%;aspect-ratio:1200/630;object-fit:cover;border-radius:14px;border:1px solid var(--line);display:block;transition:transform .25s}
.card:hover img{transform:translateY(-3px)}
.card b{display:block;font-size:16.5px;line-height:1.35;margin:11px 0 1px;letter-spacing:-.01em}
.card span{display:block;color:var(--muted);font-size:14px;line-height:1.45}
.card em{display:block;font-style:normal;color:var(--muted);font-size:12.5px;margin-top:4px}

/* research: every project shows its figure */
.publication-row{padding:26px 0 30px;border-bottom:1px solid var(--line);display:flex;flex-direction:column}
.publication-row:first-of-type{padding-top:4px}
.publication-content{display:contents}
.pub-title{order:1;font-weight:700;font-size:17.5px;line-height:1.4;letter-spacing:-.01em}.pub-title a{color:var(--ink)}.pub-title a:hover{color:var(--link)}
.pub-authors{order:2;font-size:13.5px;color:var(--muted);margin-top:3px}
.pub-venue{order:3;font-size:13.5px;color:var(--muted)}
.publication-image{order:4;margin:16px 0 14px}
.publication-image img{display:block;width:100%;max-height:440px;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px}
.pub-abstract{order:5;font-size:15px}
.pub-abstract summary{cursor:pointer;list-style:none}.pub-abstract summary::-webkit-details-marker{display:none}
.pub-abstract summary::after{content:" Read the abstract +";color:var(--link);font-size:13px;font-weight:600;white-space:nowrap}
.pub-abstract details[open] summary::after{content:" Close −"}
.pub-abstract details[open] summary{margin-bottom:10px;font-weight:600}
.pub-abstract ul{padding-left:20px;margin:8px 0}
main > h2{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:600;margin:54px 0 6px}
main > h2:first-of-type{margin-top:10px}
@media (max-width:640px){.grid,.grid.three{grid-template-columns:1fr}.grid.three .card{max-width:320px}}
"""

CSS = BASE_CSS + EXTRA_CSS
CSS = CSS.replace('.treepick{position:fixed;z-index:3;left:16px;bottom:16px;font-size:12.5px;color:var(--muted);display:flex;gap:8px;align-items:center}', '')


VER = hashlib.md5((CSS + FOREST_JS).encode('utf8')).hexdigest()[:8]


def page(title, main, path='/', active='', extra_head='', extra_body='', desc=DESC, img=OGIMG):
    root = '/'
    nav = [('Home', ''), ('Research', 'publications/'), ('Blog', 'blog/'), ('Art', 'art/')]
    links = ''.join('<a class="%s" href="%s%s">%s</a>' % ('on' if n == active else '', root, h, n) for n, h in nav)
    url = SITE + path
    meta = ('<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n'
            '<meta property="og:site_name" content="Victoria Zhang">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:type" content="website">\n<meta property="og:url" content="%s">\n<meta property="og:image" content="%s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:site" content="@ZhangZhanqi">\n<meta name="twitter:image" content="%s">\n'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','%s');</script>"
            ) % (html.escape(desc, True), html.escape(url, True), html.escape(title, True), html.escape(desc, True), html.escape(url, True), html.escape(SITE + img, True), html.escape(SITE + img, True), GTAG, GTAG)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{meta}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<script>{HEAD_JS}</script>
<link rel="stylesheet" href="/assets/site/site.css?v={VER}">
{extra_head}</head>
<body>
<canvas id="forest" aria-hidden="true"></canvas>
<header class="top"><a class="brand" href="/">Victoria Zhang</a><nav>{links}<a href="{RESUME}">Resume</a><button class="theme-toggle" onclick="toggleTheme()" aria-label="Light or dark"><i class="fa-solid fa-circle-half-stroke"></i></button></nav></header>
{main}
<footer class="foot">Victoria &nbsp;·&nbsp; 2026</footer>
{extra_body}<aside class="say" id="say" aria-live="polite"><p id="sayText"></p><span id="sayMeta"></span></aside>
<div class="clock"><span id="cap">San Diego</span><input id="when" type="range" min="0" max="23.99" step="0.25" aria-label="Preview another time of day"><button id="now" hidden>now</button></div>
<script src="/assets/site/forest.js?v={VER}"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ covers
INK, TEAL = '#1f2326', '#2f7d7a'
GREENS = [['#a3c39c', '#b7d2ae', '#cde0c2'], ['#b3bf96', '#c6d0a9', '#d9e0c0'], ['#a5c4b8', '#bad5ca', '#cfe2d9']]
YEL = ['#e3d08a', '#eddd9f', '#f5e9bb']
PINK = ['#e6b5bf', '#efc8d0', '#f7dce1']


def canopy(R, cx, cy, r, pal):
    p1, p2, p3, a1 = R.random() * 6.28, R.random() * 6.28, R.random() * 6.28, .1 + R.random() * .12
    rad = lambda th: r * (.78 + a1 * math.sin(th * 2 + p1) + .09 * math.sin(th * 3 + p2) + .06 * math.sin(th * 5 + p3))
    pts = ' '.join('%.0f,%.0f' % (cx + math.cos(i / 40 * 6.283) * rad(i / 40 * 6.283) * .9, cy + math.sin(i / 40 * 6.283) * rad(i / 40 * 6.283) * .9) for i in range(40))
    sh = ' '.join('%.0f,%.0f' % (cx + r * .06 + math.cos(i / 40 * 6.283) * rad(i / 40 * 6.283) * 1.04, cy + r * .09 + math.sin(i / 40 * 6.283) * rad(i / 40 * 6.283) * 1.04) for i in range(40))
    out = ['<polygon points="%s" fill="#323c2d" fill-opacity=".1"/><polygon points="%s" fill="%s"/>' % (sh, pts, pal[0])]
    dabs = []
    for _ in range(int(40 + r * .5)):
        t = R.random() * 6.283
        q = (R.random() ** .6) * rad(t) * .98
        dx, dy = math.cos(t) * q, math.sin(t) * q
        light = (-dx * .6 - dy * .8) / r + (R.random() - .5) * .7
        dabs.append((2 if light > .22 else 0 if light < -.25 else 1, dx, dy, r * (.1 + R.random() * .085), .5 + R.random() * .3, R.random() * 180))
    for c, dx, dy, a, b, rot in sorted(dabs):
        out.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" transform="rotate(%.0f %.0f %.0f)" fill="%s"/>' % (cx + dx, cy + dy, a, a * b, rot, cx + dx, cy + dy, pal[c]))
    return ''.join(out)


def bird(x, y, ang, body, wing, head):
    return ('<g transform="translate(%d %d) rotate(%d) scale(2.3)"><path d="M-6-2.4Q-20-2-29-.9Q-30.6 0-29 .9Q-20 2-6 2.4Z" fill="%s"/>'
            '<ellipse rx="10" ry="6.2" fill="%s"/><ellipse cx="-2.2" cy="3.6" rx="7" ry="2.5" fill="%s"/><ellipse cx="-2.2" cy="-3.6" rx="7" ry="2.5" fill="%s"/>'
            '<ellipse cx="12.5" rx="2.1" ry="1.5" fill="#cfa25a"/><circle cx="8.2" r="4.3" fill="%s"/></g>') % (x, y, ang, wing, body, wing, wing, head)


def L(x1, y1, x2, y2, c=INK, w=5, o=1, dash=''):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round"%s/>' % (x1, y1, x2, y2, c, w, o, ' stroke-dasharray="%s"' % dash if dash else '')


def C(x, y, r, fill='#fffdf8', stroke=INK, w=5, o=1):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, o, stroke, w)


def Rc(x, y, w, h, fill='#fffdf8', stroke=INK, sw=5, rx=14, o=1, dash=''):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, fill, o, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else '')


def Pth(d, c=INK, w=5, fill='none', o=1):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (d, fill, c, w, o)


def motif(name):
    o = []
    if name == 'rnn':  # the same cell unrolled through time, state passed along
        for i in range(4):
            x = 330 + i * 180
            o += [Pth('M%d 268 C%d 190 %d 190 %d 268' % (x - 26, x - 60, x + 60, x + 26), TEAL, 5), C(x, 315, 46, YEL[2] if i < 3 else PINK[1])]
            if i < 3: o.append(L(x + 50, 315, x + 130, 315))
            o.append(L(x, 365, x, 420, INK, 5, .45))
    elif name == 'transformer':  # an attention map
        R = random.Random(3)
        for r in range(6):
            for c in range(6):
                a = .95 if r == c else max(.06, .7 - abs(r - c) * .2 + R.random() * .2 - .1)
                o.append('<rect x="%d" y="%d" width="54" height="54" rx="10" fill="%s" fill-opacity="%.2f"/>' % (420 + c * 62, 132 + r * 62, TEAL, a))
    elif name == 'llm':  # tokens in a row, the next one still to come
        for i, w in enumerate([120, 84, 150, 96]):
            x = 250 + sum([120, 84, 150, 96][:i]) + i * 22
            o.append(Rc(x, 280, w, 70, [YEL[2], '#fffdf8', PINK[2], '#fffdf8'][i]))
        o += [Rc(790, 280, 130, 70, 'none', TEAL, 5, 14, 1, '12 10'), Pth('M700 250 C740 190 810 190 850 262', TEAL, 5), Pth('M836 240 L852 264 L874 246', TEAL, 5)]
    elif name == 'mle':  # a likelihood curve over the data
        pts = ' '.join('%s%d %d' % ('M' if i == 0 else 'L', 300 + i * 10, 440 - 250 * math.exp(-((i - 30) / 11.0) ** 2)) for i in range(61))
        o += [Pth(pts + ' L900 440 L300 440 Z', 'none', 0, YEL[1], 1), Pth(pts, INK, 5), L(280, 440, 920, 440), L(600, 190, 600, 440, TEAL, 4, 1, '10 10')]
        for x in [470, 540, 575, 610, 632, 690, 760]: o.append(C(x, 472, 9, TEAL, TEAL, 0))
    elif name == 'temperature':  # the same distribution, cold to hot
        for k, hs in enumerate([[200, 40, 16, 8], [150, 90, 50, 26], [84, 76, 70, 64]]):
            for i, h in enumerate(hs):
                o.append('<rect x="%d" y="%d" width="34" height="%d" rx="8" fill="%s"/>' % (300 + k * 220 + i * 42, 440 - h, h, [TEAL, '#7fb0a8', YEL[0], PINK[0]][k if False else i]))
            o.append(L(292 + k * 220, 448, 300 + k * 220 + 168, 448))
    elif name == 'speculative-decoding':  # a small model drafts, a big one checks
        for i in range(5):
            x = 330 + i * 116
            o += [Rc(x, 215, 84, 60, YEL[2], INK, 4, 14, 1, '10 8'), Rc(x, 365, 84, 60, '#fffdf8' if i < 3 else PINK[2]), L(x + 42, 283, x + 42, 357, TEAL, 4, .6)]
            o.append(Pth('M%d 395 l10 11 l20 -22' % (x + 27), TEAL, 6) if i < 3 else Pth('M%d 383 l24 24 M%d 383 l-24 24' % (x + 30, x + 54), '#c9788a', 6))
    elif name == 'moe':  # a router sends each token down a few paths
        o.append(C(330, 315, 40, YEL[2]))
        for i in range(5):
            y = 135 + i * 90
            on = i in (1, 3)
            o += [Pth('M372 315 C480 315 520 %d 640 %d' % (y + 30, y + 30), TEAL if on else INK, 6 if on else 4, 'none', 1 if on else .25), Rc(645, y, 200, 60, PINK[2] if on else '#fffdf8', INK, 5, 14, 1 if on else .5)]
    elif name == 'attention-matmul':  # where the time goes: the matmul is the small slice
        for r, segs in enumerate([[(0, 90, TEAL), (90, 330, YEL[1]), (420, 180, PINK[1])], [(0, 60, TEAL), (60, 200, YEL[1]), (260, 340, PINK[1])], [(0, 110, TEAL), (110, 400, YEL[1]), (510, 90, PINK[1])]]):
            for x, w, c in segs:
                o.append('<rect x="%d" y="%d" width="%d" height="56" rx="12" fill="%s" stroke="#f1efe6" stroke-width="5"/>' % (300 + x, 195 + r * 86, w, c))
    elif name == 'sft':  # a loss curve that flattens: when to stop
        o += [L(300, 150, 300, 460), L(300, 460, 900, 460), Pth('M320 180 C400 400 520 425 880 432', TEAL, 6), Pth('M320 220 C400 380 500 380 600 372 S780 330 880 280', '#c9788a', 5), L(600, 150, 600, 460, INK, 4, .5, '10 10'), C(600, 372, 11, YEL[1])]
    elif name == 'decode-prefill':  # one wide pass, then many thin ones
        o.append(Rc(290, 205, 300, 220, YEL[2]))
        for i in range(8): o.append(Rc(630 + i * 36, 205, 20, 220, PINK[2], INK, 4, 8))
    elif name == 'ai-infra':  # every trick is a trade between three resources
        A, B, D = (600, 150), (380, 470), (820, 470)
        o += [Pth('M%d %d L%d %d L%d %d Z' % (A + B + D), INK, 5, YEL[2], 1), C(A[0], A[1], 36, '#fffdf8'), C(B[0], B[1], 36, '#fffdf8'), C(D[0], D[1], 36, '#fffdf8'), C(640, 360, 15, TEAL, TEAL, 0), L(640, 360, 600, 186, TEAL, 3, .5), L(640, 360, 412, 458, TEAL, 3, .5), L(640, 360, 788, 458, TEAL, 3, .5)]
    elif name == 'gated-attention':  # attention weights pass through one switch
        for i, on in enumerate([1, 0, 1, 1, 0]):
            y = 175 + i * 70
            o += [L(300, y, 540, y, TEAL, 6), L(660, y, 900, y, TEAL, 6, 1 if on else .15), C(540, y, 9, TEAL, TEAL, 0)]
            o.append(L(540, y, 660, y, INK, 6) if on else L(540, y, 640, y - 40, INK, 6))
            o.append(C(660, y, 9, '#fffdf8', INK, 4))
    elif name == 'vision-language':  # two strands that keep crossing
        a = ' '.join('%s%d %.0f' % ('M' if i == 0 else 'L', 280 + i * 8, 315 + 105 * math.sin(i / 13.0)) for i in range(81))
        b = ' '.join('%s%d %.0f' % ('M' if i == 0 else 'L', 280 + i * 8, 315 - 105 * math.sin(i / 13.0)) for i in range(81))
        for i in range(4, 80, 6):
            y = 105 * math.sin(i / 13.0)
            if abs(y) > 28: o.append(L(280 + i * 8, 315 - y * .86, 280 + i * 8, 315 + y * .86, INK, 4, .3))
        o += [Pth(a, TEAL, 8), Pth(b, '#c9788a', 8)]
    return ''.join(o)


COVERS = ['rnn', 'transformer', 'llm', 'mle', 'temperature', 'speculative-decoding', 'moe', 'attention-matmul', 'sft', 'decode-prefill', 'ai-infra', 'gated-attention', 'vision-language']
BIRDS = [('#a6abb0', '#8d9399', '#b3b4a8'), ('#f7f4ec', '#e3dfd3', '#f0e2a4'), ('#8fbd84', '#6f9c6b', '#ecd98a')]


def cover_svg(name, k):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#fbf9f3"/>%s</svg>' % motif(name))


# ---- essay covers, after the "photo abstract editorial" recipe: the photo untouched on top, and below it a flat ivory
# panel with a few marks taken from what is in the photo (its lines, intervals and colours) and a short serif title.
def _ticks(seed, n, x0, x1, y, cols):
    R = random.Random(seed)
    return ''.join('<line x1="%.0f" y1="%d" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (x, y, x + R.uniform(-3, 3), y - R.uniform(8, 24), R.choice(cols))
                   for x in [x0 + (x1 - x0) * i / (n - 1) + R.uniform(-3, 3) for i in range(n)])


def _fan(cx, cy, r, col):
    return ''.join('<line x1="%d" y1="%d" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="1.5" stroke-linecap="round"/>' % (cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), col)
                   for a in [-2.9, -2.3, -1.7, -1.1, -.5, .1])


USE_ESSAY_ART = False
ESSAY_ART = {
    'young.JPG': (4 / 3, 'Three by the Water',
        '<line x1="30" y1="70" x2="370" y2="70" stroke="#7c8985" stroke-width="1.2"/>'
        + ''.join('<line x1="%d" y1="70" x2="%d" y2="%d" stroke="#94999b" stroke-width="3"/>' % (x, x, 70 - h) for x, h in [(118, 10), (130, 16), (146, 22), (160, 12)])
        + '<path d="M30 118 Q88 150 150 112" fill="none" stroke="#5b6d70" stroke-width="1.5"/><line x1="150" y1="104" x2="150" y2="150" stroke="#5b6d70" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M208 150 L211 80 Q215 73 219 80 L222 150Z" fill="#1d2427"/><path d="M233 128 L235 100 Q238 95 241 100 L243 128Z" fill="#6c615e"/><path d="M255 150 L258 84 Q262 77 266 84 L269 150Z" fill="#413c3d"/>'),
    'IMG_9575.JPEG': (4 / 3, 'Tower Among Palms',
        '<line x1="40" y1="28" x2="120" y2="28" stroke="#82a5d6" stroke-width="6" stroke-linecap="round" opacity=".5"/><line x1="250" y1="22" x2="330" y2="22" stroke="#82a5d6" stroke-width="6" stroke-linecap="round" opacity=".5"/>'
        '<path d="M196 138 L198 54 L200 36 L202 54 L204 138Z" fill="#a89c86"/><circle cx="200" cy="31" r="2.5" fill="#a89c86"/>'
        '<line x1="60" y1="150" x2="360" y2="110" stroke="#7f7970" stroke-width="1.5"/>'
        + ''.join('<path d="M%d %d a14 14 0 0 1 28 0" fill="none" stroke="#2c321f" stroke-width="1.5"/>' % (x, y) for x, y in [(215, 160), (262, 154), (309, 148)])
        + _fan(120, 112, 20, '#2c321f') + _fan(326, 82, 24, '#2c321f')),
    'IMG_9057.jpeg': (4 / 3, 'Pink Above the Cliff',
        '<line x1="250" y1="30" x2="370" y2="30" stroke="#6e8db6" stroke-width="1.5"/>'
        '<line x1="215" y1="54" x2="280" y2="54" stroke="#c8b6b9" stroke-width="6" stroke-linecap="round"/><line x1="200" y1="70" x2="320" y2="70" stroke="#d1bec1" stroke-width="10" stroke-linecap="round"/><line x1="230" y1="88" x2="340" y2="88" stroke="#d1bec1" stroke-width="8" stroke-linecap="round" opacity=".8"/>'
        + ''.join('<line x1="30" y1="%d" x2="%d" y2="160" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (62 + k * 16, 240 - k * 33, c) for k, c in enumerate(['#6c5d54', '#6c5d54', '#57524e', '#493828', '#493828', '#382e1f']))),
    'IMG_2671.JPEG': (16 / 9, 'Grass Before the Sea',
        '<line x1="60" y1="40" x2="250" y2="40" stroke="#b8b4a9" stroke-width="7" stroke-linecap="round" opacity=".8"/><line x1="120" y1="56" x2="340" y2="56" stroke="#b8b4a9" stroke-width="7" stroke-linecap="round" opacity=".8"/><line x1="40" y1="72" x2="200" y2="72" stroke="#a1a5a3" stroke-width="7" stroke-linecap="round" opacity=".7"/>'
        '<line x1="250" y1="92" x2="370" y2="92" stroke="#d9d4be" stroke-width="5" stroke-linecap="round"/><line x1="30" y1="112" x2="370" y2="112" stroke="#877f6f" stroke-width="1.5"/>'
        + ''.join('<line x1="30" y1="%d" x2="370" y2="%d" stroke="#98917d" stroke-width="2" stroke-dasharray="18 14" stroke-dashoffset="%d" stroke-linecap="round"/>' % (y, y, o) for y, o in [(130, 0), (146, 11), (162, 22)])
        + _ticks(4, 44, 30, 370, 226, ['#a0802a', '#736213', '#8a7238'])),
    'Breath-of-the-Wild-Casual-Gamer-Culture.webp': (16 / 9, 'One Figure, Wide World',
        '<circle cx="250" cy="72" r="50" fill="none" stroke="#e8c08d" stroke-width="1"/><circle cx="250" cy="72" r="34" fill="#f6dab1"/>'
        + ''.join('<circle cx="%d" cy="%d" r="1.5" fill="#686069"/>' % c for c in [(300, 34), (310, 28), (321, 36), (331, 30)])
        + '<path d="M30 152 L110 130 L170 148 L240 124 L300 144 L370 128" fill="none" stroke="#5b708b" stroke-width="1.5"/><path d="M30 172 L90 160 L160 170 L250 154 L370 166" fill="none" stroke="#808793" stroke-width="1.2"/>'
        '<path d="M118 226 L140 184 L176 176 L202 226Z" fill="#302f2e"/><line x1="100" y1="227" x2="226" y2="227" stroke="#757052" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M155 177 L157 152 Q158.5 147 160 152 L162 177Z" fill="#49607e"/><line x1="162" y1="162" x2="177" y2="174" stroke="#666d74" stroke-width="1"/>'),
    'flower.JPG': (1210 / 734, 'Pink, Held in Paper',
        '<path d="M70 50 L150 196 L250 196 L330 50" fill="none" stroke="#e6a07d" stroke-width="1.5" stroke-linejoin="round"/><path d="M150 196 L200 150 L250 196" fill="none" stroke="#e6a07d" stroke-width="1.2"/>'
        + ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % c for c in [(160, 108, 24, '#df9a8d'), (207, 92, 20, '#ee8981'), (242, 122, 22, '#f2d0a8'), (192, 138, 17, '#c97a64'), (226, 158, 13, '#df9a8d'),
                                                                        (128, 78, 7, '#b9a0c4'), (141, 66, 6, '#b9a0c4'), (150, 82, 6, '#b9a0c4'), (262, 82, 7, '#b9a0c4'), (275, 70, 6, '#b9a0c4'), (269, 96, 6, '#b9a0c4')])
        + '<line x1="134" y1="60" x2="128" y2="46" stroke="#7c8a55" stroke-width="1.5" stroke-linecap="round"/><line x1="270" y1="62" x2="278" y2="48" stroke="#7c8a55" stroke-width="1.5" stroke-linecap="round"/>'),
}


def essay_art(src, root):
    """HTML for one essay cover, or '' if we have no recipe for that photo."""
    key = os.path.basename(src)
    if not USE_ESSAY_ART or key not in ESSAY_ART:
        return ''
    ar, title, marks = ESSAY_ART[key]
    ph = 400 / ar
    hp = 520 - ph
    return ('<span class="pae"><img src="%s%s" alt="" loading="lazy" style="aspect-ratio:%.4f">'
            '<svg viewBox="0 0 400 %.0f" role="img" aria-label="%s"><rect width="400" height="%.0f" fill="#f4efe3"/>%s'
            '<text x="30" y="%.0f" font-family="Cormorant Garamond, Georgia, serif" font-size="21" font-weight="500" fill="#2a2a28">%s</text></svg></span>'
            % (root, src, ar, hp, title, hp, marks, hp - 24, title))


# ------------------------------------------------------------------ posts
def front(md):
    m = re.match(r'---\s*\n(.*?)\n---\s*\n?', md, re.S)
    fm, body = {}, md
    if m:
        body = md[m.end():]
        for line in m.group(1).split('\n'):
            mm = re.match(r'([\w-]+):\s*(.*)', line)
            if mm: fm[mm.group(1)] = mm.group(2).strip().strip('"')
    return fm, body


POST_JS = r"""
(function(){
  var md=window.MD,math=[];
  md=md.replace(/\{%\s*highlight\s*(\w+)[^%]*%\}/g,'```$1').replace(/\{%\s*endhighlight\s*%\}/g,'```').replace(/\{%[^%]*%\}/g,'');
  // keep the maths away from the markdown parser, the way kramdown does
  md=md.replace(/(^|\n)[ \t]*\$\$([\s\S]+?)\$\$[ \t]*(?=\n|$)/g,function(m,a,t){math.push('\\['+t+'\\]');return a+'\n\n@@M'+(math.length-1)+'@@\n\n';});
  md=md.replace(/\$\$([^\n]+?)\$\$/g,function(m,t){math.push('\\('+t+'\\)');return '@@M'+(math.length-1)+'@@';});
  if(window.MATH)md=md.replace(/\$([^$\n]+?)\$/g,function(m,t){math.push('\\('+t+'\\)');return '@@M'+(math.length-1)+'@@';});
  md=md.replace(/\\\(([\s\S]+?)\\\)/g,function(m,t){math.push('\\('+t+'\\)');return '@@M'+(math.length-1)+'@@';});
  var h=marked.parse(md,{gfm:true});
  h=h.replace(/\n?\{:\s*\.([\w-]+)[^}]*\}\s*<\/p>/g,'</p><!--k:$1-->').replace(/\{:[^}]*\}/g,'');
  h=h.replace(/<p>([\s\S]*?)<\/p><!--k:([\w-]+)-->/g,'<p class="$2">$1</p>');
  h=h.replace(/@@M(\d+)@@/g,function(m,i){return math[+i].replace(/&/g,'&amp;').replace(/</g,'&lt;');});
  h=h.replace(/<table>/g,'<div class="tw"><table>').replace(/<\/table>/g,'</table></div>');
  document.getElementById('content').innerHTML=h;
  [].forEach.call(document.querySelectorAll('#content iframe[src$=".pdf"]'),function(f){
    var p=document.createElement('p');p.className='pdf';var a=document.createElement('a');a.href=f.getAttribute('src');a.target='_blank';a.rel='noopener';
    a.textContent='Open the PDF: '+decodeURIComponent(f.getAttribute('src').split('/').pop())+' ↗';p.appendChild(a);f.parentNode.insertBefore(p,f);});
  if(window.MathJax&&MathJax.typesetPromise)MathJax.typesetPromise();
})();
"""
MATH_HEAD = """<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true,tags:'none'}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
"""
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def social(p):
    from urllib.parse import quote
    u, t = quote(p['live'], safe=''), quote(p['title'], safe='')
    return ('<div class="share"><span>Share</span>'
            '<a href="https://twitter.com/intent/tweet?text=%s&url=%s" aria-label="Share on X"><i class="fa-brands fa-x-twitter"></i></a>'
            '<a href="https://www.facebook.com/sharer/sharer.php?u=%s" aria-label="Share on Facebook"><i class="fa-brands fa-facebook"></i></a>'
            '<a href="https://www.linkedin.com/shareArticle?mini=true&url=%s" aria-label="Share on LinkedIn"><i class="fa-brands fa-linkedin"></i></a>'
            '<button type="button" id="copylink" data-u="%s" aria-label="Copy link"><i class="fa-solid fa-link"></i></button></div>'
            '<section class="comments"><h3>Likes and comments</h3><div id="disqus_thread"></div></section>'
            '<script>document.getElementById("copylink").onclick=function(){var b=this;navigator.clipboard&&navigator.clipboard.writeText(b.getAttribute("data-u")).then(function(){b.classList.add("ok");setTimeout(function(){b.classList.remove("ok");},1200);});};'
            'var disqus_config=function(){this.page.url=%s;};(function(){var d=document.createElement("script");d.async=true;d.src="https://https-zhanqizhang66-github-io.disqus.com/embed.js";document.body.appendChild(d);})();</script>'
            % (t, u, u, u, html.escape(p['live']), json.dumps(p['live'])))


def build():
    write('assets/site/site.css', CSS)
    write('assets/site/forest.js', FOREST_JS)
    for k, name in enumerate(COVERS):
        write('assets/site/covers/%s.svg' % name, cover_svg(name, k))
    write('.nojekyll', '')

    # ---- posts
    posts = []
    for f in sorted(x for x in os.listdir(os.path.join(REPO, '_posts')) if x.endswith('.md')):
        fm, body = front(read('_posts/' + f))
        base = f[:-3]
        y, mo, d, rest = re.match(r'(\d+)-(\d+)-(\d+)-(.*)', base).groups()
        dirn = '%s-%02d-%02d-%s' % (y, int(mo), int(d), rest.replace(' ', '-'))  # the same address Jekyll gave the post
        cov = fm.get('cover-img', '')
        tags = [t.strip() for t in fm.get('tags', '').strip('[]').split(',') if t.strip()]
        is_tut = 'tutorials' in tags
        cover = ('/assets/site/covers/' + os.path.basename(cov)) if '/blog/covers/' in cov else ('/' + cov.lstrip('/') if cov else '')
        live = '%s/%s/' % (SITE, dirn)
        share = fm.get('share-img', '') or (cover if cover and not cover.endswith('.svg') else OGIMG)
        if 'og-preview' in share: share = OGIMG
        posts.append(dict(slug=dirn, share='/' + share.lstrip('/'), title=fm.get('title', base), sub=fm.get('subtitle', ''), date=(int(y), int(mo), int(d)),
                          cover=cover, tags=tags, tut=is_tut, live=live, body=body, math='mathjax' in fm.get('head-extra', '')))
    posts.sort(key=lambda p: p['date'], reverse=True)
    for i, p in enumerate(posts):
        nice = '%s %d, %d' % (MONTHS[p['date'][1] - 1], p['date'][2], p['date'][0])
        p['nice'] = nice
        root = ''
        cov = p['cover']
        newer, older = (posts[i - 1] if i > 0 else None), (posts[i + 1] if i + 1 < len(posts) else None)
        pn = '<nav class="pn">%s%s</nav>' % (
            '<a href="/%s/"><span>Older</span>%s</a>' % (older['slug'], html.escape(older['title'])) if older else '<span></span>',
            '<a href="/%s/" style="text-align:right"><span>Newer</span>%s</a>' % (newer['slug'], html.escape(newer['title'])) if newer else '')
        main = '<main class="post"><a class="back" href="/blog/">← All posts</a><h1>%s</h1>%s<p class="pmeta" style="margin-top:%s">%s%s</p>%s<article class="prose" id="content"></article>%s</main>' % (
            html.escape(p['title']), '<p class="sub" style="margin-bottom:10px">%s</p>' % html.escape(p['sub']) if p['sub'] else '', '0' if p['sub'] else '6px', nice,
            ' &nbsp;·&nbsp; ' + ' '.join('<span class="tg">%s</span>' % html.escape(t) for t in p['tags'][:4]) if p['tags'] else '',
            ('<div class="pae-wrap">%s</div>' % essay_art(p['cover'], root) if essay_art(p['cover'], root) else '<img class="cover-img" src="%s" alt="">' % cov) if cov else '', social(p) + pn)
        data = '<script>window.MATH=%s;window.MD=%s;</script><script>%s</script>\n' % ('true' if p['math'] else 'false', json.dumps(p['body']).replace('</', '<\\/'), POST_JS)
        write('%s/index.html' % p['slug'], page(p['title'] + ' · Victoria Zhang', main, path='/%s/' % p['slug'], active='Blog', extra_head=MATH_HEAD, extra_body=data,
                                                desc=p['sub'] or p['title'], img=p['share']))

    # ---- blog index
    def card(p):
        art = essay_art(p['cover'], '') if not p['tut'] else ''
        pic = art or ('<img src="%s" alt="" loading="lazy">' % p['cover'] if p['cover'] else '')
        return '<a class="card" href="/%s/">%s<b>%s</b>%s<em>%s</em></a>' % (
            p['slug'], pic, html.escape(p['title']), '<span>%s</span>' % html.escape(p['sub']) if p['sub'] else '', p['nice'])
    blog = ('<main><h1>Blog</h1><p class="sub">Learning notes and essays.</p>'
            '<h2>Learning notes</h2><div class="grid">%s</div><h2>Essays</h2><div class="grid three">%s</div></main>') % (
        ''.join(card(p) for p in posts if p['tut']), ''.join(card(p) for p in posts if not p['tut']))
    write('blog/index.html', page('Blog · Victoria Zhang', blog, path='/blog/', active='Blog', desc='Learning notes on machine learning, and personal essays, by Victoria Zhang.'))

    # ---- research, with every figure showing
    pub = front(read('publications.md'))[1]
    pub = re.sub(r'<!-- Google tag.*?</script>\s*<script>.*?</script>', '', pub, flags=re.S)
    pub = re.sub(r'<style>.*?</style>', '', pub, flags=re.S)
    pub = re.sub(r'<!--.*?-->', '', pub, flags=re.S)
    pub = re.sub(r'\[\\\[CODE\\\]\]\((\S+?)\)', r'<a class="code" href="\1">Code</a>', pub)
    assert '[CODE' not in pub
    pub, n = re.subn(r"\s*<em>This work currently can't be viewed publicly due to the course policy</em>", '', pub)
    assert n == 1
    pub = re.sub(r'<div class="publication-image">\s*<img src="/assets/img/paper_fig/"[^>]*>\s*</div>', '', pub)
    pub = re.sub(r'^#{2,3}\s*(.+)$', r'<h2>\1</h2>', pub, flags=re.M)
    pub = pub.replace('src="/assets/', 'loading="lazy" src="/assets/')
    simple = read('site-src/nest-source.html')
    ab = re.search(r'NEST learns one embedding.*?</p>', simple, re.S).group(0)[:-4]
    full = re.search(r'<summary>Abstract</summary><div>(Real-world data.*?)<img', simple, re.S).group(1)
    nest = ('\n<div class="publication-row"><div class="publication-content">'
            '<div class="pub-title"><a href="https://arxiv.org/abs/2610.30520">NEST: Nested Embedding Representation for Multiscale Clustering</a></div>'
            '<div class="pub-authors"><b>Zhang, Z.</b>, Aoi, M., &amp; Mishne, G.</div><div class="pub-venue"><b>preprint</b></div>'
            '<div class="pub-abstract"><details><summary>TL;DR: %s</summary>%s</details></div>'
            '<div class="publication-image"><img loading="lazy" src="/assets/img/paper_fig/nest.png" alt="NEST"></div></div></div>\n') % (ab, full)
    i = pub.index('<div class="publication-row">')
    pub = pub[:i] + nest + pub[i:]
    SRC = 'https://cloud.google.com/blog/products/ai-machine-learning/scaling-deep-retrieval-tensorflow-two-towers-architecture'
    google = ('\n<div class="publication-row" id="google"><div class="publication-content">'
              '<div class="pub-title">Filtered vector search at billion scale</div>'
              '<div class="pub-authors">Work done as a Student Researcher at Google (Summer 2026)</div>'
              '<div class="pub-abstract"><details><summary>TL;DR: Made approximate nearest neighbor search maintain its target recall even with highly restrictive metadata filters, at the scale of billions of vectors.</summary>'
              '<p>Vector search finds documents based on <b>embedding similarity</b>, while metadata filters narrow the results based on conditions like language, date, or access permissions. '
              'In practice, search systems often need to do both: find the most similar documents that also satisfy the query’s filters.</p>'
              '<p>Large-scale vector search systems speed things up by clustering similar embeddings and searching only a small number of promising clusters. '
              'This works well without filters, but becomes challenging when filters are highly selective. For example, if only 1 in 1,000 documents passes a filter, '
              'the nearest matching documents may be much harder to find. Searching the usual number of clusters can miss them entirely, causing recall to fall below its target.</p>'
              '<p>I designed and implemented <b>selectivity-aware autotuning</b> for a production vector search system. The system estimates how restrictive each query’s filter is at runtime '
              'and adjusts the search budget across different levels of the index. This allows it to search more broadly when needed while maintaining the target recall across different filter selectivities.</p>'
              '<p>I also evaluated the impact on throughput and latency through large-scale distributed load tests, and explored ways to update index centroids as the data changes without rebuilding the entire index.</p>'
              '</details></div>'
              '<div class="publication-image"><img loading="lazy" src="/assets/img/paper_fig/google_vector_search.jpg" alt="Partitioned vector search: centroids, leaf partitions and re-scoring">'
              '<p class="figsrc">Figure source: <a href="%s">Google Cloud Blog, Scaling deep retrieval with TensorFlow Recommenders and Vertex AI Matching Engine</a>.</p></div>'
              '</div></div>\n') % SRC
    NB = 'https://www.meta.com/ai-glasses/meta-ray-ban-display/?srsltid=AfmBOoqJgguuzbd2lgoz1FicSW5Bnj5K1sXeNkIHcpDYIU3ILs_aoC2d'
    meta_new = ('<summary>TL;DR: Built models that made handwriting recognition on the Meta Neural Band more robust; shipped in the product, live demoed at Meta Connect 2025, and named one of <em>TIME</em>’s Best Inventions of 2025.</summary>'
                '<p>The <a href="%s">Meta Neural Band</a> is a wristband that reads <b>surface EMG</b>, the electrical activity of forearm muscles, and turns subtle finger movements into input for AI glasses. '
                'One of its features is handwriting: you trace letters with your finger on any surface, and the band decodes them into text.</p>'
                '<p>Decoding handwriting from muscle signals is hard to make reliable. The signals differ from person to person and from one wearing of the band to the next, '
                'and the model has to run in real time on a product people use every day.</p>'
                '<p>I developed models that improved the <b>robustness</b> of the handwriting recognition system productionized in the Neural Band. '
                'The work was <a href="https://www.youtube.com/live/D97ILdUbYww?si=krptKIikEhFvF9O9&t=2975">live demoed at Meta Connect 2025</a> and later recognized as one of '
                '<a href="https://time.com/collections/best-inventions-2025/7318319/meta-ray-ban-display/"><em>TIME</em>’s Best Inventions of 2025</a>.</p>') % (NB, )
    pub, n = re.subn(r'<summary>TL;DR: Built models that improved the robustness.*?(?=\s*</details>)', lambda m: meta_new, pub, count=1, flags=re.S)
    assert n == 1
    meta24 = ('<summary>TL;DR: Developed EMG–vision multimodal foundation models for Meta’s neural wristbands, improving several downstream tasks including pose estimation.</summary>'
              '<p>Neural wristbands read <b>surface EMG</b>, the electrical activity of forearm muscles. The signal says a lot about what the hand is doing, '
              'but it is noisy, and it differs from person to person, so a model trained on one task or one group of users often does not carry over to another.</p>'
              '<p>Vision gives a complementary view of the same movement: a camera sees the hand’s pose directly, while EMG senses the muscle activity that produces it. '
              'Learning from both together can give a representation that neither signal provides alone.</p>'
              '<p>I developed <b>EMG–vision multimodal foundation models</b> at <a href="https://research.facebook.com/">Meta</a>, using joint representation learning between EMG signals and synchronized vision streams. '
              'The models improved performance on multiple downstream tasks, such as pose estimation, and were built to generalize across users and tasks.</p>')
    pub, n = re.subn(r'<summary>TL;DR: Developed EMG–vision multimodal foundation models.*?(?=\s*</details>)', lambda m: meta24, pub, count=1, flags=re.S)
    assert n == 1
    h = '<h2>Industry Research</h2>'
    j = pub.index(h) + len(h)
    k = pub.index('<div class="publication-row">', j)
    pub = pub[:j] + '\n' + google + pub[k:].replace('<div class="publication-row">', '<div class="publication-row" id="meta">', 1)
    write('publications/index.html', page('Research · Victoria Zhang',
                                          '<main><h1>Selected Projects</h1><p class="sub">Papers, industry work and early projects.</p>%s</main>' % pub,
                                          path='/publications/', active='Research', desc='Papers, industry research and projects by Victoria Zhang.'))

    # ---- art and home
    art = ('<main><h1>Sometimes I draw</h1><p class="sub">I would like to paint the way a bird sings, and fill a space in a beautiful way.</p>'
           '<section><script src="https://static.elfsight.com/platform/platform.js" data-use-service-core defer></script>'
           '<div class="elfsight-app-0cca0446-147e-49ce-94da-272276274e9c"></div></section></main>')
    write('art/index.html', page('Art · Victoria Zhang', art, path='/art/', active='Art', desc='Drawings and paintings by Victoria Zhang.'))
    cover = HOME_MAIN[HOME_MAIN.index('<div class="cover">'):HOME_MAIN.index('<section id="news">')]
    old = '<p class="tag">Ph.D. candidate at UC San Diego. Previously at Google and Meta.</p>'
    assert old in cover
    cover = cover.replace(old, '<p class="tag"><span class="nw">Machine Learning Research Scientist</span><br><span class="nw">Ph.D., UC San Diego</span> · <span class="nw">Ex-Google &amp; Meta</span></p>')
    cover = must(cover, '<p class="tag">Working on <b>representation learning</b> and <b>retrieval</b>.</p>',
                 '<p class="tag">Representation · AI Agents · Reasoning · Adaptation</p>')
    cover = must(cover, '<a href="https://twitter.com/ZhangZhanqi"><i class="fa-brands fa-x-twitter"></i>X</a>',
                 '<a href="https://twitter.com/ZhangZhanqi"><i class="fa-brands fa-x-twitter"></i>X</a>')
    about = re.search(r'<section class="about">.*?</section>', HOME_MAIN, re.S).group(0)
    teach = re.search(r'<section><h3>Teaching</h3>.*?</section>', HOME_MAIN, re.S).group(0)
    exp = re.search(r'<section><h3>Experience</h3>.*?</section>', HOME_MAIN, re.S).group(0)
    for a, b in [
        ('<span class="d">2021 –</span>', '<span class="d">2021 – 2026</span>'),
        ('<span class="d">2016 – 21</span>', '<span class="d">2016 – 2021</span>'),
        ('B.S. CS &amp; EE, M.S. CS', 'B.S. Computer Science and Electrical Engineering, M.S. Computer Science')]:
        if a not in exp: a = a.replace('&amp;', '&')
        exp = must(exp, a, b)
    about = must(about, 'a Ph.D. candidate in Computer Science at <a href="https://cse.ucsd.edu/">UC San Diego</a>, supported by the HDSI Ph.D. Fellowship. I’m co-advised by',
                 'an ML research scientist. I finished my Ph.D. in Computer Science at <a href="https://cse.ucsd.edu/">UC San Diego</a> in 2026, supported by the HDSI Ph.D. Fellowship and co-advised by')
    def row(d, t, old=False):
        return '<div class="ln%s"><span class="d">%s</span><span>%s</span></div>' % (' old' if old else '', d, t)
    A = lambda u, t: '<a href="%s">%s</a>' % (u, t)
    news = ''.join([
        row('Nov 6, 2026', '<b>Defended my Ph.D.</b> in Computer Science at UC San Diego.'),
        row('Oct 2026', 'New preprint: ' + A('https://arxiv.org/abs/2610.30520', 'NEST: Nested Embedding Representation for Multiscale Clustering') + '.'),
        row('Summer 2026', 'Student Researcher at <b>Google</b>, working on vector search and retrieval.'),
        row('May 2026', 'New preprint: ' + A('https://arxiv.org/abs/2605.07127', 'The Position Curse: LLMs Struggle to Locate the Last Few Items in a List') + '.'),
        row('2026', A('https://arxiv.org/abs/2603.18299', 'ALIGN') + ', on adversarial domain adaptation, accepted at UAI.'),
        row('2025', A('https://openreview.net/forum?id=hOE8xaCByN', 'BEHAVE') + ' accepted at the ' + A('https://data-brain-mind.github.io/', 'NeurIPS 2025 Workshop on Data on Brain and Mind') + '.', True),
        row('2025', A('https://www.science.org/doi/10.1126/sciadv.adq7342', 'Brain Feature Maps Reveal Progressive Animal-Feature Representations') + ' published in <em>Science Advances</em> and ' + A('https://brain.harvard.edu/hbi_news/when-neurons-discover-on-their-own/', 'featured by Harvard Brain Institute News') + '.', True),
        row('2025', 'Co-authored ' + A('https://www.nature.com/articles/s41586-025-09544-4', 'Arousal as a universal embedding for spatiotemporal brain dynamics') + ', published in <em>Nature</em>.', True),
        row('2024', 'Preprint on ' + A('https://www.medrxiv.org/content/10.1101/2024.11.14.24317348v2', 'Behavioral Dynamics in Bipolar Disorder') + ' on medRxiv.', True),
    ])
    work = ''.join('<div class="ln"><span class="d">%s</span>%s</div>' % (v, A(u, t)) for v, t, u in [
        ('arXiv 2026', 'NEST: Nested Embedding Representation for Multiscale Clustering', 'https://arxiv.org/abs/2610.30520'),
        ('arXiv 2026', 'The Position Curse: LLMs Struggle to Locate the Last Few Items in a List', 'https://arxiv.org/abs/2605.07127'),
        ('UAI 2026', 'ALIGN: Adversarial Learning for Generalizable Speech Neuroprosthesis', 'https://arxiv.org/abs/2603.18299'),
        ('Google 2026', 'Filtered vector search at billion scale', '/publications/#google'),
        ('Meta 2025', 'Handwriting decoding for the Meta Neural Band', '/publications/#meta')])
    home = ('<main>' + cover
            + '<section id="news"><h3>News</h3><div class="newsl" id="newsl">%s</div><button class="more" id="more">Earlier news ↓</button></section>' % news
            + '<section><h3>Selected work</h3>%s<p class="after"><a href="/publications/">Check out my work →</a></p></section>' % work
            + exp + about + teach + '</main>')
    home_js = "<script>document.getElementById('more').onclick=function(){var l=document.getElementById('newsl').classList.toggle('all');this.textContent=l?'Fewer ↑':'Earlier news ↓';};</script>\n"
    assert 'href="research.html' not in home and 'href="blog.html' not in home
    write('index.html', page('Victoria Zhang', home, path='/', active='Home', extra_body=home_js))

    # ---- not found, and the old addresses that no longer have a page of their own
    lost = ('<main><h1>This page flew away.</h1><p class="sub">There is nothing at this address.</p>'
            '<p><a href="/">Back to the home page →</a></p><p><a href="/blog/">Or read the blog →</a></p></main>')
    write('404.html', page('Page not found · Victoria Zhang', lost, path='/404.html'))
    for old, to in [('aboutme', '/'), ('essays', '/blog/'), ('tutorials', '/blog/'), ('popular', '/blog/'), ('tags', '/blog/'), ('page2', '/blog/'), ('page3', '/blog/'), ('page4', '/blog/')]:
        write(old + '/index.html', '<!doctype html><meta charset="utf-8"><title>Victoria Zhang</title><link rel="canonical" href="%s%s">'
                                   '<meta http-equiv="refresh" content="0; url=%s"><a href="%s">This page has moved.</a>\n' % (SITE, to, to, to))
    print('built', len(posts), 'posts into', OUT)


if __name__ == '__main__':
    build()
