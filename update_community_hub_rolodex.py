with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Add horizontal Rolodex wheel CSS for the Community Hub buttons
rolodex_css = """
        /* Horizontal Sideways-Sliding Community Hub Rolodex */
        .community-hub-rolodex {
            display: flex;
            flex-direction: row;
            gap: 10px;
            overflow-x: auto;
            padding: 6px 2px 12px 2px;
            scroll-behavior: smooth;
            scroll-snap-type: x mandatory;
        }
        .community-hub-rolodex::-webkit-scrollbar { height: 6px; }
        .community-hub-rolodex::-webkit-scrollbar-thumb {
            background: rgba(94, 234, 212, 0.45);
            border-radius: 4px;
        }
        .community-hub-rolodex .fyi-btn {
            min-width: 215px;
            max-width: 235px;
            flex-shrink: 0;
            scroll-snap-align: start;
            flex-direction: column;
            align-items: flex-start;
            justify-content: space-between;
            padding: 12px 14px;
            min-height: 96px;
        }
        .community-hub-rolodex .fyi-btn:hover {
            transform: translateY(-3px);
        }
"""

html = html.replace("</style>", rolodex_css + "\n    </style>")

# 2. Replace the right-hand column ("For Your Info" + 10:00 PM Reveal) with "Community Hub" horizontal Rolodex
old_right_column = """                <!-- RIGHT COLUMN: For Your Info (FYI) Strip + Click to View Daily Vote + 10 PM Reveal -->
                <div class="dash-panel">
                    <div>
                        <div class="panel-heading">
                            <span>📌 For Your Info (FYI)</span>
                        </div>

                        <!-- Skinny, Comfortable Navigation Buttons -->
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
                    </div>
                </div>"""

new_right_column = """                <!-- RIGHT COLUMN: Community Hub (Horizontal Sideways-Sliding Rolodex) -->
                <div class="dash-panel" style="overflow: hidden;">
                    <div>
                        <div class="panel-heading">
                            <span>⚓ Community Hub</span>
                            <span style="font-size: 0.7rem; color: #cbd5e1;">Swipe Sideways →</span>
                        </div>

                        <div class="community-hub-rolodex">
                            <button type="button" class="fyi-btn fyi-mentor" onclick="switchView('wallOfSeriousnessView')">
                                <div>
                                    <div class="fyi-btn-title">🧱 The Wall of Seriousness</div>
                                    <div class="fyi-btn-sub">Real questions answered with directness for those serious moments.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem;">Open →</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-kids" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(14, 116, 144, 0.75)); border-color: #38bdf8; color: #e0f2fe;" onclick="openHubSection('kidsCornerSection')">
                                <div>
                                    <div class="fyi-btn-title">🌐 The Gathering Place</div>
                                    <div class="fyi-btn-sub">Connecting those 21 and under — chat amongst yourselves &amp; share pics.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem;">Open →</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-rec" onclick="openHubSection('recTimeSection', 'vote')">
                                <div>
                                    <div class="fyi-btn-title">☕ The Rec Area</div>
                                    <div class="fyi-btn-sub">Take a moment and relax — funny pics, 30s clips &amp; random trivia.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem;">Open →</span>
                            </button>

                            <button type="button" class="fyi-btn fyi-wood" onclick="openHubSection('harborPostingSpotSection')">
                                <div>
                                    <div class="fyi-btn-title">🪵 Pass It On</div>
                                    <div class="fyi-btn-sub">Pay forward usable equipment, tools, and gear to ease another's journey.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem;">Open →</span>
                            </button>
                        </div>
                    </div>
                </div>"""

if old_right_column in html:
    html = html.replace(old_right_column, new_right_column)
    print("COMMUNITY_HUB_ROLODEX_UPDATED_SUCCESS")
else:
    print("WARNING: Could not find exact right column block.")

with open("templates/index.html", "w") as f:
    f.write(html)
