with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Update CSS for the bottom twin-buttons container and the larger flashing CLICK + neon pulsating HERE
old_twin_css_block = """        .twin-buttons { display: flex; gap: 12px; width: 100%; max-width: 480px; justify-content: space-between; margin-top: 10px; }"""

new_twin_css_block = """        .twin-buttons {
            display: flex;
            gap: 36px;
            width: 94%;
            max-width: 820px;
            justify-content: space-between;
            margin-top: 26px;
        }
        @media (max-width: 640px) {
            .twin-buttons {
                flex-direction: column;
                gap: 14px;
                width: 92%;
            }
        }"""

if old_twin_css_block in html:
    html = html.replace(old_twin_css_block, new_twin_css_block)

old_neon_css = """        .twin-btn-pill-rich {
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
        }"""

new_neon_css = """        .twin-btn-pill-rich {
            flex: 1;
            max-width: 340px;
            background: rgba(13, 56, 63, 0.42);
            border: 1.5px solid rgba(94, 234, 212, 0.6);
            padding: 12px 20px;
            border-radius: 50px;
            cursor: pointer;
            color: #ffffff;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35);
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
        }
        .twin-btn-pill-rich:hover {
            background: rgba(15, 61, 68, 0.72);
            border-color: #fde047;
            transform: translateY(-3px);
        }
        .pill-member-stack {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }
        .pill-top-label {
            font-size: 0.88rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }
        .neon-click-wrap {
            font-size: 1.7rem;
            font-weight: 900;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            line-height: 1.05;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .neon-click-flash {
            color: #ffffff;
            animation: flashClickWord 1.1s infinite;
        }
        @keyframes flashClickWord {
            0%, 49% {
                opacity: 1;
                color: #ffffff;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.9), 0 0 20px rgba(56, 189, 248, 0.75);
            }
            50%, 100% {
                opacity: 0.35;
                color: #94a3b8;
                text-shadow: none;
            }
        }
        .neon-here-pulse {
            color: #5eead4;
            font-weight: 900;
            animation: neonPulseHere 1.2s infinite alternate;
        }"""

if old_neon_css in html:
    html = html.replace(old_neon_css, new_neon_css)

# 2. Update the two HTML buttons so both have single-row top titles and the big flashing CLICK + neon HERE underneath
old_buttons_html = """            <div class="twin-buttons">
                <button class="twin-btn-pill-rich pill-member-stack" onclick="switchView('becomeMemberView')">
                    <span style="font-size: 0.8rem; font-weight: 800; letter-spacing: 0.02em;">🤝 Become a Member</span>
                    <span class="neon-click-wrap">CLICK <span class="neon-here-pulse">HERE</span></span>
                </button>
                <button class="twin-btn-pill-rich pill-guest-split" onclick="switchView('donorVisitorView')">
                    <span style="font-size: 0.78rem; font-weight: 800; text-align: left; line-height: 1.2;">❤️ Guests &amp;<br>Contributors</span>
                    <span class="neon-click-wrap">CLICK <span class="neon-here-pulse">HERE</span></span>
                </button>
            </div>"""

new_buttons_html = """            <div class="twin-buttons">
                <button class="twin-btn-pill-rich pill-member-stack" onclick="switchView('becomeMemberView')">
                    <span class="pill-top-label">🤝 Become a Member</span>
                    <span class="neon-click-wrap"><span class="neon-click-flash">CLICK</span><span class="neon-here-pulse">HERE</span></span>
                </button>
                <button class="twin-btn-pill-rich pill-member-stack" onclick="switchView('donorVisitorView')">
                    <span class="pill-top-label">❤️ Guests &amp; Contributors</span>
                    <span class="neon-click-wrap"><span class="neon-click-flash">CLICK</span><span class="neon-here-pulse">HERE</span></span>
                </button>
            </div>"""

if old_buttons_html in html:
    html = html.replace(old_buttons_html, new_buttons_html)
    print("WELCOME_TWIN_PILLS_UPDATED_SUCCESS")
else:
    print("WARNING: Could not match old_buttons_html.")

with open("templates/index.html", "w") as f:
    f.write(html)
