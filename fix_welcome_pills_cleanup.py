with open("templates/index.html", "r") as f:
    html = f.read()

# Replace the twin-buttons CSS to remove the aggressive mobile media override and lock exact bottom-left positioning
old_pill_css = """        .twin-buttons {
            position: absolute;
            bottom: 28px;
            left: 28px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 25;
        }
        .twin-btn-pill-rich {
            width: 236px;
            background: rgba(13, 56, 63, 0.52);
            border: 1.5px solid rgba(94, 234, 212, 0.75);
            padding: 9px 14px;
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
        @media (max-width: 640px) {
            .twin-buttons {
                position: relative;
                bottom: auto;
                left: auto;
                margin: 16px auto 0 auto;
                width: 250px;
            }
        }"""

new_pill_css = """        .twin-buttons {
            position: absolute;
            bottom: 24px;
            left: 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 25;
        }
        .twin-btn-pill-rich {
            width: 230px;
            background: rgba(13, 56, 63, 0.58);
            border: 1.5px solid rgba(94, 234, 212, 0.8);
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
        }"""

if old_pill_css in html:
    html = html.replace(old_pill_css, new_pill_css)
    print("WELCOME_PILLS_CLEANUP_SUCCESS")
else:
    print("WARNING: Could not find old pill CSS block.")

with open("templates/index.html", "w") as f:
    f.write(html)
