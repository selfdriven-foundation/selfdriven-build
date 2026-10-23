#!/usr/bin/env python3
"""Bundle the three TrialThread pages into one self-contained trialthread.html.

index.html (front door), trialthread-plan.html (concept plan) and the Observer
app are each carried whole as an in-page view, so nothing navigates to another
file. A Notes panel (right side) lets a reviewer pick any section from a
dropdown, write a note, and download the notes as JSON; notes are kept in the
browser (localStorage) until downloaded. Links between them switch views instead; the plan's two reference images
are inlined. The three source pages stay the source: edit them, then rebuild.

Run after scripts/build-plan.py:  python3 scripts/build-single.py
"""
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "trialthread.html"
OBS = "areas-of-focus/02-enablement/workings/trialthread-observer-app.html"
APP = "areas-of-focus/02-enablement/workings/trialthread-app.html"
VIEWS = [  # key, label, source; the first is where the page opens
    ("app", "Try the app", APP),
    ("home", "Overview", "index.html"),
    ("plan", "The plan", "trialthread-plan.html"),
    ("observer", "Observer app", OBS),
]

# Runs inside each view: route cross-page links to the parent, follow its theme.
BRIDGE = """<script>(function(){
const K={'trialthread-app.html':'app','index.html':'home','trialthread-plan.html':'plan','trialthread-observer-app.html':'observer'};
function route(href){if(!href)return null;const m=href.match(/(?:^|\\/)(trialthread-app\\.html|index\\.html|trialthread-plan\\.html|trialthread-observer-app\\.html)(#.*)?$/);return m?{view:K[m[1]],hash:m[2]||''}:null}
document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('a[href]');if(!a)return;const r=route(a.getAttribute('href'));if(!r)return;e.preventDefault();e.stopPropagation();parent.postMessage({tt:'go',view:r.view,hash:r.hash},'*')},true);
addEventListener('message',e=>{const d=e.data||{};if(d.tt==='theme'){if(d.theme)document.documentElement.dataset.theme=d.theme;else delete document.documentElement.dataset.theme;const b=document.getElementById('themeBtn');if(b){const dk=d.theme?d.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;b.textContent=dk?'\\u2600':'\\u263e'}}
 if(d.tt==='hash'){const el=d.hash&&d.hash.length>1&&document.getElementById(decodeURIComponent(d.hash.slice(1)));if(el)el.scrollIntoView({behavior:'smooth'});else if(d.top)scrollTo(0,0)}});
const tb=document.getElementById('themeBtn');if(tb)tb.addEventListener('click',()=>setTimeout(()=>parent.postMessage({tt:'theme',theme:document.documentElement.dataset.theme||''},'*'),0));
})();</script>"""

# Runs inside each view: per-section note tags. The parent owns the notes and
# the editor (one panel on the right); a view only reports its sections, which
# one is on screen, and outlines the section being noted.
NOTES_FRAME = r"""<style>
.ttn-badge{position:absolute;top:76px;right:14px;z-index:45;font:700 11px/1 'JetBrains Mono',ui-monospace,monospace;padding:7px 11px;border-radius:999px;cursor:pointer;background:rgba(12,9,8,.86);color:#ffb4a8;border:1px dashed #e85d4a;box-shadow:0 6px 20px rgba(0,0,0,.25);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.ttn-badge:hover{color:#fff;border-style:solid}
.ttn-badge.has{background:#e85d4a;color:#fff;border:1px solid #e85d4a}
.ttn-target{outline:2px dashed rgba(232,93,74,.6);outline-offset:-6px}
</style>
<script>(function(){
let VIEW='',ON=false,NOTES={},hereKey='',ht=0;
const targets=()=>[...document.querySelectorAll('header[id],section[id],.step[data-s]')];
const keyOf=el=>el.matches('.step[data-s]')?'story-scene-'+(+el.dataset.s+1):el.id;
function titleOf(el){const h=el.querySelector('h1,h2,h3');const t=(h&&h.textContent.trim())||(el.querySelector('.eyebrow,.num')||{}).textContent||keyOf(el);
 const eb=el.querySelector('.eyebrow,.num');const pre=eb&&h?eb.textContent.trim()+' · ':'';return (pre+t).replace(/\s+/g,' ').replace(/^(\d+)(?=[A-Za-z])/,'$1 · ').trim().slice(0,110)}
const post=m=>parent.postMessage(Object.assign({view:VIEW},m),'*');
function render(){document.querySelectorAll('.ttn-badge').forEach(b=>b.remove());if(!ON){mark('');return}
 targets().forEach(el=>{const k=keyOf(el),has=NOTES[k]&&NOTES[k].text&&NOTES[k].text.trim();if(getComputedStyle(el).position==='static')el.style.position='relative';
  const b=document.createElement('button');b.type='button';b.className='ttn-badge'+(has?' has':'');b.textContent=has?'✎ Note':'✎ Add note';b.title='Note on: '+titleOf(el);
  b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();post({tt:'pick',key:k})});el.appendChild(b)})}
function mark(k){document.querySelectorAll('.ttn-target').forEach(t=>t.classList.remove('ttn-target'));const el=k&&k!=='_page'?targets().find(t=>keyOf(t)===k):null;if(el&&ON)el.classList.add('ttn-target');return el}
function here(){if(!ON||!innerHeight)return;const y=innerHeight*.35;let best=null;for(const el of targets()){const r=el.getBoundingClientRect();if(r.height&&r.top<=y&&r.bottom>y)best=el}
 const k=best?keyOf(best):'_page';if(k!==hereKey){hereKey=k;post({tt:'here',key:k})}}
addEventListener('scroll',()=>{clearTimeout(ht);ht=setTimeout(here,120)},{passive:true});
addEventListener('message',e=>{const d=e.data||{};
 if(d.tt==='notes'){const was=ON;VIEW=d.view;ON=!!d.on;NOTES=d.notes||{};render();if(ON&&!was){post({tt:'sections',list:targets().map(el=>({key:keyOf(el),title:titleOf(el)}))});hereKey='';here()}}
 if(d.tt==='goto'){const el=mark(d.key);if(d.scroll){if(el)el.scrollIntoView({behavior:'smooth',block:'start'});else if(d.key==='_page')scrollTo({top:0,behavior:'smooth'})}}
 if(d.tt==='here?'){hereKey='';here()}});
})();</script>"""

NOTES_SHELL_CSS = r"""
.nbtn{position:fixed;top:76px;right:max(16px,env(safe-area-inset-right));z-index:12;display:inline-flex;align-items:center;gap:8px;font:700 12px/1 'JetBrains Mono',monospace;padding:9px 14px;border-radius:999px;cursor:pointer;color:#f0ede8;background:rgba(12,9,8,.82);border:1px solid rgba(232,93,74,.55);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 10px 30px rgba(0,0,0,.3)}
.nbtn .n{min-width:18px;height:18px;border-radius:9px;background:#e85d4a;color:#fff;display:inline-grid;place-items:center;font-size:10px;padding:0 5px}
body.notes-open .nbtn{display:none}
.npanel{position:fixed;top:0;right:0;bottom:0;z-index:20;width:380px;max-width:100vw;display:flex;flex-direction:column;gap:0;overflow-y:auto;background:#0e0b0a;color:#f0ede8;border-left:1px solid rgba(232,93,74,.45);box-shadow:-20px 0 60px rgba(0,0,0,.35);padding:18px 18px 28px;font-family:'Poppins',system-ui,sans-serif}
.npanel[hidden]{display:none}
@media(min-width:900px){body.notes-open iframe{width:calc(100% - 380px)}body.notes-open .switch{right:396px}}
@media(max-width:899px){.npanel{width:min(420px,100vw)}body.notes-open .switch{display:none}}
.npanel .nhead{display:flex;align-items:center;gap:10px}
.npanel h3{font-size:18px;font-weight:800;letter-spacing:-.02em}
.npanel .ncount{font:700 11px/1 'JetBrains Mono',monospace;color:#ff8a78;background:rgba(232,93,74,.14);padding:5px 9px;border-radius:999px}
.npanel .x{margin-left:auto;width:32px;height:32px;padding:0;border-radius:50%;font-size:18px;line-height:1}
.npanel .nintro{font-size:12.5px;color:#b0a89e;line-height:1.5;margin-top:8px}
.npanel label{display:block;font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#ff8a78;margin:16px 0 6px}
.npanel input[type=search],.npanel select,.npanel textarea{width:100%;border-radius:12px;border:1px solid #3a302a;background:#070605;color:#f0ede8;padding:10px 12px;font:14px/1.45 'Poppins',system-ui,sans-serif}
.npanel select{appearance:none;-webkit-appearance:none;padding-right:34px;background-image:linear-gradient(45deg,transparent 50%,#ff8a78 50%),linear-gradient(135deg,#ff8a78 50%,transparent 50%);background-position:calc(100% - 18px) 50%,calc(100% - 13px) 50%;background-size:5px 5px;background-repeat:no-repeat;cursor:pointer}
.npanel select option,.npanel select optgroup{background:#0e0b0a;color:#f0ede8}
.npanel textarea{min-height:150px;resize:vertical}
.npanel input:focus,.npanel select:focus,.npanel textarea:focus{outline:2px solid #e85d4a;outline-offset:1px}
.npanel .follow{font:11px 'JetBrains Mono',monospace;color:#9c9389;margin-top:6px}
.npanel .follow button{background:none;border:0;color:#ff8a78;padding:0;font:inherit;text-decoration:underline;cursor:pointer}
.npanel .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px}
.npanel button{font:700 12px/1 'Poppins',system-ui,sans-serif;border-radius:999px;padding:9px 13px;cursor:pointer;border:1px solid #5a4a40;background:transparent;color:#f0ede8}
.npanel button.pri{background:#e85d4a;border-color:#e85d4a;color:#fff}
.npanel button:disabled{opacity:.4;cursor:default}
.npanel .danger{color:#ff8a78;border-color:#5a2a22}
.npanel .st{margin-left:auto;font:11px 'JetBrains Mono',monospace;color:#9c9389}
.npanel .sep{height:1px;background:#2a2320;margin:20px 0 4px}
.npanel h4{font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#ff8a78;margin:18px 0 8px}
.npanel .list{display:grid;gap:8px}
.npanel .it{border:1px solid #2a2a2a;border-radius:12px;padding:9px 11px;cursor:pointer;background:#141010;text-align:left}
.npanel .it:hover,.npanel .it.sel{border-color:#e85d4a}
.npanel .it small{display:block;font:700 10px/1.35 'JetBrains Mono',monospace;color:#ff8a78;letter-spacing:.04em}
.npanel .it span{display:block;font-size:12.5px;color:#d6cdc2;margin-top:3px;white-space:pre-wrap;max-height:3.9em;overflow:hidden}
.npanel .empty{font-size:12.5px;color:#8a8076}
.npanel .msg{font:11px 'JetBrains Mono',monospace;color:#3fb97a;margin-top:8px;min-height:14px}
"""

NOTES_SHELL_HTML = r"""<button class="nbtn" id="notesBtn" aria-expanded="false" aria-controls="notesPanel">&#9998; Notes <span class="n" id="notesN">0</span></button>
<aside class="npanel" id="notesPanel" hidden aria-label="Review notes">
<div class="nhead"><h3>Review notes</h3><span class="ncount" id="notesCount">0 notes</span><button class="x" id="notesClose" aria-label="Close notes">&#215;</button></div>
<p class="nintro">Pick a section, or just scroll: the section follows what you're reading. Sections with a note are marked &#9679;. Write your note, then download the file and send it to Peter.</p>
<label for="notesName">Your name</label><input type="search" id="notesName" name="tt-reviewer" placeholder="e.g. Giau" autocomplete="off" data-1p-ignore data-lpignore="true" data-bwignore spellcheck="false">
<label for="notesSec">Section</label><select id="notesSec"></select>
<div class="follow" id="notesFollow"></div>
<label for="notesText">Note</label><textarea id="notesText" placeholder="What should change, what is wrong, what is missing?"></textarea>
<div class="row"><button class="pri" id="notesSave">Save note</button><button id="notesDel">Delete</button><span class="st" id="notesStat" role="status"></span></div>
<div class="sep"></div>
<div class="row"><button class="pri" id="notesDl">&#8595; Download JSON</button><button id="notesImp">Import JSON</button><button class="danger" id="notesClr">Clear all</button><input type="file" id="notesFile" accept="application/json,.json" hidden></div>
<div class="msg" id="notesMsg" role="status"></div>
<h4>All notes</h4><div class="list" id="notesList"></div>
</aside>"""

NOTES_SHELL_JS = r"""
const NKEY='tt-notes-v1',NAMEKEY='tt-notes-author',LABEL=Object.fromEntries([...document.querySelectorAll('.switch button')].map(b=>[b.dataset.v,b.textContent]));
const $n=id=>document.getElementById(id);
let NOTES={},NON=false,SECTIONS={},SEL={view:null,key:null},manual=false,nT=0;
try{NOTES=JSON.parse(localStorage.getItem(NKEY)||'{}')||{}}catch(e){NOTES={}}
const nName=$n('notesName'),nSel=$n('notesSec'),nText=$n('notesText'),nStat=$n('notesStat');
try{nName.value=localStorage.getItem(NAMEKEY)||''}catch(e){}
nName.addEventListener('input',()=>{try{localStorage.setItem(NAMEKEY,nName.value)}catch(e){}});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const has=(v,k)=>!!(NOTES[v]&&NOTES[v][k]&&NOTES[v][k].text&&NOTES[v][k].text.trim());
const flat=()=>Object.keys(VIEWS).flatMap(v=>Object.entries(NOTES[v]||{}).filter(([k])=>has(v,k)).map(([k,n])=>({view:v,key:k,...n})));
function titleFor(v,k){if(k==='_page')return 'Whole page';const s=(SECTIONS[v]||[]).find(s=>s.key===k);return s?s.title:(NOTES[v]&&NOTES[v][k]&&NOTES[v][k].title)||k}
function nPersist(){try{localStorage.setItem(NKEY,JSON.stringify(NOTES))}catch(e){}}
function nSend(k){const f=frames[k];if(f&&f.dataset.ready)f.contentWindow.postMessage({tt:'notes',view:k,on:NON,notes:NOTES[k]||{}},'*')}
function nPost(v,m){const f=frames[v];if(!f)return;const go=()=>f.contentWindow.postMessage(m,'*');if(f.dataset.ready)go();else f.addEventListener('load',()=>setTimeout(go,150),{once:true})}
function nMsg(t){const m=$n('notesMsg');m.textContent=t;clearTimeout(m._t);m._t=setTimeout(()=>m.textContent='',4000)}
function nOptions(){nSel.innerHTML=Object.keys(VIEWS).map(v=>{const secs=SECTIONS[v]||[],extra=Object.keys(NOTES[v]||{}).filter(k=>k!=='_page'&&has(v,k)&&!secs.some(s=>s.key===k)).map(k=>({key:k,title:titleFor(v,k)}));
  return `<optgroup label="${esc(LABEL[v]||v)}"><option value="${v}|_page">${has(v,'_page')?'● ':''}${esc(LABEL[v]||v)} · whole page</option>`+secs.concat(extra).map(s=>`<option value="${v}|${esc(s.key)}">${has(v,s.key)?'● ':''}${esc(s.title)}</option>`).join('')+'</optgroup>'}).join('');
 if(SEL.view)nSel.value=SEL.view+'|'+SEL.key}
function nFollow(){$n('notesFollow').innerHTML=manual?'Section locked. <button type="button" id="notesUnlock">Follow my scrolling</button>':'Following what you’re reading.';const u=$n('notesUnlock');if(u)u.onclick=()=>{manual=false;nFollow();nPost(cur,{tt:'here?'})}}
function nRender(){const all=flat();$n('notesN').textContent=all.length;$n('notesCount').textContent=all.length+' note'+(all.length===1?'':'s');$n('notesDl').disabled=!all.length;
 $n('notesList').innerHTML=all.length?all.map(n=>`<button type="button" class="it${SEL.view===n.view&&SEL.key===n.key?' sel':''}" data-v="${esc(n.view)}" data-k="${esc(n.key)}"><small>${esc(LABEL[n.view]||n.view)} · ${esc(n.title||titleFor(n.view,n.key))}</small><span>${esc(n.text)}</span></button>`).join(''):'<p class="empty">No notes yet.</p>';
 document.querySelectorAll('#notesList .it').forEach(el=>el.onclick=()=>nSelect(el.dataset.v,el.dataset.k,{scroll:true,lock:true}));nOptions()}
function nSave(){clearTimeout(nT);nT=0;if(!SEL.view)return;const v=NOTES[SEL.view]=NOTES[SEL.view]||{},t=nText.value,had=has(SEL.view,SEL.key);
 if(t.trim())v[SEL.key]={title:titleFor(SEL.view,SEL.key),text:t,author:(nName.value||'').trim()||null,updated:new Date().toISOString()};else delete v[SEL.key];
 nPersist();nSend(SEL.view);nStat.textContent=t.trim()?'saved':(had?'deleted':'');if(had!==has(SEL.view,SEL.key)||t.trim())nRender()}
function nSelect(v,k,o={}){if(nT)nSave();if(o.lock){manual=true;nFollow()}SEL={view:v,key:k};nSel.value=v+'|'+k;nText.value=has(v,k)?NOTES[v][k].text:'';nStat.textContent=has(v,k)?'saved':'';
 document.querySelectorAll('#notesList .it').forEach(el=>el.classList.toggle('sel',el.dataset.v===v&&el.dataset.k===k));
 if(v!==cur)show(v,'',true);nPost(v,{tt:'goto',key:k,scroll:!!o.scroll})}
nSel.onchange=()=>{const [v,...r]=nSel.value.split('|');nSelect(v,r.join('|'),{scroll:true,lock:true})};
nText.addEventListener('input',()=>{if(!manual){manual=true;nFollow()}nStat.textContent='saving…';clearTimeout(nT);nT=setTimeout(nSave,500)});
$n('notesSave').onclick=()=>{nSave();if(nText.value.trim())nMsg('Note saved.')};
$n('notesDel').onclick=()=>{nText.value='';nSave()};
function nToggle(on){NON=on;document.body.classList.toggle('notes-open',on);$n('notesPanel').hidden=!on;$n('notesBtn').setAttribute('aria-expanded',on);
 if(on){Object.keys(VIEWS).forEach(frame);if(!SEL.view){SEL={view:cur,key:'_page'}}nFollow();nRender();nSelect(SEL.view===cur?SEL.view:cur,SEL.view===cur?SEL.key:'_page')}else if(nT)nSave();
 Object.keys(frames).forEach(nSend)}
$n('notesBtn').onclick=()=>nToggle(true);
$n('notesClose').onclick=()=>nToggle(false);
addEventListener('keydown',e=>{if(e.key==='Escape'&&NON&&document.activeElement!==nText)nToggle(false)});
const __show=show;show=function(k,h,p){__show(k,h,p);if(NON&&SEL.view!==cur){manual=false;nFollow();nSelect(cur,'_page')}};
$n('notesDl').onclick=()=>{if(nT)nSave();const all=flat(),who=(nName.value||'').trim(),now=new Date();
 const data={format:'trialthread-notes/v1',page:'trialthread.html',exportedAt:now.toISOString(),reviewer:who||null,count:all.length,
  notes:all.map(n=>({view:n.view,viewLabel:LABEL[n.view]||n.view,section:n.key,sectionTitle:n.key==='_page'?'Whole page':(n.title||n.key),note:n.text,author:n.author||who||null,updated:n.updated}))};
 const slug=(who||'reviewer').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'reviewer',d=now.toISOString().slice(0,10).replace(/-/g,'');
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=`trialthread-notes-${slug}-${d}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);nMsg(`Downloaded ${all.length} note${all.length===1?'':'s'}.`)};
$n('notesImp').onclick=()=>$n('notesFile').click();
$n('notesFile').onchange=async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;
 try{const d=JSON.parse(await file.text());if(!d||!Array.isArray(d.notes))throw 0;let n=0;
  d.notes.forEach(x=>{if(!x||!x.view||!x.section||typeof x.note!=='string'||!x.note.trim())return;const v=NOTES[x.view]=NOTES[x.view]||{},old=v[x.section];
   if(old&&old.text&&old.text.trim()){if(old.text.includes(x.note))return;v[x.section]={...old,text:old.text+'\n\n— '+(x.author||'imported')+': '+x.note,updated:new Date().toISOString()}}
   else v[x.section]={title:x.sectionTitle||x.section,text:x.note,author:x.author||null,updated:x.updated||new Date().toISOString()};n++});
  nPersist();nRender();Object.keys(frames).forEach(nSend);if(SEL.view)nSelect(SEL.view,SEL.key);nMsg(n?`Imported ${n} note${n===1?'':'s'}${d.reviewer?' from '+d.reviewer:''}.`:'Nothing new to import.')}
 catch(err){nMsg('That file is not a TrialThread notes export.')}};
let clrArmed=0;$n('notesClr').onclick=e=>{const b=e.currentTarget;if(!flat().length)return;
 if(!clrArmed){b.textContent='Click again to clear';clrArmed=setTimeout(()=>{clrArmed=0;b.textContent='Clear all'},3000);return}
 clearTimeout(clrArmed);clrArmed=0;b.textContent='Clear all';NOTES={};nText.value='';nPersist();nRender();Object.keys(frames).forEach(nSend);nMsg('All notes cleared.')};
addEventListener('message',e=>{const d=e.data||{};if(!d.tt||!d.view)return;
 if(d.tt==='sections'){SECTIONS[d.view]=d.list;nOptions()}
 if(d.tt==='here'&&NON&&!manual&&d.view===cur&&!nT&&!(SEL.view===d.view&&SEL.key===d.key))nSelect(d.view,d.key);
 if(d.tt==='pick'){nSelect(d.view,d.key,{lock:true});nText.focus()}});
nFollow();nRender();
"""


def inline_images(html: str) -> str:
    def fix(m):
        p = ROOT / m.group(1)
        if not p.exists():
            return m.group(0)
        mime = "image/jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else f"image/{p.suffix[1:].lower()}"
        return f'src="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"'
    return re.sub(r'src="((?:\.\./)*areas-of-focus/[^"]+\.(?:jpe?g|png|webp|gif))"', fix, html)


def view_html(src: str) -> str:
    s = inline_images((ROOT / src).read_text())
    s = s.replace('<a class="btn" id="mdvRaw"', '<a class="btn" id="mdvRaw" hidden')  # raw .md lives in another file
    return s.replace("</body>", BRIDGE + "\n" + NOTES_FRAME + "\n</body>", 1)


def main():
    data = {k: view_html(src) for k, _, src in VIEWS}
    payload = json.dumps(data).replace("</", "<\\/")
    tabs = "".join(f'<button role="tab" data-v="{k}" aria-selected="false">{label}</button>' for k, label, _ in VIEWS)
    OUT.write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>TrialThread</title>
<!-- catalogue -->
<meta name="sd:title" content="TrialThread">
<meta name="sd:group" content="selfdriven">
<meta name="sd:tone"  content="caring">
<meta name="sd:icon"  content="ic-thread">
<meta name="sd:tag"   content="clinical trials">
<meta name="sd:line"  content="One verified thread from source to submission. AI observers check every record; a named human signs.">
<meta name="sd:cta"   content="Follow the thread">
<meta name="sd:order" content="50">
<!-- /catalogue -->
<!-- Generated by scripts/build-single.py from trialthread-app.html, index.html, trialthread-plan.html and the Observer app. Do not edit; rebuild. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f5f2ed;--text:#1a1410;--accent:#c8442f;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a0a0a;--text:#f0ede8;--accent:#e85d4a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0a0a0a;--text:#f0ede8;--accent:#e85d4a;color-scheme:dark}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;background:var(--bg);overflow:hidden}}
iframe{{position:fixed;inset:0;width:100%;height:100%;border:0;display:none;background:var(--bg)}}
iframe.on{{display:block}}
.switch{{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));z-index:10;display:flex;gap:4px;padding:5px;border-radius:999px;background:rgba(12,9,8,.82);border:1px solid rgba(232,93,74,.45);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 14px 40px rgba(0,0,0,.35);max-width:calc(100vw - 32px)}}
.switch button{{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;letter-spacing:.02em;color:#d6cdc2;background:transparent;border:0;border-radius:999px;padding:9px 14px;cursor:pointer;white-space:nowrap;transition:background .25s,color .25s}}
.switch button:hover{{color:#fff}}
.switch button[aria-selected="true"]{{background:#e85d4a;color:#fff;box-shadow:0 6px 20px rgba(232,93,74,.5)}}
.switch button:focus-visible{{outline:2px solid #ff8a78;outline-offset:2px}}
@media(max-width:420px){{.switch button{{padding:8px 10px;font-size:11px}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
{NOTES_SHELL_CSS}
</style>
</head>
<body>
<nav class="switch" role="tablist" aria-label="TrialThread views">{tabs}</nav>
{NOTES_SHELL_HTML}
<script>
const VIEWS={payload};
const frames={{}};let cur=null,theme='';
try{{theme=localStorage.getItem('tt-theme')||''}}catch(e){{}}
if(theme)document.documentElement.dataset.theme=theme;
function frame(k){{if(frames[k])return frames[k];const f=document.createElement('iframe');f.title=k;f.srcdoc=VIEWS[k];f.addEventListener('load',()=>{{f.dataset.ready=1;nSend(k)}});document.body.appendChild(f);frames[k]=f;return f}}
function show(k,hash,push){{if(!VIEWS[k])k='app';const f=frame(k);
 for(const [n,el] of Object.entries(frames))el.classList.toggle('on',n===k);
 document.querySelectorAll('.switch button').forEach(b=>b.setAttribute('aria-selected',b.dataset.v===k));
 const send=()=>{{f.contentWindow.postMessage({{tt:'theme',theme}},'*');f.contentWindow.postMessage({{tt:'hash',hash,top:k!==cur}},'*')}};
 if(f.dataset.ready)send();else f.addEventListener('load',()=>{{f.dataset.ready=1;send()}},{{once:true}});
 cur=k;const h='#'+k;if(push&&location.hash!==h)history.pushState(null,'',h);f.focus()}}
document.querySelectorAll('.switch button').forEach(b=>b.onclick=()=>show(b.dataset.v,'',true));
addEventListener('message',e=>{{const d=e.data||{{}};
 if(d.tt==='go')show(d.view,d.hash,true);
 if(d.tt==='theme'){{theme=d.theme||'';if(theme)document.documentElement.dataset.theme=theme;else delete document.documentElement.dataset.theme;
  for(const f of Object.values(frames))if(f.contentWindow&&f.contentWindow!==e.source)f.contentWindow.postMessage({{tt:'theme',theme}},'*')}}}});
{NOTES_SHELL_JS}
addEventListener('popstate',()=>show(location.hash.slice(1)||'app','',false));
show(location.hash.slice(1)||'app','',false);
</script>
</body>
</html>
""")
    print(f"single {OUT.name}  {OUT.stat().st_size/1e6:.2f} MB  ({', '.join(k for k, _, _ in VIEWS)})")


if __name__ == "__main__":
    main()
