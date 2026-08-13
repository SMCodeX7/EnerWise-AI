# EnerWise AI

**EnerWise AI** is an evidence-grounded multi-agent renewable energy feasibility and decision-support platform developed for the **Information Retrieval and Web Analytics (IT3041)** module.

The platform combines **Agentic AI, Large Language Models, Natural Language Processing, Information Retrieval, Retrieval-Augmented Generation, deterministic calculations, security controls, and Responsible AI** to support preliminary renewable-energy feasibility assessments.

> EnerWise AI is designed as a decision-support system and does not replace certified engineers, renewable-energy consultants, electrical professionals, installers, or other qualified experts.

---

## Project Title

**EnerWise AI: An Evidence-Grounded Multi-Agent Renewable Energy Feasibility and Decision-Support Platform Using LLMs, NLP, Hybrid Information Retrieval, RAG and Responsible AI**

---

## Overview

Renewable-energy decisions require users to consider several factors at the same time, including:

* Energy consumption
* Location
* Property type
* Available roof or land area
* Budget
* Renewable-energy technology
* Battery requirements
* Technical feasibility
* Installation costs
* Potential savings
* Environmental impact
* Available technical evidence
* Uncertainty

General-purpose AI systems can provide useful information, but they may also produce unsupported recommendations, outdated information, hallucinated numerical values, or explanations without reliable evidence.

EnerWise AI addresses these limitations by using specialized AI agents, trusted information retrieval, deterministic calculations, evidence verification, and transparent recommendations.

---

## Main Objectives

EnerWise AI aims to:

* Extract renewable-energy requirements from natural-language user input.
* Convert user requirements into structured energy profiles.
* Retrieve relevant information from a trusted renewable-energy knowledge base.
* Use hybrid lexical and semantic Information Retrieval.
* Ground important AI-generated recommendations using retrieved evidence.
* Compare renewable-energy technologies based on user constraints.
* Perform numerical calculations using deterministic software functions.
* Generate ranked renewable-energy recommendations.
* Explain why recommendations were produced.
* Provide source citations and evidence traceability.
* Estimate recommendation confidence using transparent scoring.
* Detect missing information and uncertainty.
* Apply Responsible AI principles throughout the system.
* Protect user data using authentication, authorization, validation, and secure API design.
* Provide a testable architecture for AI security and vulnerability assessments.

---

## Supported Renewable-Energy Technologies

The initial system focuses on:

* Solar PV
* Solar PV with Battery Storage
* Small Wind Energy

Additional renewable-energy technologies may be supported in future versions.

---

## Multi-Agent Architecture

EnerWise AI uses multiple specialized AI agents with separate responsibilities.

### 1. Coordinator / Orchestrator Agent

Controls the overall AI workflow.

Responsibilities include:

* Understanding the current assessment state
* Identifying missing information
* Selecting the required agents
* Coordinating agent execution
* Preventing required workflow stages from being skipped
* Combining structured outputs

---

### 2. Energy Requirement Intelligence Agent

Processes natural-language user requirements.

Responsibilities include:

* Intent recognition
* Requirement extraction
* Numerical value extraction
* Unit identification
* User constraint identification
* Missing-information detection
* Structured energy-profile generation
* Follow-up question generation

Example extracted information:

```json
{
  "location": "Kandy",
  "property_type": "hotel",
  "monthly_consumption_kwh": 2500,
  "budget_lkr": 3000000,
  "roof_area_m2": 150,
  "objective": "reduce_grid_dependency",
  "battery_preference": true
}
```

---

### 3. Renewable Energy Research & Retrieval Agent

Responsible for the Information Retrieval and RAG pipeline.

Responsibilities include:

* Query generation
* Query rewriting
* Metadata filtering
* Semantic retrieval
* Lexical retrieval
* Hybrid ranking
* Source reliability checking
* Evidence-pack generation
* Citation tracking

---

### 4. Feasibility & Recommendation Agent

Evaluates renewable-energy technologies against the user's requirements.

It considers:

* Energy consumption
* Property characteristics
* Available space
* Budget
* User objectives
* Technology constraints
* Retrieved technical evidence
* Deterministic calculation results

The agent produces ranked technology alternatives rather than selecting a technology without explanation.

---

### 5. Scenario, Cost & Sustainability Agent

Evaluates the impact of different renewable-energy scenarios.

It works with deterministic calculation services for:

* Energy demand
* Renewable-energy contribution
* System capacity
* Cost ranges
* Estimated savings
* Payback indicators
* Battery requirements
* Carbon-impact estimates
* Scenario comparison

The LLM is used to interpret and explain calculations rather than performing basic arithmetic.

---

### 6. Evidence & Safety Verification Agent

Validates recommendations before they are shown to the user.

The Verification Agent checks:

* Whether important claims have supporting evidence
* Whether retrieved sources are relevant
* Whether contradictory evidence exists
* Whether important information is missing
* Whether numerical calculations are consistent
* Whether recommendations contain unsupported claims
* Whether confidence is excessive
* Whether retrieved content contains suspicious instructions
* Whether citations are available

Possible outcomes include:

```text
APPROVED
APPROVED_WITH_WARNING
MORE_INFORMATION_REQUIRED
REGENERATE
REJECTED
```

---

## Information Retrieval and RAG

Information Retrieval is a major component of EnerWise AI.

The system uses a renewable-energy knowledge base containing trusted technical documents.

### Knowledge Sources

Possible sources include:

* Government publications
* Renewable-energy authority publications
* Technical reports
* Research papers
* Solar-energy documentation
* Battery-storage documentation
* Wind-energy publications
* Energy-efficiency reports
* Relevant standards and policies

---

## Knowledge Base Pipeline

```text
Document Upload
      ↓
File Validation
      ↓
Text Extraction
      ↓
Text Cleaning
      ↓
Chunking
      ↓
Metadata Assignment
      ↓
Embedding Generation
      ↓
PostgreSQL + pgvector
```

---

## Hybrid Retrieval

EnerWise AI combines:

### Lexical Retrieval

Keyword and full-text based retrieval.

### Semantic Retrieval

Embedding-based similarity search using pgvector.

### Metadata Filtering

Documents can be filtered using metadata such as:

* Technology
* Region
* Organization
* Publication date
* Document type
* Reliability level

### Ranking

Lexical and semantic retrieval results are combined and ranked before being provided to the AI agents.

---

## Source Metadata

Knowledge-base documents may contain metadata such as:

```text
Document ID
Title
Organization
Publication Date
Document Type
Technology
Region
Reliability Classification
Upload Date
Status
```

Each retrieved chunk remains connected to its original source for citation and traceability.

---

## Evidence-Grounded Recommendations

Important technical recommendations should be supported by retrieved evidence.

EnerWise AI distinguishes between:

### Evidence-Supported Facts

Information directly supported by retrieved knowledge-base sources.

### Calculated Estimates

Values generated using deterministic software calculations.

### AI-Generated Interpretation

Explanations or reasoning generated by the AI model.

### Assumptions

Conditions assumed because complete data was unavailable.

### Missing Information

Important information that was not supplied by the user.

### Limitations

Factors that prevent the system from providing professional engineering certification.

---

## Recommendation Confidence Engine

EnerWise AI includes a transparent confidence-scoring mechanism.

Confidence may consider factors such as:

* Requirement completeness
* Evidence coverage
* Retrieval relevance
* Source reliability
* Agent agreement
* Numerical-input completeness

Example:

```text
Recommendation Confidence: 82% - High

Requirement completeness: 90%
Evidence coverage: 85%
Source reliability: 92%
Retrieval relevance: 80%
Agent agreement: 78%
Numerical completeness: 70%
```

Confidence values are calculated using predefined software rules rather than being randomly generated by an LLM.

---

## Suitability Scoring

Suitability scores are different from confidence scores.

### Suitability Score

Measures how suitable a renewable-energy technology is for the user's requirements.

### Confidence Score

Measures how confident the system is in the quality of the overall assessment.

Example:

```text
Grid-Connected Solar PV        84/100
Solar PV + Battery Storage     78/100
Small Wind Energy              41/100
```

---

## Evidence and Decision Provenance

EnerWise AI tracks how recommendations are produced.

A recommendation can be connected to:

* User requirements
* Retrieved evidence
* Calculation results
* Agent outputs
* Assumptions
* Verification decisions

Example:

```text
Solar PV Recommendation
        │
        ├── User Energy Consumption
        ├── Available Roof Area
        ├── Budget Constraint
        ├── Retrieved Solar Evidence
        ├── Energy Calculation
        ├── Feasibility Assessment
        └── Verification Result
```

This improves transparency and explainability.

---

## What-If Scenario Analysis

Users can modify assessment variables and compare different renewable-energy scenarios.

Example questions:

```text
What if my budget increases by 30%?

What if I do not want battery storage?

What if my electricity consumption increases?

What if my property changes from residential to commercial?
```

The system recalculates affected values and compares the original scenario with the modified scenario.

---

## Renewable Energy Claim Verification

EnerWise AI may also include a secondary feature for checking unsupported renewable-energy claims.

Example:

```text
"This solar system will eliminate 100% of my electricity costs."
```

The system can:

* Retrieve relevant evidence
* Analyse the claim
* Identify unsupported statements
* Detect exaggerated claims
* Explain whether sufficient evidence exists

---

## Responsible AI

Responsible AI is integrated into the system architecture.

Key mechanisms include:

* Source attribution
* Evidence-based recommendations
* Confidence scoring
* Uncertainty communication
* Assumption disclosure
* Missing-information detection
* Explainability
* User-data protection
* Hallucination reduction
* Human oversight
* Recommendation limitations
* Verification before final output

EnerWise AI clearly communicates that its results are preliminary decision-support recommendations.

---

## Security

Security is implemented throughout the platform.

### Authentication

Users must securely authenticate before accessing protected functionality.

### Authorization

The system supports roles such as:

```text
USER
ADMIN
```

Users can only access resources that belong to their own accounts.

---

## API Security

The backend includes protections such as:

* Authentication checks
* Authorization checks
* Input validation
* Request validation
* Request-size limits
* Rate limiting where appropriate
* Secure error handling
* Restricted CORS configuration

---

## AI Security

EnerWise AI is designed to defend against:

* Prompt injection
* Jailbreak attempts
* Prompt leakage
* Instruction override
* Role manipulation
* Multi-turn prompt attacks
* Indirect prompt injection
* Malicious retrieved documents
* Cross-agent manipulation

Retrieved document content is treated as untrusted data rather than executable instructions.

---

## Agent Permission Boundaries

Agents operate with restricted capabilities.

For example:

### Requirement Intelligence Agent

Can:

* Read assessment input
* Extract structured requirements

Cannot:

* Manage users
* Upload knowledge-base documents
* Access unrelated assessments

### Retrieval Agent

Can:

* Search approved knowledge-base documents

Cannot:

* Modify user accounts
* Change document trust classifications
* Bypass verification

### Verification Agent

Can:

* Approve recommendations
* Add warnings
* Request additional information
* Reject unsupported output

Cannot:

* Modify retrieved evidence
* Modify deterministic calculations

---

## Privacy

EnerWise AI protects user-specific information such as:

* Name
* Email
* Property information
* Energy consumption
* Saved assessments
* Recommendations
* Scenario history

User-owned data is isolated using authenticated user identifiers and backend authorization checks.

Sensitive information should not be unnecessarily included in LLM prompts or application logs.

---

## Audit Logging

The platform records selected system events for monitoring, testing, and evaluation.

Example audit information:

```json
{
  "run_id": "RUN-001",
  "assessment_id": "ASSESS-001",
  "agent": "retrieval_agent",
  "retrieved_documents": [
    "DOC-010",
    "DOC-025"
  ],
  "verification_status": "APPROVED"
}
```

The system does not intentionally log:

* Passwords
* API keys
* Access tokens
* Database credentials
* Other application secrets

---

## Main Application Pages

### Public Pages

* Landing Page
* About
* Features
* How It Works
* Login
* Register

### User Pages

* Dashboard
* New Energy Assessment
* Requirement Input
* Requirement Confirmation
* Assessment Progress
* Recommendation Results
* Evidence and Sources
* Scenario Comparison
* Saved Assessments
* User Profile

### Admin Pages

* Admin Dashboard
* Knowledge Base
* Document Management
* Document Metadata
* User Management
* Audit Logs
* System Information

---

## Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* Python
* FastAPI
* Pydantic

### Agent Orchestration

* LangGraph

### Database

* PostgreSQL

### Information Retrieval

* PostgreSQL Full-Text Search
* pgvector
* Hybrid Lexical and Semantic Retrieval

### Authentication

* Supabase Auth

### AI

* Large Language Model provider with structured-output support
* Embedding model for semantic retrieval

### Testing

* Pytest
* Vitest
* Playwright
* AI evaluation datasets
* Security and red-team testing tools

---

## High-Level Architecture

```text
User
 │
 ▼
Next.js Web Application
 │
 ▼
Authentication & Authorization
 │
 ▼
FastAPI Backend
 │
 ▼
Coordinator / Orchestrator Agent
 │
 ▼
Requirement Intelligence Agent
 │
 ▼
Structured Energy Profile
 │
 ▼
Research & Retrieval Agent
 │
 ├── Lexical Search
 │
 └── Vector Search
 │
 ▼
Hybrid Ranking
 │
 ▼
Trusted Evidence Pack
 │
 ▼
Feasibility Agent
 │
 ▼
Scenario, Cost & Sustainability Agent
 │
 ▼
Deterministic Calculation Services
 │
 ▼
Recommendation Scoring
 │
 ▼
Evidence & Safety Verification Agent
 │
 ▼
Explainable Recommendation
 │
 ├── Sources
 ├── Confidence
 ├── Assumptions
 ├── Missing Information
 ├── Limitations
 └── Evidence Provenance
```

Security, Responsible AI, auditing, and testing operate across the entire architecture.

---

## Repository Structure

```text
enerwise-ai/
│
├── apps/
│   ├── web/
│   │   └── Next.js frontend
│   │
│   └── api/
│       └── FastAPI backend
│
├── docs/
│   ├── architecture/
│   ├── assignment/
│   └── security/
│
├── scripts/
│
├── tests/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Environment Configuration

Secrets must never be committed to the repository.

The project uses environment variables for configuration.

Example:

```env
APP_ENV=development

NEXT_PUBLIC_API_URL=http://localhost:8000

NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

DATABASE_URL=

LLM_PROVIDER=
LLM_API_KEY=
LLM_MODEL=

EMBEDDING_PROVIDER=
EMBEDDING_MODEL=
```

Create local `.env` files using `.env.example` as a reference.

---

## Development Principles

The project follows these principles:

* Evidence before unsupported generation
* Deterministic calculations where appropriate
* Structured agent communication
* Security by design
* Responsible AI by design
* Privacy by design
* Testability by design
* Explainable recommendations
* Modular architecture
* Human oversight
* No committed secrets
* No fabricated test results
* No fabricated evaluation metrics

---

## Testing

EnerWise AI is designed to support multiple forms of testing.

### Functional Testing

* Authentication
* Assessment creation
* Requirement extraction
* Recommendation generation
* Scenario comparison
* Saved assessments

### Agent Testing

* Agent routing
* Structured outputs
* Missing-information detection
* Verification behaviour
* Tool access

### Information Retrieval Testing

* Retrieval relevance
* Semantic retrieval
* Lexical retrieval
* Hybrid retrieval
* Source reliability
* Citation correctness

### Security Testing

* Authentication
* Authorization
* API protection
* Prompt injection
* Jailbreak attempts
* Cross-user access
* Agent manipulation
* Knowledge-base security

### Responsible AI Testing

* Hallucination
* Bias
* Fairness
* Transparency
* Explainability
* Overconfidence
* Unsupported claims
* Missing-information behaviour

---

## Commercialization Concept

EnerWise AI can potentially be offered using several service tiers.

### Free

* Limited energy assessments
* Basic recommendations
* Limited saved assessments

### Personal / Pro

* Detailed feasibility analysis
* Evidence-supported recommendations
* Scenario comparison
* Saved history
* Detailed reports

### Business

* Multiple properties
* Team access
* Advanced reporting
* Scenario analytics

### Enterprise / API

* Renewable-energy consultant integration
* Installer integration
* API access
* White-label solutions

Potential users include:

* Homeowners
* Small businesses
* Hotels
* Offices
* Property developers
* Renewable-energy consultants
* Solar installers
* Energy service companies

---

## Project Scope

The initial version does not attempt to provide:

* Professional structural assessment
* Detailed electrical engineering design
* Final installer quotations
* Real-time smart-meter integration
* Real-time electricity-grid integration
* Complex GIS analysis
* Native mobile applications
* Full payment processing
* Custom LLM training
* Enterprise-scale distributed infrastructure

These areas may be explored as future extensions.

---

## Future Enhancements

Potential future improvements include:

* Additional renewable-energy technologies
* Real-time solar-resource APIs
* Smart-meter integration
* Advanced GIS analysis
* Energy tariff integration
* Installer marketplace integration
* Advanced renewable-energy forecasting
* Automated professional reports
* Enterprise API integration
* Mobile applications
* Advanced explainability visualizations

---

## Academic Integrity

The project does not intentionally use fabricated:

* Evaluation metrics
* Testing results
* Research references
* Security findings
* Accuracy measurements
* Performance benchmarks
* Source citations

Evaluation results should be generated through actual experiments and documented testing.

---

## Disclaimer

EnerWise AI provides **preliminary AI-assisted renewable-energy feasibility and decision support**.

The platform does not provide professional engineering certification, structural approval, electrical design approval, regulatory approval, investment guarantees, or installation certification.

Final renewable-energy decisions should be reviewed by appropriately qualified professionals.
