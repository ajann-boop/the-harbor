with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Update CSS to add Cork Board, Hub Sub-Views, and Sensory Coloring styles
extra_css = """
        /* Hub Sub-Views (Posting Board, REC Time, Kids Corner, Teachers Lounge Cork Board) */
        .hub-subview { display: none; background: rgba(11, 46, 51, 0.85); border: 1.5px solid #5eead4; border-radius: 14px; padding: 18px; margin-bottom: 18px; backdrop-filter: blur(14px); box-shadow: 0 10px 28px rgba(0,0,0,0.45); }
        .hub-subview.active { display: block; }
        .subview-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(94, 234, 212, 0.3); padding-bottom: 10px; margin-bottom: 14px; }
        .subview-title { font-size: 1.1rem; font-weight: 800; color: #5eead4; }
        .back-hub-btn { background: rgba(94, 234, 212, 0.15); border: 1px solid #5eead4; color: #5eead4; padding: 5px 12px; border-radius: 50px; font-size: 0.76rem; font-weight: 700; cursor: pointer; }
        .back-hub-btn:hover { background: #5eead4; color: #0b2e33; }

        /* Cork Board Styling for Teachers Lounge */
        .cork-board-area { background: linear-gradient(135deg, rgba(120, 72, 32, 0.32), rgba(88, 52, 22, 0.42)); border: 2px solid rgba(217, 155, 82, 0.55); border-radius: 12px; padding: 14px; margin-top: 12px; }
        .cork-note { background: rgba(15, 61, 68, 0.88); border: 1px solid rgba(253, 224, 71, 0.45); border-radius: 10px; padding: 12px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.35); position: relative; }
        .cork-highlight-badge { display: inline-block; background: #fde047; color: #0b2e33; font-weight: 800; font-size: 0.72rem; padding: 3px 10px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; box-shadow: 0 2px 6px rgba(253, 224, 71, 0.35); }
        .cork-question-text { font-size: 0.88rem; color: #ffffff; font-weight: 600; line-height: 1.4; }
        .cork-meta { font-size: 0.72rem; color: #cbd5e1; margin-top: 6px; display: flex; justify-content: space-between; align-items: center; }

        /* Sensory Coloring & Trivia in REC Time */
        .rec-tabs { display: flex; gap: 8px; margin-bottom: 14px; }
        .rec-tab-btn { flex: 1; padding: 8px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.4); background: rgba(15, 61, 68, 0.5); color: #cbd5e1; font-weight: 700; font-size: 0.8rem; cursor: pointer; }
        .rec-tab-btn.active { background: #5eead4; color: #0b2e33; border-color: #5eead4; }
        .swatch-row { display: flex; justify-content: center; gap: 10px; margin: 12px 0; flex-wrap: wrap; }
        .color-swatch { width: 30px; height: 30px; border-radius: 50%; border: 2px solid #ffffff; cursor: pointer; transition: transform 0.15s; }
        .color-swatch:hover { transform: scale(1.15); }
        .coloring-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 10px; }
        .color-zone { background: rgba(255, 255, 255, 0.08); border: 2px dashed rgba(94, 234, 212, 0.45); border-radius: 10px; padding: 18px 10px; text-align: center; font-weight: 700; font-size: 0.82rem; color: #e2e8f0; cursor: pointer; transition: background 0.25s, color 0.25s; }
"""

html = html.replace("</style>", extra_css + "\n    </style>")

# 2. Replace the Sideways Rolodex section with the updated Sanctuary Hub + 4 Interactive Sub-Views
old_rolodex_block = """            <!-- Sideways Spinning Wheel Rolodex -->
            <div class="sideways-rolodex-wrapper">
                <div style="font-size: 0.85rem; font-weight: 700; color: #5eead4; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span>🎡 Sanctuary Hub Rolodex (Swipe or Scroll Sideways)</span>
                </div>
                <div class="rolodex-wheel">
                    <div class="rolodex-category-card" onclick="alert('Entering Teachers Lounge: Resources, school communications, and educator tips.');">
                        <div class="rolodex-cat-title">👩‍🏫 Teachers' Lounge</div>
                        <div class="rolodex-cat-desc">Direct teacher comms, school updates, and IEP support strategies.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="alert('Entering Kids Harbor & Kids Talk: Secure, kid-friendly interaction space.');">
                        <div class="rolodex-cat-title">🎨 Kids' Harbor & Talk</div>
                        <div class="rolodex-cat-desc">A secure, supervised space where kids connect, share drawings, and chat safely.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="alert('Entering Activities & Respite: Local parks, events, and family outings.');">
                        <div class="rolodex-cat-title">🌲 Activities & Outings</div>
                        <div class="rolodex-cat-desc">Sensory-friendly parks, community events, and family respite ideas.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="alert('Entering Equipment & Gear Exchange: Safe exchange of adaptive gear and tools.');">
                        <div class="rolodex-cat-title">🛡️ Gear & Resource Exchange</div>
                        <div class="rolodex-cat-desc">Pass on adaptive equipment and medical tools to families in need.</div>
                    </div>
                </div>
            </div>"""

new_hub_block = """            <!-- Sanctuary Hub Navigation Strip -->
            <div class="sideways-rolodex-wrapper">
                <div style="font-size: 0.88rem; font-weight: 700; color: #5eead4; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                    <span>⚓ Sanctuary Hub (Swipe or Scroll Sideways)</span>
                </div>
                <div class="rolodex-wheel">
                    <div class="rolodex-category-card" onclick="openHubSection('postingBoardSection')">
                        <div class="rolodex-cat-title">📋 The Harbor Posting Board</div>
                        <div class="rolodex-cat-desc">Storm gear being offered that is not needed at the present time, in usable condition, to help ease another's journey.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="openHubSection('recTimeSection')">
                        <div class="rolodex-cat-title">🖍️ REC Time</div>
                        <div class="rolodex-cat-desc">Caregiver trivia, interactive coloring, and sensory-friendly coloring pages to unwind.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="openHubSection('kidsCornerSection')">
                        <div class="rolodex-cat-title">🌟 Kids Corner</div>
                        <div class="rolodex-cat-desc">A safe, welcoming space where kids can connect and share their daily journey.</div>
                    </div>
                    <div class="rolodex-category-card" onclick="openHubSection('teachersLoungeSection')">
                        <div class="rolodex-cat-title">📌 Teachers' Lounge</div>
                        <div class="rolodex-cat-desc">Community cork board for serious specialty questions on autism, illness, disease, and special needs.</div>
                    </div>
                </div>
            </div>

            <!-- SUB-VIEW 1: THE HARBOR POSTING BOARD -->
            <div id="postingBoardSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">📋 The Harbor Posting Board</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">Storm gear being offered that is not needed at the present time in usable condition to help ease another's journey.</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close Board</button>
                </div>

                <!-- Search by ZIP or International Mail Code -->
                <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap;">
                    <input type="text" id="gearSearchCode" class="dark-input" style="flex: 1; min-width: 200px;" placeholder="Search by ZIP code or international mail code (e.g. 17976, SW1A 1AA)..." oninput="filterStormGear()">
                    <button class="back-hub-btn" onclick="document.getElementById('gearSearchCode').value=''; filterStormGear();">Show All</button>
                </div>

                <!-- Offer Storm Gear Form -->
                <form onsubmit="event.preventDefault(); postStormGear();" style="background: rgba(15, 61, 68, 0.55); padding: 12px; border-radius: 10px; border: 1px solid rgba(94, 234, 212, 0.3); margin-bottom: 14px;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #5eead4; margin-bottom: 8px;">+ Offer Usable Storm Gear</div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 8px; margin-bottom: 8px;">
                        <input type="text" id="gearItemInput" class="dark-input" required placeholder="Storm gear item & usable condition (e.g. Weighted Blanket, Adaptive Stroller)">
                        <input type="text" id="gearPostalInput" class="dark-input" required placeholder="ZIP / Intl Mail Code">
                    </div>
                    <button type="submit" class="action-btn" style="padding: 8px; font-size: 0.82rem; margin-top: 0;">Post to Harbor Posting Board</button>
                </form>

                <!-- Gear Listings -->
                <div id="stormGearList" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="tally-card gear-listing" data-postal="17976 PA">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #5eead4;">Sensory Compression Vest (Youth Medium - Clean & Usable)</strong>
                            <span class="finalist-tag">Mail Code: 17976</span>
                        </div>
                        <p style="font-size: 0.78rem; color: #e2e8f0; margin-top: 4px;">Outgrown by our son and ready to help ease another family's journey.</p>
                        <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 4px;">Offered by @HopeWalker &bull; <a href="#" onclick="alert('Message request sent to @HopeWalker! All arrangements are coordinated directly between members.'); return false;" style="color: #5eead4;">Connect with Member</a></div>
                    </div>
                </div>
            </div>

            <!-- SUB-VIEW 2: REC TIME (TRIVIA & SENSORY-FRIENDLY COLORING) -->
            <div id="recTimeSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">🖍️ REC Time</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">Take a breather with rapid trivia, coloring, and sensory-friendly coloring pages.</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close REC Time</button>
                </div>

                <div class="rec-tabs">
                    <button class="rec-tab-btn active" id="recTabSensoryBtn" onclick="switchRecTab('sensory')">🌿 Sensory-Friendly Coloring</button>
                    <button class="rec-tab-btn" id="recTabClassicBtn" onclick="switchRecTab('classic')">🎨 Classic Coloring</button>
                    <button class="rec-tab-btn" id="recTabTriviaBtn" onclick="switchRecTab('trivia')">⏱️ 30s Caregiver Trivia</button>
                </div>

                <!-- Sensory-Friendly Coloring (Low-Stimulation Muted Tones) -->
                <div id="recSensoryPanel">
                    <div style="text-align: center; font-size: 0.8rem; color: #cbd5e1;">Calming, low-glare muted tones. Tap a soothing swatch, then tap a section below.</div>
                    <div class="swatch-row">
                        <div class="color-swatch" style="background: #64748b;" title="Soft Slate" onclick="activeCrayon='#64748b'"></div>
                        <div class="color-swatch" style="background: #5eead4;" title="Calm Seafoam" onclick="activeCrayon='#5eead4'"></div>
                        <div class="color-swatch" style="background: #7dd3fc;" title="Misty Sky" onclick="activeCrayon='#7dd3fc'"></div>
                        <div class="color-swatch" style="background: #86efac;" title="Sage Leaf" onclick="activeCrayon='#86efac'"></div>
                        <div class="color-swatch" style="background: #c4b5fd;" title="Soft Lavender" onclick="activeCrayon='#c4b5fd'"></div>
                        <div class="color-swatch" style="background: #fed7aa;" title="Warm Sand" onclick="activeCrayon='#fed7aa'"></div>
                    </div>
                    <div class="coloring-grid" id="sensoryColorGrid">
                        <div class="color-zone" onclick="paintZone(this)">🌊 Gentle Harbor Waves</div>
                        <div class="color-zone" onclick="paintZone(this)">☁️ Quiet Morning Clouds</div>
                        <div class="color-zone" onclick="paintZone(this)">🌲 Pine Forest Path</div>
                        <div class="color-zone" onclick="paintZone(this)">⚓ Safe Anchor Cove</div>
                        <div class="color-zone" onclick="paintZone(this)">🌙 Peaceful Evening Sky</div>
                        <div class="color-zone" onclick="paintZone(this)">🐚 Smooth Shoreline</div>
                    </div>
                    <div style="text-align: center; margin-top: 10px;">
                        <button class="back-hub-btn" onclick="resetColorGrid('sensoryColorGrid')">Reset Sensory Page</button>
                    </div>
                </div>

                <!-- Classic Coloring -->
                <div id="recClassicPanel" style="display: none;">
                    <div style="text-align: center; font-size: 0.8rem; color: #cbd5e1;">Bright classic colors! Tap a crayon color, then tap any section to fill it in.</div>
                    <div class="swatch-row">
                        <div class="color-swatch" style="background: #3b82f6;" onclick="activeCrayon='#3b82f6'"></div>
                        <div class="color-swatch" style="background: #22c55e;" onclick="activeCrayon='#22c55e'"></div>
                        <div class="color-swatch" style="background: #eab308;" onclick="activeCrayon='#eab308'"></div>
                        <div class="color-swatch" style="background: #ef4444;" onclick="activeCrayon='#ef4444'"></div>
                        <div class="color-swatch" style="background: #a855f7;" onclick="activeCrayon='#a855f7'"></div>
                        <div class="color-swatch" style="background: #f97316;" onclick="activeCrayon='#f97316'"></div>
                    </div>
                    <div class="coloring-grid" id="classicColorGrid">
                        <div class="color-zone" onclick="paintZone(this)">🚀 Rocket Nose Cone</div>
                        <div class="color-zone" onclick="paintZone(this)">🛸 Star Window</div>
                        <div class="color-zone" onclick="paintZone(this)">🔥 Booster Thrusters</div>
                        <div class="color-zone" onclick="paintZone(this)">🪐 Ringed Planet</div>
                    </div>
                    <div style="text-align: center; margin-top: 10px;">
                        <button class="back-hub-btn" onclick="resetColorGrid('classicColorGrid')">Reset Coloring Page</button>
                    </div>
                </div>

                <!-- 30s Caregiver Trivia -->
                <div id="recTriviaPanel" style="display: none; text-align: center;">
                    <div id="recTriviaStart">
                        <p style="font-size: 0.82rem; color: #cbd5e1; margin-bottom: 10px;">30 seconds of lighthearted caregiver & movie trivia.</p>
                        <button class="action-btn" style="max-width: 260px;" onclick="startRecTrivia()">🚀 Start 30-Second Trivia</button>
                    </div>
                    <div id="recTriviaActive" style="display: none; text-align: left;">
                        <div style="display: flex; justify-content: space-between; font-weight: 700; color: #5eead4; font-size: 0.82rem; margin-bottom: 8px;">
                            <span id="recTimerText">⏱️ Time: 30s</span>
                            <span id="recScoreText">🏆 Score: 0</span>
                        </div>
                        <div id="recQuestionText" style="font-size: 0.92rem; font-weight: 700; margin-bottom: 10px;"></div>
                        <div id="recOptionsBox" style="display: flex; flex-direction: column; gap: 6px;"></div>
                    </div>
                </div>
            </div>

            <!-- SUB-VIEW 3: KIDS CORNER -->
            <div id="kidsCornerSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">🌟 Kids Corner</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">A space where kids can connect and share their daily journey.</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close Kids Corner</button>
                </div>

                <form onsubmit="event.preventDefault(); postKidsJourney();" style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;">
                    <input type="text" id="kidNameInput" class="dark-input" style="max-width: 170px;" required placeholder="Kid's First Name / Nickname">
                    <input type="text" id="kidJourneyInput" class="dark-input" style="flex: 1; min-width: 200px;" required placeholder="Share something cool from your daily journey today...">
                    <button type="submit" class="back-hub-btn" style="padding: 8px 16px;">Share Journey ✨</button>
                </form>

                <div id="kidsCornerFeed" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="tally-card">
                        <strong style="color: #fde047;">🌟 Marcus (Age 7)</strong>
                        <p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">Tested out the Hoover Power Scrub and helped clean the living room carpet today!</p>
                    </div>
                    <div class="tally-card">
                        <strong style="color: #5eead4;">🎨 Lewie</strong>
                        <p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">Had a great afternoon listening to music and hanging out.</p>
                    </div>
                </div>
            </div>

            <!-- SUB-VIEW 4: TEACHERS' LOUNGE (CORK BOARD FOR SERIOUS SPECIALTY QUESTIONS) -->
            <div id="teachersLoungeSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">📌 Teachers' Lounge — Specialty Cork Board</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">Pin serious questions about autism, illness, disease, and special needs so experienced caregivers can share what worked for them.</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close Lounge</button>
                </div>

                <!-- Post to Cork Board Form -->
                <form onsubmit="event.preventDefault(); postCorkBoardQuestion();" style="background: rgba(15, 61, 68, 0.65); padding: 12px; border-radius: 10px; border: 1px solid rgba(253, 224, 71, 0.45);">
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label class="form-label" style="color: #fde047; font-size: 0.78rem;">Highlighted Topic / Specialty Tag (e.g., Autism, Questions About Autism, Chronic Illness, Rare Disease):</label>
                        <input type="text" id="corkTopicInput" class="dark-input" required placeholder="e.g., Questions About Autism">
                    </div>
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label class="form-label" style="font-size: 0.78rem;">I have a question about...</label>
                        <textarea id="corkDescInput" class="dark-input" rows="2" required placeholder="Describe your question (e.g., Son likes to take cold showers, or likes to shower with flip-flops on — has anyone else navigated this?)"></textarea>
                    </div>
                    <button type="submit" class="action-btn" style="background: #fde047; color: #0b2e33; padding: 8px; font-size: 0.82rem; margin-top: 0;">📌 Pin Question to Cork Board</button>
                </form>

                <!-- Cork Board Notes Feed -->
                <div class="cork-board-area" id="corkBoardFeed">
                    <div class="cork-note">
                        <span class="cork-highlight-badge">Questions About Autism</span>
                        <div class="cork-question-text">I have a question about: Son likes to take cold showers and insists on showering with flip-flops on. Has anyone else experienced sensory temperature or texture preferences like this during bath routines?</div>
                        <div class="cork-meta">
                            <span>Pinned by @AnthonyJ</span>
                            <button class="reply-btn-mini" onclick="replyToCorkNote(this)">💬 Share Lived Experience</button>
                        </div>
                    </div>
                    <div class="cork-note">
                        <span class="cork-highlight-badge">Chronic Illness & Medical Care</span>
                        <div class="cork-question-text">I have a question about: Managing overnight medication alarms without waking the rest of the household — what silent vibration setups have worked best for other caregivers?</div>
                        <div class="cork-meta">
                            <span>Pinned by @BeaconMom</span>
                            <button class="reply-btn-mini" onclick="replyToCorkNote(this)">💬 Share Lived Experience</button>
                        </div>
                    </div>
                </div>
            </div>"""

if old_rolodex_block in html:
    html = html.replace(old_rolodex_block, new_hub_block)
else:
    print("WARNING: Could not find exact rolodex block.")

# 3. Add JavaScript handlers for the 4 Sanctuary Hub sections
hub_js = """
        function openHubSection(sectionId) {
            closeHubSections();
            const el = document.getElementById(sectionId);
            if (el) {
                el.classList.add('active');
                el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }

        function closeHubSections() {
            ['postingBoardSection', 'recTimeSection', 'kidsCornerSection', 'teachersLoungeSection'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active');
            });
            if (recTriviaInterval) clearInterval(recTriviaInterval);
        }

        // Harbor Posting Board (Storm Gear + ZIP/Postal Filter)
        function postStormGear() {
            const item = document.getElementById('gearItemInput').value.trim();
            const postal = document.getElementById('gearPostalInput').value.trim();
            if (!item || !postal) return;
            const member = document.getElementById('dashMemberName').innerText || 'Member';
            const list = document.getElementById('stormGearList');
            const card = document.createElement('div');
            card.className = 'tally-card gear-listing';
            card.setAttribute('data-postal', postal.toLowerCase());
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #5eead4;">${item}</strong>
                    <span class="finalist-tag">Mail Code: ${postal}</span>
                </div>
                <p style="font-size: 0.78rem; color: #e2e8f0; margin-top: 4px;">Usable storm gear offered to help ease another's journey.</p>
                <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 4px;">Offered by ${member} &bull; <a href="#" onclick="alert('Message request sent to ${member}!'); return false;" style="color: #5eead4;">Connect with Member</a></div>
            `;
            list.prepend(card);
            document.getElementById('gearItemInput').value = '';
            document.getElementById('gearPostalInput').value = '';
        }

        function filterStormGear() {
            const query = document.getElementById('gearSearchCode').value.trim().toLowerCase();
            document.querySelectorAll('.gear-listing').forEach(card => {
                const code = (card.getAttribute('data-postal') || '').toLowerCase();
                const text = card.innerText.toLowerCase();
                card.style.display = (!query || code.includes(query) || text.includes(query)) ? 'block' : 'none';
            });
        }

        // REC Time (Sensory Coloring, Classic Coloring, Trivia)
        let activeCrayon = '#5eead4';
        let recTriviaInterval = null;
        let recScore = 0;
        let recTime = 30;
        const recQuestions = [
            { q: "If you reheat the same cup of coffee 4 times before 10 AM, how much actually gets finished?", opts: ["All of it", "Half a cup", "Zero — it becomes iced coffee", "Two pots"], ans: 2 },
            { q: "In Finding Nemo, what is the famous Sydney address?", opts: ["P. Sherman, 42 Wallaby Way", "100 Harbor Cove", "22 Reef Street", "88 Ocean Ave"], ans: 0 },
            { q: "In the movie Up, what lifts Carl's house into the sky?", opts: ["A giant kite", "Thousands of balloons", "Jet boosters", "A cloud"], ans: 1 }
        ];

        function switchRecTab(tab) {
            ['recTabSensoryBtn', 'recTabClassicBtn', 'recTabTriviaBtn'].forEach(id => document.getElementById(id).classList.remove('active'));
            ['recSensoryPanel', 'recClassicPanel', 'recTriviaPanel'].forEach(id => document.getElementById(id).style.display = 'none');
            if (recTriviaInterval) clearInterval(recTriviaInterval);

            if (tab === 'sensory') {
                document.getElementById('recTabSensoryBtn').classList.add('active');
                document.getElementById('recSensoryPanel').style.display = 'block';
                activeCrayon = '#5eead4';
            } else if (tab === 'classic') {
                document.getElementById('recTabClassicBtn').classList.add('active');
                document.getElementById('recClassicPanel').style.display = 'block';
                activeCrayon = '#3b82f6';
            } else {
                document.getElementById('recTabTriviaBtn').classList.add('active');
                document.getElementById('recTriviaPanel').style.display = 'block';
            }
        }

        function paintZone(el) {
            el.style.background = activeCrayon;
            el.style.color = '#0b2e33';
            el.style.borderStyle = 'solid';
        }

        function resetColorGrid(gridId) {
            document.querySelectorAll('#' + gridId + ' .color-zone').forEach(z => {
                z.style.background = 'rgba(255, 255, 255, 0.08)';
                z.style.color = '#e2e8f0';
                z.style.borderStyle = 'dashed';
            });
        }

        function startRecTrivia() {
            if (recTriviaInterval) clearInterval(recTriviaInterval);
            recScore = 0;
            recTime = 30;
            document.getElementById('recTriviaStart').style.display = 'none';
            document.getElementById('recTriviaActive').style.display = 'block';
            document.getElementById('recScoreText').innerText = '🏆 Score: 0';
            document.getElementById('recTimerText').innerText = '⏱️ Time: 30s';
            nextRecQuestion();
            recTriviaInterval = setInterval(() => {
                recTime--;
                document.getElementById('recTimerText').innerText = '⏱️ Time: ' + recTime + 's';
                if (recTime <= 0) {
                    clearInterval(recTriviaInterval);
                    alert("Time's up! You scored " + recScore + " points!");
                    document.getElementById('recTriviaActive').style.display = 'none';
                    document.getElementById('recTriviaStart').style.display = 'block';
                }
            }, 1000);
        }

        function nextRecQuestion() {
            const item = recQuestions[Math.floor(Math.random() * recQuestions.length)];
            document.getElementById('recQuestionText').innerText = item.q;
            const box = document.getElementById('recOptionsBox');
            box.innerHTML = '';
            item.opts.forEach((opt, i) => {
                const btn = document.createElement('button');
                btn.className = 'back-hub-btn';
                btn.style.textAlign = 'left';
                btn.innerText = opt;
                btn.onclick = () => {
                    if (i === item.ans) {
                        recScore++;
                        document.getElementById('recScoreText').innerText = '🏆 Score: ' + recScore;
                    }
                    nextRecQuestion();
                };
                box.appendChild(btn);
            });
        }

        // Kids Corner
        function postKidsJourney() {
            const kid = document.getElementById('kidNameInput').value.trim();
            const msg = document.getElementById('kidJourneyInput').value.trim();
            if (!kid || !msg) return;
            const feed = document.getElementById('kidsCornerFeed');
            const card = document.createElement('div');
            card.className = 'tally-card';
            card.innerHTML = `<strong style="color: #5eead4;">🌟 ${kid}</strong><p style="font-size: 0.82rem; color: #ffffff; margin-top: 3px;">${msg}</p>`;
            feed.prepend(card);
            document.getElementById('kidNameInput').value = '';
            document.getElementById('kidJourneyInput').value = '';
        }

        // Teachers' Lounge Cork Board
        function postCorkBoardQuestion() {
            const topic = document.getElementById('corkTopicInput').value.trim();
            const desc = document.getElementById('corkDescInput').value.trim();
            if (!topic || !desc) return;
            const member = document.getElementById('dashMemberName').innerText || 'Member';
            const feed = document.getElementById('corkBoardFeed');
            const note = document.createElement('div');
            note.className = 'cork-note';
            note.innerHTML = `
                <span class="cork-highlight-badge">${topic}</span>
                <div class="cork-question-text">I have a question about: ${desc}</div>
                <div class="cork-meta">
                    <span>Pinned by ${member}</span>
                    <button class="reply-btn-mini" onclick="replyToCorkNote(this)">💬 Share Lived Experience</button>
                </div>
            `;
            feed.prepend(note);
            document.getElementById('corkTopicInput').value = '';
            document.getElementById('corkDescInput').value = '';
        }

        function replyToCorkNote(btn) {
            const answer = prompt("Share what worked for you or your lived experience with this question:");
            if (!answer || !answer.trim()) return;
            const member = document.getElementById('dashMemberName').innerText || 'Member';
            const note = btn.closest('.cork-note');
            const replyBox = document.createElement('div');
            replyBox.className = 'chat-reply-indicator';
            replyBox.style.marginTop = '8px';
            replyBox.innerHTML = `<strong>${member} shared:</strong> ${answer.trim()}`;
            note.appendChild(replyBox);
        }
"""

html = html.replace("let currentReplyTo = null;", hub_js + "\n        let currentReplyTo = null;")

with open("templates/index.html", "w") as f:
    f.write(html)
print("SANCTUARY_HUB_UPDATED_SUCCESS")
