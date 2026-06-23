# Deployment and Submission Guide

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Derrick Redman, Zion Moore, Oriah Molton-Bowman

This guide explains how to run the project locally, deploy it on the required virtual machines, update GitHub, and prepare assignment evidence for submission.

## 1. Important Project Rules

| Rule | Explanation |
| --- | --- |
| Do not upload `.env` to GitHub | `.env` contains the OpenAI API key and must stay only on the local computer or VM. |
| Use `.env.example` for setup instructions | This shows the required environment variable without exposing the real key. |
| Use Flask/HTML for the shared prototype | The team agreed to continue with Flask and HTML, not Streamlit. |
| Pull from GitHub before testing | Always get the newest version before running or editing the project. |
| Commit only useful project files | Avoid uploading old PDFs, screenshots, temporary files, virtual environments, or private keys. |

## 2. Local Desktop Setup

Use this when testing on Derrick's desktop or any team member's personal computer.

### Windows PowerShell

```powershell
cd C:\Users\redma\Desktop\CapstoneProject
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open the app in a browser:

```text
http://127.0.0.1:5000/
```

Important: `127.0.0.1` only works on the computer that is running Flask. Other team members cannot open Derrick's `127.0.0.1` from their own computer.

## 3. Ubuntu 24.04 LTS VM Deployment

The professor noted that the app is expected to be hosted on the Ubuntu VM listening on port 80 or 443. For the prototype, port 80 is the simplest option.

### Install Prerequisites

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

### Get the Project From GitHub

```bash
cd ~
git clone https://github.com/Dredman72/security-log-threat-timeline.git
cd security-log-threat-timeline
```

If the repository already exists on the VM, update it instead:

```bash
cd ~/security-log-threat-timeline
git pull
```

### Create the Environment File

Create a `.env` file on the VM:

```bash
nano .env
```

Add this line with the real API key:

```text
OPENAI_API_KEY=your_real_api_key_here
```

Save and close the file.

### Install Python Packages

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run on Port 80

Flask normally runs on port 5000, but the professor wants port 80 or 443 for VM hosting.

Run:

```bash
sudo .venv/bin/python app.py
```

If `app.py` still runs on port 5000, update the bottom of `app.py` later so it can listen on `0.0.0.0` and port `80` for VM deployment:

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
```

Then the app should be available at:

```text
http://UBUNTU_VM_EXTERNAL_IP/
```

or, from another VM in the same subnet:

```text
http://UBUNTU_VM_INTERNAL_IP/
```

## 4. Ubuntu Firewall Check

If the app does not load from the browser, allow HTTP traffic:

```bash
sudo ufw allow 80/tcp
sudo ufw status
```

Also confirm the Google Cloud firewall allows HTTP traffic for the VM.

## 5. Windows Server 2025 VM Deployment

Use this if the team needs to demonstrate the app from the Windows Server VM.

### Install Python and Git

Install Python 3.12 from:

```text
https://www.python.org/downloads/
```

Install Git from:

```text
https://git-scm.com/download/win
```

Restart PowerShell after installing.

### Get the Project From GitHub

```powershell
cd C:\Users\Administrator\Desktop
git clone https://github.com/Dredman72/security-log-threat-timeline.git
cd security-log-threat-timeline
```

If the repository already exists:

```powershell
cd C:\Users\Administrator\Desktop\security-log-threat-timeline
git pull
```

### Create `.env`

Create a `.env` file in the project folder:

```text
OPENAI_API_KEY=your_real_api_key_here
```

### Install and Run

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open locally on the VM:

```text
http://127.0.0.1:5000/
```

For external access, the app needs to listen on `0.0.0.0`, and the Windows firewall must allow the selected port.

## 6. Open Windows Firewall Ports

Run PowerShell as Administrator:

```powershell
New-NetFirewallRule -DisplayName "Allow HTTP Port 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "Allow HTTPS Port 443" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
```

If using Flask port 5000 for testing:

```powershell
New-NetFirewallRule -DisplayName "Allow Flask Port 5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

## 7. GitHub Update Workflow

Use this process whenever project files are updated.

| Step | Action |
| --- | --- |
| 1 | Open `CapstoneProject` in VS Code. |
| 2 | Go to Source Control. |
| 3 | Pull or Sync Changes before editing. |
| 4 | Make or review changes. |
| 5 | Stage the changed files. |
| 6 | Write a clear commit message. |
| 7 | Commit the changes. |
| 8 | Push or Sync Changes to GitHub. |

Example commit messages:

```text
Add milestone TODO checklist
Add demo workflow instructions
Update Week 4 project progress
Add parser sample output
Update frontend report placeholder
```

## 8. Team Branch Workflow

Team members should avoid pushing unfinished work directly into `main`.

Recommended process:

| Step | Action |
| --- | --- |
| 1 | Team member creates a new branch for their work. |
| 2 | Team member commits only their role-specific files. |
| 3 | Team member pushes the branch to GitHub. |
| 4 | Team member opens a pull request. |
| 5 | Derrick reviews the files and checks for issues. |
| 6 | Team merges the pull request into `main` after review. |
| 7 | Everyone pulls/syncs the updated `main` branch. |

## 9. What Each Team Member Should Upload

| Member | Should Upload | Should Avoid |
| --- | --- | --- |
| Derrick | LLM prompt updates, Flask/OpenAI integration, README/project docs, weekly journals, milestone checklists | `.env`, private API keys, temporary files |
| Zion | Parser code, sample parsed JSON, backend schema, parser tests, backend notes | Separate unrelated full project folders |
| Oriah | HTML/CSS/JS frontend work, report layout, timeline placeholder, screenshots/wireframes if needed | Streamlit files unless the team changes direction |

## 10. Submission Evidence Checklist

Use these screenshots or files as evidence for assignments and weekly journals.

| Done | Evidence | Purpose |
| --- | --- | --- |
| [ ] | GitHub repository main page | Shows the shared repository and README. |
| [ ] | GitHub commits page | Shows project updates and contribution history. |
| [ ] | Flask homepage running locally | Shows the app can run. |
| [ ] | Sample logs pasted or uploaded | Shows test input. |
| [ ] | Generated report output | Shows OpenAI summarization and report generation. |
| [ ] | Threat timeline section | Shows chronological event output. |
| [ ] | Parser test output | Shows backend parsing progress. |
| [ ] | Frontend wireframe or placeholder | Shows UI/report progress. |
| [ ] | OpenAI usage page | Shows API activity without revealing the API key. |
| [ ] | Ubuntu VM browser page | Shows VM deployment on the required server. |
| [ ] | Windows Server VM browser page, if required | Shows Windows Server deployment/testing. |

## 11. Weekly Journal Submission Checklist

Each weekly team journal should include:

| Done | Required Section |
| --- | --- |
| [ ] | Milestones achieved |
| [ ] | Brief description of each milestone |
| [ ] | Subtasks completed |
| [ ] | Brief description of each subtask |
| [ ] | Detailed testing description |
| [ ] | Demo screenshots as evidence |
| [ ] | Lessons learned |
| [ ] | Contribution of each team member |
| [ ] | Whether progress matches the plan |
| [ ] | Plan adjustments, if any |
| [ ] | Team sign-off section, if required |

## 12. Final Submission Checklist

Before final submission, confirm:

| Done | Item |
| --- | --- |
| [ ] | GitHub README is updated and matches the project plan. |
| [ ] | `MILESTONE_TODOS.md` reflects current progress. |
| [ ] | `DEMO_WORKFLOW_INSTRUCTIONS.md` is current. |
| [ ] | The app runs locally. |
| [ ] | The app runs on the Ubuntu VM using port 80 or 443. |
| [ ] | Sample logs are included or documented. |
| [ ] | Screenshots are saved for evidence. |
| [ ] | API key is not exposed in GitHub or screenshots. |
| [ ] | Team member contributions are documented. |
| [ ] | Final presentation/demo steps are practiced. |
