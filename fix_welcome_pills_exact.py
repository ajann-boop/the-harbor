with open("templates/index.html", "r") as f:
    html = f.read()

# Replace the twin-buttons CSS to match columns 72-79 sizing exactly
old_pill_layout_css = """        .twin-buttons {
            display: flex;
            gap: 24px;
            width: 90%;
            max-width: 680px;
            justify-content: space-between;
            margin-top: 18px;
            align-items: center;
        }
        @media (max-width: 640px) {
            .twin-buttons {
                flex-direction: column;
                gap: 12px;
                width: 90%;
            }
        }
        .twin-btn-pill-rich {
            width: 275px;
            max-width: 48%;
            background: rgba(13, 56, 63, 0.45);
            border: 1.5px solid rgba(94, 234, 212, 0.65);
            padding: 10px 14px;
            border-radius: 50px;
            cursor: pointer;
            color: #ffffff;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35);
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
        }"""

new_pill_layout_css = """        .twin-buttons {
            display: grid;
            grid-template-columns: repeat(100, 1fr);
            width: 100%;
            max-width: 860px;
            margin-top: 14px;
            position: relative;
            height: 75px;
        }
        .twin-btn-pill-rich {
            grid-column: 72 / 86;
            background: rgba(13, 56, 63, 0.48);
            border: 1.5px solid rgba(94, 234, 212, 0.7);
            padding: 8px 12px;
            border-radius: 50px;
            cursor: pointer;
            color: #ffffff;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35);
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .twin-btn-pill-rich:nth-child(2) {
            grid-column: 88 / 102;
        }
        @media (max-width: 768px) {
            .twin-buttons {
                display: flex;
                flex-direction: column;
                height: auto;
                gap: 12px;
                max-width: 320px;
                margin: 14px auto 0 auto;
            }
            .twin-btn-pill-rich {
                width: 100%;
            }
        }"""

if old_pill_layout_css in html:
    html = html.replace(old_pill_layout_css, new_pill_layout_css)
    print("WELCOME_PILLS_EXACT_LAYOUT_SUCCESS")
else:
    print("WARNING: Could not find old_pill_layout_css block.")

with open("templates/index.html", "w") as f:
    f.write(html)
