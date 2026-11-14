import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()

# Exact original margins
for section in doc.sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.55)
    section.right_margin = Inches(0.55)

# Original Document Navy Blue Palette: #1F4E79 (RGB: 31, 78, 121)
ORIGINAL_NAVY = RGBColor(31, 78, 121)
DARK_TEXT = RGBColor(26, 26, 26)
GRAY_DATES = RGBColor(85, 85, 85)

# Set base font to Calibri
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(9.5)
style.font.color.rgb = DARK_TEXT

def add_header(name, title, contact):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    
    r_name = p.add_run(name + "\n")
    r_name.font.size = Pt(16)
    r_name.font.bold = True
    r_name.font.color.rgb = ORIGINAL_NAVY
    
    r_title = p.add_run(title + "\n")
    r_title.font.size = Pt(10)
    r_title.font.bold = True
    r_title.font.color.rgb = DARK_TEXT
    
    r_contact = p.add_run(contact)
    r_contact.font.size = Pt(9)
    r_contact.font.color.rgb = DARK_TEXT

def add_section_title(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(title)
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = ORIGINAL_NAVY

def add_role_title(role, company, dates):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(1)
    
    r1 = p.add_run(role + " | ")
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    
    r2 = p.add_run(company + " | ")
    r2.font.bold = True
    r2.font.size = Pt(9.5)
    
    r3 = p.add_run(dates)
    r3.font.italic = True
    r3.font.color.rgb = GRAY_DATES
    r3.font.size = Pt(9)

def add_bullet(lead, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.08
    r_lead = p.add_run(lead + " ")
    r_lead.font.bold = True
    r_lead.font.size = Pt(9)
    r_text = p.add_run(text)
    r_text.font.size = Pt(9)

# Build Document
add_header(
    "DEBASHIS MOHAPATRA",
    "Senior Engineering Director | Enterprise Architect | AI, Platform & Cloud Transformation Leader",
    "debkiitian@gmail.com | +91-9731429550 | LinkedIn: Debashis | GitHub: debrej2021 | insights.debprod.com | Bangalore / Remote"
)

p_prof = doc.add_paragraph()
p_prof.paragraph_format.space_before = Pt(3)
p_prof.paragraph_format.space_after = Pt(4)
r_prof = p_prof.add_run("Engineering Leader and Enterprise Architect with 17+ years of experience leading multi-cloud (AWS/Azure), SaaS, and GenAI transformations. Proven record scaling engineering organizations from 5 to 100+ engineers, standing up Global Capability Centers (GCCs), and architecting fault-tolerant, HIPAA/FHIR/SOC 2-compliant platforms. Blends hands-on full-stack mastery (.NET 10, Python, React) with enterprise architecture governance (TOGAF-aligned), FinOps cloud economics, and production-grade LLM/agentic systems.")
r_prof.font.size = Pt(9)
r_prof.font.italic = True

add_section_title("CORE COMPETENCIES")
p_comp = doc.add_paragraph()
p_comp.paragraph_format.space_after = Pt(3)
r_comp = p_comp.add_run("Engineering Leadership | Global Capability Centers (GCC) | Cross-Functional Scaling (up to 100+) | Architecture Review Board (ARB) & Governance | Vendor & Partner Management (Deloitte, Accenture, Wipro) | Agile Delivery & DORA Metrics | Enterprise Architecture (TOGAF-aligned) | Event-Driven & Microservices | Strangler-Fig Pattern | SAGA Orchestration | AWS & Azure Multi-Cloud | Kubernetes & Container Platforms | FinOps & Unit Economics | Agentic AI (LangGraph, PyTorch ReAct) | GraphRAG & Vector Retrieval | LLM-as-a-Judge & Eval Frameworks | Infor Data Lake & Apache Spark | HIPAA / FHIR / SOC 2 / GDPR / UAE PDPL")
r_comp.font.size = Pt(8.5)

add_section_title("TECHNICAL SKILLS")
add_bullet("Languages & Core:", ".NET (6–10, Minimal APIs, Identity, Native AOT), C#, Python, TypeScript, JavaScript, PHP, C++, SQL")
add_bullet("Frameworks & Libraries:", "ASP.NET Core, EF Core 8/10, MediatR, Polly, FastAPI, Flask, PyTorch, TensorFlow, OpenCV, React JS, Next.js, Three.js, Angular, Node.js")
add_bullet("Cloud & DevOps:", "AWS (EKS, Lambda, DynamoDB, Kinesis, Bedrock, KMS, RDS, Neptune), Azure (AKS, Azure AI, Azure DevOps, Functions, Cosmos DB, Foundry), Docker, Kubernetes, Helm, Terraform, Ansible, .NET Aspire, YARP")
add_bullet("AI, Agentic & Big Data:", "LangChain, LangGraph multi-agent orchestration, GraphRAG, Claude API, GPT-4, MedLM, Vector DBs (OpenSearch, Pinecone, FAISS, Milvus), Infor Data Lake, Apache Spark (PySpark, Spark Streaming), Databricks/Delta Lake & Snowflake integration, PyTorch first-principles tool calling, LLM Evaluations")
add_bullet("Databases & Messaging:", "PostgreSQL, MySQL, SQL Server, Redis, Kafka, RabbitMQ, DynamoDB, Cosmos DB")
add_bullet("Security & Governance:", "OAuth 2.0, JWT, Policy/Resource-based Auth, OWASP, SIEM, Snyk, Veracode, HIPAA, FHIR, SOC 2, UAE PDPL, GDPR")

add_section_title("PROFESSIONAL EXPERIENCE")

add_role_title("Technology Consultant & Hands-On Engineering Practice", "Independent", "Dec 2025 – Present")
add_bullet("Bilingual GCC EdTech Platform:", "Architecting an Arabic-RTL / English-LTR education platform (React PWA + Laravel/MySQL 8 backend) with contract-first OpenAPI 3.x, OAuth 2.0/JWT stateless auth, and versioned APIs preparing for Phase 2 Flutter mobile rollout.")
add_bullet("GCC Enterprise Scale & Compliance:", "Designed Docker/Kubernetes autoscaling architecture engineered for a 300,000 concurrent-user target, integrating SCORM 1.2/2004, xAPI, UAE PASS SSO, Tabby/Tamara card reconciliation, and UAE PDPL/GDPR data residency.")
add_bullet("Governed 'AI Matrix' & FinOps:", "Implemented modular AI services (Career Advisor, Skills-Gap Analysis, Chatbots) enforced with strict per-feature cost caps, rate-limiting throttles, and token FinOps monitoring grounded on localized course content.")
add_bullet("Frontier-AI Model Evaluation Specialist:", "Executing production-track pairwise and multi-model evaluations; authoring LLM-as-a-judge rubrics calibrated against human golden labels across C#, Python, and multi-step tool-calling agent traces.")
add_bullet("MAANG Speech-Transcription Eval ('Muse'):", "Delivered benchmark transcription validations (aviation ATC audio, FAA formatting, callsign verification) validating frontier speech-to-text safety prior to commercial launch.")
add_bullet("High-Throughput Simulations & Vision:", "Built high-throughput Payment Gateway simulator with SAGA orchestration (-35% P95 latency, -20% TCO); developed industrial CAD dimensional anomaly detection via OpenFOAM CFD and OpenSees C++ pipelines driven by Python.")
add_bullet("First-Principles ReAct Agent:", "Trained a custom PyTorch tool-calling agent (nn.Module: Embedding -> RNN -> Linear, loss <0.05) emitting strict ACT:tool[arg] grammars routed deterministically via regex controllers.")

add_role_title("Co-Founder & CTO", "Worthum Business Solutions (CIN: U72900DL2022PTC400369)", "Mar 2024 – Nov 2025")
add_bullet("Startup Leadership & Delivery:", "Co-founded and scaled enterprise product engineering firm from scratch; directed cross-functional teams delivering cloud-native, GenAI, and full-stack solutions across 10+ B2B/B2C/D2C clients.")
add_bullet("Agentic AI Workflows:", "Architected and shipped an agentic AI co-pilot and human-in-the-loop multi-agent document classification pipeline, cutting turnaround from days to hours.")
add_bullet("Healthcare GenAI:", "Deployed Google MedLM clinical intelligence layer with HIPAA-compliant document parsing, entity extraction, and RBAC audit trails, slashing manual clinical review time by ~25%.")
add_bullet("FinOps & Observability:", "Implemented systemic FinOps model routing, semantic caching, and dynamic batching paired with OpenTelemetry guardrails, securing client retention across all premier tier accounts.")

add_role_title("Director – Engineering | India Engineering Head", "Upfront Healthcare (Acquired by HealthCatalyst)", "Oct 2023 – Mar 2024")
add_bullet("Organizational Leadership:", "Headed engineering organization (60–100 engineers), driving operational resiliency, resource governance, and cloud optimization that cut operating costs by 30% while lifting uptime to 99.9%.")
add_bullet("Clinical AI Integration:", "Spearheaded development of HIPAA-compliant MedLLM (GPT-3.5 + OpenSearch vector retrieval), reducing clinical documentation time by ~30% and boosting patient engagement by 15–20%.")
add_bullet("Compliance & Cloud Standards:", "Integrated Azure AI Document Intelligence and FHIR + Azure BAA protocols, ensuring 100% regulatory compliance.")
add_bullet("Architecture Modernization:", "Modernized service boundaries via .NET 6+ Common Application Platform (CAP) and schema-per-service segregation, accelerating core API response times by 30%; embedded DORA-aligned CI/CD automation cutting deployment cycles by 20%.")

add_role_title("Sr. Manager – Software Engineering", "JLL (Jones Lang LaSalle)", "Feb 2022 – Sep 2023")
add_bullet("Enterprise SaaS Delivery:", "Managed a 30+ engineer organization delivering enterprise SaaS products for global accounts including Amazon and Nike; improved sprint delivery efficiency by 40%.")
add_bullet("Microservices Migration:", "Spearheaded monolithic migration to AWS microservices (30% reduction in run-rate operational costs); aligned multi-tier system designs with the 4+1 architectural view model.")
add_bullet("Spark Streaming for IoT Telemetry:", "Engineered distributed Apache Spark (Spark Streaming / PySpark) data pipelines processing high-velocity MQTT IoT sensor streams across commercial facilities, feeding aggregated telemetry into real-time React + .NET dashboards with sub-second latency (lifted sensor throughput by 40%).")
add_bullet("Spark Batch ETL & ML Valuation:", "Built scalable Apache Spark batch ETL workflows to cleanse, transform, and engineer geospatial/property feature sets, training predictive real-estate valuation models (Random Forest) that lifted user engagement by 50%.")

add_role_title("Engineering Manager", "Koch Industries", "Apr 2020 – Feb 2022")
add_bullet("Strategic Vendor Partnerships:", "Managed cross-functional teams and strategic vendor engagements (Deloitte, Accenture, Wipro) to drive digital transformation, enhancing operational delivery efficiency by 30%.")
add_bullet("GCC Leadership:", "Played a pivotal leadership role in standing up a 300+ engineer Global Capability Center (GCC), lifting cross-regional productivity by 30%.")
add_bullet("AWS Modernization & Infor Data Lake:", "Architected strangler-fig migration of legacy .NET Framework monoliths to AWS .NET Core microservices, streaming enterprise ERP transactional data directly into Infor Data Lake for unified reporting and downstream analytics.")
add_bullet("Cloud Resiliency & Overhead Reduction:", "Led on-premise to AWS cloud migration, cutting infrastructure overhead by 30% through event-driven messaging, idempotent consumers, Redis distributed caching, and Polly resilience on auto-scaling nodes.")

add_role_title("Engineering Manager", "Cliksource / Hyqoo", "Jul 2018 – Apr 2020")
add_bullet("MVP to Enterprise Scale:", "Scaled early-stage MVP into an enterprise-grade revenue engine with a 99% sprint success rate; executed monolith-to-microservices decomposition using SAGA distributed transaction patterns.")

add_role_title("Engineering Manager", "Accenture", "Aug 2013 – Jun 2018")
add_bullet("Global Enterprise Accounts:", "Led enterprise cloud modernization programs for key global accounts (Pfizer, BMS, UBS); spearheaded establishment and mentoring of a full-scale engineering unit in Krakow, Poland.")
add_bullet("High-Scale Architecture:", "Designed ASP.NET Web API backend for internal corporate platforms supporting 50,000+ users and 10,000+ concurrent sessions using distributed caching and read-replica SQL topologies.")

add_role_title("Senior Developer — Global Services", "Fiserv, Bangalore", "Sep 2012 – Aug 2013")
add_bullet("Core Banking:", "Engineered high-throughput financial transaction processing and core banking middleware.")

add_role_title("Senior Developer / Developer", "Mindtree Ltd., Bangalore", "Mar 2009 – Sep 2012")
add_bullet("Enterprise Modernization:", "Developed distributed enterprise software solutions across multi-tier client deployments.")

add_section_title("EDUCATION & ACCREDITATIONS")
add_bullet("Education:", "B.Tech. in Computer Science & Engineering | Kalinga Institute of Industrial Technology (KIIT) (2008)")
add_bullet("Professional Accreditations:", "Microsoft Certified: Azure AI Engineer Associate (AI-102) | DevOps & Multi-Cloud Engineering (GenAI & LLMs): Hero Vired & Microsoft | Certified Scrum Master (CSM): Scrum Alliance | AWS Cloud Architecture Accredited | Microsoft Azure Certified (AZ-900, Score: 928) | Data Resiliency with RabbitMQ | HackerRank Certified (C#, REST APIs)")

add_section_title("SELECTED ARCHITECTURAL & ENGINEERING WINS")
add_bullet(".NET 8/10 AOT Optimization:", "Migrated high-volume services to AOT-compiled Minimal APIs + MediatR pipelines, producing 35–55% P95 latency reductions, lower cold-starts, and minimal RAM footprint.")
add_bullet("Public Utility Platforms:", "Independently designed and launched reach.debprod.com (distress reporting) and factcheck.debprod.com (economic data visualization).")
add_bullet("Identity & GovTech Integration:", "Built DigiLocker / Setu OAuth connection registration app over Anthropic Claude API, completing automated KYC verification in a unified conversational flow.")
add_bullet("Enterprise AI Gateway & MCP Labs:", "Implemented Microsoft Foundry and AWS Bedrock integrations featuring secure enterprise RAG, Model Context Protocol (MCP) servers, and least-privilege IAM policies for regulated banking use cases.")

add_section_title("BEYOND ENGINEERING")
p_end = doc.add_paragraph()
p_end.paragraph_format.space_before = Pt(2)
r_end = p_end.add_run("Former competitive cricketer; active weekend leather-ball player. The game reinforces high-pressure composure, field tactical analysis, and collective accountability—traits directly applied to steering high-stakes engineering teams.")
r_end.font.size = Pt(9)

doc.save("Debashis_Mohapatra_OriginalStyle.docx")
print("Saved Debashis_Mohapatra_OriginalStyle.docx with exact original colors and Calibri formatting.")