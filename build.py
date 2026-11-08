#!/usr/bin/env python3
"""Builds index.html for pittner/bucket-list-vision-board.

A single-purpose page for the "bucket list vision board" / "bucket list ideas 2027" search intent
(lists are made in December and January): 36 ideas in 6 groups (adventure and travel, learn and create,
body and challenge, people and memories, give back and grow, everyday joy), each with why it matters
and a first step; one click opens the free maker prefilled as a phone lock screen. Plus 12 questions,
a 45-minute plan, a box for your own item, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/bucket-list-vision-board/"
SRC = "ghpages_bucket"
CAMPAIGN = "bucket_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Adventure and travel", [
        ("See the northern lights", "A trip with one clear aim is easier to plan and to pay for than a vague wish to travel.", "Pick the month and the place, then set a price alert for flights"),
        ("Take a road trip with no fixed plan", "Unplanned days are where the stories you retell for years come from.", "Choose a start city, a rough direction and three free days in the calendar"),
        ("Visit a country on every continent I can reach", "A long list becomes doable when you take one country at a time.", "Write the next three countries in order and the cheapest month for the first"),
        ("Sleep under the stars", "One night outside resets how small your daily worries feel.", "Look up one dark-sky spot or campsite within two hours of home"),
        ("Go on a trip alone", "A solo trip shows you what you enjoy when nobody else is deciding.", "Book a two-night stay somewhere you have never been"),
        ("Live in another country for a month", "A month abroad feels like a different life, not a holiday.", "Write which city, which month and how you would work or pay for it"),
    ]),
    ("Learn and create", [
        ("Learn to speak a new language", "Speaking with one real person beats years of apps you never open.", "Book one trial lesson or find one conversation partner this week"),
        ("Write a book", "A book is written in small daily pages, not in one burst of inspiration.", "Write 200 words today, about anything, and put the date on the page"),
        ("Learn to play an instrument", "Ten minutes a day gets you further than one long session a month.", "Borrow or rent an instrument and play for 10 minutes"),
        ("Take a course I have always wanted", "A paid, dated course gets finished more often than a free one you bookmark.", "Pick one course and put the first lesson in your calendar"),
        ("Make something with my hands", "Making things is the opposite of scrolling and it lifts your mood.", "Choose one small project and buy or find the first material"),
        ("Share my work with strangers", "Work that nobody sees cannot get feedback, and feedback is how you improve.", "Pick one piece you already made and post or send it to one person"),
    ]),
    ("Body and challenge", [
        ("Run a marathon", "A race date gives every training day a reason.", "Find a race about 20 weeks away and walk-run for 30 minutes today"),
        ("Hike a famous trail", "A long trail is just many short days in a row.", "Choose the trail, the season and the number of days it would need"),
        ("Do a full pull-up", "One clear strength goal beats a vague wish to get fitter.", "Hang from a bar for as long as you can and write the number"),
        ("Try a sport I have never done", "A first lesson costs little and shows you what you might love.", "Book one beginner session of climbing, surfing, dancing or boxing"),
        ("Swim in the sea in every season", "Small hard things teach you that discomfort passes.", "Plan a short cold swim and invite one friend"),
        ("Complete a 30-day challenge", "Finishing one small streak proves to you that you keep your word.", "Choose one tiny daily action and mark day 1 on a calendar"),
    ]),
    ("People and memories", [
        ("Throw a party for the people I love", "Most people remember being invited more than the party itself.", "Pick a date, write the guest list and send the first invitation"),
        ("Reconnect with an old friend", "Old friends are glad to hear from you more often than you fear.", "Send a short message to one person you have not talked to in years"),
        ("Take a trip with my parents or grandparents", "These trips cannot wait for a better time.", "Ask them where they have always wanted to go"),
        ("Record my family's stories", "A story that is not written down is lost with the person who knows it.", "Ask one relative a question and record the answer on your phone"),
        ("Make a photo book of my best year", "Photos in a phone are rarely looked at; a book gets picked up.", "Choose 20 photos from this year in one folder"),
        ("Celebrate a big birthday in a way I will remember", "Marking a milestone on purpose makes the years feel full.", "Decide the place and the people, then set a date to book it"),
    ]),
    ("Give back and grow", [
        ("Volunteer for a cause I care about", "Helping others is one of the most reliable ways to feel better yourself.", "Find one local group and send them a short message today"),
        ("Mentor someone", "Teaching what you know shows you how much you have learned.", "Think of one person who could use your help and offer a call"),
        ("Plant a tree or start a garden", "A living thing you tend gives you a reason to slow down.", "Pick a spot and a plant, even if it is one pot on a windowsill"),
        ("Donate regularly to a cause", "A small monthly amount does more than a large gift you never get around to.", "Choose one cause and set up a monthly donation you can afford"),
        ("Give a talk about something I know", "Speaking in public is a skill that opens doors in every field.", "Write the topic in one sentence and the first group you could tell"),
        ("Write letters to the people who shaped me", "People rarely hear how much they mattered, and you will feel better too.", "Write the first letter, even if it is only five lines"),
    ]),
    ("Everyday joy", [
        ("Watch a sunrise from a hilltop", "A small early effort gives you a day that starts well.", "Look up tomorrow's sunrise time and the nearest high point"),
        ("Eat at a restaurant I have always wanted to try", "A planned treat is something to look forward to for weeks.", "Book a table for a date within the next month"),
        ("See my favourite band live", "Live music gives you a memory no recording can.", "Check tour dates and set an alert for tickets"),
        ("Read 30 books", "A book a week or two is only a few pages every day.", "Choose the next three books and read 10 pages tonight"),
        ("Spend a full day offline", "A day without a phone shows you how much of the day you were giving away.", "Pick a Sunday, tell the people who need to know and switch off at sunrise"),
        ("Do something spontaneous every month", "Surprise keeps life from feeling like the same week on repeat.", "Write 12 small ideas, one per month, and do the first this week"),
    ]),
]

QUESTIONS = [
    "What have I always said I would do 'one day'?",
    "What would I regret not doing if I could not do it after next year?",
    "Which experience have I already done that I would happily repeat?",
    "What do I want to be able to tell my grandchildren I did?",
    "Which item on my list is really someone else's dream?",
    "Where do I want to wake up on my next birthday?",
    "Who do I want to share my best experiences with?",
    "What scares me a little, in a good way?",
    "What would I do with a free week and a small budget?",
    "What is the cheapest thing on my list that I could do this month?",
    "Which skill would make my life richer if I learned it?",
    "If I could cross off just three things in 2027, which would they be?",
]

PLAN = [
    ("10 minutes: write 30 things.", "Empty your head without judging. Big trips, small treats, skills, people to see."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three for 2027.", "Not thirty. Choose three, one big, one cheap and one with another person, and give each a month."),
    ("10 minutes: make it visible.", "Turn your first item and its first step into a phone lock screen, so you see it every day and act on it, not only add it to a list."),
]

FAQ = [
    ("What should I put on a bucket list?",
     "Put things you would regret not doing: places, skills, people and small joys. Mix big and cheap items so you can tick something off every month. "
     "This page has 36 ideas in 6 groups (adventure and travel, learn and create, body and challenge, people and memories, give back and grow, everyday joy), each with a first step for this week."),
    ("How do I turn a bucket list into a vision board?",
     "Pick three items, write each as a short sentence with a month, add one first step, and put it where you see it every day. "
     "A phone lock screen works best because you see it dozens of times a day."),
    ("How many items should a bucket list have?",
     "A list of 30 to 100 is fine to dream with, but pick only three for the year. Fewer items get done more often."),
    ("Why do most bucket lists never get done?",
     "Items without a date or a first step stay wishes. Give every item a month and a step you can do this week, and keep the list visible."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full bucket list vision board with all my items?",
     "Yes. Start from your items in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bucket List Vision Board 2027: %%COUNT%% Bucket List Ideas with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% bucket list ideas for 2027 (adventure and travel, learn and create, body and challenge, people and memories, give back, everyday joy), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Bucket list vision board 2027 - %%COUNT%% bucket list ideas with a first step and a free lock screen">
<meta property="og:description" content="Travel, learning, challenge, people and everyday joy ideas with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Bucket list vision board 2027: %%COUNT%% bucket list ideas, each with a first step for this week</h1>
  <p class="lede">A bucket list that lives in a notes app rarely happens, because nothing on it has a month or a first step. Below are %%COUNT%% bucket list ideas for 2027, from the northern lights and a first marathon to a day offline and letters to people who shaped you, each with why it matters and a first step you can do this week, plus %%NQ%% questions to find out what you really want to do. Press an idea and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every day until you cross it off.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My bucket list item for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. See the northern lights in March" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Set a flight price alert today" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose your bucket list</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Make your bucket list board in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full bucket list vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/manifestation-vision-board/">manifestation vision board</a>,
  <a href="https://pittner.github.io/dream-home-vision-board/">dream home vision board</a>,
  <a href="https://pittner.github.io/fitness-vision-board/">fitness vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-relationships/">relationships vision board</a>,
  <a href="https://pittner.github.io/travel-vision-board/">travel vision board</a>,
  <a href="https://pittner.github.io/self-care-vision-board/">self care vision board</a>,
  <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/bucket-list-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
