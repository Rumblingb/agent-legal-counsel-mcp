# Agent Legal Counsel MCP ⚖️🤖

**Premium AI agent legal contract generator** — Generate legally-structured contracts for AI agent services, terms of service, NDAs, data processing agreements, and more.

> **Get Pro: [Subscribe for $19/mo →](https://buy.stripe.com/eVq9AVa1xgAk3rygvx1oI0A)**

---

## Features

### Tools

| Tool | Description | Free | Pro |
|------|-------------|------|-----|
| `legal_generate_contract` | Generate AI service agreement, DPA, SaaS terms, or NDA | 1/month | 50/month |
| `legal_generate_tos` | Generate Terms of Service for AI products | 1/month | 50/month |
| `legal_generate_waiver` | Generate liability waivers for AI services | 1/month | 50/month |
| `legal_list_templates` | List available contract templates | Unlimited | Unlimited |
| `legal_validate_contract` | Validate existing contracts against a checklist | Unlimited | Unlimited |

### Templates (hardcoded, 500-1000 words each)

1. **AI Agent Service Agreement** — Standard AI service contract with scope, fees, IP, liability
2. **AI Agent Data Processing Agreement** — GDPR/CCPA-compliant data processing addendum
3. **AI Agent SaaS Subscription Terms** — SaaS terms with uptime SLAs and support
4. **AI Agent Non-Disclosure Agreement** — Mutual NDA with AI-specific protections

### Pricing

| Feature | Free | Pro ($19/mo) |
|---------|------|--------------|
| Contracts per month | 1 | 50 |
| Daily API calls | 50 | 500 |
| All 4 contract templates | Yes | Yes |
| Enhanced customization | No | Yes |
| Pro watermark removal | — | Yes |
| Priority support | — | Yes |

**[Subscribe to Pro →](https://buy.stripe.com/eVq9AVa1xgAk3rygvx1oI0A)**

---

## Quick Start

### Prerequisites

- Python 3.10+
- MCP SDK (`pip install mcp`)

### Installation

```bash
pip install -r requirements.txt
```

### Usage

**As an MCP server** (connect from any MCP client like Claude):

```bash
python server.py
```

**CLI demo mode:**

```bash
python server.py --cli
```

### MCP Client Configuration

Add to your MCP client config:

```json
{
  "mcpServers": {
    "agent-legal-counsel": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "free_demo_key_2024"
      }
    }
  }
}
```

---

## API Key System

- **Free keys**: Start with `free_` — 1 contract/month, 50 calls/day
- **Pro keys**: Start with `prol_` — 50 contracts/month, 500 calls/day

Pro keys are obtained by subscribing at the link above.

---

## Development

### Project Structure

```
agent-legal-counsel-mcp/
├── server.py          # MCP server with all contract templates
├── requirements.txt   # Python dependencies
├── smithery.yaml      # Smithery deployment config
├── README.md          # This file
└── index.html         # GitHub Pages landing page
```

### Contract Templates

All templates are hardcoded in `server.py` and generate ~500-1000 words each. No external API dependencies. Parameters can be customized per generation request.

### Rate Limiting

Rate limiting is in-memory:
- Free: 50 calls/day, 1 contract/month
- Pro: 500 calls/day, 50 contracts/month

---

## Deployment

### GitHub Pages

This repo is deployed at: **https://rumblingb.github.io/agent-legal-counsel-mcp/**

### Smithery

Deploy on [Smithery](https://smithery.ai) using the included `smithery.yaml`.

---

## License

Proprietary. Unauthorized commercial use is prohibited.

---

*Built by [Rumblingb](https://github.com/Rumblingb)*
