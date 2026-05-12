<p align="center">
  <img src="https://myclover.tech/images/logo.png" alt="MyClover.Tech" width="80">
</p>

<h1 align="center">CloverBot</h1>
<p align="center"><strong>AI-Powered Support Agent for MyClover.Tech</strong></p>
<p align="center">
  Embeddable chat widget + intelligent backend that knows your products, pricing, hardware specs, and troubleshooting inside and out.
</p>

---

## What Is CloverBot?

CloverBot is a branded AI support agent designed for [MyClover.Tech](https://myclover.tech). It combines a beautiful dark-theme chat widget with a RAG-powered backend that retrieves answers from your product knowledge base.

**Key highlights:**
- **One-line embed** — drop a `<script>` tag on any page
- **Cloud or Local AI** — start with OpenAI, swap to Ollama with one env var
- **RAG-powered** — vector search over product docs, not generic AI responses
- **Personality** — confident, witty, technically sharp (not a corporate chatbot)
- **Lead capture + Slack alerts** — capture visitor info, get notified on escalations

---

## Architecture

```
┌──────────────────┐          ┌──────────────────────────┐
│  Your Website    │   API    │  CloverBot Backend       │
│  + cloverbot.js  │ ◄─────► │  (FastAPI · port 8400)   │
│  (chat widget)   │          │                          │
└──────────────────┘          │  ├─ LLM (OpenAI/Ollama)  │
                              │  ├─ RAG (ChromaDB)       │
                              │  ├─ SQLite (logs)        │
                              │  └─ Slack (escalation)   │
                              └──────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.9+
- An OpenAI API key (or Ollama installed locally)

### 1. Install dependencies

```bash
cd cloverbot
pip install -r requirements.txt
```

### 2. Configure environment

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Open `.env` and set your `OPENAI_API_KEY`.

### 3. Start the server

```bash
python main.py
```

CloverBot starts on `http://localhost:8400`. The knowledge base auto-ingests on first boot.

### 4. Test it

Open your browser to: **http://localhost:8400/widget**

You'll see a branded demo page with CloverBot's chat bubble in the bottom-right corner. Click it and start chatting.

---

## Project Structure

```
cloverbot/
├── main.py                  # FastAPI server (entry point)
├── config.py                # Configuration + system prompt personality
├── llm.py                   # LLM interface (OpenAI + Ollama)
├── rag.py                   # RAG pipeline (ChromaDB vector search)
├── database.py              # SQLite conversation & lead logging
├── escalation.py            # Slack webhook escalation alerts
├── requirements.txt         # Python dependencies
├── .env.example             # Configuration template
│
├── static/
│   ├── cloverbot.js         # Chat widget v2.0 (embed on your site)
│   └── widget.html          # Branded demo/showcase page
│
├── knowledge/               # Product docs for RAG ingestion
│   ├── products-overview.md # Full product catalog with pricing
│   ├── faq.md               # Frequently asked questions
│   ├── accessories.md       # Accessories & add-ons
│   └── technical-support.md # Deep troubleshooting guides
│
└── scripts/
    └── ingest.py            # Manual knowledge re-ingestion
```

---

## Embedding on Your Website

When you're ready to go live, add this single line before your closing `</body>` tag:

```html
<script src="https://YOUR_SERVER:8400/static/cloverbot.js" data-api-url="https://YOUR_SERVER:8400"></script>
```

Replace `YOUR_SERVER` with your CloverBot server's address.

**That's it.** The widget handles everything: rendering, state, API calls, mobile responsiveness.

---

## Widget Features (v2.0)

| Feature | Description |
|---------|-------------|
| **Dark premium theme** | Slack-inspired design with Inter font, smooth animations |
| **Message grouping** | Consecutive messages from the same sender are visually grouped |
| **Timestamps** | Show on hover, like Slack |
| **Quick-action pills** | Pre-set conversation starters (Products, Hardware, Pricing, AI Agent) |
| **Typing indicator** | Animated dots while CloverBot thinks |
| **Markdown rendering** | Bold, italic, code, links, lists, blockquotes |
| **Lead capture form** | Optional pre-chat name/email/company collection |
| **Responsive design** | Adapts beautifully from desktop to mobile |
| **Keyboard shortcuts** | Enter to send, Shift+Enter for newline, Escape to close |
| **Open/close animation** | Spring-physics scale animation |
| **Auto-resize input** | Textarea grows with content |

---

## Switching to Ollama (Self-Hosted AI)

1. Install Ollama: https://ollama.com
2. Pull a model: `ollama pull llama3.1`
3. Update `.env`:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1
   ```
4. Restart CloverBot. Same widget, same API, local AI brain.

---

## Updating the Knowledge Base

Add or edit `.md` / `.txt` files in the `knowledge/` directory.

**Options to re-ingest:**
- Restart the server (auto-ingests on startup)
- Run manually: `python scripts/ingest.py`
- Hit the API: `POST http://localhost:8400/api/ingest`

### Writing Knowledge Docs

CloverBot's personality comes through in three layers:
1. **System prompt** (`config.py`) — how it talks
2. **Knowledge docs** (`knowledge/`) — what it retrieves
3. **Widget greeting** (`cloverbot.js`) — first impression

When writing docs for the `knowledge/` folder, add personality! The current docs include humor, real-talk explanations, and technical depth. CloverBot retrieves and synthesizes from these, so the tone of the docs affects the tone of the answers.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/api/chat` | Send a message, get a reply |
| `POST` | `/api/lead` | Capture visitor lead info |
| `POST` | `/api/ingest` | Re-ingest knowledge base |
| `GET` | `/api/conversations` | List recent conversations (admin) |
| `GET` | `/api/leads` | List captured leads (admin) |
| `GET` | `/widget` | Branded demo page |
| `GET` | `/static/cloverbot.js` | Chat widget script |

### POST /api/chat

```json
{
  "message": "What products do you offer?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "reply": "Great question! MyClover.Tech offers...",
  "session_id": "abc123",
  "escalated": false
}
```

### POST /api/lead

```json
{
  "session_id": "abc123",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "company": "Acme Corp"
}
```

---

## Configuration Reference

All settings are in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `openai` | `openai` or `ollama` |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.1` | Ollama model name |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8400` | Server port |
| `ALLOWED_ORIGINS` | `https://myclover.tech,...` | CORS allowed origins |
| `SLACK_WEBHOOK_URL` | — | Slack webhook for escalations |
| `RATE_LIMIT_PER_MINUTE` | `10` | Max messages per IP per minute |
| `SESSION_TIMEOUT_MINUTES` | `30` | Conversation session timeout |
| `REQUIRE_LEAD_INFO` | `false` | Force lead capture before chat |
| `KNOWLEDGE_DIR` | `./knowledge` | Path to knowledge docs |
| `DB_PATH` | `./cloverbot.db` | SQLite database path |

---

## Security Notes

- **Admin endpoints** (`/api/conversations`, `/api/leads`) should be protected behind authentication in production
- **Slack webhook URL** is server-side only, never exposed to the browser
- **Rate limiting** is per-IP, configurable via `RATE_LIMIT_PER_MINUTE`
- **CORS** is restricted to your allowed origins
- **No telemetry** — CloverBot doesn't phone home or send data anywhere you don't configure

---

## Production Deployment

For production, we recommend:

1. **Reverse proxy** (nginx/Caddy/Traefik) in front of CloverBot for SSL termination
2. **Process manager** (systemd/PM2/supervisor) to keep the server running
3. **Auth on admin endpoints** — add API key or basic auth to `/api/conversations` and `/api/leads`
4. **Restrict CORS** — update `ALLOWED_ORIGINS` to only your production domain
5. **Monitor** — CloverBot logs conversations to SQLite; set up log rotation if needed

---

## License

Proprietary — MyClover.Tech. All rights reserved.

---

<p align="center">
  Built by <a href="https://myclover.tech">MyClover.Tech</a> — where IT meets AI.
</p>
