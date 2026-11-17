with open("templates/index.html", "r") as f:
    html = f.read()

# 1. CSS Updates: Neon Pulsating "HERE", Transparent Step 1 & Dashboard, Uniform Donor/Tour Buttons
polish_css = """
        /* Neon Pulsating "HERE" Text inside Welcome Twin Pills */
        .twin-btn-pill-rich {
            flex: 1;
            background: rgba(13, 56, 63, 0.36);
            border: 1.5px solid rgba(94, 234, 212, 0.55);
            padding: 10px 16px;
            border-radius: 50px;
            cursor: pointer;
            color: #ffffff;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            box-shadow: 0 4px 14px rgba(0,0,0,0.28);
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
        }
        .twin-btn-pill-rich:hover {
            background: rgba(15, 61, 68, 0.65);
            border-color: #5eead4;
            transform: translateY(-2px);
        }
        .pill-member-stack {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            gap: 4px;
        }
        .pill-guest-split {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        .neon-click-wrap {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            color: #cbd5e1;
            text-transform: uppercase;
        }
        .neon-here-pulse {
            color: #5eead4;
            font-weight: 900;
            margin-left: 3px;
            animation: neonPulseHere 1.4s infinite alternate;
        }
        @keyframes neonPulseHere {
            0% {
                color: #5eead4;
                text-shadow: 0 0 6px #5eead4, 0 0 14px #2dd4bf;
                opacity: 0.78;
            }
            100% {
                color: #fde047;
                text-shadow: 0 0 10px #fde047, 0 0 22px #f59e0b, 0 0 32px #fde047;
                opacity: 1;
            }
        }

        /* More Transparent Step 1 Verification Card & Dashboard Panels */
        #becomeMemberView {
            background: rgba(11, 46, 51, 0.34) !important;
            backdrop-filter: blur(6px) !important;
            border: 1.5px solid rgba(94, 234, 212, 0.55);
        }
        #becomeMemberView .mission-callout,
        #becomeMemberView .dark-input {
            background: rgba(11, 46, 51, 0.38) !important;
        }
        .dashboard-screen {
            background: rgba(11, 46, 51, 0.38) !important;
            backdrop-filter: blur(6px) !important;
        }
        .dashboard-screen .dash-panel,
        .dashboard-screen .member-profile-bar {
            background: rgba(11, 46, 51, 0.46) !important;
            backdrop-filter: blur(8px);
        }
        .dashboard-screen .chat-msg {
            background: rgba(15, 61, 68, 0.55) !important;
        }

        /* Uniform Inviting Donor & Tour Buttons */
        .uniform-portal-btn-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 14px;
        }
        .uniform-portal-btn {
            flex: 1;
            min-width: 210px;
            background: linear-gradient(135deg, rgba(13, 148, 136, 0.65), rgba(3, 105, 161, 0.72));
            border: 1.5px solid #5eead4;
            color: #ffffff;
            font-weight: 700;
            font-size: 0.82rem;
            padding: 10px 14px;
            border-radius: 50px;
            cursor: pointer;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            transition: all 0.22s ease;
        }
        .uniform-portal-btn:hover {
            transform: translateY(-2px);
            border-color: #fde047;
            box-shadow: 0 6px 18px rgba(94, 234, 212, 0.35);
        }
        .contribution-impact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 8px;
            margin-top: 10px;
        }
        .impact-item-card {
            background: rgba(15, 61, 68, 0.58);
            border: 1px solid rgba(94, 234, 212, 0.35);
            border-radius: 10px;
            padding: 9px 11px;
            font-size: 0.76rem;
            color: #e2e8f0;
        }
"""

html = html.replace("</style>", polish_css + "\n    </style>")

# 2. Color-Code the Floating Terms Behind Step 1 Email Verification
old_join_bg = """    <div id="joinBg" class="join-bg">
        <div class="floating-term" style="left: 4%; animation-duration: 12s; animation-delay: 0s;">MD & Specialist Care</div>
        <div class="floating-term" style="left: 22%; animation-duration: 10s; animation-delay: 2s;">DMD Warrior</div>
        <div class="floating-term" style="left: 42%; animation-duration: 11s; animation-delay: 1s;">Pediatric Caregiver</div>
        <div class="floating-term" style="left: 62%; animation-duration: 13s; animation-delay: 3.5s;">Autism Support</div>
        <div class="floating-term" style="left: 78%; animation-duration: 12s; animation-delay: 1.5s;">Storm Survivor</div>
    </div>"""

new_join_bg = """    <div id="joinBg" class="join-bg">
        <div class="floating-term" style="left: 4%; color: #38bdf8; text-shadow: 0 0 12px rgba(56,189,248,0.8); animation-duration: 12s; animation-delay: 0s;">🩺 MD &amp; Specialist Care</div>
        <div class="floating-term" style="left: 20%; color: #fb7185; text-shadow: 0 0 12px rgba(251,113,133,0.85); animation-duration: 10s; animation-delay: 2s;">🎗️ DMD Warrior</div>
        <div class="floating-term" style="left: 38%; color: #fde047; text-shadow: 0 0 12px rgba(253,224,71,0.8); animation-duration: 11s; animation-delay: 1s;">🧸 Pediatric Caregiver</div>
        <div class="floating-term" style="left: 58%; color: #a78bfa; text-shadow: 0 0 12px rgba(167,139,250,0.85); animation-duration: 13s; animation-delay: 3.5s;">🧩 Autism Support</div>
        <div class="floating-term" style="left: 76%; color: #34d399; text-shadow: 0 0 12px rgba(52,211,153,0.8); animation-duration: 12s; animation-delay: 1.5s;">⚓ Storm Survivor</div>
        <div class="floating-term" style="left: 14%; color: #f472b6; text-shadow: 0 0 12px rgba(244,114,182,0.8); animation-duration: 14s; animation-delay: 4s;">💜 Rare Disease Family</div>
        <div class="floating-term" style="left: 66%; color: #fbbf24; text-shadow: 0 0 12px rgba(251,191,36,0.8); animation-duration: 11.5s; animation-delay: 2.5s;">🤝 Lived Experience</div>
    </div>"""

if old_join_bg in html:
    html = html.replace(old_join_bg, new_join_bg)

# 3. Fix any broken mosaic tile image on Welcome Screen with automatic fallback
html = html.replace(
    """<img src="{{ url_for('static', filename='images/mosaic/' + img) }}" class="mosaic-tile" alt="Mosaic photo">""",
    """<img src="{{ url_for('static', filename='images/mosaic/' + img) }}" onerror="this.onerror=null; this.src='{{ url_for('static', filename='images/community_gathering.jpg') }}';" class="mosaic-tile" alt="Mosaic photo">"""
)

# 4. Update Twin Buttons on Welcome Page with Neon Pulsating "HERE"
old_twin_buttons = """            <div class="twin-buttons">
                <button class="twin-btn-pill" onclick="switchView('becomeMemberView')"><span>🤝</span> Become a Member</button>
                <button class="twin-btn-pill" onclick="switchView('donorVisitorView')"><span>❤️</span> Welcome Guests & Contributors</button>
            </div>"""

new_twin_buttons = """            <div class="twin-buttons">
                <button class="twin-btn-pill-rich pill-member-stack" onclick="switchView('becomeMemberView')">
                    <span style="font-size: 0.8rem; font-weight: 800; letter-spacing: 0.02em;">🤝 Become a Member</span>
                    <span class="neon-click-wrap">CLICK <span class="neon-here-pulse">HERE</span></span>
                </button>
                <button class="twin-btn-pill-rich pill-guest-split" onclick="switchView('donorVisitorView')">
                    <span style="font-size: 0.78rem; font-weight: 800; text-align: left; line-height: 1.2;">❤️ Guests &amp;<br>Contributors</span>
                    <span class="neon-click-wrap">CLICK <span class="neon-here-pulse">HERE</span></span>
                </button>
            </div>"""

if old_twin_buttons in html:
    html = html.replace(old_twin_buttons, new_twin_buttons)

# 5. Update Dashboard Header to "⚓ Caregiver Dashboard"
html = html.replace("⚓ Caregiver Sanctuary Dashboard", "⚓ Caregiver Dashboard")

# 6. Drop the "Paste Pic/Media Link" button in Community Chat (keep only Add Attachment)
old_attach_bar = """                        <!-- Attachment Bar -->
                        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <label for="chatFileUpload" class="attach-btn-mini" style="cursor: pointer;">📎 Add Attachment</label>
                                <input type="file" id="chatFileUpload" accept="image/*,video/*" style="display: none;" onchange="handleAttachmentSelected(this)">
                                <button type="button" class="attach-btn-mini" onclick="togglePasteMediaBox()">🔗 Paste Pic/Media Link</button>
                            </div>
                            <span id="attachmentStatusLabel" style="font-size: 0.7rem; color: #fde047;"></span>
                        </div>

                        <div id="pasteMediaBox" style="display: none; margin-bottom: 6px;">
                            <input type="url" id="chatMediaUrlInput" class="dark-input" style="font-size: 0.78rem; padding: 6px 10px;" placeholder="Paste image or funny pic URL here..." oninput="handleMediaUrlTyped(this)">
                        </div>"""

new_attach_bar = """                        <!-- Attachment Bar -->
                        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <label for="chatFileUpload" class="attach-btn-mini" style="cursor: pointer;">📎 Add Attachment</label>
                                <input type="file" id="chatFileUpload" accept="image/*,video/*" style="display: none;" onchange="handleAttachmentSelected(this)">
                            </div>
                            <span id="attachmentStatusLabel" style="font-size: 0.7rem; color: #fde047;"></span>
                        </div>"""

if old_attach_bar in html:
    html = html.replace(old_attach_bar, new_attach_bar)

# Clean up reference to chatMediaUrlInput in postChatSubmission()
html = html.replace("document.getElementById('chatMediaUrlInput').value = '';", "")

# 7. Make Top-Right "Reason Behind the Mission" Video Active & Reliable
old_mission_video = """            <div class="video-container">
                <video controls autoplay playsinline>
                    <source src="{{ url_for('static', filename='videos/mission_intro.mp4') }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>"""

new_mission_video = """            <div class="video-container" style="background: radial-gradient(circle at center, #0f3d44, #072226);">
                <video id="missionIntroPlayer" controls playsinline preload="metadata" poster="{{ url_for('static', filename='images/community_gathering.jpg') }}">
                    <source src="{{ url_for('static', filename='videos/mission_intro.mp4') }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>"""

if old_mission_video in html:
    html = html.replace(old_mission_video, new_mission_video)

# 8. Update Guest, Donor & Sponsor Portal + Tour View with Uniform Buttons, Contribution Impact List & Tour Video Preview
old_donor_and_tour = """        <!-- 3. DONOR / VISITOR & SPONSOR PORTAL VIEW -->
        <div id="donorVisitorView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">Guest, Donor & Sponsor Portal</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>
            <div class="mission-callout" style="border-left-color: #f59e0b;">
                <strong>Welcome!</strong> Sponsorships, donations, and blessings are very much appreciated, needed, and usable. Thank you for supporting our mission.
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
                <button class="action-btn" style="flex: 1;" onclick="alert('Thank you for your interest! Somebody from support@shareyourwalk.com will reach out to you via email within 1 to 2 business days.')">🤝 Are you interested in contributing?</button>
                <button class="twin-btn-pill" style="flex: 1; justify-content: center; margin-top: 8px;" onclick="switchView('tourView')">🧭 Take a Tour of The Harbor</button>
            </div>
        </div>

        <!-- 4. TOUR VIEW -->
        <div id="tourView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">Explore The Harbor & Mission Tour</div>
                <button class="close-btn" onclick="switchView('donorVisitorView')">&times;</button>
            </div>
            <div style="font-size: 0.88rem; line-height: 1.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 10px;">
                <div style="background: rgba(15, 61, 68, 0.4); padding: 12px; border-radius: 8px;">
                    <strong style="color: #5eead4;">1. The Caregiver Sanctuary</strong>
                    <p style="margin-top: 3px;">A safe, verified online hub where caregivers find peers who truly understand the daily triumphs and hurdles.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.4); padding: 12px; border-radius: 8px;">
                    <strong style="color: #5eead4;">2. Lived & Learned Experience Sharing</strong>
                    <p style="margin-top: 3px;">Members connect through shared walks, real-time community boards, and mutual encouragement without judgment.</p>
                </div>
            </div>
            <button class="action-btn" style="margin-top: 16px;" onclick="switchView('donorVisitorView')">Back to Donor Portal</button>
        </div>"""

new_donor_and_tour = """        <!-- 3. DONOR / VISITOR & SPONSOR PORTAL VIEW -->
        <div id="donorVisitorView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">❤️ Guests, Donors &amp; Sponsors Portal</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>
            <div class="mission-callout" style="border-left-color: #fde047;">
                <strong>Welcome!</strong> Sponsorships, donations, and blessings are very much appreciated, needed, and directly usable. Every single contribution lifts a real caregiver family.
            </div>

            <!-- What Even the Smallest Contribution Can Do -->
            <div style="font-size: 0.85rem; font-weight: 800; color: #5eead4; margin-bottom: 4px;">✨ What Even the Smallest Contribution Can Do:</div>
            <div class="contribution-impact-grid">
                <div class="impact-item-card">
                    <strong style="color: #fde047;">🎁 Digital Activity Gift Cards</strong>
                    <p style="margin-top: 3px;">Funds digital gift cards for Rec Area trivia winners, family movie nights, and weekly photo spotlights.</p>
                </div>
                <div class="impact-item-card">
                    <strong style="color: #38bdf8;">☕ Caregiver Respite &amp; Coffee Cards</strong>
                    <p style="margin-top: 3px;">Sends a $5–$15 coffee or meal e-card to a parent pulling an overnight hospital or therapy shift.</p>
                </div>
                <div class="impact-item-card">
                    <strong style="color: #f472b6;">🧩 Sensory &amp; Comfort Supplies</strong>
                    <p style="margin-top: 3px;">Helps ship weighted lap pads, headphones, and usable gear listed on our Pass It On board.</p>
                </div>
                <div class="impact-item-card">
                    <strong style="color: #4ade80;">⚓ Keeping The Harbor Free</strong>
                    <p style="margin-top: 3px;">Covers hosting, domain, and security tools so caregivers never pay a dime to belong.</p>
                </div>
            </div>

            <!-- Uniform Inviting Buttons -->
            <div class="uniform-portal-btn-row">
                <button class="uniform-portal-btn" onclick="alert('Thank you for your heart to help! Somebody from support@shareyourwalk.com will reach out within 1 to 2 business days.')">
                    <span>🤝</span> Are You Interested in Contributing?
                </button>
                <button class="uniform-portal-btn" onclick="switchView('tourView')">
                    <span>🧭</span> Take a Tour of The Harbor
                </button>
            </div>
        </div>

        <!-- 4. TOUR VIEW (WITH PLATFORM WALKTHROUGH VIDEO) -->
        <div id="tourView" class="view-screen" style="max-width: 760px;">
            <div class="screen-header">
                <div class="screen-title">🧭 Explore The Harbor — Platform Tour</div>
                <button class="close-btn" onclick="switchView('donorVisitorView')">&times;</button>
            </div>

            <div class="video-container" style="background: radial-gradient(circle at center, #0f3d44, #072226); margin-bottom: 12px;">
                <video id="harborTourPlayer" controls playsinline preload="metadata" poster="{{ url_for('static', filename='images/community_gathering.jpg') }}">
                    <source src="{{ url_for('static', filename='videos/harbor_tour.mp4') }}" type="video/mp4">
                    <source src="{{ url_for('static', filename='videos/mission_intro.mp4') }}" type="video/mp4">
                </video>
            </div>

            <div style="font-size: 0.85rem; line-height: 1.5; color: #cbd5e1; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px;">
                <div style="background: rgba(15, 61, 68, 0.55); padding: 11px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.3);">
                    <strong style="color: #5eead4;">💬 Live Community Chat</strong>
                    <p style="margin-top: 3px;">Real-time encouragement, photo sharing, and threaded replies from caregivers who truly understand.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.55); padding: 11px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.3);">
                    <strong style="color: #fde047;">🧱 The Wall of Seriousness</strong>
                    <p style="margin-top: 3px;">Priority-ranked serious caregiving questions answered with directness and lived wisdom.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.55); padding: 11px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.3);">
                    <strong style="color: #38bdf8;">🌐 Gathering Place &amp; Rec Area</strong>
                    <p style="margin-top: 3px;">A dedicated 21-and-under space plus daily photo voting, funny clips, and 30-second trivia.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.55); padding: 11px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.3);">
                    <strong style="color: #fcd34d;">🪵 Pass It On &amp; Resources</strong>
                    <p style="margin-top: 3px;">Pay forward usable gear by mail code and access direct links to SSA, MDA, and support foundations.</p>
                </div>
            </div>

            <div class="uniform-portal-btn-row">
                <button class="uniform-portal-btn" onclick="switchView('becomeMemberView')">🤝 Become a Member</button>
                <button class="uniform-portal-btn" onclick="switchView('donorVisitorView')">← Back to Guests &amp; Contributors</button>
            </div>
        </div>"""

if old_donor_and_tour in html:
    html = html.replace(old_donor_and_tour, new_donor_and_tour)

# 9. Add a compact Tour Video Preview toggle inside Become a Member so prospective members can watch it right on the sign-up screen too
old_member_callout_end = """            <div class="mission-callout" id="joinCallout">
                Treat others in this community as you want to be treated. Respect goes a long way. Remember, you struggled too and you made it.
            </div>"""

new_member_callout_with_tour = """            <div class="mission-callout" id="joinCallout">
                Treat others in this community as you want to be treated. Respect goes a long way. Remember, you struggled too and you made it.
                <div style="margin-top: 8px;">
                    <button type="button" class="back-hub-btn" onclick="const box = document.getElementById('signupTourVideoBox'); box.style.display = box.style.display === 'none' ? 'block' : 'none';">🎬 Watch Quick Tour of The Harbor</button>
                </div>
                <div id="signupTourVideoBox" style="display: none; margin-top: 10px;">
                    <div class="video-container" style="margin-bottom: 0;">
                        <video controls playsinline preload="metadata" poster="{{ url_for('static', filename='images/community_gathering.jpg') }}">
                            <source src="{{ url_for('static', filename='videos/harbor_tour.mp4') }}" type="video/mp4">
                            <source src="{{ url_for('static', filename='videos/mission_intro.mp4') }}" type="video/mp4">
                        </video>
                    </div>
                </div>
            </div>"""

if old_member_callout_end in html:
    html = html.replace(old_member_callout_end, new_member_callout_with_tour)

# 10. Auto-play mission video cleanly when opening missionVideoView
html = html.replace(
    "document.getElementById(viewId).classList.add('active');",
    """document.getElementById(viewId).classList.add('active');
                if (viewId === 'missionVideoView') {
                    const mv = document.getElementById('missionIntroPlayer');
                    if (mv) { mv.currentTime = 0; mv.play().catch(() => {}); }
                }"""
)

with open("templates/index.html", "w") as f:
    f.write(html)
print("HARBOR_POLISH_APPLIED_SUCCESS")
