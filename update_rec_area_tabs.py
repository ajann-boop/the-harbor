with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Replace the REC Time / The Rec Area sub-view HTML
start_marker = "<!-- EXPANDABLE SUB-VIEW 3: REC TIME"
end_marker = "<!-- EXPANDABLE SUB-VIEW 4: THE HARBOR'S POSTING SPOT"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_rec_area_html = """<!-- EXPANDABLE SUB-VIEW 3: THE REC AREA (4 SEPARATE TABS + 30-SECOND RANDOM TRIVIA) -->
            <div id="recTimeSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">☕ The Rec Area — Take a Moment, and Relax</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">Cast your daily picture vote, browse funny pics, watch 30-second clips, or test your speed in Random Trivia!</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close Rec Area</button>
                </div>

                <!-- 4 Separate Top Tab Buttons -->
                <div class="rec-tabs">
                    <button class="rec-tab-btn active" id="recTabVoteBtn" onclick="switchRecTab('vote')">🗳️ Daily Picture Vote</button>
                    <button class="rec-tab-btn" id="recTabPicsBtn" onclick="switchRecTab('pics')">😂 Funny Pics</button>
                    <button class="rec-tab-btn" id="recTabVideosBtn" onclick="switchRecTab('videos')">
                        <div>🎬 Funny Videos</div>
                        <div style="font-size: 0.64rem; font-weight: 600; opacity: 0.85;">(30 seconds or less)</div>
                    </button>
                    <button class="rec-tab-btn" id="recTabTriviaBtn" onclick="switchRecTab('trivia')">🧠 Random Trivia</button>
                </div>

                <!-- TAB 1: DAILY PICTURE VOTE (24-HR DAILY VOTE + SATURDAY RUN-OFF) -->
                <div id="recVotePanel">
                    <div style="font-size: 0.84rem; font-weight: 700; color: #5eead4; margin-bottom: 4px;">📸 Today's 3 Random Pics (Refreshes Every 24 Hours)</div>
                    <div style="font-size: 0.74rem; color: #cbd5e1; margin-bottom: 8px;">Vote for your favorite photo submitted from Community Chat!</div>

                    <div class="three-pic-vote-grid" id="dailyThreePicsGrid">
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Pic 1">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Sunny Park Breakthrough</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By Caregiver Sarah</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #1</button>
                        </div>
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" alt="Pic 2">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Evening Porch Laughs</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By BeaconMom</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #2</button>
                        </div>
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Pic 3">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Morning Coffee Victory</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By HopeWalker</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #3</button>
                        </div>
                    </div>

                    <!-- Saturday Election Run-Off Card -->
                    <div style="margin-top: 18px; border-top: 1px solid rgba(94, 234, 212, 0.3); padding-top: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                            <div style="font-size: 0.9rem; font-weight: 800; color: #fde047;">🏆 Saturday Election Run-Off Card (Mon / Wed / Fri Winners)</div>
                            <span style="font-size: 0.7rem; background: rgba(244, 63, 94, 0.25); color: #fb7185; padding: 3px 8px; border-radius: 50px; font-weight: 700;">Saturday Head-to-Head Hidden Till 10:00 PM</span>
                        </div>

                        <div class="three-pic-vote-grid">
                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">1. Monday's Winner</span>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Monday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">Caregiver Sarah</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Monday Tally: 28 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'Caregiver Sarah')">🗳️ Vote in Saturday Run-Off</button>
                            </div>

                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">2. Wednesday's Winner</span>
                                <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" alt="Wednesday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">HopeWalker</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Wednesday Tally: 34 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'HopeWalker')">🗳️ Vote in Saturday Run-Off</button>
                            </div>

                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">3. Friday's Winner</span>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Friday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">BeaconMom</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Friday Tally: 31 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'BeaconMom')">🗳️ Vote in Saturday Run-Off</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 2: FUNNY PICS (SEPARATE TAB) -->
                <div id="recPicsPanel" style="display: none;">
                    <div style="font-size: 0.84rem; font-weight: 700; color: #5eead4; margin-bottom: 8px;">😂 Funny Pics Gallery — Quick Caregiver Laughs</div>
                    <div class="three-pic-vote-grid">
                        <div class="tally-card">
                            <strong style="color: #5eead4;">🧺 The Endless Laundry Mountain</strong>
                            <p style="font-size: 0.78rem; color: #e2e8f0; margin: 6px 0;">"Folded one basket today. Three more mysteriously appeared behind me."</p>
                            <button class="back-hub-btn" onclick="this.innerText='😂 Haha! (19)'">😂 Haha! (18)</button>
                        </div>
                        <div class="tally-card">
                            <strong style="color: #fde047;">☕ Reheated Coffee #4</strong>
                            <p style="font-size: 0.78rem; color: #e2e8f0; margin: 6px 0;">"Found my morning coffee in the microwave at 3:30 PM. Still counts as hydrated."</p>
                            <button class="back-hub-btn" onclick="this.innerText='😂 Haha! (25)'">😂 Haha! (24)</button>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: FUNNY VIDEOS (30 SECONDS OR LESS — SEPARATE TAB) -->
                <div id="recVideosPanel" style="display: none;">
                    <div style="font-size: 0.84rem; font-weight: 700; color: #fde047; margin-bottom: 8px;">🎬 Funny Videos (30 seconds or less)</div>
                    <div class="three-pic-vote-grid">
                        <div class="tally-card">
                            <strong style="color: #fde047;">⏱️ 0:24 — When the Morning Meds Alarm Goes Off</strong>
                            <p style="font-size: 0.78rem; color: #e2e8f0; margin: 6px 0;">"Me at 6:00 AM trying to remember which pill organizer is Tuesday."</p>
                            <button class="back-hub-btn" onclick="alert('Playing 24-second community funny clip!')">▶ Play Clip (24s)</button>
                        </div>
                        <div class="tally-card">
                            <strong style="color: #38bdf8;">⏱️ 0:18 — Cat Supervisory Inspection</strong>
                            <p style="font-size: 0.78rem; color: #e2e8f0; margin: 6px 0;">"Our black cat inspecting every grocery bag before we're allowed to put anything away."</p>
                            <button class="back-hub-btn" onclick="alert('Playing 18-second community funny clip!')">▶ Play Clip (18s)</button>
                        </div>
                    </div>
                </div>

                <!-- TAB 4: RANDOM TRIVIA (30-SECOND TIMED BLITZ & HEAD-TO-HEAD SCOREBOARD) -->
                <div id="recTriviaPanel" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div style="font-size: 0.88rem; color: #5eead4; font-weight: 800;">🧠 Random Trivia — 30-Second Speed Challenge</div>
                            <div style="font-size: 0.72rem; color: #cbd5e1;">See how many shuffled questions you can get right in 30 seconds or less and post your score!</div>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 800; color: #fde047;" id="recTimerDisplay">⏱️ 30s Left</div>
                    </div>

                    <div id="triviaLobbyBox" style="background: rgba(15, 61, 68, 0.75); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 10px; padding: 16px; text-align: center;">
                        <p style="font-size: 0.84rem; color: #e2e8f0; margin-bottom: 12px;">Questions shuffle randomly every round — from how to fry an egg to deep life &amp; science trivia. Score points and compare against fellow members!</p>
                        <button type="button" class="action-btn" style="max-width: 280px; margin: 0 auto;" onclick="startThirtySecondTrivia()">🚀 Start 30-Second Random Trivia</button>
                    </div>

                    <div id="triviaPlayBox" style="display: none; background: rgba(15, 61, 68, 0.82); border: 1.5px solid #5eead4; border-radius: 10px; padding: 14px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.76rem; font-weight: 700; margin-bottom: 6px;">
                            <span id="recCategoryLabel" style="color: #38bdf8; text-transform: uppercase;">Category</span>
                            <span id="recScoreText" style="color: #4ade80;">Score: 0 / 0</span>
                        </div>
                        <div id="recQuestionText" style="font-size: 0.98rem; font-weight: 800; color: #ffffff; margin-bottom: 12px;"></div>
                        <div id="recOptionsBox" style="display: flex; flex-direction: column; gap: 7px;"></div>
                    </div>

                    <!-- Friendly Member Scoreboard -->
                    <div style="margin-top: 12px; background: rgba(11, 46, 51, 0.75); border: 1px solid rgba(94, 234, 212, 0.3); border-radius: 10px; padding: 10px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #fde047; margin-bottom: 6px;">🏆 30-Second Random Trivia Leaderboard</div>
                        <div id="triviaLeaderboardList" style="display: flex; flex-direction: column; gap: 4px; font-size: 0.76rem; color: #e2e8f0;">
                            <div style="display: flex; justify-content: space-between;"><span>1. HopeWalker</span><span style="color: #5eead4; font-weight: 700;">16 / 20 in 30s</span></div>
                            <div style="display: flex; justify-content: space-between;"><span>2. Caregiver Sarah</span><span style="color: #5eead4; font-weight: 700;">14 / 18 in 30s</span></div>
                        </div>
                    </div>
                </div>
            </div>

            """

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_rec_area_html + html[end_idx:]
else:
    print("WARNING: Could not locate REC Time block markers.")

# 2. Replace the REC Time JS logic with the 4-tab switcher & 30-second shuffled Random Trivia engine
old_rec_js_start = html.find("/* REC Time Tabs, 24-Hr Vote, Saturday Run-Off, & 100+ Trivia Bank */")
old_rec_js_end = html.find("/* Kids Corner Post */")
if old_rec_js_end == -1:
    old_rec_js_end = html.find("/* The Gathering Place (21 & Under) Post + Picture Upload */")

new_rec_js = """/* The Rec Area Tabs, Daily Vote, Saturday Run-Off, & 30-Second Random Trivia */
        let triviaTimerInterval = null;
        function switchRecTab(tab) {
            ['recTabVoteBtn', 'recTabPicsBtn', 'recTabVideosBtn', 'recTabTriviaBtn'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active');
            });
            ['recVotePanel', 'recPicsPanel', 'recVideosPanel', 'recTriviaPanel'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            });
            if (triviaTimerInterval) clearInterval(triviaTimerInterval);

            if (tab === 'vote') {
                document.getElementById('recTabVoteBtn').classList.add('active');
                document.getElementById('recVotePanel').style.display = 'block';
            } else if (tab === 'pics') {
                document.getElementById('recTabPicsBtn').classList.add('active');
                document.getElementById('recPicsPanel').style.display = 'block';
            } else if (tab === 'videos') {
                document.getElementById('recTabVideosBtn').classList.add('active');
                document.getElementById('recVideosPanel').style.display = 'block';
            } else {
                document.getElementById('recTabTriviaBtn').classList.add('active');
                document.getElementById('recTriviaPanel').style.display = 'block';
                document.getElementById('triviaLobbyBox').style.display = 'block';
                document.getElementById('triviaPlayBox').style.display = 'none';
                document.getElementById('recTimerDisplay').innerText = '⏱️ 30s Left';
            }
        }

        function voteForDailyPic(btn) {
            document.querySelectorAll('#dailyThreePicsGrid button').forEach(b => { b.disabled = true; b.style.opacity = '0.55'; });
            btn.style.opacity = '1';
            btn.innerText = '✓ 24-Hr Vote Cast!';
        }

        function voteSaturdayRunoff(btn, caregiverName) {
            alert('Your Saturday Run-Off vote for ' + caregiverName + ' has been recorded! Live totals remain hidden until the 10:00 PM reveal.');
            btn.innerText = '✓ Run-Off Vote Cast';
            btn.disabled = true;
        }

        /* Expandable Random Trivia Question Bank (Shuffles every round) */
        const triviaBank = [
            { cat: "Everyday Kitchen Basics", q: "When frying an egg sunny-side up, what helps the whites set evenly without burning the bottom?", opts: ["Cranking the burner to max high", "Medium-low heat with a lid or gentle butter basting", "Adding cold water to the oil", "Stirring constantly with a whisk"], ans: 1 },
            { cat: "Deep & Serious Reflections", q: "In caregiving psychology, what is 'compassion fatigue'?", opts: ["Forgetting to take vitamins", "Physical and emotional exhaustion from prolonged caregiving without respite", "Sleeping too many hours", "Being allergic to hospital soap"], ans: 1 },
            { cat: "Everyday Life & Home", q: "What is the quickest way to neutralize lingering odors in a refrigerator?", opts: ["An open box of baking soda or activated charcoal", "Leaving the door open all night", "Spraying window cleaner inside", "Turning the fridge off"], ans: 0 },
            { cat: "Serious Medical & Care Knowledge", q: "Why is keeping an updated one-page Emergency Care Summary vital for pediatric or special-needs caregivers?", opts: ["It replaces health insurance", "It gives ER teams immediate baseline vitals, meds, and sensory triggers", "It is only needed for air travel", "It lowers pharmacy prices"], ans: 1 },
            { cat: "Everyday Kitchen Basics", q: "Why should you let cooked meat rest for 5–10 minutes before slicing?", opts: ["To let it get completely cold", "So juices redistribute throughout the meat instead of running onto the board", "To make it harder to chew", "To evaporate the salt"], ans: 1 },
            { cat: "Serious Life & Resilience", q: "What makes peer-to-peer lived experience different from textbook advice?", opts: ["It comes from people who actually walked the storm in real time", "It is written by robots", "It ignores real-world emotions", "It only applies to doctors"], ans: 0 },
            { cat: "Science & Nature", q: "Which planet in our solar system has the most moons?", opts: ["Mars", "Saturn", "Venus", "Mercury"], ans: 1 },
            { cat: "Everyday Basics", q: "What temperature does water boil at sea level in Fahrenheit?", opts: ["180°F", "212°F", "250°F", "100°F"], ans: 1 },
            { cat: "Geography & World", q: "Which ocean is the largest and deepest on Earth?", opts: ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"], ans: 2 },
            { cat: "Classic Music & Culture", q: "Which classic rock band released the legendary 1977 album 'Rumours'?", opts: ["Fleetwood Mac", "The Eagles", "Led Zeppelin", "The Rolling Stones"], ans: 0 },
            { cat: "Everyday Kitchen Basics", q: "What ingredient makes bread dough rise by producing carbon dioxide bubbles?", opts: ["Olive oil", "Yeast", "Paprika", "Sea salt"], ans: 1 },
            { cat: "Serious Health & Wellness", q: "Why is deep diaphragmatic breathing effective during an acute stress spike?", opts: ["It raises blood pressure immediately", "It stimulates the vagus nerve and slows heart rate", "It stops oxygen flow", "It only works while asleep"], ans: 1 }
        ];

        let shuffledTriviaPool = [];
        let triviaPointer = 0;
        let triviaRightCount = 0;
        let triviaAttemptedCount = 0;
        let triviaSecondsLeft = 30;

        function shuffleArray(arr) {
            const copy = arr.slice();
            for (let i = copy.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [copy[i], copy[j]] = [copy[j], copy[i]];
            }
            return copy;
        }

        function startThirtySecondTrivia() {
            if (triviaTimerInterval) clearInterval(triviaTimerInterval);
            shuffledTriviaPool = shuffleArray(triviaBank);
            triviaPointer = 0;
            triviaRightCount = 0;
            triviaAttemptedCount = 0;
            triviaSecondsLeft = 30;

            document.getElementById('triviaLobbyBox').style.display = 'none';
            document.getElementById('triviaPlayBox').style.display = 'block';
            document.getElementById('recScoreText').innerText = 'Score: 0 / 0';
            document.getElementById('recTimerDisplay').innerText = '⏱️ 30s Left';

            renderNextRandomTrivia();

            triviaTimerInterval = setInterval(() => {
                triviaSecondsLeft--;
                document.getElementById('recTimerDisplay').innerText = `⏱️ ${triviaSecondsLeft}s Left`;
                if (triviaSecondsLeft <= 0) {
                    clearInterval(triviaTimerInterval);
                    finishTriviaRound();
                }
            }, 1000);
        }

        function renderNextRandomTrivia() {
            if (triviaPointer >= shuffledTriviaPool.length) {
                shuffledTriviaPool = shuffleArray(triviaBank);
                triviaPointer = 0;
            }
            const item = shuffledTriviaPool[triviaPointer++];
            document.getElementById('recCategoryLabel').innerText = 'Category: ' + item.cat;
            document.getElementById('recQuestionText').innerText = item.q;
            const box = document.getElementById('recOptionsBox');
            box.innerHTML = '';
            item.opts.forEach((opt, idx) => {
                const b = document.createElement('button');
                b.type = 'button';
                b.className = 'back-hub-btn';
                b.style.textAlign = 'left';
                b.style.padding = '8px 12px';
                b.innerText = opt;
                b.onclick = () => {
                    triviaAttemptedCount++;
                    if (idx === item.ans) triviaRightCount++;
                    document.getElementById('recScoreText').innerText = `Score: ${triviaRightCount} / ${triviaAttemptedCount}`;
                    renderNextRandomTrivia();
                };
                box.appendChild(b);
            });
        }

        function finishTriviaRound() {
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';
            const board = document.getElementById('triviaLeaderboardList');
            const row = document.createElement('div');
            row.style.display = 'flex';
            row.style.justifyContent = 'space-between';
            row.innerHTML = `<span>⭐ ${member} (You)</span><span style="color: #fde047; font-weight: 800;">${triviaRightCount} / ${triviaAttemptedCount} in 30s</span>`;
            board.prepend(row);

            alert(`Time's up! You got ${triviaRightCount} out of ${triviaAttemptedCount} right in 30 seconds!`);
            document.getElementById('triviaPlayBox').style.display = 'none';
            document.getElementById('triviaLobbyBox').style.display = 'block';
        }

        """

if old_rec_js_start != -1 and old_rec_js_end != -1:
    html = html[:old_rec_js_start] + new_rec_js + html[old_rec_js_end:]
else:
    print("WARNING: Could not locate REC JS block markers.")

# Also update Community Hub button subtitle for The Rec Area
html = html.replace(
    "Take a moment and relax — funny pics, 30s clips &amp; random trivia.",
    "Daily picture vote, funny pics, funny videos (30s or less) &amp; random trivia."
)

with open("templates/index.html", "w") as f:
    f.write(html)
print("REC_AREA_TABS_UPDATED_SUCCESS")
