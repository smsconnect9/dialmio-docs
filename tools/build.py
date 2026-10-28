#!/usr/bin/env python3
"""Builds the Dialmio Help Center as static HTML with clean folder URLs.

Edit the PAGES content below, then run:  python3 tools/build.py
Each page is written to <slug>/index.html (home page to index.html).
"""
import html, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
SITE = "Dialmio Help Center"
SUPPORT_PHONE = "+91 99209 37711"
SUPPORT_WA = "919920937711"
SUPPORT_EMAIL = "support@dialmio.com"
PLAY_URL = "https://play.google.com/store/search?q=dialmio&c=apps"


def shot(img, cap):
    return f'<figure class="shot"><img src="{{R}}assets/img/{img}.jpg" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>'


def shots(*items):
    return '<div class="shots">' + "".join(shot(i, c) for i, c in items) + "</div>"


def ui(t):
    return f'<span class="ui">{t}</span>'


# ---------------------------------------------------------------- pages
# Each page: slug, title, nav label, group, icon, summary, body (HTML; h2 get ids automatically)
PAGES = []


# Videos shown at the end of a page: slug -> file name in assets/video (mp4 + jpg poster)
VIDEOS = {"getting-started": "getting-started", "call-analytics": "call-analytics"}


def video_block(name, R):
    return (f'<h2>Video guide</h2><div class="video"><video controls preload="none" playsinline '
            f'poster="{R}assets/video/{name}.jpg"><source src="{R}assets/video/{name}.mp4?v=3" type="video/mp4"></video></div>')


def page(slug, title, group, icon, summary, body, nav=None):
    PAGES.append(dict(slug=slug, title=title, nav=nav or title, group=group, icon=icon, summary=summary, body=body))


page("getting-started", "Getting started with Dialmio", "Start here", "🚀",
     "Install the app, make Dialmio your phone app, sign in and turn on backup in five minutes.", f"""
<p>Dialmio is a business dialer and call-management CRM for Android. It replaces your normal phone app, so every call you make or receive is logged with the customer's details, status and next follow-up — without changing how you call.</p>

<h2>Install the app</h2>
<ol class="steps">
<li>Open <b>Google Play Store</b> on your Android phone and search <b>Dialmio</b>. Tap <b>Install</b>.</li>
<li>Open Dialmio. The dialer is <b>free forever</b> — no login or signup is needed to start calling.</li>
</ol>
<div class="note"><b>Android only</b>Dialmio is available for Android phones. There is no iPhone app at the moment.</div>

<h2>Make Dialmio your default phone app</h2>
<p>Google Play lets only your <i>default</i> phone app see your call history. That is why Dialmio asks for this — without it, calls cannot be logged automatically.</p>
<ol class="steps">
<li>On the welcome screen tap {ui("Make Default Dialer, It's Free")}.</li>
<li>In the pop-up <b>Set Dialmio as your default phone app?</b> select <b>Dialmio</b> and tap {ui("Set as default")}.</li>
</ol>
<div class="tip"><b>Your normal calls work exactly the same</b>Incoming calls, the keypad and your contacts keep working as before. Your calls and customer data stay private on the phone until you choose to sign in and back them up.</div>

<h2>Get to know the home screen</h2>
<h3>Top tabs</h3>
<table>
<tr><th>Tab</th><th>What it shows</th></tr>
<tr><td>Call Logs</td><td>Every call with name, SIM, duration, total calls and first-call date. Each entry has {ui("Edit")} {ui("Reminder")} {ui("Remark")} {ui("Status")} {ui("History")} buttons plus Call, WhatsApp and SMS shortcuts.</td></tr>
<tr><td>Assigned</td><td>Leads assigned to you by your admin or by round-robin.</td></tr>
<tr><td>WhatsApp</td><td>Chats from your connected WhatsApp Business API number.</td></tr>
<tr><td>Leads</td><td>All leads with their status and next follow-up.</td></tr>
<tr><td>Clients</td><td>Paid clients and their renewals.</td></tr>
<tr><td>Reminders</td><td>Follow-ups due today and upcoming.</td></tr>
</table>
<p>The <b>Today</b> strip shows incoming, outgoing, missed and rejected calls for the day. Use the filters at the bottom — {ui("All")} {ui("Analytics")} and one chip per SIM — to slice your calls.</p>
<h3>Bottom bar</h3>
<p>{ui("Home")} {ui("Keypad")} {ui("Auto Dial")} {ui("All Tools")} {ui("Bulk WA")} {ui("More")}</p>
<p><b>All Tools</b> opens Quick options (Contacts, Auto WhatsApp, Follow-up series (DRIP), Templates, Excluded numbers, Lost Lead, Notes) and Setup and account (Login account, Settings, Sync settings, Connect any CRM API, Team plans, App Language, Ask AI, Video guides, Support).</p>

<h2>Sign in</h2>
<p>Signing in is only needed when you want backup, sync across devices or team features.</p>
<ol class="steps">
<li>Open {ui("All Tools")} → {ui("Login account")}.</li>
<li>Choose <b>Phone</b> (or <b>Email</b>), enter your mobile number and tap {ui("Get OTP")}.</li>
<li>Enter the 6-digit code sent to your number and tap {ui("Verify &amp; continue")}. On most phones the code is filled in automatically.</li>
</ol>

<h2>Turn on backup &amp; sync</h2>
<p>After sign-in Dialmio walks you through a 3-step Backup &amp; sync setup. See <a href="{{R}}backup-sync/">Backup &amp; sync</a> for every option explained.</p>
""")

page("calling", "Calling & auto dialer", "Features", "📞",
     "Auto dial from Excel, after-call notes, call recording, follow-up alarms and missed-call callbacks.", f"""
<h2>Auto dial from Excel</h2>
<p>Upload a list and let Dialmio dial it for you — up to 100 numbers with one tap. No more dialling by hand.</p>
<ol class="steps">
<li>Tap {ui("Auto Dial")} in the bottom bar.</li>
<li>Import your numbers from an Excel/CSV file, or pick leads already in Dialmio.</li>
<li>Start the session. After each call, fill the after-call sheet and Dialmio moves to the next number.</li>
</ol>
<div class="tip"><b>Tip</b>Keep a column for the customer name in your Excel file so the caller sees who they are calling.</div>

<h2>After-call sheet</h2>
<p>When a call ends, a two-tap sheet lets you save the outcome right away: set the <b>Status</b>, add a <b>Remark</b> and schedule a <b>Reminder</b>. You can do the same later from any call-log entry using the {ui("Status")} {ui("Remark")} {ui("Reminder")} buttons, and see the full timeline with {ui("History")}.</p>

<h2>Full customer detail on every call</h2>
<p>When a known number calls, Dialmio shows the name, status, last note and next follow-up on screen — caller ID comes from your own records.</p>

<h2>Call recording</h2>
<p>Dialmio can attach call recordings to the lead on supported Android phones. Recording availability depends on the phone model and Android version.</p>

<h2>Follow-up alarms</h2>
<p>Every reminder you set rings as an alarm at the right time, and all due follow-ups are listed in the <b>Reminders</b> tab.</p>

<h2>Missed-call callback queue</h2>
<p>Missed calls are collected in a callback queue so no enquiry is forgotten.</p>

<h2>Works with mobile data off</h2>
<p>Calling and logging work offline. Data syncs to your account the next time you are online (if backup is on).</p>

<h2>Analytics</h2>
<p>See call counts, talk time and charts for any date range. Full guide: <a href="{{R}}call-analytics/">Call analytics</a>.</p>

<h2>App language</h2>
<p>Dialmio supports 40 languages. Change it from {ui("All Tools")} → {ui("App Language")}.</p>
""")

page("call-analytics", "Call analytics", "Features", "📊",
     "See total calls, talk time, connected rate and monthly charts — then export or share the report.", f"""
<h2>Open Analytics</h2>
<ol class="steps">
<li>Open Dialmio and stay on the {ui("Home")} screen.</li>
<li>At the bottom of the call list, tap {ui("Analytics")} (next to {ui("All")} and your SIM chips).</li>
</ol>
<p>The top of the screen shows the <b>total calls</b> and <b>total talk time</b> for the period you choose.</p>

<h2>Choose a date range and SIM</h2>
<ol class="steps">
<li>Tap {ui("Today")}, {ui("Last 7 days")}, {ui("This month")} or {ui("All time")}.</li>
<li>For your own dates tap {ui("Custom")}, pick the start date and end date on the calendar and tap {ui("Apply")}.</li>
<li>Tap a SIM chip (for example {ui("airtel")} or {ui("Vi India")}) to see only that SIM's calls.</li>
</ol>

<h2>Summary tab</h2>
<p>{ui("Summary")} shows each number as a ring so you can read it at a glance:</p>
<table>
<tr><th>Ring</th><th>Meaning</th></tr>
<tr><td>Incoming / Outgoing</td><td>Calls received and made, with talk time under each</td></tr>
<tr><td>Missed</td><td>Incoming calls you did not answer</td></tr>
<tr><td>Connected</td><td>Calls that were answered, with total talk time</td></tr>
<tr><td>Unique</td><td>Different phone numbers you spoke with</td></tr>
<tr><td>Rejected</td><td>Calls you declined</td></tr>
<tr><td>Lost Lead</td><td>Calls with numbers marked as lost leads</td></tr>
<tr><td>Blocked / Spam</td><td>Calls from blocked or spam numbers</td></tr>
</table>

<h2>Analysis tab</h2>
<p>Tap {ui("Analysis")} to see the same figures as a list: total calls, incoming and outgoing (count and time), missed, rejected, connected with <b>connect rate %</b>, unique numbers, lost leads, blocked, spam, total talk time and WhatsApp.</p>

<h2>Monthly charts</h2>
<p>Scroll down to see two charts:</p>
<ul>
<li><b>Call count (per month)</b> — incoming, outgoing, missed and rejected calls each month.</li>
<li><b>Call duration (hours)</b> — incoming and outgoing talk time each month.</li>
</ul>

<h2>Export and share the report</h2>
<ol class="steps">
<li>Scroll to the bottom to <b>Export calls</b>. It exports the calls for the range you selected.</li>
<li>Tap {ui("Excel")} or {ui("PDF")} to save the file or share it.</li>
<li>Tap {ui("Share today's report")} to send today's call summary — for example to your manager on WhatsApp.</li>
</ol>
<div class="tip"><b>Tip</b>Use {ui("Custom")} with one SIM selected to check a single team member's or a single number's performance for any period.</div>
""")

page("leads", "Leads & automation", "Features", "🎯",
     "Get leads from IndiaMART, Facebook, Google Sheets and more, distribute them round-robin and track every stage.", f"""
<h2>Lead sources</h2>
<p>Leads can come into Dialmio automatically from:</p>
<ul>
<li><b>IndiaMART</b> enquiries</li>
<li><b>Facebook / Instagram Lead Ads</b></li>
<li><b>Google Sheets</b></li>
<li><b>Website forms</b></li>
<li><b>Excel / CSV</b> import</li>
<li><b>API</b> — from any software (see <a href="{{R}}developer-api/">Developer API</a>)</li>
</ul>
<p>Any caller who is not yet a lead can be added with the {ui("Add")} button on the call-log entry.</p>
<div class="note"><b>Need help connecting a source?</b>Our team will set up IndiaMART, Facebook Lead Ads or Google Sheets for you. <a href="{{R}}contact/">Contact support</a>.</div>

<h2>Round-robin distribution</h2>
<p>New leads can be shared automatically among your team one by one, so every caller gets a fair share. Assigned leads show in each caller's <b>Assigned</b> tab.</p>

<h2>Lead statuses &amp; fields</h2>
<p>Use lead statuses (for example New, Interested, Follow-up, Won, Lost) to track each stage, and custom lead fields to store anything your business needs. Leads you close without a sale can be moved to <b>Lost Lead</b>.</p>

<h2>Paid clients &amp; renewals</h2>
<p>When a lead buys, mark them as a paid client. The <b>Clients</b> tab keeps your paying customers, their products/packages and renewal dates.</p>

<h2>Excluded numbers</h2>
<p>Add personal numbers (family, friends) to {ui("All Tools")} → {ui("Excluded numbers")}. Their calls are never uploaded and never become leads.</p>
""")

page("whatsapp", "WhatsApp", "Features", "💬",
     "Auto WhatsApp after every call, bulk campaigns and a shared inbox using your WhatsApp Business API.", f"""
<h2>Connect your WhatsApp Business API</h2>
<p>Dialmio works with any WhatsApp Business API provider. We recommend <a href="https://wappconnect.com" target="_blank" rel="noopener">WappConnect</a>, which connects in a few minutes and supports chatbot automation.</p>
<div class="note"><b>Meta charges</b>WhatsApp conversation charges are set by Meta and billed by your API provider, not by Dialmio.</div>

<h2>Auto WhatsApp after the call</h2>
<p>Send an automatic follow-up message the moment a call ends, so no lead goes cold. Set it up from {ui("All Tools")} → {ui("Auto WhatsApp")} and pick an approved template from {ui("Templates")}.</p>

<h2>Bulk WhatsApp campaigns</h2>
<p>Tap {ui("Bulk WA")} to send a campaign to your leads, to contacts from your call logs, or to numbers you copy-paste. There are two send modes:</p>
<table>
<tr><th>Mode</th><th>How it sends</th><th>Use it for</th></tr>
<tr><td><b>Server campaign</b> (recommended)</td><td>Through the Meta WhatsApp Business API</td><td>Bulk messages — verified and safe for large lists</td></tr>
<tr><td><b>One by one</b></td><td>Opens your phone's own WhatsApp app for each number</td><td>Chatting with a single lead after the 24-hour API window has closed</td></tr>
</table>
<div class="warn"><b>Do not use “One by one” for bulk</b>Sending many messages from a normal WhatsApp number can get the number blocked by WhatsApp. Always use Server campaign for bulk.</div>

<h2>Shared WhatsApp inbox</h2>
<p>Replies that come to your API number appear in the <b>WhatsApp</b> tab. Any chat can be converted into a lead with one tap.</p>

<h2>Follow-up series (DRIP)</h2>
<p>Create a sequence of messages that go out automatically over several days. Open {ui("All Tools")} → {ui("Follow-up series (DRIP)")}.</p>

<h2>Automation with WappConnect</h2>
<p>When Dialmio is connected to WappConnect, a change in lead stage can trigger a WappConnect chatbot or automation flow — for example, sending a brochure when a lead moves to <i>Interested</i>.</p>
""")

page("backup-sync", "Backup & sync", "Features", "☁️",
     "Keep your call history and CRM data safe in your account and on every device.", f"""
<p>Backup keeps your call history and CRM data safe in your account. Get it back on a new phone or share it with your team. Data is sent encrypted and used only for backup and sync. <b>Nothing goes up until you sign in and tap I Agree.</b></p>

<h2>Step 1 — Agree</h2>
<p>Read what is backed up and tap {ui("I Agree")}. Tap {ui("Not now")} to keep everything on the phone only.</p>

<h2>Step 2 — Choose what to back up</h2>
<table>
<tr><th>Option</th><th>What it does</th></tr>
<tr><td>Attendance app</td><td>Syncs only attendance, location and leads. Calls and everything else stay on the phone.</td></tr>
<tr><td>Which SIM's calls to back up</td><td>Turn each SIM on or off. Both SIMs are on at first. Calls on a SIM turned off are never uploaded.</td></tr>
<tr><td>Only calls in working hours</td><td>Calls before or after your branch's working hours, or on its day off, stay on the phone. Needs a branch with working hours — ask your admin to set them.</td></tr>
<tr><td>Only calls with leads</td><td>Calls with numbers that are not leads stay on the phone. When a number becomes a lead, its older calls sync too.</td></tr>
</table>

<h2>Step 3 — Exclude numbers (optional)</h2>
<p>Numbers on this list are never uploaded. Their calls and CRM data stay only on this phone. Tap {ui("Add numbers to exclude")}, then {ui("Skip &amp; Finish")}.</p>

<h2>Check sync status</h2>
<p>Open {ui("All Tools")} → {ui("Sync settings")} (or {ui("Settings")} → {ui("Backup &amp; sync")}). The <b>Cloud sync</b> section shows progress for call logs, leads, follow-ups, message templates, paid clients, products, packages, attachments, lead fields and lead statuses.</p>
<ul>
<li><b>Pending</b> — waiting to upload. It clears automatically when you are online.</li>
<li><b>Empty</b> — nothing to sync in that section yet.</li>
<li><b>Synced</b> — everything is up to date.</li>
</ul>
<p>Use <b>Force full resync</b> if data looks out of date, and <b>Sync log</b> to see what happened.</p>
<div class="tip"><b>Change it anytime</b>All these choices can be changed later from {ui("Settings")} → {ui("Backup &amp; sync")}.</div>
""")

page("team", "Team & owner tools", "For owners", "👥",
     "Live dashboard, daily call report, selfie attendance, permissions and team plans.", f"""
<h2>Add your team</h2>
<p>Using Dialmio with a team? Assign leads, give each caller their own list and see everyone's calls. Open {ui("All Tools")} → {ui("Team plans")} to choose a plan and add users.</p>

<h2>Live dashboard</h2>
<p>See every caller's calls, talk time and lead progress in one place, live.</p>

<h2>Automatic daily call report</h2>
<p>Get a summary of the day's calls for each team member without asking anyone for it.</p>

<h2>Selfie attendance</h2>
<p>Team members mark attendance with a selfie and location. Use the <b>Attendance app</b> backup option if a phone should sync only attendance, location and leads.</p>

<h2>Permissions</h2>
<p>Control what each user can see and do — for example, whether callers can see other callers' leads.</p>

<h2>Branches &amp; working hours</h2>
<p>Set working hours for each branch. Phones that use <i>Only calls in working hours</i> will then skip personal calls made outside office time.</p>

<h2>Unified search</h2>
<p>Search a name or number once to find their calls, lead record, notes and WhatsApp chats together.</p>
""", nav="Team & owners")

page("developer-api", "Developer API", "For owners", "🔌",
     "Connect Dialmio with your own CRM or software in both directions.", f"""
<h2>Connect any CRM API</h2>
<p>Push leads into Dialmio from your website, CRM or any other software, and pull call and lead data out. Open {ui("All Tools")} → {ui("Connect any CRM API")} to get started.</p>

<h2>Outbound lead-status API</h2>
<p>Dialmio can notify your system whenever a lead's status changes. Your own CRM or WhatsApp platform can use this to run its own automation — for example, send a quotation when a lead becomes <i>Interested</i>.</p>

<div class="note"><b>API keys &amp; full reference</b>Write to <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a> with your use case and we will share API access and the endpoint reference.</div>
""")

page("pricing", "Plans & pricing", "Account", "💳",
     "The dialer is free forever. CRM plans start at ₹159 per user per month.", f"""
<table>
<tr><th>Plan</th><th>Price</th><th>Billing</th></tr>
<tr><td><b>Dialer</b></td><td>Free forever</td><td>No login needed</td></tr>
<tr><td><b>CRM — Monthly</b></td><td>₹249 / user / month + GST</td><td>Minimum 3 months (₹747 + GST per user)</td></tr>
<tr><td><b>CRM — Yearly</b></td><td>₹159 / user / month + GST</td><td>₹1,908 + GST per user, billed yearly</td></tr>
</table>
<p>All prices are exclusive of GST. WhatsApp conversation charges are billed separately by Meta through your API provider.</p>
<p>To buy or upgrade, open {ui("All Tools")} → {ui("Team plans")}, or <a href="{{R}}contact/">talk to us</a>.</p>
""")

page("faq", "Frequently asked questions", "Account", "❓",
     "Quick answers to the most common questions.", f"""
<details><summary>Is the dialer really free?</summary><p>Yes. The Dialmio dialer is free forever with no login. You pay only if you want the CRM and team features.</p></details>
<details><summary>Why does Dialmio need to be my default phone app?</summary><p>Google Play allows only the default phone app to read call history. Without it, Dialmio cannot log your calls automatically. Your calls work exactly the same.</p></details>
<details><summary>Is there an iPhone app?</summary><p>Not at the moment. Dialmio is available for Android.</p></details>
<details><summary>Will my personal calls be uploaded?</summary><p>No, not if you don't want them to be. Nothing is uploaded until you sign in and agree. You can turn off a SIM, back up only calls with leads, only calls in working hours, or exclude specific numbers. See <a href="{{R}}backup-sync/">Backup &amp; sync</a>.</p></details>
<details><summary>Does call recording work on my phone?</summary><p>Call recording works on supported Android phones. It depends on your phone model and Android version.</p></details>
<details><summary>Does it work without internet?</summary><p>Yes. Calling and logging work with mobile data off. Data syncs when you are back online.</p></details>
<details><summary>Can I use my own WhatsApp API provider?</summary><p>Yes. Any WhatsApp Business API can be connected. We recommend WappConnect.</p></details>
<details><summary>Can I send bulk WhatsApp from my normal WhatsApp?</summary><p>Not recommended — it can get your number blocked. Use Server campaign through the WhatsApp Business API for bulk.</p></details>
<details><summary>How do I move to a new phone?</summary><p>Install Dialmio on the new phone, sign in with the same number and your backed-up data syncs down.</p></details>
<details><summary>How do I get IndiaMART or Facebook leads into Dialmio?</summary><p>Our team will connect them for you. <a href="{{R}}contact/">Contact support</a>.</p></details>
""", nav="FAQs")

page("contact", "Contact support", "Account", "🛟",
     "Talk to the Dialmio team on WhatsApp, phone or email.", f"""
<table>
<tr><th>Channel</th><th>Details</th></tr>
<tr><td>WhatsApp</td><td><a href="https://wa.me/{SUPPORT_WA}" target="_blank" rel="noopener">{SUPPORT_PHONE}</a></td></tr>
<tr><td>Phone</td><td><a href="tel:+{SUPPORT_WA}">{SUPPORT_PHONE}</a></td></tr>
<tr><td>Email</td><td><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></td></tr>
<tr><td>Hours</td><td>Monday – Saturday, 10 am – 7 pm IST</td></tr>
<tr><td>Website</td><td><a href="https://dialmio.com" target="_blank" rel="noopener">dialmio.com</a></td></tr>
</table>
<p>Inside the app you can also open {ui("All Tools")} → {ui("Support")}, {ui("Video guides")} or {ui("Ask AI")}.</p>
<p>Want a live walkthrough? Message us on WhatsApp for a free online demo.</p>
""", nav="Contact support")

GROUPS = ["Start here", "Features", "For owners", "Account"]

# ---------------------------------------------------------------- rendering
SEARCH_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def slugify(t):
    t = re.sub(r"<[^>]+>", "", html.unescape(t)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def plain(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(t))).strip()


def section_text(body):
    parts = re.split(r"<h2[^>]*>.*?</h2>", body)
    return [plain(x)[:400] for x in parts[1:]]


def add_ids(body):
    heads = []
    def rep(m):
        text = m.group(1)
        i = slugify(text)
        heads.append((i, re.sub(r"<[^>]+>", "", html.unescape(text))))
        return f'<h2 id="{i}">{text}</h2>'
    return re.sub(r"<h2>(.*?)</h2>", rep, body), heads


def topbar(R):
    return f'''<header class="topbar">
<button class="menu-btn" aria-label="Menu">☰</button>
<a class="brand" href="{R}"><img src="{R}assets/img/logo.png" alt="Dialmio"><span>Dial<b>mio</b></span><small>Help</small></a>
<div class="top-search" data-search>{SEARCH_SVG}<input type="search" placeholder="Search help articles…" aria-label="Search"><div class="results"></div></div>
<nav class="top-links"><a href="https://dialmio.com" target="_blank" rel="noopener">dialmio.com</a><a class="btn" href="{PLAY_URL}" target="_blank" rel="noopener">Get the app</a></nav>
</header>'''


def head(title, desc, R):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{R}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/style.css?v=2">
</head><body>'''


def foot(R):
    return f'''<footer>© Dialmio · Call Management CRM · <a href="{R}contact/">Contact support</a></footer>
<script src="{R}assets/search-index.js"></script><script src="{R}assets/app.js?v=2"></script></body></html>'''


def sidebar(cur, R, heads):
    out = ['<aside class="sidebar">']
    for g in GROUPS:
        out.append(f"<h4>{g}</h4>")
        for p in PAGES:
            if p["group"] != g:
                continue
            c = ' class="current"' if p["slug"] == cur else ""
            out.append(f'<a href="{R}{p["slug"]}/"{c}>{p["nav"]}</a>')
            if p["slug"] == cur and heads:
                out.append('<div class="sub">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in heads) + "</div>")
    out.append("</aside>")
    return "".join(out)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    index = []
    order = [p for g in GROUPS for p in PAGES if p["group"] == g]
    for n, p in enumerate(order):
        R = "../"
        raw = p["body"].replace("{R}", R)
        if p["slug"] in VIDEOS:
            raw += video_block(VIDEOS[p["slug"]], R)
        body, heads = add_ids(raw)
        index.append(dict(u=p["slug"] + "/", t=p["title"], p=p["summary"], k=""))
        texts = section_text(body)
        for (i, t), txt in zip(heads, texts):
            index.append(dict(u=f'{p["slug"]}/#{i}', t=t, p=p["title"], k=txt))
        prev = order[n - 1] if n else None
        nxt = order[n + 1] if n + 1 < len(order) else None
        pager = '<div class="pager">'
        pager += f'<a href="{R}{prev["slug"]}/"><small>← Previous</small>{prev["title"]}</a>' if prev else "<span></span>"
        pager += f'<a class="next" href="{R}{nxt["slug"]}/"><small>Next →</small>{nxt["title"]}</a>' if nxt else "<span></span>"
        pager += "</div>"
        toc = ('<nav class="toc"><b>On this page</b>' + "".join(f'<a href="#{i}">{t}</a>' for i, t in heads) + "</nav>") if heads else ""
        helpbox = f'<div class="help-box"><div><b>Still need help?</b><p>Our team replies Mon–Sat, 10 am – 7 pm IST.</p></div><a class="btn" href="https://wa.me/{SUPPORT_WA}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>'
        html_out = (head(f'{p["title"]} · {SITE}', p["summary"], R) + topbar(R) + '<div class="layout">' + sidebar(p["slug"], R, heads)
                    + f'<main><div class="crumb"><a href="{R}">Help Center</a> › {p["group"]}</div><h1>{p["title"]}</h1><p class="lead">{p["summary"]}</p>'
                    + body + pager + helpbox + "</main>" + toc + "</div>" + foot(R))
        write(f'{p["slug"]}/index.html', html_out)

    # Home
    R = ""
    cards = "".join(f'<a class="card" href="{p["slug"]}/"><div class="ico">{p["icon"]}</div><h3>{p["title"]}</h3><p>{p["summary"]}</p></a>' for p in order)
    popular = [("getting-started/#make-dialmio-your-default-phone-app", "Make Dialmio your default phone app"),
               ("calling/#auto-dial-from-excel", "Auto dial a list from Excel"),
               ("whatsapp/#bulk-whatsapp-campaigns", "Send a bulk WhatsApp campaign"),
               ("backup-sync/#step-2-choose-what-to-back-up", "Back up only business calls"),
               ("leads/#lead-sources", "Get IndiaMART & Facebook leads"),
               ("whatsapp/#auto-whatsapp-after-the-call", "Auto WhatsApp after every call"),
               ("getting-started/#sign-in", "Sign in with your phone number"),
               ("pricing/", "Plans & pricing")]
    pop = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in popular)
    home = (head(SITE, "Guides and answers for Dialmio — the free business dialer and call-management CRM for Android.", R) + topbar(R)
            + f'''<section class="hero"><h1>How can we <b>help</b>?</h1><p>Guides and answers for the Dialmio dialer and CRM.</p>
<div class="big-search" data-search>{SEARCH_SVG.replace('width="16" height="16"', 'width="20" height="20"')}<input type="search" placeholder="Search e.g. auto dialer, backup, bulk WhatsApp…" aria-label="Search"><div class="results"></div></div></section>
<div class="home"><div class="cards">{cards}</div><h2>Popular articles</h2><ul class="popular">{pop}</ul>
<div class="help-box"><div><b>Can't find what you need?</b><p>Chat with the Dialmio team on WhatsApp — Mon–Sat, 10 am – 7 pm IST.</p></div><a class="btn" href="https://wa.me/{SUPPORT_WA}" target="_blank" rel="noopener">Chat on WhatsApp</a></div></div>'''
            + foot(R))
    write("index.html", home)

    # Search index (URLs relative to site root; prefix added at runtime)
    write("assets/search-index.js", "(function(){var b=document.currentScript.src.replace(/assets\\/search-index\\.js.*$/,'');window.DIALMIO_INDEX="
          + json.dumps(index, ensure_ascii=False) + ".map(function(x){x.u=b+x.u;return x})})();\n")
    write("404.html", head("Page not found · " + SITE, "Page not found", "/dialmio-docs/") + topbar("/dialmio-docs/")
          + '<div class="home" style="text-align:center"><h1>Page not found</h1><p>Try the search above or go to the <a href="/dialmio-docs/">Help Center home</a>.</p></div>' + foot("/dialmio-docs/"))
    print("built", len(order) + 1, "pages")


if __name__ == "__main__":
    main()
