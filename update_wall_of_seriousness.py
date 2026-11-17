with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Add CSS for The Wall of Seriousness dedicated page, slider, paper-pin animation & hover tooltip
wall_css = """
        /* THE WALL OF SERIOUSNESS (DEDICATED PAGE) */
        .wall-seriousness-screen {
            max-width: 1000px;
            background: linear-gradient(145deg, rgba(24, 22, 54, 0.94), rgba(15, 23, 42, 0.96));
            border: 2px solid #818cf8;
        }
        .highlighted-topic-box {
            background: rgba(253, 224, 71, 0.14);
            border: 2px solid #fde047;
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 12px;
            box-shadow: 0 0 15px rgba(253, 224, 71, 0.18);
        }
        .highlighted-topic-input {
            width: 100%; background: rgba(15, 23, 42, 0.85); border: 1.5px solid #fde047;
            color: #fde047; font-weight: 800; font-size: 0.95rem; padding: 8px 12px; border-radius: 8px; outline: none;
        }
        .highlighted-topic-input::placeholder { color: rgba(253, 224, 71, 0.55); font-weight: 600; }

        .care-checkbox-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin-bottom: 12px;
        }
        .care-check-pill {
            display: flex; align-items: center; gap: 8px; background: rgba(49, 46, 129, 0.5);
            border: 1px solid rgba(129, 140, 248, 0.45); padding: 8px 10px; border-radius: 8px;
            font-size: 0.8rem; font-weight: 600; color: #e0e7ff; cursor: pointer; user-select: none;
        }
        .care-check-pill input { accent-color: #fde047; width: 16px; height: 16px; cursor: pointer; }

        .priority-slider-box {
            background: rgba(30, 27, 75, 0.7); border: 1px solid rgba(129, 140, 248, 0.4);
            border-radius: 10px; padding: 10px 14px; margin-bottom: 12px;
        }
        .priority-slider { width: 100%; accent-color: #f43f5e; cursor: pointer; margin-top: 6px; }

        /* Physical Cork/Stone Wall & Pinned Papers */
        .serious-wall-surface {
            background: radial-gradient(circle at top, rgba(71, 51, 35, 0.55), rgba(38, 27, 18, 0.78));
            border: 2px solid rgba(217, 155, 82, 0.6);
            border-radius: 14px; padding: 16px; margin-top: 16px;
            box-shadow: inset 0 4px 20px rgba(0,0,0,0.65);
        }
        .pinned-papers-grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin-top: 12px;
        }
        .pinned-paper-note {
            position: relative;
            background: #fef9c3; color: #1e293b;
            border-radius: 4px 4px 14px 4px;
            padding: 14px 14px 12px 14px;
            box-shadow: 3px 6px 14px rgba(0,0,0,0.45);
            border-top: 6px solid #eab308;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }
        .pinned-paper-note:hover {
            transform: translateY(-4px) rotate(-0.5deg);
            box-shadow: 5px 10px 22px rgba(0,0,0,0.65);
            z-index: 15;
        }
        /* Hover Floating Topic Tag */
        .paper-hover-topic {
            position: absolute; top: -14px; right: 10px;
            background: #0f172a; color: #fde047; border: 1.5px solid #fde047;
            font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 50px;
            text-transform: uppercase; letter-spacing: 0.04em;
            opacity: 0; transform: translateY(4px); pointer-events: none;
            transition: opacity 0.18s ease, transform 0.18s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .pinned-paper-note:hover .paper-hover-topic {
            opacity: 1; transform: translateY(0);
        }

        /* Paper Attaching to Wall Animation */
        @keyframes pinPaperToWall {
            0% { opacity: 0; transform: scale(1.28) translateY(-35px) rotate(6deg); box-shadow: 0 25px 40px rgba(0,0,0,0.75); }
            65% { opacity: 1; transform: scale(0.97) translateY(3px) rotate(-1deg); }
            100% { opacity: 1; transform: scale(1) translateY(0) rotate(0deg); }
        }
        .paper-just-pinned {
            animation: pinPaperToWall 0.65s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
        .paper-pin-dot {
            width: 12px; height: 12px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #f87171, #991b1b);
            box-shadow: 0 2px 4px rgba(0,0,0,0.5); position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
        }
"""

html = html.replace("</style>", wall_css + "\n    </style>")

# 2. Update the FYI Serious Question Posting button to open the dedicated Wall of Seriousness page
html = html.replace(
    """onclick="openHubSection('seriousQuestionsSection')" """,
    """onclick="switchView('wallOfSeriousnessView')" """
).replace(
    """onclick="openHubSection('seriousQuestionsSection')">""",
    """onclick="switchView('wallOfSeriousnessView')">"""
)

# 3. Remove the old inline seriousQuestionsSection sub-view inside communityDashboardView
old_inline_serious = html[html.find("<!-- EXPANDABLE SUB-VIEW 1: SERIOUS QUESTION POSTING"):html.find("<!-- EXPANDABLE SUB-VIEW 2: KIDS CORNER")]
if old_inline_serious:
    html = html.replace(old_inline_serious, "")

# 4. Insert the dedicated full-page "The Wall of Seriousness" view screen right after communityDashboardView
wall_page_html = """
        <!-- 1C. DEDICATED PAGE: THE WALL OF SERIOUSNESS -->
        <div id="wallOfSeriousnessView" class="view-screen wall-seriousness-screen">
            <div class="screen-header" style="border-bottom-color: rgba(129, 140, 248, 0.35);">
                <div>
                    <div class="screen-title" style="color: #fde047; font-size: 1.4rem;">🧱 The Wall of Seriousness</div>
                    <div style="font-size: 0.8rem; color: #c7d2fe; font-weight: 600;">Real questions answered with directness.</div>
                </div>
                <button class="back-hub-btn" style="border-color: #fde047; color: #fde047;" onclick="switchView('communityDashboardView')">← Back to Sanctuary</button>
            </div>

            <!-- Question Composer Form -->
            <form onsubmit="event.preventDefault(); pinPaperToSeriousWall();" style="background: rgba(30, 27, 75, 0.72); border: 1px solid rgba(129, 140, 248, 0.45); border-radius: 14px; padding: 16px;">
                <!-- Highlighted Topic Field -->
                <div class="highlighted-topic-box">
                    <label class="form-label" style="color: #fde047; font-size: 0.82rem; font-weight: 800; margin-bottom: 6px;">
                        ✨ Highlighted Topic — What is this question about? (Type e.g., Cancer, Autism, Autistic Meltdown, DMD):
                    </label>
                    <input type="text" id="wallTopicInput" class="highlighted-topic-input" required placeholder="Type topic here (e.g., Autism, Cancer, Autistic Meltdown)...">
                </div>

                <!-- Care Group Checkboxes -->
                <div style="font-size: 0.78rem; font-weight: 700; color: #e0e7ff; margin-bottom: 6px;">Who does this involve? (Select all that apply):</div>
                <div class="care-checkbox-grid" id="wallCareCheckboxes">
                    <label class="care-check-pill"><input type="checkbox" value="Elder Care"> 👴 Elder Care</label>
                    <label class="care-check-pill"><input type="checkbox" value="Pediatric Care"> 🧸 Pediatric Care</label>
                    <label class="care-check-pill"><input type="checkbox" value="Family Member"> 🏠 Family Member</label>
                    <label class="care-check-pill"><input type="checkbox" value="Non-Family Member"> 🤝 Non-Family Member</label>
                </div>

                <!-- Level of Importance Slider (1 to 10) -->
                <div class="priority-slider-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; font-weight: 700;">
                        <span style="color: #e0e7ff;">🚨 Level of Importance (Helps members reply faster):</span>
                        <span id="prioritySliderReadout" style="color: #fbbf24; font-size: 0.88rem; font-weight: 800;">5 / 10 — Moderate Priority</span>
                    </div>
                    <input type="range" id="wallPrioritySlider" class="priority-slider" min="1" max="10" value="5" oninput="updatePriorityReadout(this.value)">
                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8; margin-top: 2px;">
                        <span>1 = Low Priority</span>
                        <span>5 = Moderate</span>
                        <span>10 = Highest Urgency</span>
                    </div>
                </div>

                <!-- Serious Question Write-Up -->
                <div class="form-group" style="margin-bottom: 10px;">
                    <label class="form-label" style="font-size: 0.82rem; color: #ffffff;">Write Your Serious Question:</label>
                    <textarea id="wallQuestionText" class="dark-input" rows="3" required placeholder="Ask directly and clearly so members who have been there can give real answers..."></textarea>
                </div>

                <button type="submit" class="action-btn" style="background: #fde047; color: #0b2e33; font-weight: 800; font-size: 0.95rem; margin-top: 0;">
                    📌 Post It to The Wall
                </button>
            </form>

            <!-- The Pinned Notes Wall -->
            <div class="serious-wall-surface">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 8px;">
                    <div style="font-size: 0.95rem; font-weight: 800; color: #fde68a;">📌 Pinned Questions Wall (Hover over any paper to see its topic)</div>
                    <input type="text" id="wallTopicFilterInput" class="dark-input" style="max-width: 240px; padding: 6px 10px; font-size: 0.78rem;" placeholder="Filter wall (e.g., Autism, Cancer)..." oninput="filterWallPapers()">
                </div>

                <div class="pinned-papers-grid" id="pinnedPapersWallGrid">
                    <!-- Sample Paper 1: Autism -->
                    <div class="pinned-paper-note wall-paper-item" data-topic="autism">
                        <div class="paper-pin-dot"></div>
                        <div class="paper-hover-topic">Autism</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 6px; font-size: 0.7rem; font-weight: 800; color: #991b1b;">
                            <span>Priority: 8/10</span>
                            <span>Pediatric Care &bull; Family Member</span>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; line-height: 1.4;">
                            Son insists on taking cold showers and wearing flip-flops every time. Looking for direct advice from parents who dealt with sensory shower routines.
                        </div>
                        <div style="margin-top: 10px; padding-top: 6px; border-top: 1px dashed rgba(15, 23, 42, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #334155;">
                            <span>Posted by Anthony</span>
                            <button type="button" style="background: #0f172a; color: #fde047; border: none; padding: 4px 10px; border-radius: 50px; font-weight: 700; font-size: 0.7rem; cursor: pointer;" onclick="replyToWallPaper(this)">💬 Direct Answer</button>
                        </div>
                    </div>

                    <!-- Sample Paper 2: Autistic Meltdown -->
                    <div class="pinned-paper-note wall-paper-item" data-topic="autistic meltdown" style="background: #fef08a; border-top-color: #f43f5e;">
                        <div class="paper-pin-dot"></div>
                        <div class="paper-hover-topic">Autistic Meltdown</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 6px; font-size: 0.7rem; font-weight: 800; color: #be123c;">
                            <span>Priority: 10/10 (Urgent)</span>
                            <span>Pediatric Care &bull; Family Member</span>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; line-height: 1.4;">
                            In public when a sudden loud siren triggers a full meltdown — what is your immediate 60-second de-escalation step that actually works?
                        </div>
                        <div style="margin-top: 10px; padding-top: 6px; border-top: 1px dashed rgba(15, 23, 42, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #334155;">
                            <span>Posted by HopeWalker</span>
                            <button type="button" style="background: #0f172a; color: #fde047; border: none; padding: 4px 10px; border-radius: 50px; font-weight: 700; font-size: 0.7rem; cursor: pointer;" onclick="replyToWallPaper(this)">💬 Direct Answer</button>
                        </div>
                    </div>

                    <!-- Sample Paper 3: Cancer -->
                    <div class="pinned-paper-note wall-paper-item" data-topic="cancer" style="background: #e0f2fe; border-top-color: #0284c7;">
                        <div class="paper-pin-dot"></div>
                        <div class="paper-hover-topic">Cancer</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 6px; font-size: 0.7rem; font-weight: 800; color: #0369a1;">
                            <span>Priority: 9/10</span>
                            <span>Elder Care &bull; Family Member</span>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; line-height: 1.4;">
                            During chemo weeks when metallic taste ruins every meal, what specific cold foods or drinks did your loved one actually keep down?
                        </div>
                        <div style="margin-top: 10px; padding-top: 6px; border-top: 1px dashed rgba(15, 23, 42, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #334155;">
                            <span>Posted by CaregiverDan</span>
                            <button type="button" style="background: #0f172a; color: #fde047; border: none; padding: 4px 10px; border-radius: 50px; font-weight: 700; font-size: 0.7rem; cursor: pointer;" onclick="replyToWallPaper(this)">💬 Direct Answer</button>
                        </div>
                    </div>
                </div>

                <!-- Bottom Highlighted Category Box (e.g., Question About Autism) -->
                <div style="margin-top: 16px; background: rgba(15, 23, 42, 0.88); border: 1.5px solid #fde047; border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="background: #fde047; color: #0f172a; font-weight: 800; font-size: 0.74rem; padding: 3px 10px; border-radius: 6px; text-transform: uppercase;">Question About Autism</span>
                        <span style="font-size: 0.78rem; color: #e2e8f0; margin-left: 8px;">Quick-jump filter for active Autism & sensory threads on the wall.</span>
                    </div>
                    <button type="button" class="back-hub-btn" style="border-color: #fde047; color: #fde047;" onclick="document.getElementById('wallTopicFilterInput').value='Autism'; filterWallPapers();">Show Autism Notes</button>
                </div>
            </div>
        </div>
"""

html = html.replace("<!-- 2. BECOME A MEMBER VIEW -->", wall_page_html + "\n        <!-- 2. BECOME A MEMBER VIEW -->")

# 5. Update switchView array to include wallOfSeriousnessView & add JS functions for The Wall of Seriousness
html = html.replace(
    "['mainGatewayView', 'memberLoginView', 'communityDashboardView', 'becomeMemberView', 'donorVisitorView', 'tourView', 'missionVideoView']",
    "['mainGatewayView', 'memberLoginView', 'communityDashboardView', 'wallOfSeriousnessView', 'becomeMemberView', 'donorVisitorView', 'tourView', 'missionVideoView']"
)

wall_js = """
        /* THE WALL OF SERIOUSNESS LOGIC */
        function updatePriorityReadout(val) {
            const readout = document.getElementById('prioritySliderReadout');
            const num = parseInt(val, 10);
            if (num >= 8) {
                readout.style.color = '#fb7185';
                readout.innerText = `${num} / 10 — Highest Priority (Fast Reply Needed)`;
            } else if (num >= 4) {
                readout.style.color = '#fbbf24';
                readout.innerText = `${num} / 10 — Moderate Priority`;
            } else {
                readout.style.color = '#5eead4';
                readout.innerText = `${num} / 10 — Low Priority`;
            }
        }

        function pinPaperToSeriousWall() {
            const topic = document.getElementById('wallTopicInput').value.trim();
            const question = document.getElementById('wallQuestionText').value.trim();
            const priority = document.getElementById('wallPrioritySlider').value;
            if (!topic || !question) return;

            const checkedGroups = [];
            document.querySelectorAll('#wallCareCheckboxes input:checked').forEach(cb => checkedGroups.push(cb.value));
            const groupLabel = checkedGroups.length > 0 ? checkedGroups.join(' • ') : 'General Care';
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';

            const grid = document.getElementById('pinnedPapersWallGrid');
            const paper = document.createElement('div');
            paper.className = 'pinned-paper-note wall-paper-item paper-just-pinned';
            paper.setAttribute('data-topic', topic.toLowerCase());
            if (parseInt(priority, 10) >= 8) {
                paper.style.borderTopColor = '#f43f5e';
            }

            paper.innerHTML = `
                <div class="paper-pin-dot"></div>
                <div class="paper-hover-topic">${topic}</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 6px; font-size: 0.7rem; font-weight: 800; color: #991b1b;">
                    <span>Priority: ${priority}/10</span>
                    <span>${groupLabel}</span>
                </div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; line-height: 1.4;">
                    ${question}
                </div>
                <div style="margin-top: 10px; padding-top: 6px; border-top: 1px dashed rgba(15, 23, 42, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #334155;">
                    <span>Posted by ${member}</span>
                    <button type="button" style="background: #0f172a; color: #fde047; border: none; padding: 4px 10px; border-radius: 50px; font-weight: 700; font-size: 0.7rem; cursor: pointer;" onclick="replyToWallPaper(this)">💬 Direct Answer</button>
                </div>
            `;

            grid.prepend(paper);
            paper.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Reset inputs
            document.getElementById('wallTopicInput').value = '';
            document.getElementById('wallQuestionText').value = '';
            document.querySelectorAll('#wallCareCheckboxes input').forEach(cb => cb.checked = false);
            document.getElementById('wallPrioritySlider').value = 5;
            updatePriorityReadout(5);
        }

        function filterWallPapers() {
            const q = document.getElementById('wallTopicFilterInput').value.trim().toLowerCase();
            document.querySelectorAll('.wall-paper-item').forEach(paper => {
                const topic = (paper.getAttribute('data-topic') || '').toLowerCase();
                const text = paper.innerText.toLowerCase();
                paper.style.display = (!q || topic.includes(q) || text.includes(q)) ? 'block' : 'none';
            });
        }

        function replyToWallPaper(btn) {
            const ans = prompt("Write a direct, real answer from your experience:");
            if (!ans || !ans.trim()) return;
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';
            const paper = btn.closest('.pinned-paper-note');
            const replyDiv = document.createElement('div');
            replyDiv.style.marginTop = '8px';
            replyDiv.style.padding = '6px 8px';
            replyDiv.style.background = 'rgba(15, 23, 42, 0.1)';
            replyDiv.style.borderLeft = '3px solid #0f172a';
            replyDiv.style.borderRadius = '4px';
            replyDiv.style.fontSize = '0.76rem';
            replyDiv.style.color = '#0f172a';
            replyDiv.innerHTML = `<strong>${member}:</strong> ${ans.trim()}`;
            paper.appendChild(replyDiv);
        }
"""

html = html.replace("/* Show / Hide Password Toggle */", wall_js + "\n        /* Show / Hide Password Toggle */")

with open("templates/index.html", "w") as f:
    f.write(html)
print("WALL_OF_SERIOUSNESS_DEPLOYED_SUCCESS")
