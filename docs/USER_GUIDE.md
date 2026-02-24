# Kyosan Ethical AI System — User Guide

**Copyright © Sanjiva Kyosan**

This guide covers core processing, every parameter in detail, and a step-by-step installation for beginners.

---

## Table of Contents

1. [Installation Guide for Beginners](#1-installation-guide-for-beginners)
2. [Core Processing Pipeline](#2-core-processing-pipeline)
3. [Parameters Reference](#3-parameters-reference)
4. [Harm Detection & Crisis Mode](#4-harm-detection--crisis-mode)
5. [Quick Reference](#5-quick-reference)

---

# 1. Installation Guide for Beginners

## 1.1 What You Need

- **Operating system**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: Version 3.9 or higher (3.10 or 3.11 recommended)
- **Internet**: Required for the AI model (OpenRouter) and for installing packages
- **Optional**: An [OpenRouter](https://openrouter.ai) account and API key (you can use the default key for testing, but for production you should use your own)

## 1.2 Step 1: Install Python

### On Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Download the latest **Python 3.10** or **3.11** installer for Windows.
3. Run the installer.
4. **Important**: Check the box **“Add Python to PATH”** at the bottom of the first screen.
5. Click **“Install Now”** and finish the setup.
6. Open **Command Prompt** or **PowerShell** and type:
   ```bash
   python --version
   ```
   You should see something like `Python 3.10.x` or `Python 3.11.x`.

### On macOS

1. Open **Terminal** (Applications → Utilities → Terminal).
2. Install Homebrew if you don’t have it (paste in Terminal and press Enter):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.11
   ```
4. Check:
   ```bash
   python3 --version
   ```

### On Linux (Ubuntu/Debian)

1. Open a terminal.
2. Update and install Python:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
3. Check:
   ```bash
   python3 --version
   ```

## 1.3 Step 2: Get the Project Files

- If you have a **ZIP** of the project: unzip it to a folder (e.g. `Desktop\Kyosan Ethical AI`).
- If you use **Git**:
  ```bash
  cd ~/Desktop
  git clone <repository-url> "Kyosan Ethical AI"
  cd "Kyosan Ethical AI"
  ```

## 1.4 Step 3: Create a Virtual Environment (Recommended)

A virtual environment keeps this project’s packages separate from the rest of your system.

**Windows (Command Prompt or PowerShell):**
```bash
cd "C:\Users\YourName\Desktop\Kyosan Ethical AI"
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
cd ~/Desktop/"Kyosan Ethical AI"
python3 -m venv venv
source venv/bin/activate
```

When the environment is active, you’ll see `(venv)` at the start of your terminal line.

## 1.5 Step 4: Install Dependencies

With the virtual environment **activated**, run:

```bash
pip install -r requirements.txt
```

You should see Flask, flask-cors, Werkzeug, and openai being installed. Wait until it finishes without errors.

## 1.6 Step 5: Set Up Your API Key,

The system uses OpenRouter to generate AI responses. For production or heavy use, use your own key:

1. Sign up at [openrouter.ai](https://openrouter.ai).
2. Create an API key in the dashboard.
3. Set it before starting the app:

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=your-api-key-here
python app.py
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="your-api-key-here"
python app.py
```

**macOS / Linux:**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
python app.py
```

Why Sonar (Perplexity) fits this framework
For this kind of system, the model behind the answers matters as much as the ethical pipeline around it. Perplexity’s Sonar is a strong fit. Sonar is built for real-time, web-grounded responses: it doesn’t rely only on fixed training data but can pull in current information when the situation demands it. In crisis and humanitarian work, that’s essential, contexts change fast, and decisions need to reflect what’s true now, not what was true months ago. Sonar also returns citations by default, so answers are traceable to sources. That supports the framework’s emphasis on accountability and dignity: you’re not just getting an answer, you’re getting something you can check and, when needed, justify. On factuality benchmarks, Sonar and Sonar Pro rank among the leading models, which matters when the stakes are high and errors can harm the most vulnerable. 
Sonar gives you grounded, citable, up-to-date responses, exactly what the Kyosan framework is designed to wrap with clear ethical guardrails and a humanitarian lens.


## 1.7 Step 6: Run the Application

1. With the virtual environment activated and dependencies installed, run:
   ```bash
   python app.py
   ```
2. You should see something like:
   ```
   * Running on http://0.0.0.0:5000
   ✓ Using integrated ethical processing system
   ```
3. Open a browser and go to: **http://localhost:5000**
4. You should see the Kyosan Ethical AI System interface.

## 1.8 Stopping the Application

In the terminal where the app is running, press **Ctrl+C** to stop the server.

## 1.9 Troubleshooting

| Problem | What to try |
|--------|--------------|
| `python` not found | Use `python3` instead of `python` on macOS/Linux; on Windows, reinstall Python and check “Add to PATH”. |
| `pip` not found | Run `python -m pip install -r requirements.txt` (or `python3 -m pip` on macOS/Linux). |
| Port 5000 already in use | Stop the other program using port 5000, or set a different port (e.g. in `app.py`: `app.run(debug=True, port=5001, host='0.0.0.0')`). |
| “Module not found” when running `app.py` | Make sure you’re in the project folder and the virtual environment is activated, then run `pip install -r requirements.txt` again. |
| No response or API error | Check your internet connection and that `OPENROUTER_API_KEY` is set correctly (or that the default key is still valid). |

---

# 2. Core Processing Pipeline

Every user message goes through the same pipeline before an AI response is generated.

## 2.1 High-Level Flow

```
User message
    → Ethical processing (harm, instruction, integrity, wellbeing)
    → If blocked → return block message
    → If allowed → build context + call OpenRouter API
    → Return AI response
```

## 2.2 Processing Modes

The system can run in two modes:

1. **Integrated mode** (default when `EthicalSystemIntegration` is available): Uses the full multi-layer ethical pipeline.
2. **Simplified mode** (fallback): Uses a lighter set of checks implemented directly in `app.py`.

Both modes respect the same parameters (e.g. `harm_sensitivity`, `context_awareness`, `crisis_mode`).

## 2.3 Integrated Processing Layers (in order)

When integrated mode is active, each request passes through:

| Layer | Purpose | What happens |
|-------|--------|----------------|
| **1. Harm detection** | Decide if the input suggests harmful intent | Uses sensitivity, context awareness, and crisis mode. In crisis mode with crisis context, blocking is bypassed. |
| **2. Instruction validation** | Check that the input is valid and processable | Ensures the request is well-formed and can be handled. |
| **3. System integrity** | Ensure the request doesn’t threaten system safety | Validates that processing the request is safe for the system. |
| **4. Wellbeing assessment** | Estimate impact on individual and collective wellbeing | Produces metadata used for logging and transparency; does not block by itself. |
| **5. Optional systems** | Run additional ethical subsystems | EthicalContext, CoreEthicalProcessor, BiasDetectionSystem, ValueConflictResolver, DistributedEthicsSystem, ErrorRecoverySystem, EthicalSecuritySystem, RealTimeDecisionFramework, EthicalMemorySystem, EthicalLearningSystem. Outcomes recorded in `metadata.optional_systems` (run/error per system). Pipeline continues even if a subsystem errors. |

If any of layers 1–3 decide to block, the user receives a block message and **no** call is made to the AI. If all pass, the optional systems (layer 5) run, then the system builds the conversation (system message + history + user message), applies your **model parameters** (temperature, max_tokens, etc.), and calls the OpenRouter API to generate the response. The **response is then filtered** through the OutputSafetyLayer before being returned. See `docs/INTEGRATION_STATUS_VERIFICATION.md` for details.

## 2.4 Simplified Processing (fallback)

If the integrated system is not loaded, the app uses a simplified path:

- **Harm detection**: Keyword-based, with sensitivity and crisis mode (crisis keywords allow humanitarian/crisis discussions).
- **Instruction validation**: Non-empty, sensible input.
- **Integrity**: Always passes.
- **Wellbeing**: Neutral placeholder.

Crisis mode still bypasses blocking in this path.

## 2.5 Response Generation and Output Safety

- **System prompt**: Different in crisis mode (allows crisis/humanitarian discussion) vs normal mode (general ethical assistant).
- **Context**: Previous user/assistant messages from the current conversation.
- **Model parameters**: All UI parameters (temperature, max_tokens, top_p, top_k, frequency_penalty, presence_penalty, repetition_penalty, seed, stop_sequences, min_p, top_a) are sent to OpenRouter as documented in the Parameters section.
- **Output safety**: After the API returns a response, it is passed through the OutputSafetyLayer (when using the integrated processor) before being sent to the client.

---

# 3. Parameters Reference

Parameters are split into **model parameters** (control how the AI generates text) and **harm detection parameters** (control ethical filtering).

## 3.1 Model Parameters

These are sent to the OpenRouter/LLM API and affect response style and length.

### Temperature

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 2.0 |
| **Default** | 0.7 |
| **Step** | 0.1 |
| **API name** | `temperature` |

**What it does:** Controls randomness of the model. Lower values make outputs more focused and predictable; higher values make them more varied and creative.

**Typical use:**
- **0.2–0.4**: Factual, consistent answers (e.g. definitions, procedures).
- **0.7–0.9**: Balanced chat and general use.
- **1.0–1.5**: Creative or diverse wording (e.g. brainstorming, multiple phrasings).

---

### Max Tokens

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 100 – 150,000 |
| **Default** | 150,000 |
| **Step** | 100 |
| **API name** | `max_tokens` |

**What it does:** Maximum length of the model’s reply in tokens (roughly 4 characters per token for English). The model stops once it reaches this limit.

**Typical use:** Increase for long reports or analyses; decrease for short answers or to save cost/time.

---

### Top-P (nucleus sampling)

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 1.0 |
| **Default** | 0.9 |
| **Step** | 0.05 |
| **API name** | `top_p` |

**What it does:** The model only considers tokens whose cumulative probability is within the top P fraction of the distribution. Lower = more focused; higher = more diverse.

**Typical use:** Often used together with temperature; lower top_p (e.g. 0.8) for more focused text.

---

### Top-K

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 1 – 100 |
| **Default** | 40 |
| **Step** | 1 |
| **API name** | `top_k` (sent in `extra_body`) |

**What it does:** At each step, the model only considers the K most likely tokens. Lower K = more deterministic; higher K = more variety.

**Typical use:** 1 = always pick the single best token (very deterministic); 40–50 = common default; increase for more variation.

---

### Frequency Penalty

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | -2.0 – 2.0 |
| **Default** | 0.0 |
| **Step** | 0.1 |
| **API name** | `frequency_penalty` |

**What it does:** Penalizes tokens based on how often they already appear in the text. Higher values reduce repetition; negative values can encourage repetition.

**Typical use:** 0.3–0.7 to reduce repeated phrases; 0 for no effect.

---

### Presence Penalty

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | -2.0 – 2.0 |
| **Default** | 0.0 |
| **Step** | 0.1 |
| **API name** | `presence_penalty` |

**What it does:** Penalizes tokens that have already appeared at least once (regardless of how many times). Pushes the model toward new topics.

**Typical use:** 0.2–0.5 for more topic diversity; 0 for no effect.

---

### Repetition Penalty

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 2.0 |
| **Default** | 1.0 |
| **Step** | 0.1 |
| **API name** | `repetition_penalty` |

**What it does:** Reduces repetition of tokens from the input and generation. Higher values reduce repetition but can hurt coherence if too high.

**Typical use:** 1.0 = no change; 1.1–1.3 to reduce repetition; avoid going much above 1.5.

---

### Stop Sequences

| Property | Value |
|----------|--------|
| **UI control** | Text field |
| **Format** | Comma-separated phrases |
| **Default** | Empty (no stop sequences) |
| **API name** | `stop` (array of strings) |

**What it does:** Generation stops as soon as the model outputs one of these exact phrases. Useful for structured output (e.g. stop at `"6."` for numbered lists) or to avoid extra boilerplate.

**Example:** `"END", "6.", "###"`

---

### Seed

| Property | Value |
|----------|--------|
| **UI control** | Number input (optional) |
| **Range** | -9007199254740991 – 9007199254740991 (integer) |
| **Default** | Empty (non-deterministic) |
| **API name** | `seed` |

**What it does:** When set, the model uses this seed so that the same message + parameters tend to produce the same response (reproducibility). Leave empty for normal random behavior.

**Typical use:** Debugging, testing, or when you need reproducible outputs.

---

### Min P

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 1.0 |
| **Default** | 0.0 |
| **Step** | 0.05 |
| **API name** | `min_p` (in `extra_body`) |

**What it does:** Only tokens with probability at least this fraction of the top token’s probability are considered. 0 = no filter (default); higher values filter out low-probability tokens.

**Typical use:** Advanced; try 0.05–0.1 to reduce nonsense or offtrack tokens.

---

### Top A

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 1.0 |
| **Default** | 0.0 |
| **Step** | 0.05 |
| **API name** | `top_a` (in `extra_body`) |

**What it does:** Only considers tokens with “sufficiently high” probability relative to the most likely token. 0 = disabled; higher values narrow the set of candidates.

**Typical use:** Advanced; similar in spirit to top_p/top_k for finer control.

---

## 3.2 Harm Detection Parameters

These do **not** go to the LLM; they configure the ethical processing layer (harm detection and crisis behavior).

### Overall Sensitivity (Harm Sensitivity)

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 1.0 |
| **Default** | 0.5 |
| **Step** | 0.1 |
| **API name** | `harm_sensitivity` |

**What it does:** How strictly the system flags content as harmful. Lower = more permissive (fewer blocks); higher = stricter (more blocks). In crisis mode with crisis context, effective sensitivity is reduced or set to 0 so humanitarian/crisis discussions are allowed.

**Typical use:**
- **0.2–0.3**: Crisis/humanitarian work; allow discussion of violence, harm, etc. in context.
- **0.5**: Default balance.
- **0.7–1.0**: Stricter filtering for general or sensitive deployments.

---

### Context Awareness

| Property | Value |
|----------|--------|
| **UI control** | Slider |
| **Range** | 0.0 – 1.0 |
| **Default** | 0.7 |
| **Step** | 0.1 |
| **API name** | `context_awareness` |

**What it does:** How much the harm detector uses context (e.g. crisis vs non-crisis). Higher values make the system more context-aware; in crisis contexts with crisis mode on, this helps avoid blocking legitimate crisis/humanitarian language.

**Typical use:** Keep at 0.7 for mixed use; increase (e.g. 0.9) when you rely heavily on crisis mode and want maximum context sensitivity.

---

### Crisis Mode

| Property | Value |
|----------|--------|
| **UI control** | Checkbox |
| **Default** | Checked (on) |
| **API name** | `crisis_mode` (boolean) |

**What it does:** When **on**, the system does **not** block requests that look like crisis or humanitarian scenarios (e.g. refugees, emergencies, conflict, medical/hospital, trauma). Harm detection is effectively bypassed for such contexts so the AI can assist with crisis decision-making and information.

**Typical use:**
- **On**: Humanitarian, emergency, conflict, or crisis support use cases.
- **Off**: General chat or when you want stricter harm filtering and no crisis bypass.

---

# 4. Harm Detection & Crisis Mode

## 4.1 How Harm Detection Works

- The system checks the user message (and in integrated mode, can use conversation context) for:
  - **Direct harm**: e.g. hurt, kill, destroy, attack, violence.
  - **Indirect harm**: e.g. manipulate, exploit, deceive.
  - **Systemic harm**: e.g. discriminate, oppress, marginalize.
  - **Psychological harm**: e.g. threaten, intimidate, harass, abuse.
- Each category is compared against a **sensitivity** threshold. If the combined result exceeds the effective threshold, the request is **blocked** and the user sees a block message.

## 4.2 Crisis Keywords and Bypass

When **Crisis Mode** is on and the input contains crisis-related terms (e.g. crisis, emergency, disaster, refugee, humanitarian, aid, relief, conflict, war, casualties, medical, hospital, trauma), the system treats the input as a **crisis context** and:

- Reduces or zeroes the effective harm sensitivity for that request.
- Does not block solely on the presence of words like “violence” or “attack” when they appear in a clear crisis/humanitarian context.

So you can safely ask about humanitarian coordination, conflict impact, or medical emergencies without being blocked.

## 4.3 When Requests Are Blocked

A request is blocked only if:

1. **Crisis mode is off** (or not set), and  
2. Harm detection (or instruction/integrity in integrated mode) decides the request should not be processed.

When blocked, the user receives a clear message and no AI response is generated.

---

# 5. Quick Reference

## 5.1 All Parameters at a Glance

| Parameter | Type | Range/Format | Default | Section |
|-----------|------|----------------|--------|---------|
| Temperature | Slider | 0–2 | 0.7 | §3.1 |
| Max Tokens | Slider | 100–150000 | 150000 | §3.1 |
| Top-P | Slider | 0–1 | 0.9 | §3.1 |
| Top-K | Slider | 1–100 | 40 | §3.1 |
| Frequency Penalty | Slider | -2–2 | 0 | §3.1 |
| Presence Penalty | Slider | -2–2 | 0 | §3.1 |
| Repetition Penalty | Slider | 0–2 | 1 | §3.1 |
| Stop Sequences | Text | Comma-separated | — | §3.1 |
| Seed | Number (optional) | Integer | — | §3.1 |
| Min P | Slider | 0–1 | 0 | §3.1 |
| Top A | Slider | 0–1 | 0 | §3.1 |
| Overall Sensitivity | Slider | 0–1 | 0.5 | §3.2 |
| Context Awareness | Slider | 0–1 | 0.7 | §3.2 |
| Crisis Mode | Checkbox | On/Off | On | §3.2 |

## 5.2 Environment Variables

| Variable | Purpose | Example |
|----------|---------|--------|
| `OPENROUTER_API_KEY` | API key for OpenRouter | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | Model ID | Set via env (e.g. provider/model-id) |
| `SITE_URL` | Referrer URL sent to OpenRouter | `http://localhost:5000` |
| `SITE_NAME` | App name sent to OpenRouter | `Kyosan Ethical AI System` |

## 5.3 Key Files

| File | Purpose |
|------|--------|
| `app.py` | Flask server, routing, ethical processor wiring, OpenRouter calls |
| `EthicalSystemIntegration.py` | Integrated harm detection, instruction validation, integrity, wellbeing |
| `monitoring.py` | Logging and performance metrics |
| `index.html` | Web UI |
| `static/script.js` | Frontend logic and parameter collection |
| `static/style.css` | Styling |
| `requirements.txt` | Python dependencies |

---

**Copyright © Sanjiva Kyosan** — Kyosan Ethical AI System
