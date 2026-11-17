with open("templates/index.html", "r") as f:
    html = f.read()

# Replace the twin-buttons CSS and layout rules
old_pill_css = """        .twin-buttons {
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
        }
        .twin-btn-pill-rich {
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
        }"""

new_pill_css = """        .twin-buttons {
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

if old_pill_css in html:
    html = html.replace(old_pill_css, new_pill_css)
    print("WELCOME_PILLS_LAYOUT_FIXED_SUCCESS")
else:
    print("WARNING: Could not find old_pill_css block.")

with open("templates/index.html", "w") as f:
    f.write(html)
