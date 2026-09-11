# Application folder structure

```text
agriguard-ai/
├── .github/workflows/       Continuous integration checks
├── .streamlit/              Streamlit configuration
├── config/                  Non-secret application and safety settings
├── data/
│   ├── knowledge/           Approved RAG source documents by crop and safety topic
│   ├── eval/                Gold evaluation dataset
│   └── generated/           Local vector index and generated test outputs
├── docs/
│   ├── architecture/        Architecture and agent-flow diagrams
│   ├── requirements/        SRS and requirement references
│   ├── test-cases/          Test specification and execution evidence
│   └── demo/                Three-minute demo plan and submission notes
├── logs/                    Local execution logs excluded from Git
├── scripts/                 Ingestion, evaluation and development utilities
├── src/agriguard/
│   ├── agents/              Intake, retrieval, advisory and safety agents
│   ├── orchestration/       Shared state, explicit multi-agent workflow and router
│   ├── rag/                 Loading, chunking, embeddings and vector retrieval
│   ├── tools/               Weather, knowledge and escalation tools or MCP server
│   ├── safety/              Confidence, guardrails and red-flag rules
│   ├── services/            Provider and application services
│   ├── models/              Typed domain and response models
│   ├── observability/       Structured tracing and metrics
│   ├── storage/             JSON or SQLite repositories
│   └── ui/                  Streamlit pages and UI components
└── tests/
    ├── unit/                Component-level tests
    ├── integration/         Agent, RAG and tool integration tests
    ├── system/              AGR-TC system and acceptance tests
    ├── security/            Secret and prompt-injection tests
    └── fixtures/            Deterministic test inputs and controlled outputs
```
