# Objective
The objective of this document is to discuss the high-level requirements for building an agentic platform for automating workflows across multiple facets of any tech-enabled organization. 

# Background

Every organization needs certain business processes or workflows which need to be executed day in and day out. Today, most organizations operate with all three approaches simultaneously:

1. **Coded Logic** - for routine data processing and basic automation, authored and maintained by technical experts (software and data engineers etc). This emerged from the need for consistent, repeatable processes at scale.
2. **Statistical & ML Models** - for predictions and pattern recognition, authored and maintained by technical experts (data scientists and ML engineers etc). These arose when rule-based systems couldn't handle pattern complexity.
3. **Documentation & SOPs** - for situations where complex decision-making, edge cases, and unknown scenarios are present, authored by domain experts and executed by operational staff. These persisted because many decisions require human judgment and context.

And now add to this, the new kid on the block, the

4. **Agents** `NEW` - add reasoning and decision making to the business processes, authored and maintained by another set of technical experts (AI engineers etc). These are emerging to bridge reasoning gaps between rules and judgment.

This approach made sense historically but has created today's integration nightmare. Adding this 4th system while seems to be a no-brainer for organizations because of the benefits it offers, however it adds more complexity to an already complex system involving so many different stakeholders.

## The Problems This Creates

This fragmented and disintegrated approach to automation creates several critical business problems:

1. **Context Loss**: Information and reasoning that flows between systems often gets siloed, lost or simplified leading to suboptimal decisions and inconsistent experiences. Teams spend significant time just coordinating handoffs between systems.
2. **No Source of Truth**: Business stakeholders cannot easily audit, understand or verify what the system actually does as Business logic is scattered across documentations, SOPs, and code and these drift from each other over time. Compliance reviews require piecing together logs and documentation from multiple disconnected systems.
3. **Change Management Issues**: Business logic buried in code requires technical expertise to modify and maintain. Simple business rule changes can take weeks to propagate across all systems, and organizations often avoid beneficial changes because the coordination overhead outweighs the benefits.
4. **Training Challenges**: New team members must learn multiple systems to understand the complete process, extending onboarding periods and increasing the risk of errors from incomplete understanding.
5. **Scaling Bottlenecks**: Manual components become bottlenecks as the business grows and the number of business processes grow. Error rates compound at handoff points between automated and manual systems.

## Conceptual Solution

What if all business processes could be written in natural language and then compiled into code wherever execution is needed? This code would be extended and reviewed by software engineers before merged into the main codebase. Further code would also be reconciled back to the natural language definition continuously.

**Enter LLMs** : LLMs are great at generating text, but that is not their only strength. They are also great at calling tools to gather context, reasoning, and finally calling other tools to take actions. These LLMs when stationed in an environment where they can sense the environment state & events, reason about the current context and take actions towards a goal also known as agentic systems, can be used to build intelligent workflows which can be used to augment human decision making. These workflows are no different from natural language SOPs which are written by humans, for humans, with the only difference being that they are executed by an agentic system. Agents bridge the gap between business intent and technical implementation, making workflows transparent, auditable, and easily modifiable by business users.

![human-ai-interaction.svg](../images/human-ai-interaction.svg)

Further with time, LLMs will be

1. Better at reasoning
2. Better at following instructions
3. Increased in context window size
4. Cheaper to run
5. Decreased latency
6. Reliable to run asynchronously over increasing amount of time
7. Available to self-host smaller models and run on-premise, specialized for specific tasks

Hence it is inevitable that most of knowledge and operational work which is SOP driven with a lot of context and domain knowledge will be replaced by agentic systems. Humans will likely be engaged to supervise these agents in the following ways:

- **Specify**: Set business goals with measurable targets, define success criteria and constraints
- **Clarify**: Resolve ambiguities when agents encounter edge cases or conflicting rules  
- **Verify**: Review outcomes, approve critical decisions, and ensure quality

This shifts human work from execution to governance, allowing experts to focus on judgment-intensive tasks while agents handle routine reasoning and coordination.

# Current Limitations of LLMs

While LLMs offer tremendous potential for automation, they come with significant limitations that must be addressed in system design. The following challenges are adapted from Andrej Karpathy's analysis:

## Core Limitations

### 1. Jagged Intelligence Profile
LLMs exhibit inconsistent performance across different domains - excelling in some areas while failing at seemingly simple tasks.

- **Example**: An LLM might solve complex mathematical proofs but struggle with basic numerical comparisons (9.11 vs 9.9)
- **Impact**: Unpredictable failure modes that require careful human oversight and validation

### 2. Anterograde Amnesia
LLMs cannot learn or retain new information after their training cutoff, making them unable to build institutional knowledge or adapt to changing contexts.

- **Analogy**: Similar to the protagonist in *Memento* or *50 First Dates* - each interaction starts fresh
- **Challenge**: Cannot develop relationships, learn from experience, or accumulate organizational knowledge
- **Requirement**: Robust memory systems and knowledge consolidation mechanisms

### 3. Hallucination and Self-Awareness Deficits
LLMs generate plausible but factually incorrect information and have poor understanding of their own capabilities and limitations.

- **Risk**: Confidently providing incorrect answers without recognizing uncertainty
- **Requirement**: External validation systems and confidence scoring mechanisms

### 4. Security Vulnerabilities
LLMs are susceptible to prompt injection attacks and can be manipulated to reveal sensitive information.

- **Risk**: Data leaks through clever prompting techniques
- **Requirement**: Robust security frameworks and input sanitization

## Design Principles

These limitations necessitate specific design approaches:

- **Explicit Specification**: Clearly define objectives, constraints, specifications, and success criteria
- **Human Oversight**: Maintain human-in-the-loop for critical decisions and validation
- **Verification Systems**: Build comprehensive validation and error detection into workflows
- **Defensive Design**: Design for limitations rather than assuming perfect capabilities
- **Memory Management**: Implement sophisticated memory and knowledge management systems
- **Security First**: Prioritize security and privacy in all system interactions

# Agentic Autonomy Levels

- **L1 - Automated Task Execution (Vanilla Agent)**: A Large Language Model (LLM) operating iteratively with access to specific tools, executing broad tasks through custom user-provided sequential instruction prompts. For example, using Claude combined with web search and Model Context Protocols (MCPs) to automate specialized coding tasks. This serves as a copilot that synchronously enhances human capabilities. The human operator must monitor the control flow and provide guidance at each step to achieve desired outcomes. This level is currently available.

- **L2 - Automated Workflow Execution (Workflow Agent)**: An agent customized to execute recurring sequences of steps following standard operating procedures (SOPs) toward specific objectives, with reasonable accuracy validation. Examples include generic open-ended workflows such as comprehensive research or specialized workflows like generating contextual performance summaries for restaurant partners. This represents a natural evolution from L1 after identifying effective patterns and automating proven components. It can operate synchronously or asynchronously to augment human capabilities. In cases where job functions lack decision-making requirements and consist purely of repeatable SOPs, it can replace human roles entirely—examples include data entry and travel agency positions. Human oversight is required at strategic decision points where errors are likely, along with batch review upon completion. This level exists to some degree but requires careful evaluation.

- **L3 - Automated Job Role Execution (Persona Agent)**: An agent capable of orchestrating multiple workflows and integrating them cohesively toward a common high-level objective, autonomously fulfilling all expectations of a specific persona's job function. This could potentially replace human workers entirely. This level is not yet available and may take considerable time to develop.

This document primarily focuses on L1 and L2, and in some cases their combination, along with methods to achieve maximum autonomy within these levels. Here are examples where combining L1 and L2 proves beneficial:

- Execute synchronous task operations multiple times to identify patterns, then formalize the acquired understanding and knowledge into a workflow.
- Employ a low-level sub-workflow as a tool during autonomous task execution.
- Perform synchronous autonomous task execution after workflow completion to engage in iterative verification through conversation.

# User Personas & Responsibilities

- **P1 (Business Owner/Domain Expert)**: Sets specific business goals with measurable targets, defines success criteria and constraints, approves final implementations
- **P2 (Process Analyst/Product Owner)**: Identifies automation opportunities, defines processes and workflows, analyzes patterns, designs solutions, defines success metrics, creates MVPs
- **P3 (Technical Expert)**: Implements production systems, handles integrations, ensures reliability and security

These personas represent functional roles rather than fixed job titles. The same individual may operate across multiple personas depending on context and organizational structure. For example:

- A product owner might act as P1 when setting goals for their business area, then shift to P2 when designing the automation solution
- In smaller organizations, one person might fulfill all three roles
- As automation matures, some P2 and P3 functions may themselves become automated
- Automation might extend beyond core business processes to include supporting functions across the entire organization.

# User Stories

## **P1 User Stories (Goal Setter - Business Owner/Domain Expert)**

### **Goal Definition & Success Criteria**
- **As P1**, I want to set specific business objectives with measurable targets (e.g., "reduce customer response time by 30%"), so that my team knows exactly what outcomes to achieve.
- **As P1**, I want to define success criteria and acceptable risk levels for automation initiatives, so that implementations align with business priorities.
- **As P1**, I want to understand the potential impact and ROI of automation opportunities, so that I can prioritize investments effectively.

### **Oversight & Approval**
- **As P1**, I want to approve final automation implementations before they go live, so that I maintain control over what changes are made to business operations.
- **As P1**, I want to receive regular reports on automation performance against my defined goals, so that I can assess whether objectives are being met.
- **As P1**, I want to be alerted when automated processes fail to meet target metrics, so that I can decide whether to adjust goals or escalate for fixes.

### **Strategic Decision Making**
- **As P1**, I want to adjust business targets based on automation capabilities and performance data, so that goals remain realistic and achievable.
- **As P1**, I want to understand which automation investments are delivering the highest ROI, so that I can allocate resources effectively.
- **As P1**, I want to identify new business opportunities enabled by successful automation, so that I can expand our competitive advantages.

## **P2 User Stories (Solution Designer - Product Owner/Process Analyst)**

### **Goal Translation & Process Discovery**
- **As P2**, I want to translate business goals into specific automation opportunities, so that technical teams can understand what needs to be built.
- **As P2**, I want to analyze current manual processes to identify automation opportunities that could achieve P1's targets, so that I can proactively suggest high-value automations.
- **As P2**, I want to break down complex business goals into structured workflow components, so that I can design implementable automation solutions.
- **As P2**, I want to define processes in natural language (like writing SOPs) based on business objectives, so that technical requirements are clearly specified.
- **As P2**, I want to estimate the effort and complexity of automating a process before committing resources, so that we can make informed investment decisions.

### **Workflow Design & Validation**
- **As P2**, I want to map business logic to agent capabilities and identify where human oversight is needed, so that I can create balanced human-AI workflows.
- **As P2**, I want to prototype and test automation workflows in a sandbox environment, so that I can iterate on designs to create MVPs before production deployment.
- **As P2**, I want to define success metrics and KPIs for automated workflows that align with P1's business targets, so that I can measure automation effectiveness and ROI.
- **As P2**, I want to analyze workflow performance data and identify bottlenecks, so that I can continuously optimize automation processes to meet business goals.
- **As P2**, I want to A/B test different workflow variations, so that I can find the most effective automation approach.

### **Process Management & Scaling**
- **As P2**, I want to define approval gates and human checkpoints in automated workflows based on business risk tolerance, so that critical decisions remain controlled.
- **As P2**, I want to design escalation paths for when automation encounters scenarios it cannot handle, so that work doesn't get stuck and business goals remain achievable.
- **As P2**, I want to extract patterns from successful automations to create templates for similar processes, so that we can accelerate future automation efforts.
- **As P2**, I want to continuously modify workflow rules when business requirements change, so that automation adapts to evolving needs while maintaining goal alignment.

## **P3 User Stories (Implementation Expert - Technical Specialist)**

### **Development & Integration**
- **As P3**, I want to convert workflow specifications/MVPs into reliable, production-ready agent systems, so that business requirements are technically implemented correctly.
- **As P3**, I want to integrate agent workflows with existing systems and APIs, so that automation works seamlessly within current infrastructure.
- **As P3**, I want to implement proper error handling, logging, and monitoring for agent workflows, so that I can maintain system reliability and debuggability.
- **As P3**, I want to implement gradual rollout mechanisms for new automations, so that we can limit blast radius of potential issues.
- **As P3**, I want to create reusable horizontal utilities that can be shared across different automations, so that we avoid duplicating effort and maintain consistency.

### **Operations & Maintenance**
- **As P3**, I want to troubleshoot automation failures without needing to understand the entire business context, so that I can provide quick technical support.
- **As P3**, I want to monitor resource consumption and costs of running automations, so that we can optimize for efficiency.
- **As P3**, I want to version control workflow configurations and track changes over time, so that I can manage evolution and rollback if needed.
- **As P3**, I want to set up automated testing and validation for agent workflows, so that I can ensure continued accuracy as systems evolve.
- **As P3**, I want to build comprehensive evaluation frameworks that assess agent performance using multiple rubrics (accuracy, speed, cost, reliability, user satisfaction), so that I can objectively measure and maintain automation quality across different dimensions over time.

### **Governance & Intelligence**
- **As P3**, I want to implement security controls and audit trails for automated processes, so that I can meet compliance and governance requirements.
- **As P3**, I want the system to learn from manual interventions and suggest workflow improvements, so that automations get better with use.
- **As P3**, I want to enable agents to analyze their own performance and automatically propose optimizations to their workflows, so that the system recursively self-improves without constant human intervention.

# Meta-Intelligence Leverage

Meta-intelligence is using intelligence to improve intelligence itself - thinking about thinking to get better at thinking, reasoning about reasoning itself. Humans have multiple levels of meta-intelligence. A chess master doesn't just make good moves; they study their decision patterns, identify cognitive traps, and develop frameworks that make them better at strategy itself. 

Similar to humans, LLMs are a sophisticated pattern-matching engines that stochastically mimic humans. Since are trained over the entire internet and further reinforcement trained to be more accurate, they absorb language patterns and reasoning styles to approximate human-like responses. Hence, we can build a bunch of other meta workflows using LLMs which work as a layer of abstraction over core workflows across the end-to-end lifecycle. This leads to a vicious dog-fooding cycle and exponential improvement in the quality of the Agentic workflows.

- **Core workflows** solve business problems (basic intelligence)
- **Meta workflows** build, manage, operate, and optimize core workflows (meta-intelligence)

This transforms automation from linear efficiency gains to exponential capability growth.

## Recursive Self-Improvement Flow

Based on this, we can build a recursive self-improvement flow where meta-workflows continuously refine the core workflows for incremental improvements. Here is what it might look like:

![Recursive Cycle](../images/recursive-cycle.svg)

# Success Criteria 
(numbers are just for reference)

- Platform Adoption
  - 70% of target users creating/invoking workflows weekly - Measures actual useful usage
- Business Impact
  - 10,000+ manual hours saved annually - Measurable reduction in repetitive tasks across organization
- Technical Reliability
  - 95% workflow success rate with <10% human intervention - Automated processes work consistently without manual fixes