# Problem Summary

The Swiggy Dineout GenAI Co-Pilot Challenge aims to build an AI-powered tool that generates structured, contextual performance summaries for restaurant partners. The primary users are Sales Executives and Account Managers who currently spend 30 minutes to 3 hours manually gathering performance metrics across multiple dashboards before restaurant interactions. The solution should automatically generate insights including recent performance metrics, ad campaign effectiveness, peer benchmarking, and actionable recommendations to improve efficiency and scalability across hundreds of partners per city.

For detailed information about the challenge requirements, datasets, and evaluation criteria, please refer to [Problem Statement](problem-statement.md).

# The Broader Business Problem
While this problem statement is very interesting, instead of trying to solve for it specifically, we will try to step back and understand what is the broader business problem that this problem statement is trying to solve.

## The Current State
Every organization needs certain business processes or workflows which need to be followed. Today, most organizations operate with all three approaches simultaneously:


1. **Coded Logic** - for routine data processing and basic automation, authored and maintained by technical experts (software and data engineers etc)
2. **Statistical & ML Models** - for predictions and pattern recognition, authored and maintained by technical experts (data scientists and ML engineers etc)
3. **Documentation & SOPs** - for situations where complex decision-making, edge cases, and unknown scenarios are present, authored by domain experts and executed by operational staff.

And now add to this, the new kid on the block, the 

4. **Agents** `NEW` - add reasoning and decision making to the business processes, authored and maintained by another set of technical experts (AI engineers etc)

Adding this 4th system while seems to be a no-brainer for organizations because of the benefits it offers, however it adds more complexity to an already complex system involving so many different stakeholders.

## The Problems This Creates
This fragmented and disintegrated approach creates several critical business problems:

1. **Context Loss**: Information and reasoning that flows between systems often gets siloed, lost or simplified leading to suboptimal decisions and inconsistent experiences.
2. **No Source of Truth**: Business stakeholders cannot easily audit, understand or verify what the system actually does as Business logic is scattered across documentations, SOPs, and code and these drift from each other over time.
3. **Change Management Issues**: Business logic buried in code requires technical expertise to modify and maintain
4. **Training Challenges**: New team members must learn multiple systems to understand the complete process
5. **Scaling Bottlenecks**: Manual components become bottlenecks as the business grows and the number of business processes grow

## Conceptual Solution
What if all business processes could be written in natural language and then compiled into code wherever execution is needed? This code would be extended and reviewed by software engineers before merged into the main codebase. Further code would also be reconciled back to the natural language definition continuously. 

![human-ai-interaction.svg](./images/human-ai-interaction.svg)

**Enter LLMs** : LLMs are great at generating text, but that is not their only strength. They are also great at calling tools to gather context, reasoning, and finally calling other tools to take actions. These LLMs when stationed in an environment where they can sense the environment state & events, reason about the current context and take actions towards a goal also known as agentic systems, can be used to build intelligent workflows which can be used to augment human decision making. These workflows are no different from natural language SOPs which are written by humans, for humans, with the only difference being that they are executed by an agentic system. Agents bridge the gap between business intent and technical implementation, making workflows transparent, auditable, and easily modifiable by business users.

Further with time, LLMs will be

1. Better at reasoning
2. Better at following instructions
3. Increased in context window size
4. Cheaper to run
5. Decreased latency
6. Reliable to run asynchronously over increasing amount of time
7. Available to self-host and run on-premise (smaller models specialized for specific tasks)

Hence it is inevitable that most of knowledge and operational work which is SOP driven with a lot of context and domain knowledge will be replaced by agentic systems. Humans will likely be engaged to supervise, verify and approve the actions taken by the agentic system.

# Business Value
The benefits of agentic systems are manifold. They can not only do tasks now that was not possible with the traditional paradigms, but also do them in a way that is consistent, auditable, and easily modifiable by business users. Further, they can help tie up the loose ends of the business processes and make them more efficient and effective. Business users can now focus on the strategic business logic and let the agentic system take care of the rest.

This is a win-win for the business and the business users.





