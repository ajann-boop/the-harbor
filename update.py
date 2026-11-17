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

        .app-container { position: relative; z-index: 5; max-width: 980px; margin: 0 auto; padding: 16px 24px; min-height: 100vh; display: flex; flex-direction: column; justify-content: space-between; }
        
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
        @keyframes fadeInWelcome {
            0% { opacity: 0; transform: translateY(-10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .to-text { 
            font-size: 0.85rem; font-weight: 500; color: #e2e8f0; margin: 2px 0;
            text-shadow: 0 1px 4px rgba(0,0,0,0.85);
            opacity: 0; animation: fadeInTo 0.8s ease forwards; animation-delay: 0.9s;
        }
        @keyframes fadeInTo {
            0% { opacity: 0; transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        .harbor-title-container { 
            position: relative; display: flex; align-items: baseline; justify-content: center; margin-top: 4px;
            opacity: 0; animation: fadeInHarborContainer 0.8s ease forwards; animation-delay: 1.8s;
        }
        @keyframes fadeInHarborContainer {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .catty-the { 
            position: absolute; top: -14px; left: -10px; font-size: 0.92rem; font-weight: 700; color: #5eead4; 
            letter-spacing: 0.05em; text-transform: uppercase; transform: rotate(-6deg);
            text-shadow: 0 2px 5px rgba(0,0,0,0.9);
            display: flex; gap: 2px;
        }
        .letter-t { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.2s; }
        .letter-h-the { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.5s; }
        .letter-e-the { opacity: 0; animation: dropLetter 0.4s ease forwards; animation-delay: 2.8s; }
        @keyframes dropLetter {
            0% { opacity: 0; transform: translateY(-15px) rotate(-10deg); }
            100% { opacity: 1; transform: translateY(0) rotate(-6deg); }
        }

        .harbor-main-text { 
            font-size: 3rem; font-weight: 800; letter-spacing: 0.04em; line-height: 1.05;
            animation: medicalAwarenessGlow 6s infinite;
        }
        @keyframes medicalAwarenessGlow {
            0% { color: #38bdf8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            33% { color: #fb7185; text-shadow: 0 0 20px rgba(251, 113, 133, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            66% { color: #fde047; text-shadow: 0 0 20px rgba(253, 224, 71, 0.9), 0 2px 6px rgba(0,0,0,0.9); } 
            100% { color: #38bdf8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.9), 0 2px 6px rgba(0,0,0,0.9); }
        }

        .harbor-subtitle { font-size: 0.82rem; font-weight: 600; color: #5eead4; margin-top: 6px; letter-spacing: 0.02em; max-width: 420px; line-height: 1.3; text-align: center; text-shadow: 0 1px 5px rgba(0,0,0,0.95); }

        /* Gateway Entrance Box & Button */
        .gateway-entrance-wrapper {
            background: rgba(13, 56, 63, 0.14); border: 2px solid; 
            border-image: linear-gradient(90deg, #38bdf8, #f43f5e, #fbbf24, #a855f7) 1;
            padding: 14px 16px; border-radius: 14px; backdrop-filter: blur(5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.25); 
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            width: 100%; max-width: 320px; height: 160px;
            margin-top: 10px;
        }

        .cube-overlay-label { font-size: 0.65rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px; text-shadow: 0 1px 4px rgba(0,0,0,0.95); }

        .enter-harbor-btn { 
            background: rgba(11, 46, 51, 0.16); 
            border: 2px solid #38bdf8; padding: 10px 14px; border-radius: 12px; cursor: pointer; 
            transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            display: flex; flex-direction: column; align-items: center; gap: 4px; width: 100%; justify-content: center;
            backdrop-filter: blur(4px);
        }
        .enter-harbor-btn:hover { transform: translateY(-2px); border-color: #f43f5e; box-shadow: 0 8px 22px rgba(244, 63, 94, 0.4); background: rgba(15, 61, 68, 0.38); }
        .btn-anchor-icon { font-size: 1.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.9)); }
        .btn-text-group { text-align: center; display: flex; flex-direction: column; align-items: center; }
        .enter-main { font-size: 0.88rem; font-weight: 800; color: #ffffff; letter-spacing: 0.02em; line-height: 1.2; text-shadow: 0 1px 4px rgba(0,0,0,0.95); }

        /* Twin Buttons */
        .twin-buttons { display: flex; gap: 12px; width: 100%; max-width: 480px; justify-content: space-between; margin-top: 10px; }
        .twin-btn-pill { flex: 1; background: rgba(13, 56, 63, 0.28); border: 1px solid rgba(94, 234, 212, 0.45); padding: 12px 14px; border-radius: 50px; cursor: pointer; color: #ffffff; font-weight: 600; font-size: 0.74rem; backdrop-filter: blur(8px); transition: all 0.25s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; text-align: center; text-shadow: 0 1px 3px rgba(0,0,0,0.85); }
        .twin-btn-pill:hover { background: rgba(15, 61, 68, 0.55); border-color: #5eead4; transform: translateY(-2px); }

        /* View Screens */
        .view-screen { display: none; width: 100%; max-width: 720px; margin: 0 auto; background: rgba(11, 46, 51, 0.55); border: 1px solid rgba(94, 234, 212, 0.45); border-radius: 18px; padding: 25px; backdrop-filter: blur(14px); box-shadow: 0 15px 35px rgba(0,0,0,0.5); text-align: left; position: relative; z-index: 20; }
        .view-screen.active { display: block; }
        .screen-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }
        .screen-title { font-size: 1.3rem; font-weight: 700; color: #5eead4; }
        .close-btn { background: none; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; }
        .close-btn:hover { color: #ffffff; }
        
        .form-group { margin-bottom: 14px; }
        .form-label { display: block; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 5px; }
        .dark-input { width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 8px; border: 1px solid rgba(94, 234, 212, 0.45); background: rgba(11, 46, 51, 0.45); color: #ffffff; font-size: 0.9rem; outline: none; backdrop-filter: blur(10px); }
        .dark-input:focus { border-color: #5eead4; box-shadow: 0 0 0 3px rgba(94, 234, 212, 0.2); }
        .action-btn { width: 100%; background: #5eead4; color: #0b2e33; font-weight: 700; padding: 12px; border-radius: 8px; border: none; cursor: pointer; font-size: 0.95rem; transition: background 0.2s; margin-top: 8px; }
        .action-btn:hover { background: #2dd4bf; }
        
        .mission-callout { background: rgba(15, 61, 68, 0.65); border-left: 4px solid #5eead4; padding: 12px; border-radius: 0 8px 8px 0; font-size: 0.88rem; line-height: 1.45; color: #e2e8f0; margin-bottom: 16px; backdrop-filter: blur(10px); }
        
        /* Badge Selector Grid */
        .badge-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; margin-top: 6px; }
        .badge-option { background: rgba(11, 46, 51, 0.6); border: 1px solid rgba(94, 234, 212, 0.3); padding: 8px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; color: #cbd5e1; cursor: pointer; text-align: center; transition: all 0.2s; user-select: none; }
        .badge-option input { display: none; }
        .badge-option.selected { background: rgba(94, 234, 212, 0.25); border-color: #5eead4; color: #ffffff; box-shadow: 0 0 10px rgba(94, 234, 212, 0.3); }

        /* Top Header Quote Banner on Login Sanctuary */
        .sanctuary-quote-banner { 
            background: rgba(13, 56, 63, 0.65); border: 1.5px solid rgba(94, 234, 212, 0.5); 
            border-radius: 12px; padding: 12px 18px; margin-bottom: 16px; 
            backdrop-filter: blur(14px); box-shadow: 0 6px 20px rgba(0,0,0,0.4); 
            text-align: center; width: 100%;
        }
        .sanctuary-quote-text { font-size: 0.95rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 4px; }
        .sanctuary-quote-author { font-size: 0.75rem; font-weight: 600; color: #5eead4; }

        /* Weekly Photo Contest Winner Spotlight & Election Schedule Widget */
        .winner-spotlight-card { background: rgba(11, 46, 51, 0.6); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 12px; overflow: hidden; margin-top: 16px; padding: 14px; text-align: center; backdrop-filter: blur(12px); }
        .winner-spotlight-title { font-size: 1rem; font-weight: 700; color: #5eead4; margin-bottom: 2px; }
        .winner-spotlight-subtitle { font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
        .winner-img { width: 100%; height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 8px; border: 1px solid rgba(94, 234, 212, 0.3); }
        .winner-caption { font-size: 0.85rem; font-weight: 600; color: #ffffff; margin-bottom: 2px; }
        .winner-author { font-size: 0.78rem; color: #cbd5e1; }
        
        .contest-schedule-box { background: rgba(15, 61, 68, 0.5); border: 1px dashed rgba(94, 234, 212, 0.4); padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 0.78rem; color: #cbd5e1; text-align: left; }

        /* Sideways Spinning Rolodex & Threaded Dashboard Layout */
        .dashboard-screen { max-width: 940px; }
        .member-profile-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; background: rgba(13, 56, 63, 0.65); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 12px; padding: 12px 16px; margin-bottom: 16px; }
        .member-badge-pill { display: inline-block; background: rgba(94, 234, 212, 0.2); border: 1px solid #5eead4; color: #5eead4; font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 50px; margin-right: 4px; margin-top: 4px; }
        
        /* Sideways Wheel Rolodex */
        .sideways-rolodex-wrapper { margin-bottom: 16px; }
        .rolodex-wheel { display: flex; gap: 12px; overflow-x: auto; padding: 6px 2px 10px 2px; scroll-behavior: smooth; }
        .rolodex-wheel::-webkit-scrollbar { height: 6px; }
        .rolodex-wheel::-webkit-scrollbar-thumb { background: rgba(94, 234, 212, 0.4); border-radius: 4px; }
        
        .rolodex-category-card { min-width: 200px; background: rgba(13, 56, 63, 0.75); border: 1.5px solid rgba(94, 234, 212, 0.45); border-radius: 12px; padding: 12px; backdrop-filter: blur(12px); box-shadow: 0 6px 15px rgba(0,0,0,0.3); transition: transform 0.2s; cursor: pointer; flex-shrink: 0; }
        .rolodex-category-card:hover { transform: translateY(-3px); border-color: #5eead4; background: rgba(15, 61, 68, 0.85); }
        .rolodex-cat-title { font-size: 0.88rem; font-weight: 700; color: #5eead4; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
        .rolodex-cat-desc { font-size: 0.74rem; color: #cbd5e1; line-height: 1.35; }

        .dashboard-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; }
        @media (max-width: 768px) { .dashboard-grid { grid-template-columns: 1fr; } }
        .dash-panel { background: rgba(11, 46, 51, 0.65); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; }
        .panel-heading { font-size: 0.95rem; font-weight: 700; color: #5eead4; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }
        
        /* Threaded Community Chat */
        .chat-feed { max-height: 330px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px; padding-right: 4px; }
        .chat-msg { background: rgba(15, 61, 68, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px; font-size: 0.82rem; }
        .chat-msg-header { display: flex; justify-content: space-between; font-size: 0.74rem; color: #5eead4; font-weight: 700; margin-bottom: 4px; }
        .chat-reply-indicator { font-size: 0.72rem; color: #38bdf8; font-style: italic; margin-bottom: 4px; background: rgba(56, 189, 248, 0.12); padding: 4px 8px; border-radius: 4px; border-left: 2px solid #38bdf8; }
        .chat-photo-preview { width: 100%; height: 110px; object-fit: cover; border-radius: 6px; margin-top: 6px; border: 1px solid rgba(94, 234, 212, 0.3); }
        .chat-btn-group { display: flex; gap: 6px; margin-top: 6px; }
        .vote-btn-mini, .reply-btn-mini { background: rgba(94, 234, 212, 0.18); border: 1px solid #5eead4; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 50px; cursor: pointer; transition: all 0.2s; }
        .vote-btn-mini:hover, .reply-btn-mini:hover { background: #5eead4; color: #0b2e33; }
        
        .tally-card { background: rgba(15, 61, 68, 0.55); border: 1px solid rgba(94, 234, 212, 0.3); border-radius: 8px; padding: 10px; margin-bottom: 8px; font-size: 0.8rem; }
        .finalist-tag { background: rgba(251, 191, 36, 0.2); border: 1px solid #fbbf24; color: #fde047; font-size: 0.68rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }

        .video-container { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #000; border-radius: 12px; overflow: hidden; margin-bottom: 16px; border: 1px solid rgba(94, 234, 212, 0.3); }
        .video-container video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }

        .footer-banner { text-align: center; font-size: 0.78rem; color: #cbd5e1; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 10px; position: relative; z-index: 10; display: flex; align-items: center; justify-content: center; gap: 6px; }
    </style>
</head>
<body>
    <div class="mosaic-bg">
        {% for img in mosaic_images %}
        <img src="{{ url_for('static', filename='images/mosaic/' + img) }}" class="mosaic-tile" alt="Mosaic photo">
        {% endfor %}
    </div>
    <div class="mosaic-overlay"></div>

    <!-- Community Gathering Background for Login & Dashboard -->
    <img src="{{ url_for('static', filename='images/community_gathering.jpg') }}" id="communityBg" class="community-bg" alt="Community Gathering">
    <div id="communityOverlay" class="community-overlay"></div>

    <!-- Floating Jargon Background for Join View -->
    <div id="joinBg" class="join-bg">
        <div class="floating-term" style="left: 4%; animation-duration: 12s; animation-delay: 0s;">MD & Specialist Care</div>
        <div class="floating-term" style="left: 22%; animation-duration: 10s; animation-delay: 2s;">Cancer Survivor</div>
        <div class="floating-term" style="left: 42%; animation-duration: 11s; animation-delay: 1s;">Pediatric Caregiver</div>
        <div class="floating-term" style="left: 62%; animation-duration: 13s; animation-delay: 3.5s;">Adult Caregiver</div>
        <div class="floating-term" style="left: 78%; animation-duration: 12s; animation-delay: 1.5s;">Autism Meltdown Warrior</div>
        <div class="floating-term" style="left: 12%; animation-duration: 9s; animation-delay: 4s;">Storm Survivor</div>
        <div class="floating-term" style="left: 52%; animation-duration: 14s; animation-delay: 2.5s;">Respite & Hope</div>
        <div class="floating-term" style="left: 32%; animation-duration: 10.5s; animation-delay: 5s;">Lived Experience Beacon</div>
        <div class="floating-term" style="left: 88%; animation-duration: 11.5s; animation-delay: 0.5s;">Special Needs Advocate</div>
    </div>
    
    <div class="app-container">
        <!-- Top Header with Sanctuary Tagline on Left and Mission Button on Right -->
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

            <!-- Gateway Entrance Box -->
            <div class="gateway-entrance-wrapper">
                <div class="cube-overlay-label">Welcome back member</div>
                <button class="enter-harbor-btn" onclick="switchView('memberLoginView')">
                    <span class="btn-anchor-icon">⚓</span>
                    <span class="btn-text-group">
                        <span class="enter-main">MEMBERS WELCOME BACK TO THE HARBOR</span>
                    </span>
                </button>
            </div>

            <!-- Twin Action Buttons -->
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

        <!-- 1. MEMBER LOGIN VIEW -->
        <div id="memberLoginView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">Member Login & Sanctuary</div>
                <button class="close-btn" onclick="switchView('mainGatewayView')">&times;</button>
            </div>

            <!-- Top Header Quote Banner -->
            <div class="sanctuary-quote-banner">
                <div id="sanctuaryQuoteText" class="sanctuary-quote-text">"You don't have to weather the storm by yourself. Your lived experiences light the path for fellow caregivers walking right beside you."</div>
                <div id="sanctuaryQuoteAuthor" class="sanctuary-quote-author">— HopeWalker</div>
            </div>

            <form onsubmit="event.preventDefault(); loginAsMember();">
                <div class="form-group">
                    <label class="form-label">Member Email or ID</label>
                    <input type="text" id="loginUserField" class="dark-input" required placeholder="you@example.com" value="AnthonyJ" autocomplete="username">
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="dark-input" required placeholder="••••••••" value="••••••••" autocomplete="current-password">
                </div>
                <button type="submit" class="action-btn">Enter Caregiver Sanctuary</button>
            </form>

            <!-- Weekly Photo Contest Winner Spotlight & Voting Schedule Widget -->
            <div class="winner-spotlight-card">
                <div class="winner-spotlight-title">Weekly Photo Contest & Election Spotlight</div>
                <div class="winner-spotlight-subtitle">This week's approved winner:</div>
                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" class="winner-img" alt="Weekly Winner">
                <div class="winner-caption">Sunny Park Day Breakthrough</div>
                <div class="winner-author">Submitted by: Caregiver Sarah</div>
                
                <div class="contest-schedule-box">
                    <strong>📅 Contest Schedule & Election Rules:</strong>
                    <ul style="margin-top: 4px; padding-left: 16px;">
                        <li><strong>Mon / Wed / Fri:</strong> Daily tally selects top voted finalists from community chat submissions.</li>
                        <li><strong>Saturday:</strong> Election Day! Vote counts remain hidden until 10:00 PM EST.</li>
                        <li><strong>Opt-In:</strong> Check the "Submit for Public Vote" box in the Community Dashboard chat when sharing your photo.</li>
                    </ul>
                </div>
            </div>

            <div style="text-align: center; margin-top: 16px;">
                <a href="#" onclick="switchView('becomeMemberView'); return false;" style="color: #cbd5e1; font-size: 0.82rem; text-decoration: underline;">Not a member yet? Click here to join</a>
            </div>
        </div>

        <!-- 1B. MEMBER COMMUNITY DASHBOARD VIEW (SIDETRACK ROLODEX & THREADED CHAT) -->
        <div id="communityDashboardView" class="view-screen dashboard-screen">
            <div class="screen-header">
                <div class="screen-title">⚓ Caregiver Sanctuary Dashboard</div>
                <button class="close-btn" style="font-size: 0.82rem; color: #5eead4; border: 1px solid rgba(94, 234, 212, 0.4); padding: 4px 10px; border-radius: 6px;" onclick="switchView('mainGatewayView')">Sign Out</button>
            </div>

            <!-- Logged-In Member Profile Bar -->
            <div class="member-profile-bar">
                <div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #ffffff;">Welcome back, <span id="dashMemberName" style="color: #5eead4;">Anthony Jannuzzi</span></div>
                    <div style="font-size: 0.74rem; color: #cbd5e1;">Shenandoah, PA &bull; Storm Caregiver</div>
                    <div>
                        <span class="member-badge-pill">Autism Parent</span>
                        <span class="member-badge-pill">Pediatric Caregiver</span>
                        <span class="member-badge-pill">Storm Survivor</span>
                    </div>
                </div>
                <div style="text-align: right; font-size: 0.75rem; color: #5eead4;">
                    <div><strong>Status:</strong> Active Member</div>
                    <div style="color: #fde047;">Next Finalist Tally: Today</div>
                </div>
            </div>

            <!-- Sideways Spinning Wheel Rolodex -->
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
            </div>

            <div class="dashboard-grid">
                <!-- Left Column: Community Chat with Threaded Replies -->
                <div class="dash-panel">
                    <div>
                        <div class="panel-heading">
                            <span>💬 Community Chat & Public Vote</span>
                            <span style="font-size: 0.7rem; color: #cbd5e1;">Threaded Replies</span>
                        </div>
                        <div class="chat-feed" id="communityChatFeed">
                            <div class="chat-msg" id="msg-1">
                                <div class="chat-msg-header">
                                    <span>Caregiver Sarah</span>
                                    <span class="finalist-tag">Mon Finalist</span>
                                </div>
                                <div>Finally got a calm afternoon at the park without sensory overload!</div>
                                <img src="{{ url_for('static', filename='images/mosaic/park 20day.jpg') }}" class="chat-photo-preview" alt="Park Day">
                                <div class="chat-btn-group">
                                    <button class="vote-btn-mini" onclick="castDailyVote(this)">👍 Vote</button>
                                    <button class="reply-btn-mini" onclick="setReplyTarget('Caregiver Sarah')">↩️ Reply</button>
                                </div>
                            </div>
                            <div class="chat-msg" id="msg-2">
                                <div class="chat-msg-header">
                                    <span>BeaconMom</span>
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

                    <!-- Post to Chat with Public Vote Opt-In Checkbox -->
                    <form onsubmit="event.preventDefault(); postChatSubmission();" style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px; margin-top: 6px;">
                        <div id="replyBanner" style="font-size: 0.75rem; color: #38bdf8; margin-bottom: 4px; display: none;">Replying to <span id="replyTargetName"></span> <span onclick="cancelReply()" style="cursor:pointer; color:#f43f5e; margin-left:6px;">[&times; cancel]</span></div>
                        <input type="text" id="chatCaptionInput" class="dark-input" style="margin-bottom: 6px; font-size: 0.8rem;" required placeholder="Share a moment or reply...">
                        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; background: rgba(15, 61, 68, 0.5); padding: 5px 8px; border-radius: 6px;">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <input type="checkbox" id="optInPublicVoteCheck" style="width: 15px; height: 15px; accent-color: #5eead4; cursor: pointer;">
                                <label for="optInPublicVoteCheck" style="font-size: 0.72rem; color: #5eead4; font-weight: 600; cursor: pointer;">Opt-in for Public Vote (Daily Tally)</label>
                            </div>
                        </div>
                        <button type="submit" class="action-btn" style="padding: 8px; font-size: 0.8rem; margin-top: 0;">Post to Community Chat</button>
                    </form>
                </div>

                <!-- Right Column: Daily Vote Tally & Saturday Election Tracker -->
                <div class="dash-panel">
                    <div>
                        <div class="panel-heading">
                            <span>🗳️ Daily Tally & Saturday Election</span>
                        </div>
                        <div id="dailyTallyStatus" class="tally-card" style="border-left: 3px solid #5eead4;">
                            <strong style="color: #5eead4;">Active Daily Vote Tally</strong>
                            <p style="margin-top: 3px; color: #e2e8f0; line-height: 1.35; font-size: 0.76rem;">Mon, Wed, & Fri tallies advance finalists. Saturday elections keep votes hidden until 10:00 PM.</p>
                        </div>

                        <div class="tally-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <strong style="color: #fde047; font-size: 0.82rem;">Saturday Election Lineup</strong>
                                <span style="font-size: 0.65rem; background: rgba(244, 63, 94, 0.25); color: #fb7185; padding: 2px 5px; border-radius: 4px; font-weight: 700;">Hidden Till 10 PM</span>
                            </div>
                            <div id="finalistsList" style="display: flex; flex-direction: column; gap: 5px; font-size: 0.76rem;">
                                <div style="background: rgba(11, 46, 51, 0.6); padding: 6px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                                    <span>1. Caregiver Sarah (Mon)</span>
                                    <span style="color: #94a3b8; font-size: 0.7rem;">🔒 Hidden</span>
                                </div>
                                <div style="background: rgba(11, 46, 51, 0.6); padding: 6px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                                    <span>2. HopeWalker (Wed)</span>
                                    <span style="color: #94a3b8; font-size: 0.7rem;">🔒 Hidden</span>
                                </div>
                                <div style="background: rgba(11, 46, 51, 0.6); padding: 6px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                                    <span>3. Friday Slot (In Tally)</span>
                                    <span style="color: #5eead4; font-size: 0.7rem;">Active</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(13, 56, 63, 0.7); border: 1px solid rgba(94, 234, 212, 0.35); border-radius: 8px; padding: 8px; font-size: 0.72rem; color: #cbd5e1;">
                        🏆 <strong>10:00 PM Reveal:</strong> Saturday's winning finalist is automatically placed in the Welcome Spotlight!
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
                <form onsubmit="event.preventDefault(); if(!document.getElementById('judgmentFreeCheck').checked) { alert('Please check the box confirming you agree to be judgment-free.'); return; } document.getElementById('verificationStep1').style.display='none'; document.getElementById('verificationStep2').style.display='block'; alert('6-digit verification code sent to your email with return magic link!');">
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

            <!-- Step 2: Email Verified Magic Link / Profile Setup -->
            <div id="verificationStep2" style="display: none;">
                <div style="background: rgba(15, 61, 68, 0.7); padding: 12px; border-radius: 8px; margin-bottom: 14px; font-size: 0.85rem; color: #5eead4; backdrop-filter: blur(10px); border: 1px solid rgba(94, 234, 212, 0.4);">
                    ✓ Email verified successfully! Welcome back via your magic verification return link. Please complete your profile details below.
                </div>
                <form onsubmit="event.preventDefault(); completeMemberRegistration();">
                    <div class="form-group">
                        <label class="form-label">Enter 6-Digit Code Received in Email</label>
                        <input type="text" class="dark-input" required placeholder="123456" maxlength="6" value="123456">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Name</label>
                        <input type="text" id="regRealName" class="dark-input" required placeholder="e.g. Anthony Jannuzzi">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Location (City, State)</label>
                        <input type="text" id="regLocation" class="dark-input" required placeholder="e.g. Shenandoah, PA">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Years Dealing with Storm-Related Caregiving</label>
                        <input type="number" id="regStormYears" class="dark-input" min="0" max="50" required placeholder="e.g. 5">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Short Summary of Your Journey (Limited to 200 characters)</label>
                        <textarea id="regSummary" class="dark-input" rows="3" maxlength="200" required placeholder="Share a brief overview of your walk and storm experiences..."></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Select Your Caregiving Badges (Select all that apply)</label>
                        <div class="badge-grid" id="regBadgeGrid">
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Autism Parent">Autism Parent</label>
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Autism Caregiver">Autism Caregiver</label>
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Elderly Caregiver">Elderly Caregiver</label>
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Pediatric Caregiver">Pediatric Caregiver</label>
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Hospice Caregiver">Hospice Caregiver</label>
                            <label class="badge-option" onclick="toggleBadge(this)"><input type="checkbox" name="badges" value="Storm Survivor">Storm Survivor</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Create Password</label>
                        <input type="password" class="dark-input" required placeholder="••••••••">
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
                <strong>Welcome!</strong> Sponsorships, donations, and blessings are very much appreciated, needed, and usable. Thank you for supporting our mission. We're glad you took the time to visit.
            </div>

            <div style="margin-bottom: 16px;">
                <h4 style="color: #5eead4; margin-bottom: 6px; font-size: 1rem;">💡 How Your Support Helps:</h4>
                <ul style="list-style: disc; padding-left: 20px; font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                    <li>Sustaining real-time caregiver community infrastructure & support tools.</li>
                    <li>Providing shared resources and respite connection events for families.</li>
                    <li>Expanding the Lewie & Marcus Network outreach across communities.</li>
                </ul>
            </div>

            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
                <button class="action-btn" style="flex: 1;" onclick="alert('Thank you for your interest! Somebody from support@shareyourwalk.com will reach out to you via email within 1 to 2 business days, Monday through Friday, so you can connect comfortably by email.')">🤝 Are you interested in contributing?</button>
                <button class="twin-btn-pill" style="flex: 1; justify-content: center; margin-top: 8px;" onclick="switchView('tourView')">🧭 Take a Tour of The Harbor</button>
            </div>
        </div>

        <!-- 4. TOUR OF THE HARBOR VIEW -->
        <div id="tourView" class="view-screen">
            <div class="screen-header">
                <div class="screen-title">Explore The Harbor & Mission Tour</div>
                <button class="close-btn" onclick="switchView('donorVisitorView')">&times;</button>
            </div>
            <div style="font-size: 0.88rem; line-height: 1.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 10px;">
                <div style="background: rgba(15, 61, 68, 0.4); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <strong style="color: #5eead4;">1. The Caregiver Sanctuary</strong>
                    <p style="margin-top: 3px;">A safe, verified online hub where caregivers find peers who truly understand the daily triumphs and hurdles.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.4); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <strong style="color: #5eead4;">2. Lived & Learned Experience Sharing</strong>
                    <p style="margin-top: 3px;">Members connect through shared walks, real-time community boards, and mutual encouragement without judgment.</p>
                </div>
                <div style="background: rgba(15, 61, 68, 0.4); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <strong style="color: #5eead4;">3. Sponsor & Organization Impact</strong>
                    <p style="margin-top: 3px;">For foundations and businesses looking to partner: every contribution directly strengthens caregiver resilience and family support networks.</p>
                </div>
            </div>
            <button class="action-btn" style="margin-top: 16px;" onclick="switchView('donorVisitorView')">Back to Donor Portal</button>
        </div>

        <!-- Footer Banner with Shield -->
        <div class="footer-banner">
            &copy; 2026 The Lewie & Marcus Network &bull; Share Your Walk (<a href="https://shareyourwalk.com" target="_blank" style="color: #5eead4; text-decoration: none;">shareyourwalk.com</a>) 🛡️
        </div>
    </div>
    
    <script>
        let currentReplyTo = null;

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

        function postChatSubmission() {
            const captionInput = document.getElementById('chatCaptionInput');
            const optInCheck = document.getElementById('optInPublicVoteCheck');
            const text = captionInput.value.trim();
            if (!text) return;

            const memberName = document.getElementById('dashMemberName').innerText || 'Anthony J.';
            const feed = document.getElementById('communityChatFeed');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'chat-msg';

            let replyIndicatorHTML = '';
            if (currentReplyTo) {
                replyIndicatorHTML = `<div class="chat-reply-indicator">${memberName} replied to ${currentReplyTo}: ${text}</div>`;
            }

            if (optInCheck.checked) {
                msgDiv.innerHTML = `
                    <div class="chat-msg-header">
                        <span>${memberName}</span>
                        <span class="finalist-tag" style="background: rgba(94, 234, 212, 0.25); border-color: #5eead4; color: #5eead4;">In Daily Vote Tally</span>
                    </div>
                    ${replyIndicatorHTML}
                    <div>${text}</div>
                    <div class="chat-btn-group">
                        <button class="vote-btn-mini" onclick="castDailyVote(this)">👍 Vote</button>
                        <button class="reply-btn-mini" onclick="setReplyTarget('${memberName}')">↩️ Reply</button>
                    </div>
                `;
            } else {
                msgDiv.innerHTML = `
                    <div class="chat-msg-header">
                        <span>${memberName}</span>
                        <span style="font-size: 0.7rem; color: #94a3b8;">Just now</span>
                    </div>
                    ${replyIndicatorHTML}
                    <div>${text}</div>
                    <div class="chat-btn-group" style="margin-top: 6px;">
                        <button class="reply-btn-mini" onclick="setReplyTarget('${memberName}')">↩️ Reply</button>
                    </div>
                `;
            }

            feed.prepend(msgDiv);
            captionInput.value = '';
            optInCheck.checked = false;
            cancelReply();
        }

        function castDailyVote(btn) {
            btn.innerText = '✓ Voted';
            btn.style.background = '#5eead4';
            btn.style.color = '#0b2e33';
            btn.disabled = true;
        }

        function completeMemberRegistration() {
            const realName = document.getElementById('regRealName').value.trim() || 'Member';
            document.getElementById('dashMemberName').innerText = realName;
            alert('Profile saved! Entering Caregiver Sanctuary Dashboard...');
            switchView('communityDashboardView');
        }

        function loginAsMember() {
            const enteredUser = document.getElementById('loginUserField').value.trim();
            if (enteredUser) {
                document.getElementById('dashMemberName').innerText = enteredUser;
            }
            switchView('communityDashboardView');
        }

        function toggleBadge(label) {
            const checkbox = label.querySelector('input');
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                label.classList.add('selected');
            } else {
                label.classList.remove('selected');
            }
        }

        const adviceList = [
            { quote: "You don't have to weather the storm by yourself. Your lived experiences light the path for fellow caregivers walking right beside you.", author: "HopeWalker" },
            { quote: "Take one hour at a time when the storm hits hardest. You are never walking alone.", author: "CaregiverDan" },
            { quote: "Find your small daily victories and hold onto them tightly. They light the darkest paths.", author: "BeaconMom" }
        ];
        let currentAdviceIdx = 0;
        function rotateSanctuaryQuote() {
            currentAdviceIdx = (currentAdviceIdx + 1) % adviceList.length;
            const item = adviceList[currentAdviceIdx];
            document.getElementById('sanctuaryQuoteText').innerText = `"${item.quote}"`;
            document.getElementById('sanctuaryQuoteAuthor').innerText = `— ${item.author}`;
        }
        setInterval(rotateSanctuaryQuote, 6000);

        function switchView(viewId) {
            document.getElementById('mainGatewayView').classList.add('hidden');
            document.getElementById('memberLoginView').classList.remove('active');
            document.getElementById('communityDashboardView').classList.remove('active');
            document.getElementById('becomeMemberView').classList.remove('active');
            document.getElementById('donorVisitorView').classList.remove('active');
            document.getElementById('tourView').classList.remove('active');
            const videoView = document.getElementById('missionVideoView');
            if (videoView) videoView.classList.remove('active');

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
                document.getElementById('verificationStep1').style.display = 'block';
                document.getElementById('verificationStep2').style.display = 'none';
                document.getElementById('joinScreenTitle').innerText = "Ready to join the Harbor? Share your walk of life. Step 1: Email Verification";
                document.getElementById('joinCallout').style.display = 'block';
                const vid = document.querySelector('video');
                if (vid) vid.pause();
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

                if (viewId === 'missionVideoView') {
                    const vid = document.querySelector('video');
                    if (vid) { vid.currentTime = 0; vid.play(); }
                }
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>
""")
print("LAYOUT_RESTORED_SUCCESS")
