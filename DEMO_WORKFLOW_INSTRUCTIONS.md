# Demo Workflow Instructions

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Purpose:** Use this checklist to practice and present the working prototype during class updates, team reviews, and the final demonstration.

## 1. Before Starting the Demo

| Done | Step | Notes |
| --- | --- | --- |
| [ ] | Confirm the latest project files are pulled from GitHub | Use VS Code Source Control and sync/pull the latest main branch before testing. |
| [ ] | Confirm `.env` exists locally | The `.env` file should contain `OPENAI_API_KEY=your_key_here`. Do not upload `.env` to GitHub. |
| [ ] | Confirm dependencies are installed | Run the project inside the Python virtual environment. |
| [ ] | Confirm sample logs are ready | Use a small test log with suspicious SSH, firewall, Windows, or Sysmon-style events. |
| [ ] | Confirm the app runs locally | The app should open at `http://127.0.0.1:5000/` on the computer running Flask. |

## 2. Start the Flask App Locally

Open PowerShell in the project folder:

```powershell
cd C:\Users\redma\Desktop\CapstoneProject
.\.venv\Scripts\Activate.ps1
python app.py
```

Then open this address in the browser:

```text
http://127.0.0.1:5000/
```

## 3. Demo Input: Paste Sample Security Logs

Use sample log text like this:

```text
Jun 17 10:14:22 webserver sshd[2214]: Failed password for invalid user admin from 203.0.113.45 port 51422 ssh2
Jun 17 10:14:29 webserver sshd[2214]: Failed password for invalid user admin from 203.0.113.45 port 51423 ssh2
Jun 17 10:15:02 webserver sshd[2288]: Accepted password for root from 203.0.113.45 port 51488 ssh2
Jun 17 10:16:10 webserver sudo: root : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND=/usr/bin/cat /etc/shadow
Jun 17 10:18:44 webserver sshd[2401]: Failed password for user oracle from 198.51.100.23 port 60011 ssh2
Jun 17 10:19:03 webserver ufw[2440]: BLOCK IN=eth0 OUT= MAC=00:16:3e:5a:7c:9b SRC=198.51.100.23 DST=10.0.0.12 LEN=60 PROTO=TCP SPT=60011 DPT=22
```

## 4. Run the Analysis

| Done | Step | Expected Result |
| --- | --- | --- |
| [ ] | Paste the sample logs into the text box | Logs appear in the input area. |
| [ ] | Click **Analyze Logs** | Flask sends the logs to the OpenAI API using the configured model. |
| [ ] | Wait for the generated report | The page should reload with structured report sections. |

## 5. Expected Report Sections

The demo should show these sections when the analysis works correctly:

| Done | Section | What to Look For |
| --- | --- | --- |
| [ ] | Executive Summary | A plain-English explanation of what happened. |
| [ ] | Risk Level | Low, Medium, High, Critical, or Unknown. |
| [ ] | Attack Type | Example: brute force, credential access, suspicious login, malware indicator, or unknown. |
| [ ] | Affected Assets | Hosts, users, IPs, or systems involved. |
| [ ] | Indicators of Compromise | Suspicious IPs, usernames, commands, event patterns, or blocked traffic. |
| [ ] | Key Findings | Short bullet points explaining the most important events. |
| [ ] | Threat Timeline | Chronological events with timestamp, source, severity, details, and evidence. |
| [ ] | Evidence | Raw log lines or important log details supporting each finding. |
| [ ] | Recommended Actions | Practical next steps for investigation, containment, and hardening. |

## 6. Explain What Is Happening During the Demo

Use this simple explanation:

> The user pastes or uploads security logs into the Flask web app. The app sends the logs to the OpenAI API using the tested model. The model returns a structured security report with a summary, risk level, findings, indicators, timeline events, evidence, and recommended actions. The goal is to help an analyst understand raw logs faster.

## 7. Team Member Talking Points

| Member | Demo Responsibility | Talking Points |
| --- | --- | --- |
| Derrick | AI/LLM workflow and team coordination | Explain the OpenAI prompt, structured output format, report sections, and GitHub project organization. |
| Zion | Backend/parser workflow | Explain how raw logs are parsed into normalized fields such as timestamp, source, host, user, event type, severity, evidence, and raw event. |
| Oriah | Frontend/report display | Explain the report layout, timeline design, user-facing sections, and future frontend improvements. |

## 8. Screenshots to Capture as Evidence

Capture these screenshots for journals, progress reports, and the final presentation:

| Done | Screenshot | Purpose |
| --- | --- | --- |
| [ ] | GitHub repository main page | Shows the shared project repository and README. |
| [ ] | GitHub commits page | Shows team progress and updates. |
| [ ] | Flask homepage | Shows the app running locally. |
| [ ] | Sample logs pasted into the app | Shows test input. |
| [ ] | Generated report summary | Shows the OpenAI analysis output. |
| [ ] | Threat timeline section | Shows chronological event display. |
| [ ] | OpenAI usage page | Shows API activity without exposing the API key. |
| [ ] | Parser output or backend test result | Shows Zion's parser work. |
| [ ] | Frontend wireframe or placeholder | Shows Oriah's frontend/report planning. |

## 9. Common Demo Issues and Fixes

| Issue | Likely Cause | Fix |
| --- | --- | --- |
| Browser says `127.0.0.1 refused to connect` | Flask app is not running | Start the app again with `python app.py`. |
| App says API key is missing | `.env` is missing or not loaded | Confirm `.env` exists and contains `OPENAI_API_KEY`. |
| OpenAI request fails | API key, model, network, or quota issue | Check the key, model name, internet connection, and OpenAI usage page. |
| Output appears incomplete | Model response may not have returned clean JSON | Re-run with a shorter log sample or improve fallback handling. |
| Teammate cannot open `127.0.0.1:5000` from their computer | `127.0.0.1` only works on the local machine | They need to run the app on their own computer or use the VM/server address. |

## 10. Final Demo Checklist

| Done | Item |
| --- | --- |
| [ ] | Latest GitHub version is pulled locally. |
| [ ] | Flask app runs without errors. |
| [ ] | OpenAI API key is configured locally but not committed to GitHub. |
| [ ] | Sample logs are ready. |
| [ ] | Report generates successfully. |
| [ ] | Timeline displays chronological events. |
| [ ] | Each team member knows their talking points. |
| [ ] | Screenshots are saved for evidence. |
| [ ] | Known limitations are ready to explain. |
