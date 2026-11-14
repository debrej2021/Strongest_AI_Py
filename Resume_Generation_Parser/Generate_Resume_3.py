import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()

# Configure margins for strict 3-page layout
for section in doc.sections:
    section.top_margin = Inches(0.4)
    section.bottom_margin = Inches(0.4)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

# Original document palette: Calibri + Navy Blue (#1F4E79)
NAVY_BLUE = RGBColor(31, 78, 121)
DARK_TEXT = RGBColor(30, 30, 30)

# Set document base style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(8.8)
style.font.color.rgb = DARK_TEXT

def add_header(name, title, contact, summary):
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1)
    r_name = p_name.add_run(name)
    r_name.font.size = Pt(15)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY_BLUE

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(1)
    r_title = p_title.add_run(title)
    r_title.font.size = Pt(9.5)
    r_title.font.bold = True
    r_title.font.color.rgb = DARK_TEXT

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_after = Pt(3)
    r_contact = p_contact.add_run(contact)
    r_contact.font.size = Pt(8.5)

    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.line_spacing = 1.05
    r_sum = p_sum.add_run(summary[0])
    r_sum.font.size = Pt(8.8)
    r_sum.font.italic = True
    r_bold = p_sum.add_run(summary[1])
    r_bold.font.size = Pt(8.8)
    r_bold.font.bold = True
    r_bold.font.italic = True

def add_section_heading(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1.5)
    run = p.add_run(title)
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = NAVY_BLUE

def add_role_heading(role, company, dates):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1)
    
    r1 = p.add_run(role + "  |  ")
    r1.font.bold = True
    r1.font.size = Pt(9)
    
    r2 = p.add_run(company + "  |  ")
    r2.font.bold = True
    r2.font.size = Pt(9)
    
    r3 = p.add_run(dates)
    r3.font.size = Pt(8.8)

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.2)
    p.paragraph_format.line_spacing = 1.05
    if bold_prefix:
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.bold = True
        r_bold.font.size = Pt(8.8)
    r_text = p.add_run(text)
    r_text.font.size = Pt(8.8)

def add_paragraph_text(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.size = Pt(8.8)

# ==================== BUILD RESUME ====================

# 1. Header
add_header(
    "DEBASHIS MOHAPATRA",
    "Senior Engineering Director  |  Enterprise Architect  |  AI, Platform & Cloud Transformation Leader",
    "debkiitian@gmail.com  |  +91-9731429550  |  LinkedIn: Debashis  |  GitHub: debrej2021  |  insights.debprod.com",
    (
        "Engineering Leader with 17 years of experience in SaaS, Cloud, and AI transformations — architecting scalable, secure, and data-driven platforms that drive business impact across healthcare, fintech, and product engineering. ",
        "Open to high-grade freelance engagements and permanent roles."
    )
)

# 2. Core Competencies
add_section_heading("CORE COMPETENCIES")
add_paragraph_text("Engineering Leadership  |  Cross-Functional Team Management  |  Strategic Technology Management  |  Cloud Engineering & DevOps  |  Observability & Telemetry  |  Data Engineering & AI  |  Agile Project Management  |  Cybersecurity & Risk Management  |  High-Impact Decision Making  |  Stakeholder & Vendor Management  |  Program & Portfolio Management  |  Digital Transformation  |  Organizational Scaling  |  Performance Optimization & Scalability")

# 3. Why Hire Me?
add_section_heading("WHY HIRE ME?")
add_bullet("17+ years of hands-on engineering leadership across healthcare, fintech, real estate, and manufacturing — building and scaling teams from 5 to 70, delivering production systems, not just roadmaps.")
add_bullet("AI architect who ships — designed and deployed HIPAA/FHIR-compliant GenAI platforms, agentic pipelines, and observability systems with real security guardrails across regulated enterprise environments.")
add_bullet("Equally strong in .NET 10, Python, and React — writing code, reviewing architecture, and mentoring engineers at every level. Technology-agnostic by conviction, .NET-native by depth.")
add_bullet("Founder-operator mindset — co-founded Worthum, delivered 10+ client solutions end-to-end, built accepted AI evaluation submissions, and independently shipped public technical assets and ML/AI demonstrations.")
add_bullet("System design at cloud scale — architects end-to-end distributed systems across AWS (EKS, Kinesis, Lambda, DynamoDB, S3) and Azure (AKS, Front Door, Azure AI, Service Bus), covering microservices, event-driven patterns, multi-tenant isolation, and cost-optimized infrastructure — whiteboard to production.")
add_bullet("Deep expertise in architectural decision patterns including graph traversal (BFS/DFS), dynamic programming, event-driven idempotent workflows, saga orchestration, and Graph RAG-backed knowledge systems used across fintech, healthcare, and industrial platforms.")

# 4. Profile Summary
add_section_heading("PROFILE SUMMARY")
add_paragraph_text("Engineering leader with 17+ years delivering scalable, secure, and AI-driven platforms across healthcare, fintech, and product engineering. Hands-on across the full stack — .NET 10 (AOT, Minimal APIs, EF Core, Vertical Slice), Python (AI inference, data pipelines, model training), and React — while leading teams of up to 70 and shaping technology roadmaps at the enterprise level. Architected HIPAA/FHIR/SOC 2-compliant cloud systems across AWS and Azure, integrating GenAI (GPT-4, LangChain, Transformers), vector retrieval, and observability into production platforms. Built AI-assisted Digital Twin and Industrial Intelligence architectures enabling real-time asset visualization, telemetry-driven anomaly detection, and predictive maintenance using graph-aware systems, sensor pipelines, and cloud-native event-driven platforms.")

# 5. Technical Skills
add_section_heading("TECHNICAL SKILLS")
add_bullet(".NET (6–10), C#, ASP.NET Core (Minimal APIs, Identity), AOT, Polly, EF Core 8/10, MediatR, Kafka, Redis, Ocelot, Scalar-OpenAPI; Python (Flask, FastAPI, Pandas, PyTorch, TensorFlow, OpenCV); React JS/TypeScript (Hooks, Redux), Angular, Node.js, GraphQL, Next.js (SSR/SEO)", "• Languages & Frameworks:")
add_bullet("AWS (EC2, S3, EKS, Lambda, DynamoDB, Kinesis, KMS, RDS, Neptune); Azure (App Services, Front Door, AKS, Azure AI, Functions, Cosmos DB, Key Vault, Azure DevOps); Vercel, Railway", "• Cloud Platforms:")
add_bullet("Claude Code, LangChain, LangGraph, GraphRAG, LangGraph multi-agent orchestration, Vector DBs (OpenSearch, Pinecone, FAISS, Milvus), GPT-4, ML.NET, PyTorch, TensorFlow, Scikit-learn, Azure ML Studio, Microsoft Foundry, Agentic pipelines, Prompt Evaluation, Zero-shot & ReAct reasoning", "• AI & ML:")
add_bullet("Kubernetes, Helm, Terraform, Jenkins, Azure DevOps, Ansible, Docker, .NET Aspire", "• DevOps & CI/CD:")
add_bullet("ASP.NET Core Auth, JWT, OAuth2, Policy-based Authorization, SIEM, Snyk, Veracode, OWASP, HIPAA, FHIR, SOC 2", "• Security & Compliance:")

# 6. Professional Experience
add_section_heading("PROFESSIONAL EXPERIENCE")

add_role_heading("Technology Consultant & Hands-On Engineering Practice", "Independent", "Dec 2025 – Present")
add_bullet("Built, benchmarked, and refined production-grade systems using Minimal APIs, AOT compilation, ASP.NET Core Identity, policy-based & resource-based authorization, and EF Core performance optimization. Shipped an auto interactive quiz generator — dynamic question generation with randomized answer shuffling — using Python/FastAPI on serverless AWS/Azure.")
add_bullet("Architecting, for a renowned Dubai-based EdTech client (under NDA), a bilingual Arabic-RTL / English-LTR AI-powered education marketplace and LMS — React PWA front-end over a Laravel (PHP 8) + MySQL 8 backend, delivered API-first: contract-first OpenAPI 3.x, OAuth 2.0/JWT stateless auth, and explicit versioning so the Phase 2 Flutter mobile apps reuse every endpoint unchanged.")
add_bullet("Designing the AI layer as a governed “AI Matrix” — Career Advisor, Skills-Gap Analysis, Resume Review, Learning-Path Generator, and bilingual Chatbot — each with per-feature cost caps, throttles, alerting dashboards, and safety guardrails, with generation grounded against provider and course content in both languages.")
add_bullet("Owning the platform architecture for GCC scale and compliance: Docker/Kubernetes with autoscaling to a 300,000-concurrent-user target (LMS video and AI load included), SCORM 1.2/2004 and xAPI-ready content delivery, SSO including UAE PASS, Tabby/Tamara + card payments with reconciliation, and UAE PDPL/GDPR data residency — ready for Gulf-wide institutional rollout.")
add_bullet("Specialist evaluator on a leading frontier-AI model-evaluation platform (production track) — running pairwise and multi-model comparisons and scoring frontier-model outputs on explicitly defined axes: correctness, grounding/faithfulness, instruction adherence, reasoning quality, safety, and production readiness — with calibrated rationales that survive adjudication. Consistently accepted submissions across C#, Python, system design, and agentic multi-step tool-calling tasks.")
add_bullet("Built and applied LLM-as-judge rubrics: defined the judging axes, wrote the scoring criteria, and validated judge-model verdicts against human golden labels — surfacing where automated judges drift from expert judgement on long agent traces and adversarial prompts.")
add_bullet("Recognized on the Numerical Solvers RL project; sharpened numerical-reasoning eval data via expert feedback on model limits.")
add_bullet("Contributed to the speech-transcription track (“Muse”) behind a recent model release from a top-tier MAANG AI lab — producing golden-benchmark transcription evaluations (aviation ATC audio, callsign verification, FAA formatting rules) used to validate speech-to-text behaviour before launch. A small role in a large release; every benchmark task cleared.")
add_bullet("Delivered high-impact AI engineering projects: (1) Payment Gateway Simulation — multi-tenant, high-throughput architecture with saga orchestration, idempotency guarantees, and event-driven reconciliation targeting 20%+ TCO reduction and 35% P95 latency improvement; (2) CAD Data Analysis using AI — computer vision pipeline for dimensional anomaly detection, design pattern classification, and structured report generation from industrial CAD files. Engineered OpenFOAM CFD simulation workflows complementing Digital Twin analysis of industrial assets. OpenFOAM & OpenSees C++ libraries driven via Python with AI analysis.")
add_bullet("Designed and evaluated production agentic pipelines using LangGraph multi-agent orchestration, tool-use patterns, memory injection, and ReAct reasoning loops — including failure mode analysis, hallucination guardrails, and evidence-based eval frameworks validated through accepted production evaluation submissions.")
add_bullet("Built a tool-calling ReAct agent from first principles in PyTorch — custom nn.Module (Embedding → RNN → Linear) trained to <0.05 loss, emitting a strict ACT:tool[arg] grammar that a regex controller routes to a Python tool registry; (logits, hidden) tuple returns carry recurrent state across autoregressive steps, with greedy argmax decoding for deterministic, parser-safe tool calls.")
add_bullet("Architected & delivered accepted OpenClaw AI engineering submission combining code-generation assessment, system design review, and production-readiness validation across resource-pooling, API exposure, environment rebuild, and regression-test scenarios.")

add_role_heading("Co-Founder & CTO", "Worthum Business Solutions (CIN: U72900DL2022PTC400369)", "Mar 2024 – Nov 2025")
add_bullet("Co-founded and scaled a product engineering startup, leading cross-functional teams to deliver cloud-native, GenAI, and full-stack solutions for 10+ clients across B2B, B2C, and D2C domains.")
add_bullet("Shipped an agentic AI co-pilot that automated key workflows, reducing resolution time and improving customer satisfaction.")
add_bullet("Built a multi-agent document pipeline (human-in-the-loop) that accelerated turnaround from days to hours and improved accuracy.")
add_bullet("Architected and deployed a Google MedLM-powered clinical intelligence layer — HIPAA-compliant document understanding, clinical entity extraction, and structured diagnostic reporting; cut manual clinical review ~25% with audit trails and RBAC.")
add_bullet("Optimized AI performance and costs through model routing, caching, and batching; established observability guardrails with OpenTelemetry; secured and retained 5 key clients in the first year.")
add_bullet("Rebuilt sensor-driven water meter architecture for accuracy and data quality; built React + Python demo and tooling front-ends.")

add_role_heading("Director – Engineering | India Engineering Head", "Upfront Healthcare (Acquired by HealthCatalyst)", "Oct 2023 – Mar 2024")
add_bullet("Directed engineering process transformation, implementing data resiliency, security, and resource management improvements — reducing operational costs by 30% while improving product scalability.")
add_bullet("Managed a high-performing team of 60–100 engineers; led intracloud migrations, DevOps automation, and HIPAA compliance.")
add_bullet("Led end-to-end design and deployment of a HIPAA-compliant MedLLM (GPT-3.5 + OpenAI) with vector-based retrieval (OpenSearch/Elasticsearch), cutting provider documentation time by ~30% and boosting patient adherence by 15–20%; delivered 15% increase in client IT investment.")
add_bullet("Integrated Azure AI Document Intelligence, increasing outreach by 70%; implemented FHIR + Azure BAA for 100% organizational compliance; optimized cloud infrastructure to achieve 99.9% uptime and reduce delivery cycles by 20%.")
add_bullet("Implemented .NET 6+ CAP (Common Application Platform) and schema-per-service segregation, improving response time by 30%; actively contributed React JS modules and .NET 8 APIs as reference implementations for junior engineers.")

add_role_heading("Sr. Manager – Software Engineering", "JLL (Jones Lang LaSalle)", "Feb 2022 – Sep 2023")
add_bullet("Managed 30+ engineers, streamlining delivery for SaaS products used by Amazon and Nike; lifted efficiency by 40%.")
add_bullet("Led migration of legacy systems to microservices, contributing to 30% reduction in operational costs; engineered scalable Apache Spark batch ETL workflows to cleanse, transform, and engineer geospatial property feature sets, training predictive real estate valuation models (Random Forest) that lifted user engagement by 50%.")
add_bullet("Engineered distributed Apache Spark (Spark Streaming / PySpark) data pipelines processing high-velocity MQTT IoT sensor streams across commercial facilities, feeding aggregated telemetry into real-time React + .NET dashboards with sub-second latency; boosted IoT sensor data throughput by 40% and aligned architectural priorities with the 4+1 view model.")

add_role_heading("Engineering Manager", "Koch Industries", "Apr 2020 – Feb 2022")
add_bullet("Managed cross-functional teams and key vendor partnerships (Wipro, Accenture, Deloitte) to drive digital transformation, enhancing operational efficiency by 30%.")
add_bullet("Led on-premise to AWS migration, reducing overhead by 30%; played a pivotal role in establishing a 300+ engineering Global Delivery Center, driving 30% increase in team productivity.")
add_bullet("Architected the Wipro-delivered migration of legacy .NET Framework monoliths to .NET Core microservices on AWS, streaming enterprise ERP transactional data directly into Infor Data Lake for unified reporting and downstream analytics — strangler-fig cutover, event-driven messaging, idempotent consumers, Redis caching and Polly resilience on stateless, auto-scaling nodes.")

add_role_heading("Engineering Manager", "Cliksource / Hyqoo", "Jul 2018 – Apr 2020")
add_bullet("Scaled an MVP into a revenue-generating enterprise product with 99% sprint success delivery rate; implemented monolith-to-microservices transformation using SAGA patterns.")

add_role_heading("Engineering Manager", "Accenture", "Aug 2013 – Jun 2018")
add_bullet("Led large-scale modernization projects for high-value clients (Pfizer, BMS, UBS), transforming legacy systems to cloud-native applications; established full-scale engineering team at Krakow, Poland.")
add_bullet("Designed the scalable ASP.NET Web API backend of an internal Accenture employee platform sized for 50,000+ users and 10,000+ concurrent sessions — stateless load-balanced nodes, distributed caching, async queues, read-replica SQL Server and load testing.")

# 7. Previous Work Experience
add_section_heading("PREVIOUS WORK EXPERIENCE")
p_prev1 = doc.add_paragraph()
p_prev1.paragraph_format.space_after = Pt(1)
r_p1 = p_prev1.add_run("Senior Developer — Global Services, Fiserv, Bangalore  |  Sep 2012 – Aug 2013")
r_p1.font.size = Pt(8.8)

p_prev2 = doc.add_paragraph()
p_prev2.paragraph_format.space_after = Pt(3)
r_p2 = p_prev2.add_run("Senior Developer / Developer — Mindtree Ltd. (LTIMindTree Now), Bangalore  |  Mar 2009 – Sep 2012")
r_p2.font.size = Pt(8.8)

# 8. Education
add_section_heading("EDUCATION")
p_edu = doc.add_paragraph()
p_edu.paragraph_format.space_after = Pt(3)
r_edu1 = p_edu.add_run("B.Tech. (Computer Science & Engineering)  |  Kalinga Institute of Industrial Technology (NIRF Rank 16)  |  2008")
r_edu1.font.size = Pt(8.8)
r_edu1.font.bold = True

# 9. Certifications & Trainings (Refined to Executive Tier)
add_section_heading("CERTIFICATIONS & TRAININGS")
add_bullet("Azure AI Engineer Associate (AI-102) – Microsoft®")
add_bullet("Herovired® & Microsoft® Certified – DevOps & Multi-Cloud Engineering (GenAI, LLM, Prompt Engineering)")
add_bullet("Certified Scrum Master (CSM) – Scrum Alliance")
add_bullet("Cloud & System Accreditations: AWS Certified | Microsoft Certified: Azure (AZ-900) | Data Resiliency with RabbitMQ – LinkedIn® | HackerRank Certified (C#, REST API)")

# 10. Recent Engineering Wins
add_section_heading("RECENT ENGINEERING WINS")
add_bullet("Won multiple pairwise coding evaluations on a specialist AI platform — ranking competing model-generated solutions on correctness, performance, and production readiness across C#, Python, and system-design tasks, with consistently accepted submissions.")
add_bullet("Engineered OpenFOAM CFD simulation pipelines for industrial Digital Twin platforms — automating mesh-to-solve-to-result workflows and feeding simulation outputs into telemetry-driven anomaly prediction and asset-health intelligence.")
add_bullet("Built Python data-document workflows with Pandas/CSV, Tesseract OCR, PDF-to-image extraction, and ReportLab PDFs. Applied asyncio queues/to_thread for I/O and ProcessPoolExecutor patterns for CPU work. Designed FastAPI/k6 10,000-user load simulations and PostgreSQL persistence for report and IoT data.")
add_bullet(".NET 8/10 production adoption using AOT-compiled Minimal APIs and MediatR pipelines — 35–55% P95 latency improvement, reduced cold-start times, and lower memory footprint on high-volume workloads.")
add_bullet("Shipped reach.debprod.com — a public missing-persons and distress-reporting platform — end-to-end: case intake, geo-tagged reports, and moderated escalation, built and operated independently.")
add_bullet("Built a DigiLocker/Setu OAuth-integrated PNG connection registration app on the Anthropic (Claude) API — government identity verification to completed registration in a single guided conversational flow.")
add_bullet("Delivered Azure AI Document Intelligence invoice and layout pipelines in both Python and C#, with a production scaling architecture for high-volume document ingestion.")
add_bullet("Built Microsoft Foundry and AWS Bedrock implementations — secure RAG, agents, MCP and AI-gateway labs, plus a .NET 10 + Python Bedrock integration with least-privilege IAM for banking use cases.")
add_bullet("EF Core 8/10 JSON columns implemented hands-on (ToJson() owned types, LINQ into nested JSON, flexible-schema migrations) plus compiled queries, bulk ops and schema-per-service — ~30% higher write throughput.")
add_bullet("API governance modernization using OpenAPI 3.1, YARP Gateway, rate limiting, and OpenTelemetry; implemented schema-per-service + CAP-based distributed transactions enforcing strict domain boundaries.")
add_bullet("Kaggle Submission: Gemma 4 – Diabetic Retinopathy Detection using production-grade evaluation pipelines and model validation workflows.")
add_bullet("Independently launched factcheck.debprod.com — a socio-economic analytics platform visualizing public data across demographic, policy, and economic indicators with production-grade frontend architecture.")
add_bullet("Designed interactive Digital Twin reference architecture for industrial assets using React + Three.js + telemetry pipelines, enabling click-based asset inspection, anomaly prediction, and sensor visualization.")
add_bullet("Published LinkedIn article series on AI reliability patterns: hallucination control, RAG/GraphRAG, evidence-based evaluation, and domain email security hardening (SPF/DKIM/DMARC).")

# 11. Leadership & Technical Highlights
add_section_heading("LEADERSHIP & TECHNICAL HIGHLIGHTS")
add_paragraph_text("Led multiple end-to-end modernization and validation programs across AWS and Azure — driving secure cloud adoption and operational efficiency improvements recognized through performance bonuses and leadership awards. Gained international experience in London and Krakow, establishing new business units and delivery models while mentoring multi-site teams. Spearheaded DevSecOps and Agile transformation initiatives across enterprises, embedding security and compliance into engineering culture. Built Centers of Excellence and Global Capability Centers to scale engineering maturity and foster high-performing, innovation-driven teams.")

# 12. Beyond Engineering
add_section_heading("BEYOND ENGINEERING")
add_paragraph_text("Former professional cricketer; still play competitive leather-ball cricket on weekends. The game taught me discipline, reading conditions and staying composed under pressure — habits that carry directly into leading engineering teams.")

# Save document
output_filename = "Debashis_Mohapatra_Executive_Refined.docx"
doc.save(output_filename)
print(f"Generated: {output_filename} (Calibrated for strict 3-page layout with refined certifications)")