/* Case study content — sourced from verified GitHub repositories, READMEs, and my own account of each project.
   Figures that were actually measured are marked projected:false; modelled/estimated figures are projected:true. */
window.PROJECTS = [
  {
    id: "tempus",
    type: "simulated",
    category: "Strategy",
    question: "Can unstructured clinical data become usable intelligence?",
    title: "Tempus AI — Clinical Data Architecture & Agentic NLP Strategy",
    tags: ["Azure Databricks", "Apache Kafka", "ClinicalBERT", "MLflow"],
    approach: ["Audit data landscape", "Design Medallion Lakehouse", "Build agentic NLP pipeline", "Add MLflow governance"],
    data: "40M patient records across three post-acquisition platforms (Paige AI, Ambry Genetics, Deep6 AI), most of it sitting as unstructured clinical text rather than structured fields.",
    insight: [
      "Only 22% of the 40M records were AI-ready out of the box. The blocker was schema incompatibility, not data volume.",
      "A confidence-gated multi-agent pipeline (≥0.90 auto-accept, 0.70–0.89 human-in-the-loop) let extraction scale without sacrificing clinical accuracy.",
      "A 6-layer Bronze–Silver–Gold Lakehouse on Azure Databricks gave the three platforms a common structure for the first time."
    ],
    impact: { num: "$28M", desc: "projected 3-year NPV from lifting structured data coverage 22% → 50% across 40M records", projected: true },
    businessValue: "The real bottleneck in clinical AI readiness usually isn't compute or model choice. It's whether the data can be trusted enough to act on. Fix that, and everything downstream gets easier: research, partner audits, model training.",
    tech: ["Azure Databricks", "Apache Kafka", "ClinicalBERT", "Bio-BERT", "MLflow", "RAG"],
    github: null
  },
  {
    id: "proof-of-green",
    type: "academic",
    typeLabelOverride: "EY / Trinity MSc Industry Dissertation",
    category: "AI & ML",
    question: "Can an AI system tell a real environmental claim from a marketing slogan?",
    title: "Proof of Green — My MSc Dissertation on EU Greenwashing Law",
    tags: ["Regulatory Compliance", "Claude Haiku 4.5", "Gemini 2.5 Flash", "Prompt Engineering"],
    approach: [
      "Scrape SME websites for claims (Playwright)",
      "Extract every claim with Claude Haiku 4.5, EN/FR",
      "Cross-check 6 live certification registries",
      "Classify RED/AMBER/GREEN with an ECGT citation + fix"
    ],
    data: "267 real environmental claims, hand-labelled across 8 certified SMEs in Ireland and France, evaluated on a 248-claim leakage-free held-out test set. As far as we could establish, it's the first bilingual EN/FR evaluation dataset built specifically for ECGT compliance, checked against six live certification registries: B Corp, Bord Bia, EU Organic, BIOPARTENAIRE, BioED, and EMAS.",
    insight: [
      "25.8% of claims from companies that were already certified were still non-compliant under ECGT. A B Corp badge doesn't make a homepage tagline legal.",
      "Gemini 2.5 Flash scored a Macro F1 of 0.678 against Claude Haiku 4.5's 0.576 on the held-out set (76.6% vs 64.5% accuracy).",
      "Cross-model agreement was strong: Cohen's Kappa of 0.627. That mattered more to us than either score on its own, because it meant the classifications were coming from the ECGT rules themselves, not from one model's particular read of the language.",
      "97% of RED violations were plain marketing slogans with no specific environmental action behind them. GREEN was the hardest call to get right, which is exactly why the tool is built to flag risk for a human to review, not to certify compliance on its own."
    ],
    impact: { num: "25.8%", desc: "of claims from already-certified SMEs were still non-compliant with incoming EU rules, across 267 hand-labelled claims (248 held out for evaluation)", projected: false },
    businessValue: "This is my MSc dissertation, and honestly the project I'm proudest of. I worked on it with EY Ireland as our industry mentor from April to July 2026, with at least three EY and client-side stakeholders reviewing the work, and presented the findings to a room of 300+ people, which was terrifying and also the best part. The dashboard went through 8 reviewed versions before we landed on one EY was comfortable putting in front of a client. ECGT makes vague environmental marketing illegal across the EU from September 2026. We were careful to frame this as a compliance screener rather than an accusation: a RED label means a claim looks like something the law prohibits, not that the company lied on purpose. EY pushed us on that distinction over nine rounds of feedback. Early estimates suggest a tool like this could cut manual ESG screening time by roughly 30%, though that figure is an estimate from the pilot, not a measured client outcome. Supervised by Dr. Baidyanath Biswas at Trinity Business School, built with Tuna Cemal Erdem and Yifei Yu.",
    tech: ["Python", "Claude Haiku 4.5", "Gemini 2.5 Flash", "Playwright", "Streamlit", "6 live certification registry APIs", "TF-IDF + SVM baseline"],
    github: "https://github.com/sundusafreen/Proof-of-Green---ESG-Analysis"
  },
  {
    id: "sephora",
    type: "academic",
    category: "AI & ML",
    question: "Do negative reviews affect everyone equally?",
    title: "Sephora — Sentiment & Customer Segmentation",
    tags: ["Python", "BERT", "TF-IDF / LDA", "Logistic Regression"],
    approach: ["Baseline with Logistic Regression + TF-IDF", "Fine-tune BERT (bert-base-uncased)", "LDA topic modelling", "Segment by skin type, tone & price tier"],
    data: "519,409 Sephora product reviews (82% positive, 7.5% neutral, 10.4% negative), segmented afterward by skin type, skin tone, and price tier.",
    insight: [
      "Fine-tuned BERT lifted negative-class F1 to about 0.76, a big jump over the logistic regression baseline. That's the gap that actually matters when you're trying to catch real complaints in an imbalanced dataset.",
      "Darker and rich skin tones showed roughly 67% higher negative-review rates than fair tones (about 14–15% vs the overall 10–11%), an inclusivity gap hiding inside an otherwise fine-looking average rating.",
      "The worst-performing segment was budget-tier, dry-skin products at 12.3% negative. The best was premium, combination-skin products at 9%. Dissatisfaction tracked an expectation-vs-value mismatch more than price on its own.",
      "LDA topic modelling surfaced five recurring complaint themes: product efficacy, dryness and moisturisation, sensitive-skin reactions, texture and smell, and acne or slow results."
    ],
    impact: { num: "67%", desc: "higher negative-review rate for darker/rich skin tones than fair tones", projected: false },
    businessValue: "Sentiment alone hides which customers are underserved. Segmenting it turns 'reviews are mostly fine' into a specific list of fixes: reformulate for dry and sensitive skin, broaden shade ranges, and fix value perception with trial sizes instead of discounting everything.",
    tech: ["Python", "Scikit-learn", "Hugging Face Transformers (BERT)", "TF-IDF", "LDA"],
    github: "https://github.com/sundusafreen/sephora-review-sentiment-analysis"
  },
  {
    id: "insightiq",
    type: "personal",
    category: "AI & ML",
    question: "Can AI become a junior analyst?",
    title: "InsightIQ — AI Business Analyst",
    tags: ["Python", "Streamlit", "Groq / OpenAI / Gemini"],
    approach: ["Upload a CSV or Excel file", "Auto-generate KPI dashboard + charts", "Ask follow-up questions in plain English", "Export a structured report"],
    data: "Any CSV or Excel file a user uploads, with no fixed schema. Users bring their own API key for one of three LLM providers.",
    insight: [
      "A working product, not just a notebook: drag-and-drop upload, auto KPI cards, interactive charts, an AI chat layer with conversation memory, and export to Markdown, Word, and PDF.",
      "Supports three interchangeable LLM providers (Groq/Llama 3.3 70B, OpenAI GPT-4o Mini, Gemini 2.0 Flash), auto-detected from the API key prefix, so there's no provider dropdown and zero hosting cost since users bring their own key.",
      "The 'ask AI about your data' chat layer turned out to be the feature worth building: free-text business questions against the uploaded dataset, working like an on-demand junior analyst."
    ],
    impact: { num: "3", desc: "interchangeable LLM providers supported, auto-detected from the user's own API key, at zero hosting cost", projected: false },
    businessValue: "Most people who need a quick read on their data can't write SQL or Python. Getting this right meant thinking about UX, multi-provider LLM integration, and export formats a business user actually needs, not just training a model and calling it done.",
    tech: ["Python", "Streamlit", "Groq (Llama 3.3 70B)", "OpenAI GPT-4o Mini", "Gemini 2.0 Flash", "python-docx", "ReportLab"],
    github: "https://github.com/sundusafreen/business-insight-generator",
    liveDemo: "https://business-insight-generator-iznknezr5a6nf55athdudq.streamlit.app"
  },
  {
    id: "order-cancel",
    type: "academic",
    category: "Business Analytics",
    question: "What's actually driving order cancellations, and can it even be fixed?",
    title: "Order Cancellation Analytics — Chi-Square, Risk Segmentation & Pareto ROI",
    tags: ["Python", "SciPy", "Chi-Square Testing", "Pareto / ROI Modelling"],
    approach: ["Chi-square + Mann-Whitney U on transaction variables", "Build customer risk segmentation matrices", "Quantify revenue loss per segment", "Pareto-rank interventions by modelled ROI"],
    data: "20,000 electronics transactions (Sept 2023–Sept 2024) from a Kaggle electronics-sales dataset, tested across 9 categorical variables plus price.",
    insight: [
      "No transaction-level variable (product type, shipping, payment method, price band) significantly predicted cancellation, all p > 0.05. Cancellation isn't a transactional pattern. It's a behavioural one.",
      "Customer segmentation told the real story: loyalty members aged 36–50 cancelled at 34.1%, higher than non-loyalty peers in the same age band (32.8%). Loyalty wasn't working as a retention lever for this group.",
      "Non-loyalty customers aged 51+ represented over $12M in combined at-risk revenue, and 18–25 male customers showed the largest gender-based cancellation gap."
    ],
    impact: { num: "$4.8M", desc: "modelled annual revenue recovery from a four-intervention portfolio costing $30K combined, at conservative 15–25% recovery-rate assumptions. An estimate, not a realised result.", projected: true },
    businessValue: "When leakage looks diffuse, teams tend to fix everything a little instead of the few things that matter. Ruling out transaction-level causes first is what made the segment-level finding trustworthy enough to act on: a low-cost pre-cancellation confirmation popup was modelled to recover the largest share of the addressable revenue for the smallest spend.",
    tech: ["Python", "pandas", "SciPy (chi-square, Mann-Whitney U)", "matplotlib", "seaborn", "NumPy (Cramér's V)"],
    github: "https://github.com/sundusafreen/Order_cancellation_analysis"
  },
  {
    id: "churn",
    type: "academic",
    category: "Data Analytics",
    question: "Why are customers leaving, and can a model actually tell us?",
    title: "E-Commerce Customer Churn Prediction",
    tags: ["Python", "XGBoost", "Random Forest", "SHAP"],
    approach: ["EDA + Logistic Regression baseline", "Train Random Forest & XGBoost", "SHAP explainability per prediction", "Translate drivers into plain-language actions"],
    data: "A 2,000-customer Kaggle e-commerce churn dataset (24.6% overall churn rate), analysed by a 10-person Trinity College Dublin team. I was project manager and storyteller, translating the technical findings for a non-technical audience.",
    insight: [
      "Country and preferred product category were the strongest churn signals, though still weak ones: India (29.3%) and Pakistan (28.0%) by country, Home (28.6%) and Electronics (25.4%) by category.",
      "All three models (logistic regression, random forest, XGBoost) converged on a ROC-AUC of roughly 0.53, consistent with near-zero feature-churn correlation in this dataset. The honest finding was that the behavioural and account fields available here barely explain churn at all.",
      "That null result was still useful. It told the team to stop tuning models and start asking whether the dataset was missing the variables that actually drive churn, things like price sensitivity, service complaints, and competitor activity."
    ],
    impact: { num: "0.54", desc: "best model's ROC-AUC (XGBoost), a near-chance result reported honestly rather than overstated", projected: false },
    businessValue: "A churn score nobody trusts doesn't get acted on, and neither does a model that's quietly overstated to look better than it is. Reporting a weak result clearly, with SHAP explaining exactly why, is what makes the recommendation to gather better data credible instead of defensive.",
    tech: ["Python", "scikit-learn", "XGBoost", "SHAP", "imbalanced-learn"],
    github: "https://github.com/sundusafreen/Analytics_in_Practice_Group_7"
  },
  {
    id: "student-success",
    type: "academic",
    category: "Data Analytics",
    question: "Can we identify struggling students before it's too late?",
    title: "Student Performance Prediction",
    tags: ["R", "Logistic Regression", "Decision Trees"],
    approach: ["Clean & wrangle records (dplyr, tidyr)", "Exploratory analysis (ggplot2)", "Logistic regression + decision tree", "Validate with confusion matrix"],
    data: "6,378 student records across 19 behavioural and academic variables, analysed end-to-end in R.",
    insight: [
      "A logistic regression and decision tree pipeline predicted academic risk ahead of formal assessment checkpoints.",
      "Decision-tree visualisation made the risk logic readable by non-technical academic staff directly, without a data team translating it for them."
    ],
    impact: { num: "6,378", desc: "student records analysed to build an early-risk model instead of a post-mortem one", projected: false },
    businessValue: "An institution can only act early if the people closest to students, not just the data team, can understand and trust why a student was flagged. That's what made decision trees the right model choice here over something more accurate but harder to read.",
    tech: ["R", "dplyr", "tidyr", "ggplot2", "rpart", "caret"],
    github: "https://github.com/sundusafreen/Student-Success-analytics"
  },
  {
    id: "film",
    type: "academic",
    category: "Business Intelligence",
    question: "Can data help decide what films to make?",
    title: "Film Production Strategy — IMDb Analytics",
    tags: ["Python", "Tableau"],
    approach: ["Clean & filter IMDb metadata", "Genre, runtime & talent analysis", "Director/actor performance segmentation", "Build interactive Tableau dashboard"],
    data: "About 278,000 IMDb productions (2005–2025), movies only, after removing adult titles, missing ratings, and duplicates.",
    insight: [
      "Drama was the most consistently high-performing genre, and Drama + Sci-Fi/Action blends showed stronger engagement potential than either alone.",
      "Average film runtime increased over the period studied. The optimal window for stronger ratings and popularity was 95–110 minutes.",
      "Director-genre alignment ('hit zone' fit) improved outcome probability more than casting a big name alone. Pairing a recognisable lead with emerging supporting talent tracked well too."
    ],
    impact: { num: "278K+", desc: "IMDb productions analysed to turn genre, runtime and talent patterns into production strategy", projected: false },
    businessValue: "New production studios often lack historical performance benchmarks. This shows where data can narrow the field (genre focus, runtime target, director-genre fit) before creative judgment takes over. It's not a replacement for that judgment, just a better starting point for it.",
    tech: ["Python", "pandas", "Tableau"],
    github: "https://github.com/sundusafreen/imdb-film-production-strategy-analytics"
  },
  {
    id: "retail-dashboard",
    type: "personal",
    category: "Business Intelligence",
    question: "What does a sales team actually need to see, at a glance?",
    title: "Retail Sales Dashboard (Excel)",
    tags: ["Excel", "PivotTables", "XLOOKUP"],
    approach: ["Clean & enrich raw transaction data", "Build calculated KPI fields", "PivotTables + PivotCharts", "Design a slicer-driven dashboard"],
    data: "A retail transaction dataset cleaned and enriched inside Excel, documented step by step alongside the workbook.",
    insight: [
      "A practice exercise in the exact skillset behind real commercial reporting: XLOOKUP/INDEX-MATCH, SUMIFS-driven KPIs, and PivotTable-based dashboard design with slicers.",
      "Built as a self-contained Excel workbook with no external tools, so every formula and pivot is auditable by anyone who opens it."
    ],
    businessValue: "This mirrors the kind of KPI dashboard sales and account teams actually use week to week. I built it from scratch to show the same Excel-based reporting discipline behind real commercial KPI work, in a format anyone can open and check.",
    tech: ["Excel", "PivotTables", "PivotCharts", "XLOOKUP", "INDEX-MATCH", "SUMIFS"],
    github: "https://github.com/sundusafreen/Retail-Sales-Dashboard-Excel"
  },
  {
    id: "schneider-pricing",
    type: "professional",
    category: "Business Analytics",
    question: "How do you price and prioritise 100+ enterprise accounts across 13 industry verticals consistently?",
    title: "Territory Pricing, Target Framework & Market Sizing — Schneider Electric",
    tags: ["Market Sizing", "Pricing Strategy", "TAM Analysis"],
    approach: ["Map accounts across 13 verticals × 12+ product lines", "Build a territory pricing & target framework", "Size the Green Hydrogen + BESS opportunity", "Brief the framework to 5 internal teams"],
    data: "Enterprise account, contract, and margin data across 100+ accounts spanning 13 industry verticals and 12+ product lines, plus external market data for the Green Hydrogen and Battery Energy Storage Systems (BESS) opportunity assessment.",
    insight: [
      "Built a territory pricing and target framework covering €47.7M in scope, used by a 15-person commercial team to prioritise where to spend time.",
      "Sized a €45M total addressable market across Green Hydrogen and BESS, the two segments leadership needed a clear read on before committing resources.",
      "Closed revenue against this framework reached €675K in FY24 and €810K in FY25."
    ],
    impact: { num: "€47.7M", desc: "territory pricing and target framework built for a 15-person commercial team across 100+ enterprise accounts", projected: false },
    businessValue: "Pricing and targets that vary account by account are hard for a team to trust or move quickly on. One consistent framework across 13 verticals and 12+ product lines gave the commercial team a defensible way to prioritise deals, and gave leadership a single view of where the Green Hydrogen and BESS opportunity actually sat.",
    tech: ["Excel", "Salesforce", "Market sizing (TAM)", "Pricing & margin analysis"],
    github: null
  },
  {
    id: "schneider-kpi-dashboard",
    type: "professional",
    category: "Business Intelligence",
    question: "How do you cut a sales team's reporting prep from six hours to under thirty minutes?",
    title: "Sales KPI Dashboard — Salesforce to Tableau Reporting Transformation",
    tags: ["Salesforce", "Tableau", "KPI Design"],
    approach: ["Audit the existing manual Salesforce reporting workflow", "Design KPI logic with sales leadership", "Rebuild reporting as a Tableau dashboard", "Roll out and train the commercial team"],
    data: "Salesforce CRM data (opportunities, accounts, pipeline stages) for a commercial segment covering 100+ enterprise accounts.",
    insight: [
      "Manual reporting prep dropped from about six hours to under thirty minutes once the dashboard replaced manual Salesforce exports.",
      "Pipeline velocity and account engagement became leading indicators the team could see before quarter-end instead of after it.",
      "Opportunity capture rate at NTPC, one of the segment's largest accounts, reached over 90% during this period."
    ],
    impact: { num: "20%+", desc: "improvement in target-achievement efficiency after rollout, with reporting prep cut from about 6 hours to under 30 minutes", projected: false },
    businessValue: "A dashboard nobody opens doesn't change anything. Building this backwards from the weekly decisions sales managers actually needed to make, instead of from every metric Salesforce could export, is what got it adopted as the segment's standard reporting tool. It also coincided with a 15% improvement in account retention.",
    tech: ["Salesforce", "Tableau", "Excel"],
    github: null
  }
];
