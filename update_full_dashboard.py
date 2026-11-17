with open("templates/index.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Lewie & Marcus Network - Share Your Walk</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background-color: #0b2e33; color: #ffffff; min-height: 100vh; overflow-x: hidden; position: relative; }
        
        /* Mosaic Background on Welcome Page */
        .mosaic-bg { position: fixed; inset: 0; width: 100vw; height: 100vh; display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 6px; padding: 6px; z-index: 0; pointer-events: none; opacity: 0.92; filter: saturate(1.15) blur(0.2px); }
        .mosaic-tile { width: 100%; height: 100px; object-fit: cover; border-radius: 6px; }
        .mosaic-overlay { position: fixed; inset: 0; z-index: 1; pointer-events: none; background: linear-gradient(135deg, rgba(11, 46, 51, 0.25), rgba(15, 61, 68, 0.18)); }
        
        /* Dedicated Community Background for Login & Dashboard */
        .community-bg { position: fixed; inset: 0; width: 100vw; height: 100vh; object-fit: cover; z-index: 0; pointer-events: none; display: none; filter: saturate(1.3); }
        .community-bg.active { display: block; }
        .community-overlay { position: fixed; inset: 0; z-index: 1; pointer-events: none; background: linear-gradient(135deg, rgba(11, 46, 51, 0.35), rgba(15, 61, 68, 0.28)); display: none; }
        .community-overlay.active { display: block; }

        /* Floating Jargon Background for Join View */
        .join-bg { position: fixed; inset: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; display: none; overflow: hidden; background: radial-gradient(circle at center, #0e373d 0%, #072226 100%); }
        .join-bg.active { display: block; }
        .floating-term {
            position: absolute; color: rgba(94, 234, 212, 0.45); font-weight: 800; font-size: 1.15rem; white-space: nowrap;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
            animation: floatJargon 14s linear infinite; user-select: none;
        }
        @keyframes floatJargon {
            0% { transform: translateY(105vh) translateX(0) rotate(0deg); opacity: 0; }
            15% { opacity: 0.9; }
            85% { opacity: 0.9; }
            100% { transform: translateY(-10vh) translateX(60px) rotate(8deg); opacity: 0; }
        }

        .app-container { position: relative; z-index: 5; max-width: 1040px; margin: 0 auto; padding: 16px 24px; min-height: 100vh; display: flex; flex-direction: column; justify-content: space-between; }
        
        .top-header { display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 5px; position: relative; z-index: 10; gap: 20px; }
        
        .top-left-group {
            background: rgba(11, 46, 51, 0.25); border: 1px solid rgba(94, 234, 212, 0.35);
            padding: 8px 14px; border-radius: 10px; backdrop-filter: blur(8px);
            max-width: 380px; height: 52px; display: flex; flex-direction: column; justify-content: center; text-align: left;
        }
        .sanctuary-intro-label { font-size: 0.72rem; font-weight: 700; color: #5eead4; display: flex; align-items: center; gap: 4px; text-shadow: 0 1px 3px rgba(0,0,0,0.8); }
        .sanctuary-intro-desc { font-size: 0.56rem; font-weight: 500; color: #e2e8f0; line-height: 1.25; margin-top: 1px; text-shadow: 0 1px 3px rgba(0,0,0,0.8); }

        .top-right-group { 
            background: rgba(11, 46, 51, 0.25); border: 1px solid rgba(94, 234, 212, 0.35); 
            padding: 8px 14px; border-radius: 10px; backdrop-filter: blur(8px); 
            width: 320px; height: 52px; display: flex; flex-direction: column; justify-content: center; align-items: flex-end; text-align: right;
        }
        .gateway-pill { 
            background: none; border: none; padding: 0; cursor: pointer; color: #ffffff; font-weight: 600; font-size: 0.75rem; 
            display: flex; align-items: center; justify-content: flex-end; gap: 6px; text-decoration: none; width: 100%;
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
        }
        .gateway-pill:hover { color: #5eead4; }
        .network-tagline { font-size: 0.58rem; font-weight: 600; color: #f43f5e; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 2px; text-shadow: 0 1px 2px rgba(0,0,0,0.9); }

        .gateway-section { display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; flex: 1; justify-content: center; padding: 5px 0; }
        .gateway-section.hidden { display: none !important; }
        
        /* Main Title Wrapper */
        .title-wrapper { 
            margin: 0 auto 12px auto; position: relative; width: 100%; max-width: 480px; 
            background: rgba(13, 56, 63, 0.18); border: 1.5px solid rgba(94, 234, 212, 0.45); 
            border-radius: 16px; padding: 22px 20px; backdrop-filter: blur(6px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        .welcome-text { 
            font-size: 1.15rem; font-weight: 700; color: #ffffff; letter-spacing: 0.1em; text-transform: uppercase;
            text-shadow: 0 2px 6px rgba(0,0,0,0.85);
            animation: fadeInWelcome 1s ease forwards;
        }
        @keyframes fadeInWelcome { 0% { opacity: 0; transform: translateY(-10px); } 100% { opacity: 1; transform: translateY(0); } }

        .to-text { 
            font-size: 0.85rem; font-weight: 500; color: #e2e8f0; margin: 2px 0;
            text-shadow: 0 1px 4px rgba(0,0,0,0.85);
            opacity: 0; animation: fadeInTo 0.8s ease forwards; animation-delay: 0.9s;
        }
        @keyframes fadeInTo { 0% { opacity: 0; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1); } }
        
        .harbor-title-container { 
            position: relative; display: flex; align-items: baseline; justify-content: center; margin-top: 4px;
            opacity: 0; animation: fadeInHarborContainer 0.8s ease forwards; animation-delay: 1.8s;
        }
        @keyframes fadeInHarborContainer { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }

        .catty-the { 
            position: absolute; top: -14px; left: -10px; font-size: 0.92rem; font-weight: 700; color: #5eead4; 
            letter-spacing: 0.05em; text-transform: uppercase; transform: rotate(-6deg);
            text-shadow: 0 2px 5px rgba(0,0,0,0.9); display: flex; gap: 2px;
        }
        .letter-t { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.2s; }
        .letter-h-the { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.5s; }
        .letter-e-the { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.8s; }
        @keyframes dropLetter { 0% { opacity: 0; transform: translateY(-15px) rotate(-10deg); } 100% { opacity: 1; transform: translateY(0) rotate(-6deg); } }

        .harbor-main-text { font-size: 3rem; font-weight: 800; letter-spacing: 0.04em; line-height: 1.05; animation: medicalAwarenessGlow 6s infinite; }
        @keyframes medicalAwarenessGlow {
            0% { color: #38bdf8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            33% { color: #fb7185; text-shadow: 0 0 20px rgba(251, 113, 133, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            66% { color: #fde047; text-shadow: 0 0 20px rgba(253, 224, 71, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            100% { color: #38bdf8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.9), 0 2px 6px rgba(0,0,0,0.9); }
        }

        .harbor-subtitle { font-size: 0.82rem; font-weight: 600; color: #5eead4; margin-top: 6px; letter-spacing: 0.02em; max-width: 420px; line-height: 1.3; text-align: center; text-shadow: 0 1px 5px rgba(0,0,0,0.95); }

        .gateway-entrance-wrapper {
            background: rgba(13, 56, 63, 0.14); border: 2px solid; 
            border-image: linear-gradient(90deg, #38bdf8, #f43f5e, #fbbf24, #a855f7) 1;
            padding: 14px 16px; border-radius: 14px; backdrop-filter: blur(5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.25); 
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            width: 100%; max-width: 320px; height: 160px; margin-top: 10px;
        }
        .cube-overlay-label { font-size: 0.65rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px; text-shadow: 0 1px 4px rgba(0,0,0,0.95); }

        .enter-harbor-btn { 
            background: rgba(11, 46, 51, 0.16); border: 2px solid #38bdf8; padding: 10px 14px; border-radius: 12px; cursor: pointer; 
            transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            display: flex; flex-direction: column; align-items: center; gap: 4px; width: 100%; justify-content: center;
            backdrop-filter: blur(4px);
        }
        .enter-harbor-btn:hover { transform: translateY(-2px); border-color: #f43f5e; box-shadow: 0 8px 22px rgba(244, 63, 94, 0.4); background: rgba(15, 61, 68, 0.38); }
        .btn-anchor-icon { font-size: 1.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.9)); }
        .enter-main { font-size: 0.88rem; font-weight: 800; color: #ffffff; letter-spacing: 0.02em; line-height: 1.2; text-shadow: 0 1px 4px rgba(0,0,0,0.95); }

        .twin-buttons { display: flex; gap: 12px; width: 100%; max-width: 480px; justify-content: space-between; margin-top: 10px; }
        .twin-btn-pill { flex: 1; background: rgba(13, 56, 63, 0.28); border: 1px solid rgba(94, 234, 212, 0.45); padding: 12px 14px; border-radius: 50px; cursor: pointer; color: #ffffff; font-weight: 600; font-size: 0.74rem; backdrop-filter: blur(8px); transition: all 0.25s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; text-align: center; text-shadow: 0 1px 3px rgba(0,0,0,0.85); }
        .twin-btn-pill:hover { background: rgba(15, 61, 68, 0.55); border-color: #5eead4; transform: translateY(-2px); }

        /* View Screens */
        .view-screen { display: none; width: 100%; max-width: 720px; margin: 0 auto; background: rgba(11, 46, 51, 0.65); border: 1px solid rgba(94, 234, 212, 0.45); border-radius: 18px; padding: 22px; backdrop-filter: blur(14px); box-shadow: 0 15px 35px rgba(0,0,0,0.5); text-align: left; position: relative; z-index: 20; }
        .view-screen.active { display: block; }
        .screen-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }
        .screen-title { font-size: 1.25rem; font-weight: 700; color: #5eead4; }
        .close-btn { background: none; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; }
        .close-btn:hover { color: #ffffff; }
        
        .form-group { margin-bottom: 14px; }
        .form-label { display: block; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 5px; }
        .dark-input { width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.45); background: rgba(11, 46, 51, 0.45); color: #ffffff; font-size: 0.9rem; outline: none; backdrop-filter: blur(10px); }
        .dark-input:focus { border-color: #5eead4; box-shadow: 0 0 0 3px rgba(94, 234, 212, 0.2); }
        .action-btn { width: 100%; background: #5eead4; color: #0b2e33; font-weight: 700; padding: 12px; border-radius: 8px; border: none; cursor: pointer; font-size: 0.95rem; transition: background 0.2s; margin-top: 8px; }
        .action-btn:hover { background: #2dd4bf; }

        /* Password Reveal Wrapper */
        .password-wrapper { position: relative; display: flex; align-items: center; }
        .password-wrapper .dark-input { padding-right: 115px; }
        .show-pass-btn {
            position: absolute; right: 8px; background: rgba(94, 234, 212, 0.18); border: 1px solid #5eead4;
            color: #5eead4; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; cursor: pointer;
        }
        .show-pass-btn:hover { background: #5eead4; color: #0b2e33; }
        
        .mission-callout { background: rgba(15, 61, 68, 0.65); border-left: 4px solid #5eead4; padding: 12px; border-radius: 0 8px 8px 0; font-size: 0.88rem; line-height: 1.45; color: #e2e8f0; margin-bottom: 16px; backdrop-filter: blur(10px); }
        
        .badge-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; margin-top: 6px; }
        .badge-option { background: rgba(11, 46, 51, 0.6); border: 1px solid rgba(94, 234, 212, 0.3); padding: 8px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; color: #cbd5e1; cursor: pointer; text-align: center; transition: all 0.2s; user-select: none; }
        .badge-option input { display: none; }
        .badge-option.selected { background: rgba(94, 234, 212, 0.25); border-color: #5eead4; color: #ffffff; box-shadow: 0 0 10px rgba(94, 234, 212, 0.3); }

        .sanctuary-quote-banner { background: rgba(13, 56, 63, 0.65); border: 1.5px solid rgba(94, 234, 212, 0.5); border-radius: 12px; padding: 12px 18px; margin-bottom: 16px; backdrop-filter: blur(14px); box-shadow: 0 6px 20px rgba(0,0,0,0.4); text-align: center; width: 100%; }
        .sanctuary-quote-text { font-size: 0.95rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 4px; }
        .sanctuary-quote-author { font-size: 0.75rem; font-weight: 600; color: #5eead4; }

        .winner-spotlight-card { background: rgba(11, 46, 51, 0.6); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 12px; overflow: hidden; margin-top: 16px; padding: 14px; text-align: center; backdrop-filter: blur(12px); }
        .winner-spotlight-title { font-size: 1rem; font-weight: 700; color: #5eead4; margin-bottom: 2px; }
        .winner-spotlight-subtitle { font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
        .winner-img { width: 100%; height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 8px; border: 1px solid rgba(94, 234, 212, 0.3); }
        .winner-caption { font-size: 0.85rem; font-weight: 600; color: #ffffff; margin-bottom: 2px; }
        .winner-author { font-size: 0.78rem; color: #cbd5e1; }
        .contest-schedule-box { background: rgba(15, 61, 68, 0.5); border: 1px dashed rgba(94, 234, 212, 0.4); padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 0.78rem; color: #cbd5e1; text-align: left; }

        /* DASHBOARD LAYOUT */
        .dashboard-screen { max-width: 1000px; }

        /* Top Member Profile & Always-Editable Check-In Bar */
        .member-profile-bar {
            display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;
            background: rgba(13, 56, 63, 0.75); border: 1px solid rgba(94, 234, 212, 0.45);
            border-radius: 12px; padding: 12px 16px; margin-bottom: 14px;
        }
        .active-status-pill {
            display: inline-flex; align-items: center; gap: 6px; background: rgba(34, 197, 94, 0.18);
            border: 1px solid #4ade80; color: #86efac; font-size: 0.72rem; font-weight: 700;
            padding: 3px 10px; border-radius: 50px; cursor: pointer;
        }
        .active-dot { width: 8px; height: 8px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 8px #4ade80; }

        /* Map-Legend Icon Badges */
        .legend-badge-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
        .icon-legend-badge {
            display: inline-flex; align-items: center; justify-content: center; gap: 4px;
            background: rgba(11, 46, 51, 0.85); border: 1.5px solid #5eead4; color: #ffffff;
            font-size: 0.78rem; font-weight: 800; padding: 3px 8px; border-radius: 8px; cursor: pointer;
            transition: transform 0.15s;
        }
        .icon-legend-badge:hover { transform: scale(1.08); border-color: #fde047; }
        .dmd-badge { border-color: #fb7185; color: #fda4af; background: rgba(136, 19, 55, 0.35); }
        .legend-key-btn { background: none; border: 1px dashed rgba(94, 234, 212, 0.5); color: #5eead4; font-size: 0.68rem; padding: 2px 7px; border-radius: 6px; cursor: pointer; }
        .legend-popup { display: none; background: rgba(7, 34, 38, 0.95); border: 1px solid #5eead4; border-radius: 8px; padding: 8px 12px; font-size: 0.72rem; color: #e2e8f0; margin-top: 6px; }
        .legend-popup.active { display: block; }

        /* Always-Changeable Daily Feeling/Doing Check-In Box */
        .daily-checkin-box { flex: 1; min-width: 260px; max-width: 400px; background: rgba(11, 46, 51, 0.65); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 10px; padding: 8px 10px; }
        .daily-checkin-label { font-size: 0.68rem; font-weight: 700; color: #5eead4; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; display: flex; justify-content: space-between; }
        .daily-checkin-input { width: 100%; background: rgba(15, 61, 68, 0.6); border: 1px solid rgba(94, 234, 212, 0.3); color: #ffffff; font-size: 0.8rem; padding: 6px 8px; border-radius: 6px; outline: none; }
        .daily-checkin-input:focus { border-color: #5eead4; }

        /* Main Two-Column Dashboard Grid */
        .dashboard-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; }
        @media (max-width: 820px) { .dashboard-grid { grid-template-columns: 1fr; } }
        .dash-panel { background: rgba(11, 46, 51, 0.7); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 14px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; }
        .panel-heading { font-size: 0.98rem; font-weight: 800; color: #5eead4; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }

        /* Community Chat (Front & Center) */
        .chat-feed { max-height: 360px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px; padding-right: 4px; }
        .chat-msg { background: rgba(15, 61, 68, 0.68); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 10px; font-size: 0.83rem; }
        .chat-msg-header { display: flex; justify-content: space-between; font-size: 0.75rem; color: #5eead4; font-weight: 700; margin-bottom: 4px; }
        .chat-reply-indicator { font-size: 0.73rem; color: #38bdf8; font-style: italic; margin-bottom: 5px; background: rgba(56, 189, 248, 0.14); padding: 4px 8px; border-radius: 5px; border-left: 2px solid #38bdf8; }
        .chat-photo-preview { width: 100%; max-height: 150px; object-fit: cover; border-radius: 8px; margin-top: 6px; border: 1px solid rgba(94, 234, 212, 0.35); }
        .chat-btn-group { display: flex; gap: 6px; margin-top: 6px; }
        .reply-btn-mini, .attach-btn-mini { background: rgba(94, 234, 212, 0.18); border: 1px solid #5eead4; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 50px; cursor: pointer; transition: all 0.2s; }
        .reply-btn-mini:hover, .attach-btn-mini:hover { background: #5eead4; color: #0b2e33; }

        /* For Your Info (FYI) Skinny Comfortable Navigation Buttons */
        .fyi-strip { display: flex; flex-direction: column; gap: 7px; margin-bottom: 14px; }
        .fyi-btn {
            display: flex; align-items: center; justify-content: space-between; gap: 10px;
            padding: 8px 12px; border-radius: 10px; cursor: pointer; text-align: left;
            transition: transform 0.18s, box-shadow 0.18s; border: 1.5px solid transparent;
        }
        .fyi-btn:hover { transform: translateX(3px); }
        .fyi-btn-title { font-size: 0.82rem; font-weight: 800; display: flex; align-items: center; gap: 6px; }
        .fyi-btn-sub { font-size: 0.69rem; line-height: 1.25; opacity: 0.92; margin-top: 1px; }

        /* Distinct Themes for the 4 FYI Buttons */
        .fyi-mentor { background: linear-gradient(135deg, rgba(67, 56, 202, 0.45), rgba(49, 46, 129, 0.65)); border-color: #818cf8; color: #e0e7ff; }
        .fyi-kids { background: linear-gradient(135deg, rgba(236, 72, 153, 0.35), rgba(245, 158, 11, 0.35)); border-color: #f472b6; color: #fdf2f8; }
        .fyi-rec { background: linear-gradient(135deg, rgba(13, 148, 136, 0.45), rgba(6, 95, 70, 0.65)); border-color: #5eead4; color: #ecfdf5; }
        /* Wood / Driftwood Log Style for The Harbor's Posting Spot */
        .fyi-wood {
            background: repeating-linear-gradient(90deg, #5c3a21 0px, #6b4426 14px, #4e301a 28px);
            border: 2px solid #c28e5c; color: #fef3c7; box-shadow: inset 0 1px 4px rgba(0,0,0,0.5);
        }

        /* Daily Vote Action Button & Reveal Box */
        .daily-vote-jump-btn {
            width: 100%; background: linear-gradient(135deg, #0284c7, #0d9488); border: 1.5px solid #38bdf8;
            color: #ffffff; font-weight: 800; font-size: 0.84rem; padding: 11px 14px; border-radius: 10px;
            cursor: pointer; text-align: center; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
            transition: transform 0.2s, box-shadow 0.2s; margin-bottom: 10px;
        }
        .daily-vote-jump-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(56, 189, 248, 0.5); }

        /* Expandable Sub-Views (REC Time, Kids Corner, Serious Questions, Harbor Posting Board) */
        .hub-subview { display: none; background: rgba(11, 46, 51, 0.92); border: 1.5px solid #5eead4; border-radius: 14px; padding: 18px; margin-top: 16px; backdrop-filter: blur(16px); box-shadow: 0 12px 32px rgba(0,0,0,0.55); }
        .hub-subview.active { display: block; }
        .subview-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(94, 234, 212, 0.3); padding-bottom: 10px; margin-bottom: 14px; }
        .subview-title { font-size: 1.1rem; font-weight: 800; color: #5eead4; }
        .back-hub-btn { background: rgba(94, 234, 212, 0.15); border: 1px solid #5eead4; color: #5eead4; padding: 5px 12px; border-radius: 50px; font-size: 0.76rem; font-weight: 700; cursor: pointer; }
        .back-hub-btn:hover { background: #5eead4; color: #0b2e33; }

        /* Cork Board for Serious Questions */
        .cork-board-area { background: linear-gradient(135deg, rgba(120, 72, 32, 0.32), rgba(88, 52, 22, 0.42)); border: 2px solid rgba(217, 155, 82, 0.55); border-radius: 12px; padding: 14px; margin-top: 12px; }
        .cork-note { background: rgba(30, 27, 75, 0.85); border: 1px solid #818cf8; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
        .cork-highlight-badge { display: inline-block; background: #fde047; color: #0b2e33; font-weight: 800; font-size: 0.72rem; padding: 3px 10px; border-radius: 6px; text-transform: uppercase; margin-bottom: 6px; }

        /* REC Time Tabs & 3-Pic Daily Vote + Saturday Run-Off */
        .rec-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 14px; }
        .rec-tab-btn { flex: 1; min-width: 120px; padding: 8px 10px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.4); background: rgba(15, 61, 68, 0.5); color: #cbd5e1; font-weight: 700; font-size: 0.76rem; cursor: pointer; }
        .rec-tab-btn.active { background: #5eead4; color: #0b2e33; border-color: #5eead4; }

        .three-pic-vote-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 10px; }
        .vote-pic-card { background: rgba(15, 61, 68, 0.7); border: 1.5px solid rgba(94, 234, 212, 0.4); border-radius: 10px; padding: 10px; text-align: center; }
        .vote-pic-card img { width: 100%; height: 130px; object-fit: cover; border-radius: 8px; margin-bottom: 6px; }
        .tally-card { background: rgba(15, 61, 68, 0.65); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 8px; padding: 10px; margin-bottom: 8px; font-size: 0.8rem; }
        .finalist-tag { background: rgba(251, 191, 36, 0.2); border: 1px solid #fbbf24; color: #fde047; font-size: 0.68rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }

        .video-container { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #000; border-radius: 12px; overflow: hidden; margin-bottom: 16px; border: 1px solid rgba(94, 234, 212, 0.3); }
        .video-container video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }

        .footer-banner { text-align: center; font-size: 0.78rem; color: #cbd5e1; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 14px; position: relative; z-index: 10; display: flex; align-items: center; justify-content: center; gap: 6px; }
    </style>
</head>
<body>
    <div class="mosaic-bg">
        {% for img in mosaic_images %}
        <img src="{{ url_for('static', filename='images/mosaic/' + img) }}" class="mosaic-tile" alt="Mosaic photo">
        {% endfor %}
    </div>
    <div class="mosaic-overlay"></div>

    <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" id="communityBg" class="community-bg" alt="Community Gathering">
    <div id="communityOverlay" class="community-overlay"></div>

    <div id="joinBg" class="join-bg">
        <div class="floating-term" style="left: 4%; animation-duration: 12s; animation-delay: 0s;">MD & Specialist Care</div>
        <div class="floating-term" style="left: 22%; animation-duration: 10s; animation-delay: 2s;">DMD Warrior</div>
        <div class="floating-term" style="left: 42%; animation-duration: 11s; animation-delay: 1s;">Pediatric Caregiver</div>
        <div class="floating-term" style="left: 62%; animation-duration: 13s; animation-delay: 3.5s;">Autism Support</div>
        <div class="floating-term" style="left: 78%; animation-duration: 12s; animation-delay: 1.5s;">Storm Survivor</div>
    </div>
    
    <div class="app-container">
        <!-- Top Header -->
        <div id="topHeaderGroup" class="top-header">
            <div class="top-left-group">
                <div class="sanctuary-intro-label">⚓ The Caregiver Sanctuary</div>
                <div class="sanctuary-intro-desc">A place where caregivers can pass on learned experiences from their caregiving journey.</div>
            </div>
            <div class="top-right-group">
                <button class="gateway-pill" onclick="switchView('missionVideoView')">
                    <span>▶ The Reason Behind the Mission</span>
                </button>
                <div class="network-tagline">The Lewie & Marcus Network</div>
            </div>
        </div>
        
        <!-- MAIN GATEWAY VIEW -->
        <div id="mainGatewayView" class="gateway-section">
            <div class="title-wrapper">
                <div class="welcome-text">WELCOME</div>
                <div class="to-text">to</div>
                <div class="harbor-title-container">
                    <div class="catty-the">
                        <span class="letter-t">T</span><span class="letter-h-the">h</span><span class="letter-e-the">e</span>
                    </div>
                    <div class="harbor-main-text">Harbor</div>
                </div>
                <div class="harbor-subtitle">Where survived struggles and lived experiences could save someone.</div>
            </div>

            <div class="gateway-entrance-wrapper">
                <div class="cube-overlay-label">Welcome back member</div>
                <button class="enter-harbor-btn" onclick="switchView('memberLoginView')">
                    <span class="btn-anchor-icon">⚓</span>
                    <span class="btn-text-group">
                        <span class="enter-main">MEMBERS WELCOME BACK TO THE HARBOR</span>
                    </span>
                </button>
            </div>

            <div class="twin-buttons">
                <button class="twin-btn-pill" onclick="switchView('becomeMemberView')"><span>🤝</span> Become a Member</button>
                <button class="twin-btn-pill" onclick="switchView('donorVisitorView')"><span>❤️</span> Welcome Guests & Contributors</button>
            </div>
        </div>

        <!-- MISSION VIDEO VIEW -->
        <div id="missionVideoView" class="view-screen" style="max-width: 740px;">
            <div class="screen-header">
                <div class="screen-title">▶ The Reason Behind the Mission</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>
            <div class="mission-callout">
                "Every shared struggle and lived experience is a beacon of hope. Take a look at the heart and journey behind The Lewie & Marcus Network."
            </div>
            <div class="video-container">
                <video controls autoplay playsinline>
                    <source src="{{ url_for('static', filename='videos/mission_intro.mp4') }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <button class="action-btn" onclick="switchView('mainGatewayView')">Return to Main Gateway</button>
        </div>

        <!-- 1. MEMBER LOGIN VIEW WITH SHOW PASSWORD BUTTON -->
        <div id="memberLoginView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">Member Login & Sanctuary</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>

            <div class="sanctuary-quote-banner">
                <div id="sanctuaryQuoteText" class="sanctuary-quote-text">"You don't have to weather the storm by yourself. Your lived experiences light the path for fellow caregivers walking right beside you."</div>
                <div id="sanctuaryQuoteAuthor" class="sanctuary-quote-author">— HopeWalker</div>
            </div>

            <form onsubmit="event.preventDefault(); loginAsMember();">
                <div class="form-group">
                    <label class="form-label">Member Email or ID</label>
                    <input type="text" id="loginUserField" class="dark-input" required placeholder="you@example.com" value="Anthony" autocomplete="username">
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <div class="password-wrapper">
                        <input type="password" id="loginPasswordField" class="dark-input" required placeholder="••••••••" value="Harbor2026" autocomplete="current-password">
                        <button type="button" class="show-pass-btn" onclick="togglePasswordVisibility('loginPasswordField', this)">👁️ Show Password</button>
                    </div>
                </div>
                <button type="submit" class="action-btn">Enter Caregiver Sanctuary</button>
            </form>

            <div class="winner-spotlight-card">
                <div class="winner-spotlight-title">Weekly Photo Contest & Election Spotlight</div>
                <div class="winner-spotlight-subtitle">This week's approved winner:</div>
                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" class="winner-img" alt="Weekly Winner">
                <div class="winner-caption">Sunny Park Day Breakthrough</div>
                <div class="winner-author">Submitted by: Caregiver Sarah</div>
            </div>

            <div style="text-align: center; margin-top: 16px;">
                <a href="#" onclick="switchView('becomeMemberView'); return false;" style="color: #cbd5e1; font-size: 0.82rem; text-decoration: underline;">Not a member yet? Click here to join</a>
            </div>
        </div>

        <!-- 1B. MEMBER COMMUNITY DASHBOARD VIEW -->
        <div id="communityDashboardView" class="view-screen dashboard-screen">
            <div class="screen-header">
                <div class="screen-title">⚓ Caregiver Sanctuary Dashboard</div>
                <button class="close-btn" style="font-size: 0.82rem; color: #5eead4; border: 1px solid rgba(94, 234, 212, 0.4); padding: 4px 10px; border-radius: 6px;" onclick="switchView('mainGatewayView')">Sign Out</button>
            </div>

            <!-- TOP: Member Profile Bar with Active Status, Map-Legend Icon Badges & Always-Editable Check-In -->
            <div class="member-profile-bar">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <span style="font-size: 1rem; font-weight: 800; color: #ffffff;">Welcome back, <span id="dashMemberName" style="color: #5eead4;">Anthony</span></span>
                        <span class="active-status-pill" id="visibilityToggleBtn" onclick="toggleActiveVisibility()" title="Click to toggle visibility to other members">
                            <span class="active-dot" id="visibilityDot"></span>
                            <span id="visibilityLabel">Active to everyone</span>
                        </span>
                    </div>

                    <!-- Map-Legend Icon Badges -->
                    <div class="legend-badge-row" id="memberBadgeRow">
                        <span class="icon-legend-badge" title="Autism">🧩</span>
                        <span class="icon-legend-badge" title="Pediatric Caregiver — Disability, Illness, or Special Needs">🩺</span>
                        <span class="icon-legend-badge dmd-badge" title="Duchenne Muscular Dystrophy (DMD)">🎗️ DMD</span>
                        <button type="button" class="legend-key-btn" onclick="toggleLegendPopup()">🗺️ Legend</button>
                        <button type="button" class="legend-key-btn" onclick="promptAddBadgeCode()">+ Add Code</button>
                    </div>
                    <div class="legend-popup" id="legendPopupBox">
                        <strong>🗺️ Badge Legend:</strong> 🧩 = Autism &bull; 🩺 = Pediatric Caregiver (Disability, Illness, or Special Needs) &bull; 🎗️ DMD = Duchenne Muscular Dystrophy
                    </div>
                </div>

                <!-- Always-Changeable How You're Feeling / Doing Box -->
                <div class="daily-checkin-box">
                    <div class="daily-checkin-label">
                        <span>💬 How I'm Feeling / Doing Today</span>
                        <span id="checkinSavedTag" style="color: #86efac;">Live</span>
                    </div>
                    <input type="text" id="dailyFeelingInput" class="daily-checkin-input" value="Hanging in there and taking it one step at a time today." oninput="document.getElementById('checkinSavedTag').innerText='Updated ✓'">
                </div>
            </div>

            <!-- MAIN TWO-COLUMN GRID -->
            <div class="dashboard-grid">
                <!-- LEFT / CENTERPIECE: Community Chat -->
                <div class="dash-panel">
                    <div>
                        <div class="panel-heading">
                            <span>💬 Community Chat</span>
                            <span style="font-size: 0.72rem; color: #cbd5e1;">Live Threaded Feed</span>
                        </div>
                        <div class="chat-feed" id="communityChatFeed">
                            <div class="chat-msg">
                                <div class="chat-msg-header">
                                    <span>Caregiver Sarah <span title="Pediatric Caregiver">🩺</span></span>
                                    <span style="font-size: 0.7rem; color: #94a3b8;">Today</span>
                                </div>
                                <div>Finally got a calm afternoon at the park without sensory overload!</div>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" class="chat-photo-preview" alt="Park Day">
                                <div class="chat-btn-group">
                                    <button class="reply-btn-mini" onclick="setReplyTarget('Caregiver Sarah')">↩️ Reply</button>
                                </div>
                            </div>
                            <div class="chat-msg">
                                <div class="chat-msg-header">
                                    <span>BeaconMom <span title="Autism">🧩</span></span>
                                    <span style="font-size: 0.7rem; color: #94a3b8;">Today</span>
                                </div>
                                <div class="chat-reply-indicator">Anthony J. replied to BeaconMom: That's wonderful news, keeping you in our thoughts!</div>
                                <div>Sending strength to everyone navigating therapy schedules this week.</div>
                                <div class="chat-btn-group">
                                    <button class="reply-btn-mini" onclick="setReplyTarget('BeaconMom')">↩️ Reply</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Chat Composer with Easy Attachment + Opt-in for Public Vote -->
                    <form onsubmit="event.preventDefault(); postChatSubmission();" style="border-top: 1px solid rgba(255,255,255,0.12); padding-top: 10px; margin-top: 6px;">
                        <div id="replyBanner" style="font-size: 0.75rem; color: #38bdf8; margin-bottom: 5px; display: none;">
                            Replying to <span id="replyTargetName"></span>
                            <span onclick="cancelReply()" style="cursor:pointer; color:#f43f5e; margin-left:6px;">[&times; cancel]</span>
                        </div>

                        <input type="text" id="chatCaptionInput" class="dark-input" style="margin-bottom: 6px; font-size: 0.82rem;" required placeholder="Share what's on your mind or reply to a member...">

                        <!-- Attachment Bar -->
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
                        </div>

                        <!-- Opt-In for Public Vote (Appears when attachment/media is added) -->
                        <div id="publicVoteOptInBox" style="display: none; align-items: center; gap: 6px; margin-bottom: 8px; background: rgba(94, 234, 212, 0.14); border: 1px solid rgba(94, 234, 212, 0.4); padding: 6px 10px; border-radius: 8px;">
                            <input type="checkbox" id="optInPublicVoteCheck" style="width: 15px; height: 15px; accent-color: #5eead4; cursor: pointer;">
                            <label for="optInPublicVoteCheck" style="font-size: 0.74rem; color: #5eead4; font-weight: 700; cursor: pointer;">Opt-in for Public Vote (Enter this photo into the 24-Hour Daily Vote)</label>
                        </div>

                        <button type="submit" class="action-btn" style="padding: 9px; font-size: 0.84rem; margin-top: 0;">Post to Community Chat</button>
                    </form>
                </div>

                <!-- RIGHT COLUMN: For Your Info (FYI) Strip + Click to View Daily Vote + 10 PM Reveal -->
                <div class="dash-panel">
                    <div>
                        <div class="panel-heading">
                            <span>📌 For Your Info (FYI)</span>
                        </div>

                        <!-- Skinny, Comfortable Navigation Buttons -->
                        <div class="fyi-strip">
                            <button type="button" class="fyi-btn fyi-mentor" onclick="openHubSection('seriousQuestionsSection')">
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
                    </div>
                </div>
            </div>

            <!-- EXPANDABLE SUB-VIEW 1: SERIOUS QUESTION POSTING (MENTOR / EDUCATOR COLOR BOX) -->
            <div id="seriousQuestionsSection" class="hub-subview" style="border-color: #818cf8; background: rgba(30, 27, 75, 0.92);">
                <div class="subview-header" style="border-bottom-color: rgba(129, 140, 248, 0.35);">
                    <div>
                        <div class="subview-title" style="color: #a5b4fc;">🎓 Serious Question Posting — Mentors & Educators Cork Board</div>
                        <div style="font-size: 0.76rem; color: #e0e7ff;">More serious questions. Get real answers for those serious moments from teachers, educators, and seasoned caregivers.</div>
                    </div>
                    <button class="back-hub-btn" style="border-color: #a5b4fc; color: #a5b4fc;" onclick="closeHubSections()">✕ Close</button>
                </div>

                <form onsubmit="event.preventDefault(); postCorkBoardQuestion();" style="background: rgba(49, 46, 129, 0.55); padding: 12px; border-radius: 10px; border: 1px solid rgba(129, 140, 248, 0.45);">
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label class="form-label" style="color: #fde047; font-size: 0.78rem;">Highlighted Topic Field (e.g., Autism, Questions About Autism, DMD, Chronic Illness):</label>
                        <input type="text" id="corkTopicInput" class="dark-input" required placeholder="e.g., Questions About Autism">
                    </div>
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label class="form-label" style="font-size: 0.78rem;">I have a question about...</label>
                        <textarea id="corkDescInput" class="dark-input" rows="2" required placeholder="e.g., Son likes to take cold showers, or likes to shower with flip-flops on..."></textarea>
                    </div>
                    <button type="submit" class="action-btn" style="background: #fde047; color: #0b2e33; padding: 8px; font-size: 0.82rem; margin-top: 0;">📌 Pin Serious Question</button>
                </form>

                <div class="cork-board-area" id="corkBoardFeed">
                    <div class="cork-note">
                        <span class="cork-highlight-badge">Questions About Autism</span>
                        <div style="font-size: 0.86rem; color: #ffffff; font-weight: 600;">I have a question about: Son likes to take cold showers and insists on showering with flip-flops on. Has anyone else navigated sensory temperature or texture preferences like this?</div>
                        <div style="font-size: 0.72rem; color: #c7d2fe; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;">
                            <span>Pinned by Anthony</span>
                            <button class="reply-btn-mini" onclick="replyToCorkNote(this)">💬 Share Real Answer</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- EXPANDABLE SUB-VIEW 2: KIDS CORNER (FUN COLORS, KIDS CONNECTING WITH KIDS, NO BRANCH-OFFS) -->
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
            </div>

            <!-- EXPANDABLE SUB-VIEW 3: REC TIME (24-HR 3-PIC VOTE, SATURDAY RUN-OFF, FUNNY PICS/30S VIDEOS, 100+ TRIVIA) -->
            <div id="recTimeSection" class="hub-subview">
                <div class="subview-header">
                    <div>
                        <div class="subview-title">☕ REC Time — Take a Moment, and Relax</div>
                        <div style="font-size: 0.76rem; color: #cbd5e1;">Cast your 24-hour daily vote, view Saturday's run-off, watch 30-second funny clips, or play 100+ trivia!</div>
                    </div>
                    <button class="back-hub-btn" onclick="closeHubSections()">✕ Close REC Time</button>
                </div>

                <div class="rec-tabs">
                    <button class="rec-tab-btn active" id="recTabVoteBtn" onclick="switchRecTab('vote')">🗳️ 24-Hr Daily Vote & Sat Run-Off</button>
                    <button class="rec-tab-btn" id="recTabFunnyBtn" onclick="switchRecTab('funny')">😂 Funny Pics & 30s Videos</button>
                    <button class="rec-tab-btn" id="recTabTriviaBtn" onclick="switchRecTab('trivia')">🧠 100+ Question Trivia</button>
                </div>

                <!-- TAB A: 24-HOUR DAILY VOTE (3 RANDOM PICS) + SATURDAY ELECTION RUN-OFF -->
                <div id="recVotePanel">
                    <div style="font-size: 0.84rem; font-weight: 700; color: #5eead4; margin-bottom: 4px;">📸 Today's 3 Random Pics (Refreshes Every 24 Hours)</div>
                    <div style="font-size: 0.74rem; color: #cbd5e1; margin-bottom: 8px;">Vote for your favorite photo submitted from Community Chat!</div>

                    <div class="three-pic-vote-grid" id="dailyThreePicsGrid">
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Pic 1">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Sunny Park Breakthrough</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By Caregiver Sarah</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #1</button>
                        </div>
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" alt="Pic 2">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Evening Porch Laughs</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By BeaconMom</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #2</button>
                        </div>
                        <div class="vote-pic-card">
                            <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Pic 3">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">Morning Coffee Victory</div>
                            <div style="font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px;">By HopeWalker</div>
                            <button class="action-btn" style="padding: 6px; font-size: 0.76rem; margin-top: 0;" onclick="voteForDailyPic(this)">👍 Vote for Pic #3</button>
                        </div>
                    </div>

                    <!-- Saturday Election Run-Off Card (Mon, Wed, Fri Winners with Pictures & Vote Counts) -->
                    <div style="margin-top: 18px; border-top: 1px solid rgba(94, 234, 212, 0.3); padding-top: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                            <div style="font-size: 0.9rem; font-weight: 800; color: #fde047;">🏆 Saturday Election Run-Off Card (Mon / Wed / Fri Winners)</div>
                            <span style="font-size: 0.7rem; background: rgba(244, 63, 94, 0.25); color: #fb7185; padding: 3px 8px; border-radius: 50px; font-weight: 700;">Saturday Head-to-Head Hidden Till 10:00 PM</span>
                        </div>

                        <div class="three-pic-vote-grid">
                            <!-- Caregiver 1: Monday Winner -->
                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">1. Monday's Winner</span>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Monday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">Caregiver Sarah</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Monday Tally: 28 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'Caregiver Sarah')">🗳️ Vote in Saturday Run-Off</button>
                            </div>

                            <!-- Caregiver 2: Wednesday Winner -->
                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">2. Wednesday's Winner</span>
                                <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" alt="Wednesday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">HopeWalker</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Wednesday Tally: 34 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'HopeWalker')">🗳️ Vote in Saturday Run-Off</button>
                            </div>

                            <!-- Caregiver 3: Friday Winner -->
                            <div class="vote-pic-card" style="border-color: #fde047;">
                                <span class="finalist-tag" style="display: inline-block; margin-bottom: 6px;">3. Friday's Winner</span>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" alt="Friday Winner">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">BeaconMom</div>
                                <div style="font-size: 0.72rem; color: #5eead4; font-weight: 700; margin: 3px 0 6px 0;">Friday Tally: 31 Votes</div>
                                <button class="back-hub-btn" style="width: 100%;" onclick="voteSaturdayRunoff(this, 'BeaconMom')">🗳️ Vote in Saturday Run-Off</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB B: FUNNY PICS & 30-SECOND FUNNY VIDEOS -->
                <div id="recFunnyPanel" style="display: none;">
                    <div style="font-size: 0.82rem; color: #cbd5e1; margin-bottom: 10px;">Quick laughs, funny caregiver pics, and 30-second video clips to recharge your battery.</div>
                    <div class="three-pic-vote-grid">
                        <div class="tally-card">
                            <strong style="color: #fde047;">🎬 30s Clip: When the Coffee Finally Kicks In</strong>
                            <p style="font-size: 0.76rem; color: #e2e8f0; margin: 6px 0;">"Me at 6:00 AM trying to remember if I already gave the morning meds."</p>
                            <button class="back-hub-btn" onclick="alert('Playing 30-second community funny clip!')">▶ Play 30s Video</button>
                        </div>
                        <div class="tally-card">
                            <strong style="color: #5eead4;">😂 Funny Pic: The Laundry Mountain</strong>
                            <p style="font-size: 0.76rem; color: #e2e8f0; margin: 6px 0;">"Folded one basket today. Three more mysteriously appeared behind me."</p>
                            <button class="back-hub-btn" onclick="this.innerText='😂 Haha! (19)'">😂 Haha! (18)</button>
                        </div>
                    </div>
                </div>

                <!-- TAB C: 100+ QUESTION TRIVIA BANK -->
                <div id="recTriviaPanel" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                        <div style="font-size: 0.82rem; color: #5eead4; font-weight: 700;">🧠 100+ Question Mix (From Frying Eggs to Deep Life Questions)</div>
                        <div style="font-size: 0.8rem; font-weight: 800; color: #fde047;" id="recScoreText">🏆 Score: 0 | Answered: 0</div>
                    </div>
                    <div style="background: rgba(15, 61, 68, 0.75); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 10px; padding: 14px;">
                        <div style="font-size: 0.7rem; color: #38bdf8; text-transform: uppercase; font-weight: 700; margin-bottom: 4px;" id="recCategoryLabel">Category: Everyday Basics</div>
                        <div id="recQuestionText" style="font-size: 0.96rem; font-weight: 700; color: #ffffff; margin-bottom: 12px;"></div>
                        <div id="recOptionsBox" style="display: flex; flex-direction: column; gap: 7px;"></div>
                        <div id="recFeedbackText" style="font-size: 0.8rem; font-weight: 700; margin-top: 10px; color: #5eead4;"></div>
                        <button type="button" class="back-hub-btn" style="margin-top: 10px;" onclick="loadNextTriviaQuestion()">Next Question →</button>
                    </div>
                </div>
            </div>

            <!-- EXPANDABLE SUB-VIEW 4: THE HARBOR'S POSTING SPOT (WOOD LOG THEME) -->
            <div id="harborPostingSpotSection" class="hub-subview" style="border-color: #c28e5c; background: linear-gradient(135deg, rgba(62, 39, 22, 0.94), rgba(42, 26, 14, 0.96));">
                <div class="subview-header" style="border-bottom-color: rgba(194, 142, 92, 0.45);">
                    <div>
                        <div class="subview-title" style="color: #fde68a;">🪵 The Harbor Posting Board</div>
                        <div style="font-size: 0.76rem; color: #fef3c7;">Public postings — have something that made your journey a little easier? Pass on usable things and gear here.</div>
                    </div>
                    <button class="back-hub-btn" style="border-color: #fde68a; color: #fde68a;" onclick="closeHubSections()">✕ Close Board</button>
                </div>

                <div style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;">
                    <input type="text" id="gearSearchCode" class="dark-input" style="flex: 1; min-width: 200px; border-color: #c28e5c;" placeholder="Search by ZIP code or international mail code..." oninput="filterStormGear()">
                    <button class="back-hub-btn" style="border-color: #fde68a; color: #fde68a;" onclick="document.getElementById('gearSearchCode').value=''; filterStormGear();">Show All</button>
                </div>

                <form onsubmit="event.preventDefault(); postStormGear();" style="background: rgba(92, 58, 33, 0.55); padding: 12px; border-radius: 10px; border: 1px solid #c28e5c; margin-bottom: 12px;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #fde68a; margin-bottom: 8px;">+ Post Usable Gear or Helpful Item</div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 8px; margin-bottom: 8px;">
                        <input type="text" id="gearItemInput" class="dark-input" style="border-color: #c28e5c;" required placeholder="Usable gear or item description...">
                        <input type="text" id="gearPostalInput" class="dark-input" style="border-color: #c28e5c;" required placeholder="ZIP / Intl Mail Code">
                    </div>
                    <button type="submit" class="action-btn" style="background: #d97706; color: #ffffff; padding: 8px; font-size: 0.82rem; margin-top: 0;">Post to Harbor Posting Board</button>
                </form>

                <div id="stormGearList" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="tally-card gear-listing" data-postal="17976 PA" style="background: rgba(62, 39, 22, 0.75); border-color: #c28e5c;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #fde68a;">Sensory Compression Vest (Clean & Usable Condition)</strong>
                            <span class="finalist-tag">Mail Code: 17976</span>
                        </div>
                        <p style="font-size: 0.78rem; color: #fef3c7; margin-top: 4px;">Made our mornings easier — ready to pass on to another family.</p>
                        <div style="font-size: 0.7rem; color: #fcd34d; margin-top: 4px;">Posted by HopeWalker &bull; <a href="#" onclick="alert('Message sent to HopeWalker!'); return false;" style="color: #ffffff; text-decoration: underline;">Connect with Member</a></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. BECOME A MEMBER VIEW -->
        <div id="becomeMemberView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title" id="joinScreenTitle">Ready to join the Harbor? Share your walk of life. Step 1: Email Verification</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>
            <div class="mission-callout" id="joinCallout">
                Please remember this is a judgment-free zone and our only goal is to help other caregivers connect with caregivers who've already been through what they're getting ready to go through. Please be respectful.
            </div>
            
            <div id="verificationStep1">
                <form onsubmit="event.preventDefault(); if(!document.getElementById('judgmentFreeCheck').checked) { alert('Please check the box confirming you agree to be judgment-free.'); return; } document.getElementById('verificationStep1').style.display='none'; document.getElementById('verificationStep2').style.display='block'; alert('6-digit verification code sent to your email!');">
                    <div class="form-group" style="display: flex; align-items: center; gap: 10px; background: rgba(11, 46, 51, 0.4); padding: 10px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.3);">
                        <input type="checkbox" id="judgmentFreeCheck" style="width: 18px; height: 18px; accent-color: #5eead4; cursor: pointer;" required>
                        <label for="judgmentFreeCheck" style="font-size: 0.84rem; color: #ffffff; cursor: pointer; font-weight: 600;">I agree to be judgment-free and respectful.</label>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Caregiver Screen Name / Username</label>
                        <input type="text" id="regUsername" class="dark-input" required placeholder="e.g. HopeWalker">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email Address</label>
                        <input type="email" class="dark-input" required placeholder="you@example.com">
                    </div>
                    <button type="submit" class="action-btn">Send 6-Digit Verification Code</button>
                </form>
            </div>

            <div id="verificationStep2" style="display: none;">
                <form onsubmit="event.preventDefault(); completeMemberRegistration();">
                    <div class="form-group">
                        <label class="form-label">Enter 6-Digit Code Received in Email</label>
                        <input type="text" class="dark-input" required placeholder="123456" maxlength="6" value="123456">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Name</label>
                        <input type="text" id="regRealName" class="dark-input" required placeholder="e.g. Anthony">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Create Password</label>
                        <div class="password-wrapper">
                            <input type="password" id="regPasswordField" class="dark-input" required placeholder="••••••••">
                            <button type="button" class="show-pass-btn" onclick="togglePasswordVisibility('regPasswordField', this)">👁️ Show Password</button>
                        </div>
                    </div>
                    <button type="submit" class="action-btn">Complete Profile & Enter Harbor</button>
                </form>
            </div>
        </div>

        <!-- 3. DONOR / VISITOR & SPONSOR PORTAL VIEW -->
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
        </div>

        <!-- Footer Banner -->
        <div class="footer-banner">
            &copy; 2026 The Lewie & Marcus Network &bull; Share Your Walk (<a href="https://shareyourwalk.com" target="_blank" style="color: #5eead4; text-decoration: none;">shareyourwalk.com</a>) 🛡️
        </div>
    </div>
    
    <script>
        /* Show / Hide Password Toggle */
        function togglePasswordVisibility(inputId, btn) {
            const input = document.getElementById(inputId);
            if (input.type === 'password') {
                input.type = 'text';
                btn.innerText = '🙈 Hide Password';
            } else {
                input.type = 'password';
                btn.innerText = '👁️ Show Password';
            }
        }

        /* Active Visibility Toggle & Map-Legend Badges */
        let isMemberActive = true;
        function toggleActiveVisibility() {
            isMemberActive = !isMemberActive;
            const label = document.getElementById('visibilityLabel');
            const dot = document.getElementById('visibilityDot');
            if (isMemberActive) {
                label.innerText = 'Active to everyone';
                dot.style.background = '#4ade80';
                dot.style.boxShadow = '0 0 8px #4ade80';
            } else {
                label.innerText = 'Quiet / Away mode';
                dot.style.background = '#fbbf24';
                dot.style.boxShadow = 'none';
            }
        }

        function toggleLegendPopup() {
            document.getElementById('legendPopupBox').classList.toggle('active');
        }

        function promptAddBadgeCode() {
            const code = prompt("Enter a condition or caregiver code to generate its legend badge (e.g., DMD, Autism, Pediatric):");
            if (!code || !code.trim()) return;
            const clean = code.trim().toUpperCase();
            const row = document.getElementById('memberBadgeRow');
            const badge = document.createElement('span');
            badge.className = 'icon-legend-badge' + (clean === 'DMD' ? ' dmd-badge' : '');
            badge.title = clean;
            badge.innerText = clean === 'DMD' ? '🎗️ DMD' : '🏅 ' + clean;
            row.insertBefore(badge, row.querySelector('.legend-key-btn'));
        }

        /* Community Chat, Threaded Replies & Easy Attachments + Public Vote Opt-In */
        let currentReplyTo = null;
        let pendingAttachmentDataUrl = null;

        function setReplyTarget(authorName) {
            currentReplyTo = authorName;
            document.getElementById('replyTargetName').innerText = authorName;
            document.getElementById('replyBanner').style.display = 'block';
            document.getElementById('chatCaptionInput').focus();
        }

        function cancelReply() {
            currentReplyTo = null;
            document.getElementById('replyBanner').style.display = 'none';
        }

        function togglePasteMediaBox() {
            const box = document.getElementById('pasteMediaBox');
            box.style.display = box.style.display === 'none' ? 'block' : 'none';
        }

        function handleAttachmentSelected(input) {
            if (input.files && input.files[0]) {
                const file = input.files[0];
                document.getElementById('attachmentStatusLabel').innerText = '📎 Attached: ' + file.name;
                document.getElementById('publicVoteOptInBox').style.display = 'flex';
                const reader = new FileReader();
                reader.onload = function(e) { pendingAttachmentDataUrl = e.target.result; };
                reader.readAsDataURL(file);
            }
        }

        function handleMediaUrlTyped(input) {
            const val = input.value.trim();
            if (val) {
                pendingAttachmentDataUrl = val;
                document.getElementById('attachmentStatusLabel').innerText = '🔗 Media link attached';
                document.getElementById('publicVoteOptInBox').style.display = 'flex';
            } else {
                pendingAttachmentDataUrl = null;
                document.getElementById('attachmentStatusLabel').innerText = '';
                document.getElementById('publicVoteOptInBox').style.display = 'none';
            }
        }

        function postChatSubmission() {
            const captionInput = document.getElementById('chatCaptionInput');
            const optInCheck = document.getElementById('optInPublicVoteCheck');
            const text = captionInput.value.trim();
            if (!text && !pendingAttachmentDataUrl) return;

            const memberName = document.getElementById('dashMemberName').innerText || 'Anthony';
            const feed = document.getElementById('communityChatFeed');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'chat-msg';

            let replyIndicatorHTML = currentReplyTo
                ? `<div class="chat-reply-indicator">${memberName} replied to ${currentReplyTo}: ${text}</div>`
                : '';

            let mediaHTML = pendingAttachmentDataUrl
                ? `<img src="${pendingAttachmentDataUrl}" class="chat-photo-preview" alt="Attached media">`
                : '';

            let voteTagHTML = (pendingAttachmentDataUrl && optInCheck.checked)
                ? `<span class="finalist-tag" style="background: rgba(94, 234, 212, 0.22); border-color: #5eead4; color: #5eead4;">Entered in 24-Hr Daily Vote</span>`
                : `<span style="font-size: 0.7rem; color: #94a3b8;">Just now</span>`;

            msgDiv.innerHTML = `
                <div class="chat-msg-header">
                    <span>${memberName} 🧩🩺</span>
                    ${voteTagHTML}
                </div>
                ${replyIndicatorHTML}
                <div>${text}</div>
                ${mediaHTML}
                <div class="chat-btn-group">
                    <button class="reply-btn-mini" onclick="setReplyTarget('${memberName}')">↩️ Reply</button>
                </div>
            `;

            feed.prepend(msgDiv);
            captionInput.value = '';
            document.getElementById('chatMediaUrlInput').value = '';
            document.getElementById('chatFileUpload').value = '';
            document.getElementById('attachmentStatusLabel').innerText = '';
            document.getElementById('publicVoteOptInBox').style.display = 'none';
            optInCheck.checked = false;
            pendingAttachmentDataUrl = null;
            cancelReply();
        }

        /* Hub Sub-Views Navigation */
        function openHubSection(sectionId, defaultRecTab) {
            closeHubSections();
            const el = document.getElementById(sectionId);
            if (el) {
                el.classList.add('active');
                if (sectionId === 'recTimeSection' && defaultRecTab) {
                    switchRecTab(defaultRecTab);
                }
                el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }

        function closeHubSections() {
            ['seriousQuestionsSection', 'kidsCornerSection', 'recTimeSection', 'harborPostingSpotSection'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active');
            });
        }

        /* REC Time Tabs, 24-Hr Vote, Saturday Run-Off, & 100+ Trivia Bank */
        function switchRecTab(tab) {
            ['recTabVoteBtn', 'recTabFunnyBtn', 'recTabTriviaBtn'].forEach(id => document.getElementById(id).classList.remove('active'));
            ['recVotePanel', 'recFunnyPanel', 'recTriviaPanel'].forEach(id => document.getElementById(id).style.display = 'none');

            if (tab === 'vote') {
                document.getElementById('recTabVoteBtn').classList.add('active');
                document.getElementById('recVotePanel').style.display = 'block';
            } else if (tab === 'funny') {
                document.getElementById('recTabFunnyBtn').classList.add('active');
                document.getElementById('recFunnyPanel').style.display = 'block';
            } else {
                document.getElementById('recTabTriviaBtn').classList.add('active');
                document.getElementById('recTriviaPanel').style.display = 'block';
                loadNextTriviaQuestion();
            }
        }

        function voteForDailyPic(btn) {
            document.querySelectorAll('#dailyThreePicsGrid button').forEach(b => { b.disabled = true; b.style.opacity = '0.55'; });
            btn.style.opacity = '1';
            btn.innerText = '✓ 24-Hr Vote Cast!';
        }

        function voteSaturdayRunoff(btn, caregiverName) {
            alert('Your Saturday Run-Off vote for ' + caregiverName + ' has been recorded! Live totals remain hidden until the 10:00 PM reveal.');
            btn.innerText = '✓ Run-Off Vote Cast';
            btn.disabled = true;
        }

        /* Trivia Bank (Everyday Basics like Frying Eggs to Deep & Serious Questions) */
        const triviaBank = [
            { cat: "Everyday Kitchen Basics", q: "When frying an egg sunny-side up, what helps the whites set evenly without burning the bottom?", opts: ["Cranking the burner to max high", "Medium-low heat with a lid or gentle butter basting", "Adding cold water to the oil", "Stirring constantly with a whisk"], ans: 1 },
            { cat: "Deep & Serious Reflections", q: "In caregiving psychology, what is 'compassion fatigue'?", opts: ["Forgetting to take vitamins", "Physical and emotional exhaustion from prolonged caregiving without respite", "Sleeping too many hours", "Being allergic to hospital soap"], ans: 1 },
            { cat: "Everyday Life & Home", q: "What is the quickest way to neutralize lingering odors in a refrigerator?", opts: ["An open box of baking soda or activated charcoal", "Leaving the door open all night", "Spraying window cleaner inside", "Turning the fridge off"], ans: 0 },
            { cat: "Serious Medical & Care Knowledge", q: "Why is keeping an updated one-page Emergency Care Summary vital for pediatric or special-needs caregivers?", opts: ["It replaces health insurance", "It gives ER teams immediate baseline vitals, meds, and sensory/communication triggers", "It is only needed for air travel", "It lowers pharmacy prices"], ans: 1 },
            { cat: "Everyday Kitchen Basics", q: "Why should you let cooked meat rest for 5–10 minutes before slicing?", opts: ["To let it get completely cold", "So juices redistribute throughout the meat instead of running onto the board", "To make it harder to chew", "To evaporate the salt"], ans: 1 },
            { cat: "Serious Life & Resilience", q: "What makes peer-to-peer lived experience different from textbook advice?", opts: ["It comes from people who actually walked the storm in real time", "It is written by robots", "It ignores real-world emotions", "It only applies to doctors"], ans: 0 }
        ];
        let triviaScore = 0;
        let triviaAnswered = 0;
        let currentTriviaIdx = 0;

        function loadNextTriviaQuestion() {
            const item = triviaBank[currentTriviaIdx % triviaBank.length];
            currentTriviaIdx++;
            document.getElementById('recCategoryLabel').innerText = 'Category: ' + item.cat;
            document.getElementById('recQuestionText').innerText = item.q;
            document.getElementById('recFeedbackText').innerText = '';
            const box = document.getElementById('recOptionsBox');
            box.innerHTML = '';
            item.opts.forEach((opt, idx) => {
                const b = document.createElement('button');
                b.type = 'button';
                b.className = 'back-hub-btn';
                b.style.textAlign = 'left';
                b.style.padding = '8px 12px';
                b.innerText = opt;
                b.onclick = () => {
                    triviaAnswered++;
                    if (idx === item.ans) {
                        triviaScore++;
                        document.getElementById('recFeedbackText').style.color = '#4ade80';
                        document.getElementById('recFeedbackText').innerText = '✓ Spot on!';
                    } else {
                        document.getElementById('recFeedbackText').style.color = '#fb7185';
                        document.getElementById('recFeedbackText').innerText = 'Correct answer: ' + item.opts[item.ans];
                    }
                    document.getElementById('recScoreText').innerText = `🏆 Score: ${triviaScore} | Answered: ${triviaAnswered}`;
                    box.querySelectorAll('button').forEach(btn => btn.disabled = true);
                };
                box.appendChild(b);
            });
        }

        /* Kids Corner Post */
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
        }

        /* Serious Questions Cork Board */
        function postCorkBoardQuestion() {
            const topic = document.getElementById('corkTopicInput').value.trim();
            const desc = document.getElementById('corkDescInput').value.trim();
            if (!topic || !desc) return;
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';
            const feed = document.getElementById('corkBoardFeed');
            const note = document.createElement('div');
            note.className = 'cork-note';
            note.innerHTML = `
                <span class="cork-highlight-badge">${topic}</span>
                <div style="font-size: 0.86rem; color: #ffffff; font-weight: 600;">I have a question about: ${desc}</div>
                <div style="font-size: 0.72rem; color: #c7d2fe; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span>Pinned by ${member}</span>
                    <button class="reply-btn-mini" onclick="replyToCorkNote(this)">💬 Share Real Answer</button>
                </div>
            `;
            feed.prepend(note);
            document.getElementById('corkTopicInput').value = '';
            document.getElementById('corkDescInput').value = '';
        }

        function replyToCorkNote(btn) {
            const answer = prompt("Share what worked for you in this serious moment:");
            if (!answer || !answer.trim()) return;
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';
            const note = btn.closest('.cork-note');
            const replyBox = document.createElement('div');
            replyBox.className = 'chat-reply-indicator';
            replyBox.style.marginTop = '8px';
            replyBox.innerHTML = `<strong>${member} answered:</strong> ${answer.trim()}`;
            note.appendChild(replyBox);
        }

        /* Harbor Posting Board (Usable Gear + Mail Code Search) */
        function postStormGear() {
            const item = document.getElementById('gearItemInput').value.trim();
            const postal = document.getElementById('gearPostalInput').value.trim();
            if (!item || !postal) return;
            const member = document.getElementById('dashMemberName').innerText || 'Anthony';
            const list = document.getElementById('stormGearList');
            const card = document.createElement('div');
            card.className = 'tally-card gear-listing';
            card.setAttribute('data-postal', postal.toLowerCase());
            card.style.background = 'rgba(62, 39, 22, 0.75)';
            card.style.borderColor = '#c28e5c';
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #fde68a;">${item}</strong>
                    <span class="finalist-tag">Mail Code: ${postal}</span>
                </div>
                <p style="font-size: 0.78rem; color: #fef3c7; margin-top: 4px;">Usable gear posted to help make another family's journey a little easier.</p>
                <div style="font-size: 0.7rem; color: #fcd34d; margin-top: 4px;">Posted by ${member} &bull; <a href="#" onclick="alert('Message sent to ${member}!'); return false;" style="color: #ffffff; text-decoration: underline;">Connect with Member</a></div>
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

        /* Auth & View Switching */
        function completeMemberRegistration() {
            const realName = document.getElementById('regRealName').value.trim() || 'Anthony';
            document.getElementById('dashMemberName').innerText = realName;
            switchView('communityDashboardView');
        }

        function loginAsMember() {
            const enteredUser = document.getElementById('loginUserField').value.trim();
            if (enteredUser) {
                document.getElementById('dashMemberName').innerText = enteredUser;
            }
            switchView('communityDashboardView');
        }

        const adviceList = [
            { quote: "You don't have to weather the storm by yourself. Your lived experiences light the path for fellow caregivers walking right beside you.", author: "HopeWalker" },
            { quote: "Take one hour at a time when the storm hits hardest. You are never walking alone.", author: "CaregiverDan" },
            { quote: "Find your small daily victories and hold onto them tightly. They light the darkest paths.", author: "BeaconMom" }
        ];
        let currentAdviceIdx = 0;
        setInterval(() => {
            currentAdviceIdx = (currentAdviceIdx + 1) % adviceList.length;
            document.getElementById('sanctuaryQuoteText').innerText = `"${adviceList[currentAdviceIdx].quote}"`;
            document.getElementById('sanctuaryQuoteAuthor').innerText = `— ${adviceList[currentAdviceIdx].author}`;
        }, 6000);

        function switchView(viewId) {
            ['mainGatewayView', 'memberLoginView', 'communityDashboardView', 'becomeMemberView', 'donorVisitorView', 'tourView', 'missionVideoView'].forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    el.classList.remove('active');
                    if (id === 'mainGatewayView') el.classList.add('hidden');
                }
            });

            const bg = document.getElementById('communityBg');
            const overlay = document.getElementById('communityOverlay');
            const joinBg = document.getElementById('joinBg');
            const topHeader = document.getElementById('topHeaderGroup');

            if (viewId === 'mainGatewayView') {
                document.getElementById('mainGatewayView').classList.remove('hidden');
                bg.classList.remove('active');
                overlay.classList.remove('active');
                joinBg.classList.remove('active');
                topHeader.style.display = 'flex';
            } else {
                document.getElementById(viewId).classList.add('active');
                if (viewId === 'memberLoginView' || viewId === 'communityDashboardView') {
                    bg.classList.add('active');
                    overlay.classList.add('active');
                    joinBg.classList.remove('active');
                    topHeader.style.display = 'none';
                } else if (viewId === 'becomeMemberView') {
                    bg.classList.remove('active');
                    overlay.classList.remove('active');
                    joinBg.classList.add('active');
                    topHeader.style.display = 'flex';
                } else {
                    bg.classList.remove('active');
                    overlay.classList.remove('active');
                    joinBg.classList.remove('active');
                    topHeader.style.display = 'flex';
                }
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>
""")
print("FULL_DASHBOARD_UPDATED_SUCCESS")
