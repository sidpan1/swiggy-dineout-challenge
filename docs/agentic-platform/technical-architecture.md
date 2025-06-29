# Technical Architecture

## Objective
Build an intelligent automation platform to build and manage agentic workflows for business process automation, with self-improving meta-workflows that continuously enhance core workflow performance through iterative refinement.

## Background : Meta-Intelligence Leverage

Meta-intelligence applies intelligence to improve intelligence itself. Just as chess masters analyze their decision patterns to enhance strategic thinking, LLMs can be used to build meta-workflows that optimize core workflows. LLMs, as sophisticated pattern-matching engines trained on vast datasets, can create abstraction layers over core workflows throughout their lifecycle. This creates a recursive improvement cycle where:

- **Core workflows** solve business problems
- **Meta workflows** build, manage, and optimize core workflows

This transforms automation from linear efficiency gains to exponential capability growth.

![Recursive Cycle](../images/recursive-cycle.svg)

Check [docs/agentic-platform/automation-platform-concept.md](automation-platform-concept.md) for more details on the automation platform concept.

## Key Definitions

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTIC SYSTEM                           │
│               (Complete Intelligent Organization)               │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   AGENTIC PLATFORM                        │  │
│  │        (Infrastructure & Runtime Environment)             │  │
│  │                                                           │  │
│  │  ┌─────────────────┐    ┌─────────────────────────────┐   │  │
│  │  │  CORE WORKFLOWS │    │     META-WORKFLOWS          │   │  │
│  │  │                 │    │                             │   │  │
│  │  │ • Customer      │ ◄──┤ • Performance Analysis      │   │  │
│  │  │   Onboarding    │    │ • Workflow Optimization     │   │  │
│  │  │ • Order         │    │ • System Health Monitoring  │   │  │
│  │  │   Processing    │    │ • Knowledge Consolidation   │   │  │
│  │  │ • Support       │    │                             │   │  │
│  │  │   Tickets       │    └─────────────────────────────┘   │  │
│  │  │ • Data Analysis │                    │                 │  │
│  │  └─────────────────┘                    │                 │  │
│  │           │                             │                 │  │
│  │           ▼                             ▼                 │  │
│  │  ┌────────────────────────────────────────────────────┐   │  │
│  │  │              PLATFORM SERVICES                     │   │  │
│  │  │ • Agent SDK        • Memory Service                │   │  │
│  │  │ • Session Mgmt     • Artifacts Service             │   │  │
│  │  │ • Tool Registry    • Scheduler Service             │   │  │
│  │  │ • Auth Service     • Monitoring & Logging          │   │  │
│  │  └────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               EXTERNAL INTEGRATIONS                       │  │
│  │    • Enterprise APIs    • Event Triggers                  │  │
│  │    • Databases          • Third-party Tools               │  │
│  │    • Message Queues     • Human Interfaces                │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

Key Interactions:
→ Meta-workflows analyze and optimize core workflows
→ All workflows use platform services for execution
→ Platform integrates with external systems
→ System learns and evolves through meta-intelligence feedback loops
```

### Agentic Workflows
Individual executable processes that solve specific business problems:
- Natural language SOPs that compile to code when deterministic execution is needed
- Executed by LLMs in a loop with tool access
- Can be nested, paused/resumed, and self-healing
- Examples: Customer onboarding, performance analysis, risk assessment

### Agentic Platform
The infrastructure and runtime environment that enables workflow creation and execution:
- Agent SDK, service architecture, and toolsets
- Provides foundation for building, deploying, and managing workflows
- Includes default tools, MCP integrations, and governance systems
- The "factory" that produces and operates individual workflows

### Agentic Systems
The complete intelligent organization ecosystem that transforms how an organization operates:
- Encompasses the entire stack: Platform + All workflows + Meta-workflows + Integration layers
- Creates a self-improving, self-managing organizational intelligence
- Includes both core business workflows AND meta-workflows that optimize the system itself
- Represents the emergent intelligent organization that adapts and evolves autonomously
- The ultimate goal: an organization that functions as a cohesive, adaptive intelligence rather than just a collection of automated processes


We talk about these 3 concepts below in more detail.

## Agentic Workflows 
Agentic Workflows have the following properties: 

- The workflows are executed by an LLM in a loop.
- The workflow definitions are expressed in natural language.
- The workflows compile into code wherever deterministic execution is required.
- The workflows can call tools to gather context, reason and take actions.
- The workflows can build higher order abstractions by using exisitng tools and workflows as building blocks.
- The workflows can invoke the human in the loop where required.
- The workflows can be triggered by a schedule, event or a user request. 
- The workflows can be hierarchically nested to call other workflows as sub-workflows.
- These workflows can be paused and resumed based on the environment state and events.
- The workflows can save and read context for communication across the different steps in a single execution.
- The workflows can retain knowledge across executions to improve their performance over time.
- The workflows are self-healing to deal with errors and failures on the fly.
- The workflows are self-evolving to improve their code/prompts over time

### Workflow Definition
- Identifier
- Prompts
    - Memory Protocol
    - Orchestration Protocol
    - Artifacts Protocol
    - Output Format
    - Tool Config
    - Workflow Instructions
    - PRD
    - ...
- Tool Config
- Executable
    - Default
    - Custom
- Evals Config
    - Datasets
    - Weighted Metrics
- Input-Output Config
- Deployment Config

## Agentic Platform
The Agentic Platform is a platform to build, manage, operate, and optimize agentic workflows.

### UX Architecture

#### Surface Types
- Internal Chat App
- SDKs
    - Backend
    - Web
    - Mobile
- 3P
    - Slack
    - Email
    - Jira
    - Customer ticketing
- Local CLI/Code Editors
    - Claude Code
    - Cursor

#### Modalities
- Chat
- Voice
- File/Image/Video Uploads
- Passive Observation (meetings, calls, etc)

### Agent Architecture
Each agent is a self-contained system that can be deployed and used in a variety of ways.

#### Agent Autonomy Levels
* Vanilla Agent - standalone LLM in a loop with access to tools
* Workflow Agent - agent customized to execute recurring sequences of steps following standard operating procedures (SOPs) toward specific objectives, with reasonable accuracy validation.
* Persona Agent (future) - agent capable of orchestrating multiple workflows and integrating them cohesively toward a common high-level objective, autonomously fulfilling all expectations of a specific persona's job function.

#### Agent SDK
- LLM Gateway Proxy
- Agentic Loop
- Default Toolsets
- MCP Client Adapter
- Output Format
- Memory Adapter
- Session Adapter
- Artifacts Adapter
- Telemetry Adapter
- Streaming Adapter
- Auth Adapter
- Agent Runtime
- Custom Control Flows (parallel, sequential, conditional, etc)

Example Agent SDK: [Google ADK](https://google.github.io/adk-docs/)

#### Default Toolsets
(Tools are installed by default in the agent SDK)
- Planning
- Bash
- Filesystem (artifacts)
- Todos
- Respawn (locally or remotely)
- Web Search
- Deep Research
- Diagramming
- Auth
- Human in the loop

#### MCP Toolsets
(can be installed after role based authentication)

- Project Management
- Federated Analytics Query Engine (metadata-augmented)
- Data Science Platform (data science tools)
- Container Runtime (Kubernetes or alternative)
- Knowledgebase (GRAG, RAG, etc)
- Memory (episodic, session, indexed etc)
- Google Drive or alternative (or any other file storage system)
- Github or alternative (or any other code repository)
- Jira or alternative (or any other ticketing system)
- Email or alternative
- Slack or alternative
- New Relic or Alternative (or any other monitoring system)
- AWS or alternative (or any other cloud provider)
- AB Testing
- Video Generation
- Image Generation
- (Any custom tool)

#### Meta Tools
(Tools which help the meta-workflows to build, manage, operate, and optimize core workflows)
- Tools Registry
- Workflow Registry
- Scheduler Tool
- Event Handler Tool
- Evaluation Tool
- Experimentation Tool

### Service Architecture
- Agent Engine Service
- Auth Service
- Streaming Service
- Session Service
- Session History Service
- Registry Service
- Memory Service
- Artifacts Service
- Knowledgebase Service
- MCP Aggregator Service
- Container Runtime Service
- Scheduler Service
- Event Handler Service
- LLM Gateway Service
- OTEL Collector Service

### Data and AI Architecture
- Data Science Platform
    - Model/Agent Evaluation
    - Model/Agent Training
    - Model/Agent Inference
    - Model/Agent Deployment
    - Model/Agent Monitoring
    - Model/Agent Logging
    - Model/Agent Alerting
- Data Engineering Platform
    - Ingestion Pipeline
        - Sessions
        - Episodic Memories
        - Artifacts
        - Telemetry
        - Enterprise Documents
        - Code Repositories
    - Transformation Pipeline
        - Graph + RAG
        - Evals Execution
        - Dataset Preparation
        - Intent Clustering
- Monitoring Dashboards

### QA Architecture
- TDD development
- Automated tests for all components
- Rubrics based evaluation for all workflows
- Continuous monitoring and alerting

### Security & Governance Architecture
- RBAC with Auth for all tools
- Centrally managed LLM guardrails 
- Security Audit Meta-Workflows (pentesting, red teaming, mcp certification, etc)
- Governance Meta-Workflows (cost, compliance, risk, etc)

### Infrastructure Architecture
- Deployment Pipelines
- Durable Runtime
- DAG Orchestrator
- Container Runtime (Kubernetes or alternative)
- Object Storage (S3 or alternative)
- Database (Postgres or alternative)
- Graph Database (Neo4j or alternative)
- Message Queue (Kafka or alternative)
- Cache (Redis or alternative)

## Agentic Systems

An Agentic System is the complete intelligent organization - all components working together to replace manual processes with self-improving automation.

### System Components

#### 1. Agentic Platform
- **Runtime Environment**: Executes workflows, manages sessions, handles authentication
- **Agent SDK**: Tools and APIs for building workflows
- **Service Layer**: Memory, artifacts, scheduling, monitoring services
- **Integration Layer**: Connects to existing enterprise systems (databases, APIs, tools)

#### 2. Core Workflows
- **Business Process Workflows**: Customer onboarding, order processing, support tickets
- **Operational Workflows**: Data analysis, reporting, compliance checks
- **Decision Workflows**: Approvals, escalations, resource allocation
- Each workflow has: prompts, tools, evaluation metrics, input/output configs

#### 3. Meta-Workflows
- **Performance Analysis**: Monitor workflow success rates, identify bottlenecks
- **Workflow Optimization**: Automatically improve prompts and tool configurations
- **System Health**: Resource monitoring, error detection, capacity planning
- **Knowledge Consolidation**: Extract learnings from workflow executions

### System Interactions

#### Core Workflow → Platform
- Workflows request execution resources from platform
- Platform provides tools, memory, and service access
- Platform logs all executions for analysis

#### Meta-Workflow → Core Workflow
- Meta-workflows analyze core workflow performance data
- Generate optimization recommendations (new prompts, tool configs)
- Deploy improvements automatically or via approval gates

#### Workflow → Workflow
- Workflows can invoke other workflows as sub-processes
- Share session context and intermediate results
- Coordinate parallel execution and dependencies

#### System → External
- Integrate with existing enterprise systems via APIs
- Trigger workflows from external events (emails, tickets, schedules)
- Export results to downstream systems

### System Evolution

#### Learning Loop
1. **Execute**: Core workflows process business requests
2. **Monitor**: Platform captures execution data, outcomes, errors
3. **Analyze**: Meta-workflows identify patterns and improvement opportunities
4. **Optimize**: Generate better prompts, tools configs, workflow logic
5. **Deploy**: Roll out improvements and measure impact

#### Scaling Mechanism
- High-performing workflows become templates for similar processes
- Successful patterns get abstracted into reusable components
- System learns which workflows work well together
- Automatic load balancing and resource optimization
