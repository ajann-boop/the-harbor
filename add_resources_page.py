with open("templates/index.html", "r") as f:
    html = f.read()

# 1. Add CSS for the Resources & Foundations page
resources_css = """
        /* RESOURCES & FOUNDATIONS DEDICATED PAGE */
        .resources-screen {
            max-width: 1000px;
            background: linear-gradient(145deg, rgba(11, 46, 51, 0.95), rgba(15, 61, 68, 0.96));
            border: 2px solid #5eead4;
        }
        .resource-category-group {
            margin-top: 16px;
        }
        .resource-cat-header {
            font-size: 0.92rem;
            font-weight: 800;
            color: #fde047;
            border-bottom: 1px solid rgba(94, 234, 212, 0.28);
            padding-bottom: 5px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .resource-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 12px;
        }
        .resource-card {
            background: rgba(13, 56, 63, 0.78);
            border: 1px solid rgba(94, 234, 212, 0.4);
            border-radius: 12px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, border-color 0.2s;
        }
        .resource-card:hover {
            transform: translateY(-2px);
            border-color: #fde047;
        }
        .resource-org-name {
            font-size: 0.92rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 4px;
        }
        .resource-org-desc {
            font-size: 0.78rem;
            color: #cbd5e1;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        .resource-visit-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: rgba(94, 234, 212, 0.16);
            border: 1px solid #5eead4;
            color: #5eead4;
            font-size: 0.76rem;
            font-weight: 700;
            padding: 7px 12px;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.2s, color 0.2s;
        }
        .resource-visit-link:hover {
            background: #5eead4;
            color: #0b2e33;
        }
"""

html = html.replace("</style>", resources_css + "\n    </style>")

# 2. Add the "Resources & Foundations" card to the Community Hub horizontal Rolodex
target_hub_card = """                            <button type="button" class="fyi-btn fyi-wood" onclick="openHubSection('harborPostingSpotSection')">
                                <div>
                                    <div class="fyi-btn-title">🪵 Pass It On</div>
                                    <div class="fyi-btn-sub">Pay forward usable equipment, tools, and gear to ease another's journey.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem;">Open →</span>
                            </button>"""

new_hub_card = target_hub_card + """

                            <button type="button" class="fyi-btn" style="background: linear-gradient(135deg, rgba(13, 148, 136, 0.55), rgba(3, 105, 161, 0.65)); border-color: #fde047; color: #ffffff;" onclick="switchView('resourcesFoundationsView')">
                                <div>
                                    <div class="fyi-btn-title" style="color: #fde047;">🏛️ Resources &amp; Foundations</div>
                                    <div class="fyi-btn-sub">Official links to SSA, MDA, DMD, Autism &amp; caregiver support foundations.</div>
                                </div>
                                <span style="align-self: flex-end; font-size: 0.8rem; color: #fde047;">Open →</span>
                            </button>"""

if target_hub_card in html:
    html = html.replace(target_hub_card, new_hub_card)
else:
    print("WARNING: Could not locate Pass It On card in Community Hub Rolodex.")

# 3. Insert the dedicated Resources & Foundations page right after wallOfSeriousnessView
resources_page_html = """
        <!-- 1D. DEDICATED PAGE: RESOURCES & FOUNDATIONS -->
        <div id="resourcesFoundationsView" class="view-screen resources-screen">
            <div class="screen-header">
                <div>
                    <div class="screen-title" style="font-size: 1.35rem;">🏛️ Caregiver Resources &amp; Foundations</div>
                    <div style="font-size: 0.78rem; color: #cbd5e1;">Trusted national agencies, disability foundations, and direct caregiver support links.</div>
                </div>
                <button class="back-hub-btn" onclick="switchView('communityDashboardView')">← Back to Dashboard</button>
            </div>

            <!-- Live Search / Filter Bar -->
            <div style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;">
                <input type="text" id="resourceSearchInput" class="dark-input" style="flex: 1; min-width: 220px;" placeholder="Search foundations or topics (e.g., Social Security, SSA, MDA, DMD, Autism, Respite)..." oninput="filterResources()">
                <button type="button" class="back-hub-btn" onclick="document.getElementById('resourceSearchInput').value=''; filterResources();">Show All</button>
            </div>

            <!-- CATEGORY 1: SOCIAL SECURITY & GOVERNMENT BENEFITS -->
            <div class="resource-category-group">
                <div class="resource-cat-header">🇺🇸 Social Security &amp; National Benefits</div>
                <div class="resource-cards-grid">
                    <div class="resource-card resource-item" data-keywords="social security administration ssa ssi ssdi disability benefits">
                        <div>
                            <div class="resource-org-name">Social Security Administration (SSA)</div>
                            <div class="resource-org-desc">Official portal for Supplemental Security Income (SSI), Social Security Disability Insurance (SSDI), and pediatric disability benefit applications.</div>
                        </div>
                        <a href="https://www.ssa.gov/benefits/disability/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit ssa.gov ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="medicaid hcbs waivers home community services insurance">
                        <div>
                            <div class="resource-org-name">Medicaid Home &amp; Community-Based Services</div>
                            <div class="resource-org-desc">Information on state Medicaid waivers, in-home nursing support, and long-term care services for children and adults with disabilities.</div>
                        </div>
                        <a href="https://www.medicaid.gov/medicaid/home-community-based-services/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit medicaid.gov ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="usa.gov disability government grants housing assistance">
                        <div>
                            <div class="resource-org-name">USA.gov Disability Services</div>
                            <div class="resource-org-desc">Central directory for federal &amp; state disability programs, assistive technology grants, and caregiver tax credits.</div>
                        </div>
                        <a href="https://www.usa.gov/disability-services" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit usa.gov ↗</a>
                    </div>
                </div>
            </div>

            <!-- CATEGORY 2: MUSCULAR DYSTROPHY & RARE DISEASE FOUNDATIONS -->
            <div class="resource-category-group">
                <div class="resource-cat-header">🎗️ Muscular Dystrophy &amp; Rare Disease Foundations</div>
                <div class="resource-cards-grid">
                    <div class="resource-card resource-item" data-keywords="muscular dystrophy association mda dmd neuromuscular clinic">
                        <div>
                            <div class="resource-org-name">Muscular Dystrophy Association (MDA)</div>
                            <div class="resource-org-desc">Care center locator, resource center support, equipment assistance guidance, and neuromuscular family programs.</div>
                        </div>
                        <a href="https://www.mda.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit mda.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="parent project muscular dystrophy ppmd dmd duchenne clinical trials">
                        <div>
                            <div class="resource-org-name">Parent Project Muscular Dystrophy (PPMD)</div>
                            <div class="resource-org-desc">Dedicated specifically to Duchenne Muscular Dystrophy (DMD) care guidelines, emergency care cards, family connect groups, and research.</div>
                        </div>
                        <a href="https://www.parentprojectmd.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit parentprojectmd.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="nord national organization for rare disorders financial assistance">
                        <div>
                            <div class="resource-org-name">National Organization for Rare Disorders (NORD)</div>
                            <div class="resource-org-desc">Patient assistance programs, co-pay and travel grants, and rare disease advocacy resources for families.</div>
                        </div>
                        <a href="https://rarediseases.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit rarediseases.org ↗</a>
                    </div>
                </div>
            </div>

            <!-- CATEGORY 3: AUTISM & SPECIAL NEEDS FOUNDATIONS -->
            <div class="resource-category-group">
                <div class="resource-cat-header">🧩 Autism &amp; Special Needs Foundations</div>
                <div class="resource-cards-grid">
                    <div class="resource-card resource-item" data-keywords="autism society of america local affiliates sensory support">
                        <div>
                            <div class="resource-org-name">Autism Society of America</div>
                            <div class="resource-org-desc">National helpline, local community affiliates, sensory-friendly resources, and family advocacy across every stage of life.</div>
                        </div>
                        <a href="https://autismsociety.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit autismsociety.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="autism speaks resource guide tool kits iep">
                        <div>
                            <div class="resource-org-name">Autism Speaks Resource Guide</div>
                            <div class="resource-org-desc">State-by-state service directory, free parent tool kits, IEP advocacy guides, and sensory safety resources.</div>
                        </div>
                        <a href="https://www.autismspeaks.org/resource-guide" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit autismspeaks.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="understood iep 504 plan learning sensory school">
                        <div>
                            <div class="resource-org-name">Understood.org</div>
                            <div class="resource-org-desc">Practical templates and step-by-step guides for IEP meetings, 504 accommodations, and sensory/learning differences.</div>
                        </div>
                        <a href="https://www.understood.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit understood.org ↗</a>
                    </div>
                </div>
            </div>

            <!-- CATEGORY 4: CAREGIVER RESPITE & WELLBEING -->
            <div class="resource-category-group">
                <div class="resource-cat-header">⚓ Caregiver Respite &amp; Crisis Support</div>
                <div class="resource-cards-grid" id="customCommunityResourcesGrid">
                    <div class="resource-card resource-item" data-keywords="caregiver action network peer support toolbox">
                        <div>
                            <div class="resource-org-name">Caregiver Action Network (CAN)</div>
                            <div class="resource-org-desc">Free caregiver help desk, peer support forums, and practical toolboxes for family caregivers.</div>
                        </div>
                        <a href="https://www.caregiveraction.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit caregiveraction.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="arch national respite network locator break relief">
                        <div>
                            <div class="resource-org-name">ARCH National Respite Locator</div>
                            <div class="resource-org-desc">Find local respite care providers and state respite coalitions so family caregivers can get safe, reliable relief.</div>
                        </div>
                        <a href="https://archrespite.org/respitelocator" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit archrespite.org ↗</a>
                    </div>

                    <div class="resource-card resource-item" data-keywords="988 crisis lifeline mental health support 24/7">
                        <div>
                            <div class="resource-org-name">988 Suicide &amp; Crisis Lifeline</div>
                            <div class="resource-org-desc">Free, confidential 24/7 call or text support whenever the storm feels too heavy to carry alone.</div>
                        </div>
                        <a href="https://988lifeline.org/" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit 988lifeline.org ↗</a>
                    </div>
                </div>
            </div>

            <!-- Member Add-a-Foundation Box -->
            <form onsubmit="event.preventDefault(); addCommunityResourceLink();" style="margin-top: 18px; background: rgba(13, 56, 63, 0.75); border: 1px solid rgba(94, 234, 212, 0.4); border-radius: 12px; padding: 14px;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #5eead4; margin-bottom: 8px;">+ Add a Verified Foundation or Resource Link</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
                    <input type="text" id="newResOrgInput" class="dark-input" required placeholder="Foundation / Agency Name">
                    <input type="url" id="newResUrlInput" class="dark-input" required placeholder="https://example.org">
                </div>
                <input type="text" id="newResDescInput" class="dark-input" style="margin-bottom: 8px;" required placeholder="How does this resource help caregivers or families?">
                <button type="submit" class="action-btn" style="padding: 8px; font-size: 0.82rem; margin-top: 0;">Add Link to Resources Directory</button>
            </form>
        </div>
"""

html = html.replace("<!-- 2. BECOME A MEMBER VIEW -->", resources_page_html + "\n        <!-- 2. BECOME A MEMBER VIEW -->")

# 4. Register resourcesFoundationsView in switchView() and add search/add JS functions
html = html.replace(
    "'wallOfSeriousnessView', 'becomeMemberView'",
    "'wallOfSeriousnessView', 'resourcesFoundationsView', 'becomeMemberView'"
)

resources_js = """
        /* RESOURCES & FOUNDATIONS DIRECTORY LOGIC */
        function filterResources() {
            const q = document.getElementById('resourceSearchInput').value.trim().toLowerCase();
            document.querySelectorAll('.resource-item').forEach(card => {
                const kw = (card.getAttribute('data-keywords') || '').toLowerCase();
                const text = card.innerText.toLowerCase();
                card.style.display = (!q || kw.includes(q) || text.includes(q)) ? 'flex' : 'none';
            });
        }

        function addCommunityResourceLink() {
            const org = document.getElementById('newResOrgInput').value.trim();
            const url = document.getElementById('newResUrlInput').value.trim();
            const desc = document.getElementById('newResDescInput').value.trim();
            if (!org || !url || !desc) return;

            const grid = document.getElementById('customCommunityResourcesGrid');
            const card = document.createElement('div');
            card.className = 'resource-card resource-item';
            card.setAttribute('data-keywords', (org + ' ' + desc).toLowerCase());
            card.innerHTML = `
                <div>
                    <div class="resource-org-name">${org}</div>
                    <div class="resource-org-desc">${desc}</div>
                </div>
                <a href="${url}" target="_blank" rel="noopener noreferrer" class="resource-visit-link">Visit Resource ↗</a>
            `;
            grid.prepend(card);

            document.getElementById('newResOrgInput').value = '';
            document.getElementById('newResUrlInput').value = '';
            document.getElementById('newResDescInput').value = '';
        }
"""

html = html.replace("/* Show / Hide Password Toggle */", resources_js + "\n        /* Show / Hide Password Toggle */")

with open("templates/index.html", "w") as f:
    f.write(html)
print("RESOURCES_AND_FOUNDATIONS_PAGE_ADDED_SUCCESS")
