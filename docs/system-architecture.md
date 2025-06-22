# System Architecture

## The Problem: Sales Intelligence at Scale

Swiggy Dineout Sales Executives spend **30 minutes to 3 hours** manually gathering restaurant performance data before each partner meeting. With hundreds of partners per city, this approach doesn't scale.

## The Solution: Restaurant Performance Agent

The Restaurant Performance Agent is an AI agent that generates a restaurant performance briefing for a given restaurant_id.

More details about the agent can be found in the [Restaurant Performance Agent PRD](restaurant-performance-agent-prd.md).

## Product Requirements

### Functional Requirements
1. **Restaurant Performance Analysis**
   - Generate 30-day performance summary (bookings, cancellations, revenue, ratings)
   - Identify notable trends and changes
   - Calculate key metrics (OPD, Revenue/GOV, Ads ROI)

2. **Ad Campaign Effectiveness**
   - Analyze spend, impressions, clicks, conversions, and ROI
   - Identify inefficiencies and highlights
   - Compare performance against benchmarks

3. **Peer Benchmarking**
   - Compare restaurant metrics with similar restaurants in same locality and cuisine
   - Identify overperforming and underperforming areas
   - Provide context for performance gaps

4. **Recommendations Engine**
   - Generate data-informed actionable recommendations
   - Suggest ad spend adjustments, discount optimizations, and campaign improvements
   - Provide specific monetary and percentage-based suggestions

### Input/Output Requirements
- **Input**: Single restaurant_id
- **Output**: Structured markdown or narrative format summary
- **Data Sources**: Mock datasets for restaurant_metrics, ads_data, peer_benchmarks

### Non-Functional Requirements

1. **Performance**
   - Generate insights within reasonable time (< 5 minutes)
   - Handle multiple restaurant requests efficiently
   - Scalable across hundreds of partners per city

2. **Quality & Accuracy**
   - Generate meaningful, context-rich summaries using LLMs
   - Handle uncertainty and low-confidence outputs appropriately, for example hallucinations
   - Provide actionable insights rather than perfect analytics accuracy

3. **Usability**
   - Clear, concise, and structured output format
   - Sales Executive-friendly language and presentation
   - Ready-to-use format for meetings and partner communications

4. **Technical Architecture**
   - Support for multiple LLM providers (OpenAI, Claude, Mistral, etc.)
   - Retrieval-Augmented Generation (RAG) or prompt chaining capabilities
   - Modular design for reusability and maintainability
   - Mock data generation and management

5. **Scalability**
   - Potential for batch processing multiple restaurants
   - Extensible architecture for additional data sources
   - Reusable modules as organizational capabilities

# Agentic Workflow Platform
Stepping back from the specific use case, these agentic workflows would have the following tenets:

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
- The workflows are self-evolving to improve their code/prompts over time.

## Core System Flow

This represents a self-improving AI system where agents continuously refine both their natural language workflow definitions and their compiled code implementations, with human expert oversight at critical decision points. The system aims to bridge business requirements with technical execution through iterative improvement cycles.

![Recursive Cycle](./images/recursive-cycle.svg)

### 1. **Initial Problem Input**
- **Product Owner** enters a problem statement to solve a business problem
- This triggers the entire agentic workflow system

### 2. **Natural Language Workflow Generation**
- Agents help build other agents or natural language workflows for a persona
- Uses the problem statement, PRD (Product Requirements Document), and other relevant context
- This is approved by Domain Expert and Product Owner after review

### 3. **Workflow Compilation**
- Agents compile these natural language workflows into a mixture of:
  - **Agents** (for cognitive execution)
  - **Code** (for deterministic execution)
- Requires Technical Expert approval at this stage
- The Technical Expert is responsible for ensuring that the code is correct and works as expected, efficient and performant
- The Technical may suggest more changes and implement them with agents.

### 5. **Code Improvement**
- Agents help improve the code to make it more:
  - Efficient
  - Performant
  - Platformized
- These tasks are done asynchronously in the background and sent for review periodically to technical experts. 

### 6. **State Reconciliation**
- Agents reconcile the state of code from the main branch
- Aligns with exact sources of truth
- Updates the natural language workflows accordingly
- Product owners, domain experts, and technical experts review this change to make sure they are in line with the source of truth. 

### 7. **Evaluation System Building**
- Agents build systems to evaluate other agents
- Uses fitness scores based on aggregate success metrics
- These evaluations are attested by domain experts to make sure labeled and agentic evaluations match.

### 8. **Evolutionary Programming**
- Agents use evolutionary programming to improve the entire system end-to-end
- This includes orchestration, code, tools, prompts, etc.
- Based on success metrics
- Product owners, domain experts, and technical experts review this change to make sure they are in line with the source of truth. 

### 8. **Model Training** 
- Agents use evolutionary programming to:
  - Build proprietary datasets
  - Write code to train small specialized models
  - Incrementally improve performance for specific use cases
- Technical experts attest the gains made through these experiments and approve the changes.

## Feedback and Improvement Loops

The system contains several recursive loops:

1. **Primary Improvement Loop**: The circular flow in the center represents continuous improvement where outputs feed back as inputs

2. **Human-in-the-Loop Validation**: Multiple approval points ensure quality:
   - Product Owner approval (business alignment)
   - Domain Expert approval (technical correctness)
   - "Expert" approval (specialized validation)

3. **Data Labeling Loop**: End users, product owners, domain experts, or third-party humans label data based on guidelines, feeding back into the system

4. **Self-Evolution Loop**: The system can modify its own code, prompts, and workflows based on performance metrics

## Current Implementation Scope
This project implements points **3** and **7** from the core workflow to build a basic POC for solving the problem statement.

## Curent Components of an Agentic Workflow
We try to keep the architecture as simple as possible, and complexity be introduced only when there is a need. For example, the first version of an agentic workflow might be entirely LLM-driven, while future versions are optimized to be partially deterministic based on the use case. This is to avoid complexity in the beginning where requirements are not that clear. And as we get to know more of the unknowns, we can optimize the workflow to be more deterministic and efficient.

These are some of the basic components that we need. 

![Components](./images/components.svg)

### 0. LLM
Claude is the LLM of choice for this POC. However, the architecture is agnostic to it and it can be replaced with any other LLM provider if needed.

### 1. Augmented LLM 

An augmented LLM can be defined as an LLM with basic tools atatched to a running process with a file system and chat history.

These tools could be:
    * Bash tool to run commands on the file system
    * File system tool to read and write files
    * Web search tool to search the web
    * Todolist tool to manage a todo list
    * Sub-agent tool to invoke other agents

We use claude code as the augmenting LLM for this in this POC. There are other similar CLI Augmented LLMs which can work with any LLM provider, which would be the choice for the future. 

### 2. Natural Language Prompts

The workflow might consist of multiple instructions which are aggregated to send to the LLM. These instructions should also be treated as code and be following the single responsibility principle. That is, a single prompt should have a single responsibility. 

The current prompts folder contains modular prompt components that define the agentic workflow:

#### Business Logic
- **orchestration.md**: Defines the Senior Sales Manager agent that coordinates specialized analyst deployment
- **instructions.md**: General system instructions and behavior guidelines
- **analysis-categories.md**: Defines 5 specialized analyst roles:
  - Revenue Optimization Analyst
  - Risk & Quality Assessment Analyst  
  - Campaign Performance Analyst
  - Financial Health Analyst
  - Competitive Intelligence Analyst
- **data-sources.md**: Specifies available database tables and data schema
- **artifacts-protocol.md**: Standardizes output formats and file organization
- **output-format.md**: Defines structured report templates

### Utilities
- **tools.md**: Available tools for database operations and analysis
- **tools-build.md**: Instructions for building and extending tool capabilities

### Evaluation Framework
- **evaluation/evaluate-solution.md**: Quality assessment criteria and metrics

Each prompt follows single responsibility principle - one specific function per prompt file. The orchestration prompt coordinates these specialized components to create comprehensive restaurant performance briefings.

### 3. Additional Tools
These are deterministic parts which augment the LLM with more context or help the LLM take actions. The LLM itself can also write tools on the fly and execute them to get results. Essentially, the llm builds higher-order abstractions based on need, converting natural language to deterministic code. These tools are present in the tools folder.

The current tools folder contains utilities organized by function:

#### Database & Session Management (`tools/utils/`)
- **init_database.py**: Initializes SQLite database schema with restaurant performance tables
- **initialize_session.py**: Sets up analysis sessions for specific restaurants (e.g., `R001`)
- **get_tools.py**: Tool discovery utility to list available analysis capabilities

#### Evaluation & Metrics (`tools/evaluation/`)
- **initialize_db.py**: Sets up evaluation database for tracking analysis quality
- **get_trends.py**: Extracts performance trends and patterns from historical data
- **save_score.py**: Records analysis quality scores and performance metrics

All tools are designed to be LLM-augmented, meaning they can be dynamically composed and extended by the AI agents during analysis workflows. Tools follow the principle of building higher-order abstractions from basic operations. 

Currently, these tools are implemented as bash tools since that was the simplest way. They could also be implemented as MCP tools integrating into clients like Claude Code easily. 

### Artifacts
Currently, all the artifacts are stored in the local artifact directory grouped by session ID. 

# CLI API Interface

The system is exposed as a Python CLI application through `main.py`, providing two operational modes for restaurant performance analysis.

## Command Line Interface

### Generate Mode (Default)
Creates restaurant improvement recommendations using specialized AI analysts:

```bash
# Generate a restaurant performance briefing for a given restaurant_id
python main.py generate R001
```

#### Generate Mode - Development (Future)
In this mode, the LLM can create functions during its execution during the development phase which can be committed and used in production. This is a way to get the LLM to build tools on the fly.

```bash
# Generate a restaurant performance briefing for a given restaurant_id
python main.py generate-dev R001
```
The prompts tool.md and tools build.md provide these instructions. Essentially, an agent is working at the meta-level, building higher-order abstractions for the future. 

### Evaluate Mode
Evaluates existing session results against PRD criteria:

```bash
# Evaluate a specific session
python main.py evaluate --session-id abc123def456
```

### Optimize Mode (Future)
Will automatically improve code, prompts, and workflows based on performance metrics:
```bash
# Optimize system components based on evaluation results
python main.py optimize --session-id abc123def456
python main.py optimize --component prompts --metric accuracy
```

### Reconcile Mode (Future)  
Will synchronize system state with source of truth and update workflows accordingly:
```bash
# Reconcile session state with main branch
python main.py reconcile --session-id abc123def456
python main.py reconcile --sync-prompts --sync-tools
```

These modes will implement points **5** and **6** from the core system flow, enabling continuous improvement and state synchronization capabilities.

## Data Flow Architecture

```
CLI Input → Session Init → Prompt Loading → Claude Analysis → Output Generation
    ↓           ↓              ↓               ↓              ↓
Restaurant  Session ID    System Prompt    AI Agents     Structured
   ID       Generation    Assembly         Execution     Reports
```

## Future Components
* LLM Gateway
* Telemetry & Observability 
* Cloud Deployments
* Orchestrator (synchronous, asynchronous and batch processing)
* Persistence (database, distributed file system, etc.)
* User interfaces (CLI, API, GUI, etc.)

# Conclusion
This architecture and implementation serve as the founding stone of a larger platform shift where we will be able to build systems with humans and machines always in sync. 