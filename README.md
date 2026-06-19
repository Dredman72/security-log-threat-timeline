# Intelligent Security Log Summarization and Threat Timeline Generation

CSC 482 Capstone prototype for uploading or pasting security logs, summarizing likely threats with OpenAI, and generating a chronological incident timeline.

## Project Structure

```text
CapstoneProject/
  app.py
  requirements.txt
  .env.example
  .gitignore
  templates/
    index.html
  uploads/
    .gitkeep
  AGENTS.md
  PROJECT_PLAN.md
```

## Prerequisites

### Windows Server 2025

Run these commands in PowerShell:

```powershell
winget install Python.Python.3.12
winget install Git.Git
cd C:\Users\redma\Desktop\CapstoneProject
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
notepad .env
python app.py
```

If PowerShell blocks the virtual environment activation script, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Set `OPENAI_API_KEY` in `.env`, then open:

```text
http://127.0.0.1:5000
```

### Ubuntu 24.04 LTS

Run these commands in a terminal:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
cd ~/CapstoneProject
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
nano .env
python app.py
```

Set `OPENAI_API_KEY` in `.env`, then open:

```text
http://127.0.0.1:5000
```

## How It Works

1. The user pastes logs or uploads a supported file.
2. Flask reads the submitted log content.
3. The app sends the first 60,000 characters to OpenAI using model `gpt-5.4-nano-2026-03-17`.
4. OpenAI returns structured JSON containing an executive summary, risk level, findings, timeline events, and recommended actions.
5. The browser displays the generated report.

## Environment Variables

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.4-nano-2026-03-17
PORT=5000
```

## Semester TODO Milestones

1. Finalize project scope and supported log sources, including Windows Event Logs, Linux auth logs, firewall logs, Sysmon, and EDR alerts.
2. Build stronger log parsing modules that normalize timestamps, source IPs, usernames, hostnames, event IDs, and process names before calling the LLM.
3. Add sample datasets and test cases for benign activity, brute-force login attempts, malware execution, privilege escalation, and firewall scanning.
4. Improve prompt engineering so summaries consistently include evidence, confidence, event ordering, and clear analyst recommendations.
5. Add interactive frontend timeline controls for filtering by severity, source system, username, IP address, and event type.
6. Store analysis history in SQLite or PostgreSQL so users can reopen prior reports and compare multiple uploaded log files.
7. Add export options for HTML, PDF, and JSON reports suitable for class demos and incident-response handoff.
8. Add authentication and role separation for student analyst, team lead, and instructor/demo users.
9. Add deployment documentation and scripts for Windows Server 2025 with IIS/reverse proxy and Ubuntu 24.04 with Gunicorn/Nginx.
10. Validate privacy and safety requirements, including file-size limits, API key handling, uploaded-log cleanup, and redaction of sensitive values.

## Notes

- No model training is required.
- The prototype uses OpenAI inference through the Python SDK.
- Uploaded files are saved in `uploads/`, which is ignored by Git except for `.gitkeep`.
- For production deployment, run Flask behind a production WSGI server instead of using `python app.py` directly.
