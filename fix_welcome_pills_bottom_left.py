with open("templates/index.html", "r") as f:
    html = f.read()

# Replace the twin-buttons CSS to stack them in the bottom left-hand corner with compact pill sizing
old_pill_css = """        .twin-buttons {
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

new_pill_css = """        .twin-buttons {
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

if old_pill_css in html:
    html = html.replace(old_pill_css, new_pill_css)
    print("WELCOME_PILLS_BOTTOM_LEFT_SUCCESS")
else:
    print("WARNING: Could not find old pill layout CSS block.")

# Ensure mainGatewayView has relative positioning so absolute bottom-left anchors correctly inside it
html = html.replace(
    """<div id="mainGatewayView" class="view-screen active" style="max-width: 760px; text-align: center;">""",
    """<div id="mainGatewayView" class="view-screen active" style="max-width: 760px; text-align: center; position: relative;">"""
)

with open("templates/index.html", "w") as f:
    f.write(html)
