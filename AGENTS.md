# AGENTS.md

## Project Information
- Title:** Intelligent Security Log Summarization and Threat Timeline Generation
- Scenario: Blue teams face overwhelming volumes of security logs (e.g., Windows Event Logs, Sysmon, firewall logs) and struggle to identify critical events quickly.
- Approach: Given raw logs or summarized log batches, an LLM extracts entities (IP addresses, users, processes) and generates a natural-language attack narrative timeline, such as: “At 14:23:05, the process powershell.exe initiated a network connection to IP 10.0.0.5, likely downloading a malicious script.”
- Key Technologies: Log parsing (regex or templates), structured LLM output (JSON schema), timeline visualization.
- Deliverable: A tool that accepts uploaded log files and produces an HTML report with an interactive timeline.
- Advanced Component: Support multi-source log correlation (e.g., firewall + EDR logs).

## Background
- This is a capstone project CSC482 Capstone Project II
- This class runs as an 8-weeks summer class session (6/1-7-28)
- Divide the project into phases from Week 1 to Week 9
- Assign tasks to each team member based on their roles
- Include realistic dates and deliverables
- Create a timeline/schedule
- Output in clean Markdown format
- Save the result as PROJECT_PLAN.md in the CapstoneProject folder

## Team Members
- Derrick Redman – Team Leader + AI/LLM Specialist
- Zion Moore – Backend & Log Processing Lead
- Oriah Molton-Bowman – Frontend & Visualization Lead