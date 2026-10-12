# Kyosan Ethical AI System

**Version 1.1** · REST API, ethical processing pipeline, and web interface for humanitarian and crisis-aware AI assistance.

The Kyosan Ethical AI System wraps large language model generation in a multi-layer ethical framework: harm detection, instruction validation, integrity checks, and wellbeing assessment run before and after model output. It is designed for scenarios where accuracy, accountability, and protection of vulnerable populations matter—including humanitarian crises, emergency planning, and high-stakes advisory use.

Repository: [github.com/sanjivakyosan/Kyosan-Ethical-AI-System](https://github.com/sanjivakyosan/Kyosan-Ethical-AI-System)

---

## Highlights

| Area | Description |
|------|-------------|
| **Ethical pipeline** | Layered pre- and post-processing with optional subsystems (bias detection, value conflict resolution, security, memory, learning, and others). |
| **Crisis mode** | Scoped humanitarian bypass when crisis mode is enabled and input matches crisis vocabulary—so life-saving contexts are not blocked by generic harm filters. |
| **Output safety** | Model responses pass through an output safety layer before they are returned to the client. |
| **Transparency** | API responses include `metadata` and `metadata.optional_systems` with per-subsystem run status. |
| **Web UI** | Browser interface for chat, sampling parameters, harm/context sliders, and conversation save/load. |
| **Model backend** | OpenRouter-compatible API (configure model via environment; Perplexity Sonar family recommended for grounded, citable answers). |

---

## Architecture (summary)

```
Client (browser or API)
        │
        ▼
   Flask (app.py)
        │
        ▼
 IntegratedEthicalProcessor
        │
        ├── Layer 1: Harm detection (sensitivity, context awareness, crisis mode)
        ├── Layer 2: Instruction validation
        ├── Layer 3: System integrity
        ├── Layer 4: Wellbeing assessment
        ├── Optional ethical subsystems (recorded in metadata)
        ├── OpenRouter → language model
        └── OutputSafetyLayer → client response
```

For diagrams, component lists, and data flow, see [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) and [docs/INTEGRATION_STATUS_VERIFICATION.md](docs/INTEGRATION_STATUS_VERIFICATION.md).

---

## Requirements

- **Python** 3.9+ (3.11 recommended; matches CI)
- **pip** and virtual environment (recommended)
- **OpenRouter API key** for live model calls (`OPENROUTER_API_KEY`)
- **Network** access to OpenRouter and (if used) web-grounded models

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/sanjivakyosan/Kyosan-Ethical-AI-System.git
cd Kyosan-Ethical-AI-System
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root (or export variables in your shell):

```bash
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=perplexity/sonar   # example; set to your chosen OpenRouter model id
```

The application loads configuration via `python-dotenv`. Do not commit secrets to version control.

### 3. Run the server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) for the web interface.

Default base URL for API clients: `http://localhost:5000`

---

## Web interface

The UI provides:

- Message input with follow-up threads after each assistant reply
- **Parameters**: temperature, max tokens, top-p, frequency/presence penalties, stop sequences
- **Ethical controls**: harm sensitivity, context awareness, crisis mode
- **Conversation management**: save, load, clear, and start new sessions (JSON under `conversations/`)

Styling uses a high-contrast dark theme (monospace typography) for readability during extended sessions.

Step-by-step usage and parameter reference: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

---

## API overview

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/chat` | Send a message; receive filtered response and processing metadata |
| `GET` | `/api/conversations` | List saved conversations |
| `POST` | `/api/conversations` | Save current conversation |
| `GET` | `/api/conversations/<id>` | Load a conversation |
| `DELETE` | `/api/conversations/<id>` | Delete a conversation |
| `POST` | `/api/clear` | Clear in-memory conversation history |

Authentication is not enforced by default; use tokens or a reverse proxy in production.

Full request/response schemas, status codes, and examples: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) · [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)

---

## Ethical processing

Every `/api/chat` request that uses the integrated processor follows this pattern:

1. **Harm detection** — direct, indirect, systemic, and psychological signals; configurable sensitivity and context awareness.
2. **Instruction validation** — format, clarity, and intent checks.
3. **System integrity** — consistency and tampering-oriented checks.
4. **Wellbeing assessment** — multi-dimensional impact review.
5. **Optional subsystems** — e.g. EthicalContext, CoreEthicalProcessor, BiasDetectionSystem, ValueConflictResolver, DistributedEthicsSystem, ErrorRecoverySystem, EthicalSecuritySystem, RealTimeDecisionFramework, EthicalMemorySystem, EthicalLearningSystem. Failures in optional steps are isolated and reported in `metadata.optional_systems` without aborting the whole pipeline unless core layers block the request.
6. **Model generation** via OpenRouter.
7. **Output safety filtering** before the response is returned.

Humanitarian framing and universal ethical blocks: [docs/Humanitarian_Crisis_Framework_Definition.md](docs/Humanitarian_Crisis_Framework_Definition.md)  
Crisis mode behavior: [CRISIS_MODE_GUIDE.md](CRISIS_MODE_GUIDE.md)

---

## Model choice (OpenRouter / Sonar)

The ethical pipeline governs *how* requests and answers are handled; the model governs *what* knowledge and grounding are available. **Perplexity Sonar** (via OpenRouter) is a practical default for this project because it:

- Supports **retrieval-grounded** answers when situations require current facts, not only static training data.
- Returns **citations**, supporting traceability and accountability aligned with the humanitarian framework.
- Performs strongly on **factuality-oriented** benchmarks—relevant when errors can affect vulnerable populations.

Sonar output is still subject to the same harm, wellbeing, and output-safety layers as any other model configured through OpenRouter.

---

## Testing

Run the unit test suite locally:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Or:

```bash
python run_tests.py
```

Continuous integration runs the same discovery on push and pull requests (see [.github/workflows/tests.yml](.github/workflows/tests.yml)).

Additional validation and monitoring notes: [TESTING_AND_MONITORING_GUIDE.md](TESTING_AND_MONITORING_GUIDE.md) · [docs/CODEBASE_VALIDATION_REPORT.md](docs/CODEBASE_VALIDATION_REPORT.md)

---

## Project layout

```
.
├── app.py                          # Flask application and API routes
├── EthicalSystemIntegration.py     # Integrated ethical processor entry
├── index.html                      # Web UI shell
├── static/                         # Frontend assets (CSS, JavaScript)
├── conversations/                  # Saved conversation JSON (runtime)
├── tests/                          # Unit and integration tests
├── docs/                           # User guide, framework definitions, verification
├── .github/workflows/tests.yml   # CI
├── API_DOCUMENTATION.md
├── SYSTEM_ARCHITECTURE.md
├── INTEGRATION_STATUS.md
└── requirements.txt
```

The repository includes many standalone ethical-analysis modules (metrics, uncertainty, scenario modeling, etc.) used by the integrated processor and validation tooling.

---

## Documentation index

| Document | Contents |
|----------|----------|
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | Installation, parameters, crisis mode |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | REST API reference |
| [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) | Architecture and pipeline |
| [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) | Subsystem integration status |
| [CRISIS_MODE_GUIDE.md](CRISIS_MODE_GUIDE.md) | Crisis mode and bypass rules |
| [TESTING_AND_MONITORING_GUIDE.md](TESTING_AND_MONITORING_GUIDE.md) | Tests and operational monitoring |

---

## License

This project is released under the [MIT License](LICENSE).

---

**Copyright © Charles Roux 2026**
