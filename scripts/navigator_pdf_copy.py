"""September 2026 Navigator PDF copy: placement overrides + procurement questions.

Scoring notes come from index.html. Do not add FedRAMP/GovRAMP claims here
that are not already in the live product notes.
"""

# Custom placement rationales where the three-lens combo needs a buyer caveat.
RATIONALE = {
    "Microsoft Copilot": (
        "Copilot is a government-ready leader on buyability: GCC / GCC High paths and a "
        "dominant M365 estate put it far to the right, with deep capability. Impact is not a "
        "quick win — agents raise the ceiling only if grounding, records, and change management "
        "are in place. Independence is established-but-locked: leaving M365 after Copilot is "
        "the switching-cost story."
    ),
    "Gemini for Government": (
        "A government-ready leader where Workspace is already the system of work, with slightly "
        "less SLED gravity than Microsoft. Impact still depends on training and policy. "
        "Independence is Workspace-dependent and still catching Microsoft in most SLED offices."
    ),
    "Anthropic Claude": (
        "Claude sits with government-ready leaders on capability, with a clearer High path "
        "(Claude for Government) and a typical SLED path (Enterprise) that Anthropic itself "
        "distinguishes. Impact is API-or-chat rather than ERP-class. Multicloud options improve "
        "independence versus Azure-only stacks; SLED references still lag federal."
    ),
    "ChatGPT Enterprise (FedRAMP Moderate)": (
        "This is the OpenAI-managed Moderate SaaS — FedRAMP Certified 20x Moderate as of "
        "9 Jan 2026 (FR2533155773) in the live notes. It is not ChatGPT Gov and is not High. "
        "Impact is fast knowledge work on a restricted feature slice. Independence is a SaaS "
        "lock to OpenAI’s gov endpoint; commercial Enterprise workspaces do not convert in place."
    ),
    "ChatGPT Gov": (
        "ChatGPT Gov is the customer-hosted path (Azure commercial or Azure Government + Azure "
        "OpenAI). The August “High only via Azure” line described this path, not the Moderate "
        "SaaS. Readiness is lower because you own the ATO and ops. Impact complexity is the "
        "agency cloud. Independence carries Azure gravity."
    ),
    "Perplexity Enterprise for Government": (
        "FedRAMP Certified 20x Class B (Low) as of 1 Feb 2026 (FR2604643715) — Low, not Moderate "
        "or High. GSA MAS / OneGov is federal-first; SLED is a piggyback story in some states. "
        "Impact is cited research with a low implementation lift. Treat as a flexible but still "
        "thin SLED research layer, not a workflow platform."
    ),
    "AWS Bedrock": (
        "Bedrock is a government-ready platform pattern — multi-model access rather than a "
        "chatbot SKU. Confirm each model’s authorization boundary; it is not a blanket High. "
        "Impact tracks whatever the agency actually ships. Multi-model choice is the point; "
        "AWS gravity and glue-code rewrite cost are the lock-in."
    ),
    "Salesforce GovCloud": (
        "Strong where CRM is already Salesforce. Agentforce IL5 on Missionforce National Security "
        "(5 Aug 2026) is a national-security path in the live notes — not a SLED FedRAMP claim. "
        "Impact is citizen casework plus agents, not a chat widget. CRM + agent ecosystem lock-in "
        "is the independence story."
    ),
    "Tyler Technologies": (
        "Pure-play SLED: highest readiness on this map, ERP-class impact, and the deepest local-gov "
        "lock-in. AI is sold as governed public-sector features — no FedRAMP claim found on Tyler’s "
        "AI page in this edition. MyGov (2026) extends smaller agencies; core Tyler remains multi-year."
    ),
    "Esri": (
        "Default SLED GIS — government-ready, high impact when spatial is the work, deepest GIS "
        "lock-in in government. FedRAMP-authorized ArcGIS Online / enterprise cloud offerings are "
        "on Esri’s public compliance pages. Treat AI assistants as features of the authorized GIS, "
        "not a separate FedRAMP product unless Esri lists one."
    ),
    "Darwin AI": (
        "Q1 readiness is up this edition because of the April 2026 Carahsoft announcement "
        "(NASPO, TIPS, OMNIA) — that is a vehicle story, still not a FedRAMP claim. Impact is "
        "oversight and inventory, not resident services. Positioned as model-agnostic and still "
        "early in SLED."
    ),
    "Axon Draft One": (
        "New this edition. Easiest where Axon Evidence/BWC is already on the belt; 2026 local "
        "adoptions are named in the live notes. No FedRAMP claim is used here. Impact is officer "
        "time on narratives with required human review. Independence is Axon ecosystem gravity."
    ),
    "Flock Safety": (
        "Widely bought via OMNIA/Region 4 ESC cooperative R250203 — a cooperative buy is not "
        "FedRAMP. Impact is investigative speed where ALPR is lawful; community-trust cost can "
        "erase the gain (Madison-area non-renewals, 2026). Network effects and camera contracts "
        "make this established-but-locked; several agencies have found early exit expensive."
    ),
    "Ellucian AI": (
        "Dominant campus SIS vendor — buy is usually an existing Ellucian relationship, not a "
        "net-new SLED RFP. FERPA-oriented responsible-AI pages; no FedRAMP claim used here. "
        "Impact is student-lifecycle transformation if you actually move SIS. Banner/Colleague "
        "lock-in is the higher-ed equivalent of Tyler in cities."
    ),
    "UiPath Automation Cloud Public Sector": (
        "FedRAMP Certified Moderate (Class C) as of 20 Mar 2024 (FR2132958724). April 2026 "
        "public-sector notes add GenAI Activities via Integration Service; some Insights features "
        "remain outside the authorization until review completes. Impact is process redesign, not "
        "a chatbot. Platform lock-in once bots live here."
    ),
    "Appian Government Cloud": (
        "Appian Government Cloud — High: FedRAMP Certified Class D (High) as of 3 Apr 2025 "
        "(FR2318051429). AI skills inherit the GovCloud boundary; model pick is constrained on "
        "GovCloud inference profiles. High ceiling if you build on Appian; stronger federal than "
        "small-city SLED. Platform lock-in."
    ),
    "Zoom AI Companion": (
        "Verified gov path: FedRAMP JAB Moderate for AI Companion on Zoom for Government "
        "(16 Sep 2024). Commercial AI Companion is a different stack — buy the Gov SKU. Easy add "
        "where Zoom Gov is already the meeting system; narrow mission impact. Mature meetings "
        "ecosystem; AI is not a system of record."
    ),
    "Palantir AIP": (
        "Palantir stated Dec 2024 that FedRAMP High for Palantir Federal Cloud Service covers "
        "the suite including AIP. Federal-first; SLED references thinner than Tyler/Esri. High "
        "capability, procurement-heavy for most cities. Ontology lock-in is the independence "
        "story — plan the exit before the ontology becomes the city."
    ),
    "Laserfiche AI": (
        "Conditional add: deep SLED records/ECM install. Laserfiche AI uses OpenAI models per "
        "Laserfiche trust pages. Enterprise Security (6 Aug 2026) is on the GovRAMP Progressing "
        "list — not GovRAMP Ready/Authorized as of this edition. Do not treat progressing as "
        "authorized. AI rides existing repository lock-in."
    ),
    "CodeComply": (
        "AI plan review / pre-check for local permitting. Official plan-review layer for CivicPlus; "
        "also sits beside Accela/Tyler/OpenGov. TXShare cooperative endorsement. No FedRAMP claim "
        "used here. Narrow by design — does not replace the permitting system of record, and is "
        "easier to unwind than swapping Accela/Tyler."
    ),
}

QUESTIONS = {
    "Microsoft Copilot": [
        "Which Microsoft cloud is this tenant actually in (commercial, GCC, GCC High), and is Copilot licensed in that same cloud?",
        "Are Researcher/Analyst agents and Agent Builder in the authorized GCC/GCC High feature list you are buying, or only in commercial?",
        "Who owns grounding data, prompt logs, and retention — and do they meet your records schedule?",
        "What is the exit plan if you later constrain Copilot to a subset of agencies or roles?",
    ],
    "Gemini for Government": [
        "Is the agency already on Google Workspace, or is this a net-new productivity stack?",
        "Which Gemini for Government SKU is listed as FedRAMP Certified on the current FedRAMP AI page — and does your use stay inside that boundary?",
        "How will you handle records and e-discovery for Gemini output versus current Workspace logs?",
        "What is the migration cost if most of the workforce still lives in Microsoft 365?",
    ],
    "Anthropic Claude": [
        "Do you need Claude for Government (FedRAMP High standalone) or Claude Enterprise for typical state/local use, as Anthropic itself distinguishes?",
        "If you go through Bedrock GovCloud or Vertex Assured Workloads, which model IDs sit inside the authorized boundary?",
        "Where will prompts and outputs be stored, and who can export them?",
        "What happens to applications if you later switch foundation models?",
    ],
    "ChatGPT Enterprise (FedRAMP Moderate)": [
        "Confirm you are buying the OpenAI-managed FedRAMP Moderate SaaS (FR2533155773) — not ChatGPT Gov and not FedRAMP High.",
        "Will existing commercial Enterprise workspaces convert, or must you stand up a new gov tenant (OpenAI states they do not convert in place)?",
        "Is Carahsoft (or another reseller) on an existing cooperative, or is this a new vehicle?",
        "Which features are in the FedRAMP-restricted slice versus commercial Enterprise?",
    ],
    "ChatGPT Gov": [
        "Who owns the Azure subscription, ATO, and ongoing ops — this is customer-hosted, not OpenAI-managed High SaaS?",
        "Are you targeting Azure commercial or Azure Government, and which controls (IL5 / CJIS / FedRAMP High) are you actually pursuing?",
        "How does this path compare in cost and calendar to ChatGPT Enterprise Moderate SaaS?",
        "What is the records and identity model inside your Azure tenant?",
    ],
    "Perplexity Enterprise for Government": [
        "FedRAMP Certified 20x Class B (Low) as of 1 Feb 2026 (FR2604643715) — is Low sufficient for the data you will paste into it?",
        "Is your SLED path a GSA MAS piggyback, or do you lack a local vehicle?",
        "What sources does it cite, and can you disable web browse for sensitive drafting?",
        "What data is retained, and can you export conversation history?",
    ],
    "AWS Bedrock": [
        "Which foundation models are inside your GovCloud / FedRAMP High boundary — Bedrock is not a blanket High for every model?",
        "Who writes and owns the glue (agents, RAG, IAM), and what is the rewrite cost to leave AWS?",
        "How will you inventory which models staff actually invoke?",
        "What logging lands in CloudTrail versus the model provider?",
    ],
    "ServiceNow Gov": [
        "Are you buying AI on an existing Now Platform estate, or a greenfield ITSM replacement?",
        "Which OneGov / partner terms apply to the AI SKUs versus the platform?",
        "Will you redesign workflow, or bolt a chatbot onto unchanged tickets?",
        "What is the five-year exit and data-export plan from the Now Platform?",
    ],
    "Salesforce GovCloud": [
        "Is Agentforce in the GovCloud org you actually run, or only on Missionforce National Security (IL5 announced 5 Aug 2026 — not a SLED FedRAMP claim)?",
        "Are you already a Salesforce CRM shop, or is this a platform conversion?",
        "Who owns agent actions that write back to cases — audit trail, human approval, records?",
        "What is the cost to unwind CRM + agent ecosystem later?",
    ],
    "Tyler Technologies": [
        "Which Tyler suite (finance, permitting, public safety) would AI actually touch, and is it GA in that module?",
        "Tyler’s public AI page is not treated here as a FedRAMP claim — what authorization, if any, applies to the specific AI feature?",
        "How does the 2026 MyGov acquisition change scope for smaller agencies versus core Tyler?",
        "What are switching costs given Tyler’s SLED install base?",
    ],
    "Oracle Cloud Gov": [
        "Confirm the Fusion public-sector AI agent SKU sits inside the authorized sovereign/government cloud boundary before treating it as FedRAMP.",
        "Is this an ERP migration, an AI add-on, or both — and which is funded?",
        "Who owns integrations to the rest of the city’s systems of record?",
        "What is the realistic unwind from Oracle finance?",
    ],
    "SAP (Joule AI)": [
        "Are you already on S/4HANA Cloud, or is this a greenfield SLED SAP program?",
        "Which Joule features are in the tenant you can actually buy for government?",
        "What SLED references exist beyond general enterprise SAP?",
        "How will you staff a multi-year SAP + AI change program?",
    ],
    "Workday AI": [
        "Confirm government-cloud availability of any Copilot-for-HR pairing before buying that SKU — do not treat the HCM tenant as a FedRAMP shortcut.",
        "Is HCM data clean enough for workforce-planning AI to be true?",
        "What is the records treatment of AI-generated HR content?",
        "How portable are extensions if you leave Workday?",
    ],
    "CGI Advantage": [
        "Is this an AI feature on Advantage you already run, or a full ERP replacement?",
        "What is the implementation calendar, given AI is integration rather than a separate SLED copilot brand?",
        "Who owns customizations at the end of the contract?",
        "What is the data-conversion plan if you leave Advantage?",
    ],
    "OpenGov": [
        "Are you buying OG Assist / AI Review as modules, or the full AI-native Public Service Platform story?",
        "How does the Ignatius acquisition (Feb 2026) change the product you are signing?",
        "Who is accountable when AI Review disagrees with a plan reviewer?",
        "How sticky is finance once it lives on OpenGov?",
    ],
    "Accela": [
        "Is CivicAI generally available in the Accela modules you run (permitting, licensing, inspections)?",
        "What is auditable — model, prompt, reviewer override?",
        "Does this replace Accela as system of record, or sit on top of it?",
        "What is data portability versus swapping the permitting stack?",
    ],
    "CentralSquare": [
        "Is Centerline AI a standalone assistant add-on, or bundled with RMS/CAD you already own?",
        "Where does Blueline police-report writing store drafts, and who reviews before they become records?",
        "Which OMNIA/cloud vehicle and which modules are in this buy?",
        "What is the switching cost across the public-safety and admin suite?",
    ],
    "Esri": [
        "Are AI assistants a feature of FedRAMP-authorized ArcGIS Online / enterprise cloud, or a separate product Esri lists on its own?",
        "What spatial data will the assistant see, and is that appropriate for the cloud org you run?",
        "Who can disable assistant features per group without losing core GIS?",
        "What is the exit plan before you extend GIS lock-in further?",
    ],
    "Granicus GXA": [
        "Are you already on Granicus CMS/meetings, or is GXA a net-new civic suite?",
        "What can digital agents do in 311/content versus what still needs a human?",
        "What are the records and public-meeting implications of AI-drafted civic content?",
        "What is the unwind cost from the civic-experience platform?",
    ],
    "Citibot": [
        "Which cooperative vehicle (Carahsoft or other) are you using?",
        "What deflection rate is contractual versus marketed, and who owns the conversation data?",
        "What accessibility and language coverage exists for SMS and web?",
        "How easily can you replace a lightweight chatbot without stranding history?",
    ],
    "Polco AI (Polly)": [
        "Is the job community input or operations? This is not an operations system.",
        "What ICMA-grounded methodology is in the contract versus marketing?",
        "Who owns survey microdata, and can residents request deletion?",
        "How does this interoperate with your existing engagement stack?",
    ],
    "CivicPlus": [
        "Which CivicPlus products (web, meetings, engagement) would AI assist, and is it included or a separate SKU?",
        "Will this replace the civic stack or incrementally assist content?",
        "What peer references exist in your state among the 4K+ client install base?",
        "What is lock-in of the cloud suite versus a thinner CMS?",
    ],
    "PublicInput": [
        "What analytics are included versus professional services?",
        "How does install size compare to CivicPlus/Granicus for peer references you can call?",
        "What is the public-records treatment of comments and the data-export path?",
        "What are cancellation and data-deletion terms?",
    ],
    "Zencity": [
        "What changed after the Commonplace acquisition in the product you are buying?",
        "Can you export sentiment data, and is that written into the contract?",
        "How will you stop leadership from treating a dashboard as a resident census?",
        "Who is allowed to query the tool, and is that logged?",
    ],
    "Madison AI": [
        "Which role-specific assistants are in production at Washoe or other named references — can you speak to them?",
        "What cooperative vehicles exist today?",
        "Where do prompts and outputs live, and who can export them?",
        "How do you avoid a second shadow-IT copilot next to M365?",
    ],
    "Darwin AI": [
        "Carahsoft + NASPO/TIPS/OMNIA (Apr 2026) is a vehicle story — not a FedRAMP claim. What authorization, if any, applies?",
        "Is this governance and inventory of models, or resident-facing AI?",
        "Who maintains the AI inventory after go-live?",
        "Model-agnostic claims — can you swap monitored models without relicensing?",
    ],
    "Polimorphic": [
        "Vendor cites 200+ departments / 36M residents — which peers match your size, and can you call them?",
        "If VoiceAI becomes the front door, what is the CRM export and call-recording records schedule?",
        "How does this integrate with existing 311/CRM?",
        "What is lock-in if it becomes the intake layer for the organization?",
    ],
    "Just Appraised": [
        "Which assessor workflows are in scope (deeds, appeals, valuations)?",
        "Thin national vehicle story — how are you buying it?",
        "Who is liable for AI-assisted valuation recommendations?",
        "Where do parcel and owner data reside, and who can export them?",
    ],
    "Hayden AI": [
        "Hardware plus software — who owns cameras at end of term, and what is the take-down cost?",
        "Which transit-authority references match your operating environment?",
        "What is the evidence chain for enforcement actions?",
        "What are privacy, retention, and sharing rules for video?",
    ],
    "Cardinality.ai": [
        "Which HHS eligibility or case systems must it integrate with, and who pays for that work?",
        "AWS Gov partner messaging is not a blanket authorization — what is the actual ATO path?",
        "How are caseworker overrides logged?",
        "Which outcomes versus speed metrics are contractual?",
    ],
    "Mark43": [
        "This is RMS/CAD replacement energy, not a copilot. Is the agency resourced for that?",
        "Which of the 200+ agencies are similar CAD/RMS replacements in your state?",
        "What is the CJIS and records migration path from the incumbent (CentralSquare/Tyler)?",
        "What is data export if you later leave the cloud RMS?",
    ],
    "Forcemetrics": [
        "Fewer national vehicles than Axon/Flock — what is the procurement path?",
        "What source systems feed the analytics, and who owns data quality?",
        "What policy constraints apply to precision-policing analytics in your jurisdiction?",
        "Can you leave without losing historical analysis?",
    ],
    "Peregrine": [
        "Which agencies will actually share data, and is that in writing before you buy?",
        "This is an integration project. Who is the integrator of record?",
        "What live SLED references exist at your scale?",
        "How portable is the integration layer if you cancel?",
    ],
    "Axon Draft One": [
        "Is Axon Evidence/BWC already on the belt, or is this a bundled hardware + software conversion?",
        "2026 local adoptions (Pittsburg CA, Prescott AZ, Kenosha WI, Alamosa CO) — can you speak with a peer about review policy?",
        "No FedRAMP claim is used in this edition — what security review does your agency require?",
        "Who is the human reviewer of record, and can narratives ship without that review? What is the unbundle cost if reports depend on Draft One but you later leave Evidence?",
    ],
    "Flock Safety": [
        "Cooperative buy via OMNIA/Region 4 ESC R250203 is not FedRAMP. What privacy and data-sharing ordinance applies locally?",
        "What are retention, hotspot sharing, and audit of who queried plates?",
        "What is early-exit and camera-removal cost — several agencies have found exit expensive.",
        "Community-trust cost: Madison-area non-renewals in 2026 are part of the SLED story. How will you handle public records and challenge?",
    ],
    "Civic Marketplace": [
        "Free for SLED — what is the data use of your searches and staff accounts?",
        "MCP connectors into Claude, ChatGPT, and Copilot (24 Aug 2026) — which models will staff use, and is that allowed on your network?",
        "This is not a full e-procurement suite. What still lives in finance and inventory?",
        "NIGP Business Council membership is not a substitute for a local legal review of cooperative use.",
    ],
    "Ellucian AI": [
        "Are you an existing Banner/Colleague customer, or is this a net-new SIS RFP?",
        "Ellucian Student as an AI-native SIS+HCM+Finance line is a multi-year campus program — what is actually in this year’s scope?",
        "FERPA-oriented responsible-AI pages; no FedRAMP claim used here. What is the campus data classification for the AI features?",
        "Lock-in: this is the higher-ed equivalent of Tyler in cities. What is the exit?",
    ],
    "UiPath Automation Cloud Public Sector": [
        "FedRAMP Certified Moderate (Class C) as of 20 Mar 2024 (FR2132958724). Which Insights or GenAI Activities remain outside the authorization until review completes?",
        "April 2026 public-sector release notes add GenAI Activities via Integration Service — are those in your authorized tenant?",
        "FIPS 140-2 and U.S.-person ops are documented — does that match your policy?",
        "Bot and orchestration lock-in — what is the rewrite plan?",
    ],
    "Appian Government Cloud": [
        "Appian Government Cloud — High: FedRAMP Certified Class D (High) as of 3 Apr 2025 (FR2318051429). Confirm the AI skills you want inherit that GovCloud boundary.",
        "Model pick is constrained on GovCloud inference profiles — which models are actually available?",
        "A 3-year DoD IL5 PA is federal/DoD — not automatically a city ATO. What is your path?",
        "Who owns the process apps if you leave Appian?",
    ],
    "Zoom AI Companion": [
        "Buy the Zoom for Government SKU. Commercial AI Companion is a different stack. Which one is on the quote?",
        "FedRAMP JAB Moderate for AI Companion on Zoom for Government (16 Sep 2024). Confirm the AI Companion feature is in the authorized Zoom Gov account you own.",
        "Where are meeting summaries stored, and are they public records?",
        "This is an add-on, not a system of record. Who can disable it per meeting?",
    ],
    "Palantir AIP": [
        "Palantir stated Dec 2024 that FedRAMP High for Palantir Federal Cloud Service covers the suite including AIP. That is federal-first. What is the SLED vehicle and reference?",
        "Ontology lock-in: what is the exit before the ontology becomes the city?",
        "Who operates AIP day to day — Palantir, a partner, or city staff?",
        "What is integration and change-management cost versus a narrower tool?",
    ],
    "CodeComply": [
        "Official plan-review layer for CivicPlus; also sits beside Accela/Tyler/OpenGov. Which system of record will it attach to?",
        "TXShare cooperative endorsement — is that usable in your state?",
        "No FedRAMP claim used here. What is the data flow for building plans (often sensitive)?",
        "Who is liable when pre-check disagrees with the adopted code? Get unwind terms in the contract — this layer should be easier to leave than swapping Accela/Tyler.",
    ],
    "Laserfiche AI": [
        "Laserfiche AI uses OpenAI models per Laserfiche trust pages. Where does that inference run, and is it acceptable for your records?",
        "Enterprise Security (6 Aug 2026) is on the GovRAMP Progressing list — not GovRAMP Ready/Authorized as of this edition. Do not treat progressing as authorized.",
        "Which AI Agents (Apr 2026) features are in your SKU?",
        "Repository lock-in: AI rides the existing Laserfiche estate. What is the export plan?",
    ],
}

GENERIC_QUESTIONS = [
    "What system of record does this attach to, and who owns that integration?",
    "What is the written data-export and cancellation path?",
    "Which public-sector references match your size and mission, and can you call them?",
]
