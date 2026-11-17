with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Remove the "Daily Picture Vote" button from the top left of The Rec Area
old_vote_btn = """<button class="rec-tab-btn active" id="recTabVoteBtn" onclick="switchRecTab('vote')">🗳️ Daily Picture Vote</button>"""
if old_vote_btn in html:
    html = html.replace(old_vote_btn, "")
    print("REMOVED_DAILY_PIC_VOTE_BUTTON")
else:
    print("WARNING: Could not find recTabVoteBtn.")

# 2. Make "Funny Pics" the active default tab when opening The Rec Area
html = html.replace(
    """<button class="rec-tab-btn" id="recTabPicsBtn" onclick="switchRecTab('pics')">😂 Funny Pics</button>""",
    """<button class="rec-tab-btn active" id="recTabPicsBtn" onclick="switchRecTab('pics')">😂 Funny Pics</button>"""
)

# 3. Default openHubSection('recTimeSection', 'vote') to open 'pics' instead
html = html.replace("openHubSection('recTimeSection', 'vote')", "openHubSection('recTimeSection', 'pics')")

# 4. Update Community Hub subtitle for The Rec Area so it matches the remaining 3 tabs
html = html.replace(
    "Daily picture vote, funny pics, funny videos (30s or less) &amp; random trivia.",
    "Funny pics, funny videos (30s or less) &amp; random trivia."
)

# 5. Clean up switchRecTab() so it handles 'pics', 'videos', and 'trivia' smoothly without crashing on missing recTabVoteBtn
old_switch_start = html.find("function switchRecTab(tab) {")
old_switch_end = html.find("function voteForDailyPic(btn)")

if old_switch_start != -1 and old_switch_end != -1:
    new_switch_fn = """function switchRecTab(tab) {
            ['recTabPicsBtn', 'recTabVideosBtn', 'recTabTriviaBtn'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active');
            });
            ['recVotePanel', 'recPicsPanel', 'recVideosPanel', 'recTriviaPanel'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            });
            if (triviaTimerInterval) clearInterval(triviaTimerInterval);

            if (tab === 'videos') {
                document.getElementById('recTabVideosBtn').classList.add('active');
                document.getElementById('recVideosPanel').style.display = 'block';
            } else if (tab === 'trivia') {
                document.getElementById('recTabTriviaBtn').classList.add('active');
                document.getElementById('recTriviaPanel').style.display = 'block';
                document.getElementById('triviaLobbyBox').style.display = 'block';
                document.getElementById('triviaPlayBox').style.display = 'none';
                document.getElementById('recTimerDisplay').innerText = '⏱️ 30s Left';
            } else {
                document.getElementById('recTabPicsBtn').classList.add('active');
                document.getElementById('recPicsPanel').style.display = 'block';
            }
        }

        """
    html = html[:old_switch_start] + new_switch_fn + html[old_switch_end:]

with open("templates/index.html", "w") as f:
    f.write(html)
print("REC_AREA_CLEANED_SUCCESS")
