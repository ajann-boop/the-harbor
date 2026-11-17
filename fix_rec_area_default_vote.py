with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Remove active highlight from Funny Pics tab by default so it only highlights when clicked
html = html.replace(
    """<button class="rec-tab-btn active" id="recTabPicsBtn" onclick="switchRecTab('pics')">😂 Funny Pics</button>""",
    """<button class="rec-tab-btn" id="recTabPicsBtn" onclick="switchRecTab('pics')">😂 Funny Pics</button>"""
)

# 2. Add a clean "← Back to Daily & Saturday Vote" button inside Funny Pics, Funny Videos, and Random Trivia panels so you can jump back to the voting cards anytime
html = html.replace(
    """<div style="font-size: 0.84rem; font-weight: 700; color: #5eead4; margin-bottom: 8px;">😂 Funny Pics Gallery — Quick Caregiver Laughs</div>""",
    """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
        <div style="font-size: 0.84rem; font-weight: 700; color: #5eead4;">😂 Funny Pics Gallery — Quick Caregiver Laughs</div>
        <button type="button" class="back-hub-btn" onclick="switchRecTab('vote')">← Back to Voting Cards</button>
    </div>"""
)

html = html.replace(
    """<div style="font-size: 0.84rem; font-weight: 700; color: #fde047; margin-bottom: 8px;">🎬 Funny Videos (30 seconds or less)</div>""",
    """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
        <div style="font-size: 0.84rem; font-weight: 700; color: #fde047;">🎬 Funny Videos (30 seconds or less)</div>
        <button type="button" class="back-hub-btn" onclick="switchRecTab('vote')">← Back to Voting Cards</button>
    </div>"""
)

# 3. Make opening The Rec Area default back to 'vote' (displaying the 3-pic vote & Saturday run-off cards directly)
html = html.replace("openHubSection('recTimeSection', 'pics')", "openHubSection('recTimeSection', 'vote')")

# 4. Update switchRecTab() so 'vote' shows recVotePanel directly while keeping the top tab button removed
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

            if (tab === 'pics') {
                document.getElementById('recTabPicsBtn').classList.add('active');
                document.getElementById('recPicsPanel').style.display = 'block';
            } else if (tab === 'videos') {
                document.getElementById('recTabVideosBtn').classList.add('active');
                document.getElementById('recVideosPanel').style.display = 'block';
            } else if (tab === 'trivia') {
                document.getElementById('recTabTriviaBtn').classList.add('active');
                document.getElementById('recTriviaPanel').style.display = 'block';
                document.getElementById('triviaLobbyBox').style.display = 'block';
                document.getElementById('triviaPlayBox').style.display = 'none';
                document.getElementById('recTimerDisplay').innerText = '⏱️ 30s Left';
            } else {
                document.getElementById('recVotePanel').style.display = 'block';
            }
        }

        """
    html = html[:old_switch_start] + new_switch_fn + html[old_switch_end:]

with open("templates/index.html", "w") as f:
    f.write(html)
print("REC_AREA_RESTORED_WITH_VOTE_CARDS_SUCCESS")
