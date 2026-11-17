with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Remove the bottom "Question About Autism" box from The Wall of Seriousness & space out nicely
old_bottom_autism_box = """                <!-- Bottom Highlighted Category Box (e.g., Question About Autism) -->
                <div style="margin-top: 16px; background: rgba(15, 23, 42, 0.88); border: 1.5px solid #fde047; border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="background: #fde047; color: #0f172a; font-weight: 800; font-size: 0.74rem; padding: 3px 10px; border-radius: 6px; text-transform: uppercase;">Question About Autism</span>
                        <span style="font-size: 0.78rem; color: #e2e8f0; margin-left: 8px;">Quick-jump filter for active Autism & sensory threads on the wall.</span>
                    </div>
                    <button type="button" class="back-hub-btn" style="border-color: #fde047; color: #fde047;" onclick="document.getElementById('wallTopicFilterInput').value='Autism'; filterWallPapers();">Show Autism Notes</button>
                </div>"""

html = html.replace(old_bottom_autism_box, "")

# Increase spacing slightly in the pinned papers grid for breathing room
html = html.replace(
    "grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin-top: 12px;",
    "grid-template-columns: repeat(auto-fill, minmax(275px, 1fr)); gap: 18px; margin-top: 16px;"
)

# 2. Change "← Back to Sanctuary" to "← Back to Dashboard"
html = html.replace("← Back to Sanctuary", "← Back to Dashboard")

# 3. Update the 4 FYI Navigation Buttons & Remove "Click to View the Daily Vote"
old_fyi_and_vote = """                        <!-- Skinny, Comfortable Navigation Buttons -->
                        <div class="fyi-strip">
                            <button type="button" class="fyi-btn fyi-mentor" onclick="switchView('wallOfSeriousnessView')">
                                <div>
                                    <div class="fyi-btn-title">🎓 Serious Question Posting</div>
                                    <div class="fyi-btn-sub">More serious questions. Get real answers for those serious moments.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-kids" onclick="openHubSection('kidsCornerSection')">
                                <div>
                                    <div class="fyi-btn-title">🌈 Kids Corner</div>
                                    <div class="fyi-btn-sub">Kids connecting with kids — fun chat & picture sharing.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-rec" onclick="openHubSection('recTimeSection', 'vote')">
                                <div>
                                    <div class="fyi-btn-title">☕ REC Time</div>
                                    <div class="fyi-btn-sub">REC Time, take a moment, and relax. Funny pics, 30s videos & 100+ trivia.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-wood" onclick="openHubSection('harborPostingSpotSection')">
                                <div>
                                    <div class="fyi-btn-title">🪵 The Harbor's Posting Spot</div>
                                    <div class="fyi-btn-sub">Have something that made your journey a little easier? Pass on usable gear.</div>
                                </div>
                                <span>→</span>
                            </button>
                        </div>
                    </div>

                    <!-- Bottom of Right Column: Click to View Daily Vote + 10:00 PM Reveal -->
                    <div>
                        <button type="button" class="daily-vote-jump-btn" onclick="openHubSection('recTimeSection', 'vote')">
                            🗳️ Click to View the Daily Vote (24-Hour Cycle)
                        </button>

                        <div style="background: rgba(13, 56, 63, 0.78); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 8px; padding: 9px; font-size: 0.73rem; color: #cbd5e1;">
                            🏆 <strong>10:00 PM Reveal:</strong> Saturday's winning finalist from the Mon/Wed/Fri run-off is automatically placed in the Welcome Spotlight!
                        </div>
                    </div>"""

new_fyi_and_bottom = """                        <!-- Skinny, Comfortable Navigation Buttons -->
                        <div class="fyi-strip">
                            <button type="button" class="fyi-btn fyi-mentor" onclick="switchView('wallOfSeriousnessView')">
                                <div>
                                    <div class="fyi-btn-title">🧱 The Wall of Seriousness</div>
                                    <div class="fyi-btn-sub">Real questions answered with directness for those serious moments.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-kids" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(14, 116, 144, 0.75)); border-color: #38bdf8; color: #e0f2fe;" onclick="openHubSection('kidsCornerSection')">
                                <div>
                                    <div class="fyi-btn-title">🌐 The Gathering Place</div>
                                    <div class="fyi-btn-sub">Connecting those 21 and under — chat amongst yourselves & share pics.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-rec" onclick="openHubSection('recTimeSection', 'vote')">
                                <div>
                                    <div class="fyi-btn-title">☕ The Rec Area</div>
                                    <div class="fyi-btn-sub">Take a moment and relax — funny pics, 30s clips & random trivia.</div>
                                </div>
                                <span>→</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-wood" onclick="openHubSection('harborPostingSpotSection')">
                                <div>
                                    <div class="fyi-btn-title">🪵 Pass It On</div>
                                    <div class="fyi-btn-sub">Pay forward usable equipment, tools, and gear to ease another's journey.</div>
                                </div>
                                <span>→</span>
                            </button>
                        </div>
                    </div>

                    <!-- Bottom of Right Column -->
                    <div>
                        <div style="background: rgba(13, 56, 63, 0.78); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 8px; padding: 10px; font-size: 0.74rem; color: #cbd5e1;">
                            🏆 <strong>10:00 PM Reveal:</strong> Saturday's winning finalist from the Mon/Wed/Fri run-off is automatically placed in the Welcome Spotlight!
                        </div>
                    </div>"""

if old_fyi_and_vote in html:
    html = html.replace(old_fyi_and_vote, new_fyi_and_bottom)
else:
    print("WARNING: Could not match old_fyi_and_vote block.")

# 4. Update Kids Corner -> "The Gathering Place" (Modern Slate/Cyan Theme, Name, Comment, Picture Upload, Submit)
old_kids_section = """            <!-- EXPANDABLE SUB-VIEW 2: KIDS CORNER (FUN COLORS, KIDS CONNECTING WITH KIDS, NO BRANCH-OFFS) -->
            <div id="kidsCornerSection" class="hub-subview" style="border-color: #f472b6; background: linear-gradient(135deg, rgba(131, 24, 67, 0.9), rgba(120, 53, 15, 0.9));">
                <div class="subview-header" style="border-bottom-color: rgba(244, 114, 182, 0.4);">
                    <div>
                        <div class="subview-title" style="color: #fbcfe8;">🌈 Kids Corner — Kids Connecting With Kids</div>
                        <div style="font-size: 0.76rem; color: #fef3c7;">Share your day, post a cool picture, and hang out with other kids!</div>
                    </div>
                    <button class="back-hub-btn" style="border-color: #fbcfe8; color: #fbcfe8;" onclick="closeHubSections()">✕ Close</button>
                </div>

                <form onsubmit="event.preventDefault(); postKidsJourney();" style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; margin-bottom: 12px;">
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
                        <input type="text" id="kidNameInput" class="dark-input" style="max-width: 170px;" required placeholder="Your Kid Name">
                        <input type="text" id="kidJourneyInput" class="dark-input" style="flex: 1; min-width: 200px;" required placeholder="Say hi or share what you did today...">
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <label for="kidPhotoUpload" class="attach-btn-mini" style="border-color: #fde047; color: #fde047; cursor: pointer;">📸 Upload Picture</label>
                            <input type="file" id="kidPhotoUpload" accept="image/*" style="display: none;" onchange="document.getElementById('kidPhotoName').innerText = this.files[0] ? this.files[0].name : ''">
                            <span id="kidPhotoName" style="font-size: 0.7rem; color: #fde047;"></span>
                        </div>
                        <button type="submit" class="action-btn" style="width: auto; padding: 7px 16px; margin-top: 0; background: #fde047; color: #0b2e33; font-size: 0.8rem;">Post to Kids Chat ✨</button>
                    </div>
                </form>

                <div id="kidsCornerFeed" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="tally-card" style="background: rgba(255, 255, 255, 0.12); border-color: #fde047;">
                        <strong style="color: #fde047;">🌟 Marcus (Age 7)</strong>
                        <p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">Tested out the Hoover Power Scrub and helped clean the living room carpet today!</p>
                    </div>
                    <div class="tally-card" style="background: rgba(255, 255, 255, 0.12); border-color: #f472b6;">
                        <strong style="color: #fbcfe8;">🎧 Lewie</strong>
                        <p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">Listening to my favorite tracks and having a chill afternoon.</p>
                    </div>
                </div>
            </div>"""

new_gathering_section = """            <!-- EXPANDABLE SUB-VIEW 2: THE GATHERING PLACE (21 AND UNDER — MODERN SLATE/CYAN THEME) -->
            <div id="kidsCornerSection" class="hub-subview" style="border-color: #38bdf8; background: linear-gradient(145deg, rgba(15, 23, 42, 0.96), rgba(14, 116, 144, 0.88));">
                <div class="subview-header" style="border-bottom-color: rgba(56, 189, 248, 0.35);">
                    <div>
                        <div class="subview-title" style="color: #38bdf8;">🌐 The Gathering Place (21 &amp; Under)</div>
                        <div style="font-size: 0.76rem; color: #bae6fd;">Connecting those 21 and under — chat amongst yourselves and share pictures.</div>
                    </div>
                    <button class="back-hub-btn" style="border-color: #38bdf8; color: #38bdf8;" onclick="closeHubSections()">✕ Close</button>
                </div>

                <form onsubmit="event.preventDefault(); postKidsJourney();" style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(56, 189, 248, 0.35); padding: 12px; border-radius: 10px; margin-bottom: 12px;">
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
                        <input type="text" id="kidNameInput" class="dark-input" style="max-width: 190px; border-color: rgba(56, 189, 248, 0.45);" required placeholder="Name">
                        <input type="text" id="kidJourneyInput" class="dark-input" style="flex: 1; min-width: 200px; border-color: rgba(56, 189, 248, 0.45);" required placeholder="Comment">
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <label for="kidPhotoUpload" class="attach-btn-mini" style="border-color: #38bdf8; color: #38bdf8; cursor: pointer;">📸 Upload Picture</label>
                            <input type="file" id="kidPhotoUpload" accept="image/*" style="display: none;" onchange="handleGatheringPhoto(this)">
                            <span id="kidPhotoName" style="font-size: 0.72rem; color: #7dd3fc;"></span>
                        </div>
                        <button type="submit" class="action-btn" style="width: auto; padding: 7px 18px; margin-top: 0; background: #38bdf8; color: #0f172a; font-weight: 800; font-size: 0.82rem;">Submit</button>
                    </div>
                </form>

                <div id="kidsCornerFeed" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="tally-card" style="background: rgba(15, 23, 42, 0.72); border-color: rgba(56, 189, 248, 0.4);">
                        <strong style="color: #38bdf8;">Marcus, Age 7</strong>
                        <p style="font-size: 0.82rem; color: #f1f5f9; margin-top: 3px;">Tested out the Hoover Power Scrub and helped clean the living room carpet today!</p>
                    </div>
                    <div class="tally-card" style="background: rgba(15, 23, 42, 0.72); border-color: rgba(56, 189, 248, 0.4);">
                        <strong style="color: #7dd3fc;">Lewie</strong>
                        <p style="font-size: 0.82rem; color: #f1f5f9; margin-top: 3px;">Listening to my favorite tracks and having a chill afternoon.</p>
                    </div>
                </div>
            </div>"""

if old_kids_section in html:
    html = html.replace(old_kids_section, new_gathering_section)

# 5. Update the Gathering Place JS to support image preview rendering on Submit
old_kids_js = """        /* Kids Corner Post */
        function postKidsJourney() {
            const kid = document.getElementById('kidNameInput').value.trim();
            const msg = document.getElementById('kidJourneyInput').value.trim();
            if (!kid || !msg) return;
            const feed = document.getElementById('kidsCornerFeed');
            const card = document.createElement('div');
            card.className = 'tally-card';
            card.style.background = 'rgba(255, 255, 255, 0.14)';
            card.style.borderColor = '#fde047';
            card.innerHTML = `<strong style="color: #fde047;">🌟 ${kid}</strong><p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">${msg}</p>`;
            feed.prepend(card);
            document.getElementById('kidNameInput').value = '';
            document.getElementById('kidJourneyInput').value = '';
            document.getElementById('kidPhotoName').innerText = '';
        }"""

new_gathering_js = """        /* The Gathering Place (21 & Under) Post + Picture Upload */
        let pendingGatheringPhotoUrl = null;
        function handleGatheringPhoto(input) {
            if (input.files && input.files[0]) {
                document.getElementById('kidPhotoName').innerText = input.files[0].name;
                const reader = new FileReader();
                reader.onload = function(e) { pendingGatheringPhotoUrl = e.target.result; };
                reader.readAsDataURL(input.files[0]);
            }
        }

        function postKidsJourney() {
            const kid = document.getElementById('kidNameInput').value.trim();
            const msg = document.getElementById('kidJourneyInput').value.trim();
            if (!kid || (!msg && !pendingGatheringPhotoUrl)) return;
            const feed = document.getElementById('kidsCornerFeed');
            const card = document.createElement('div');
            card.className = 'tally-card';
            card.style.background = 'rgba(15, 23, 42, 0.78)';
            card.style.borderColor = '#38bdf8';
            const imgTag = pendingGatheringPhotoUrl ? `<img src="${pendingGatheringPhotoUrl}" class="chat-photo-preview" alt="Uploaded photo">` : '';
            card.innerHTML = `<strong style="color: #38bdf8;">${kid}</strong><p style="font-size: 0.82rem; color: #f1f5f9; margin-top: 3px;">${msg}</p>${imgTag}`;
            feed.prepend(card);
            document.getElementById('kidNameInput').value = '';
            document.getElementById('kidJourneyInput').value = '';
            document.getElementById('kidPhotoUpload').value = '';
            document.getElementById('kidPhotoName').innerText = '';
            pendingGatheringPhotoUrl = null;
        }"""

if old_kids_js in html:
    html = html.replace(old_kids_js, new_gathering_js)

# 6. Also update titles inside REC Area & Pass It On subviews to match button labels
html = html.replace("☕ REC Time — Take a Moment, and Relax", "☕ The Rec Area — Take a Moment, and Relax")
html = html.replace("✕ Close REC Time", "✕ Close Rec Area")
html = html.replace("🪵 The Harbor Posting Board", "🪵 Pass It On — Public Posting Board")

with open("templates/index.html", "w") as f:
    f.write(html)
print("GATHERING_AND_WALL_UPDATED_SUCCESS")
