# Tech Stack

## Language & Runtime
| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.12+ | 3.11 minimum, 3.12 tested |
| Async Runtime | asyncio | Built-in, used for all LLM calls |

## Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| `openai` | >=1.0.0 | OpenAI-compatible API client (sumopod) |
| `python-dotenv` | >=1.0.0 | `.env` file loading |
| `pydantic` | >=2.0.0 | Data validation (installed, available for future use) |

## Web UI
| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | >=1.28.0 | Web application framework |
| `altair` | >=4.0 | Charting (Streamlit dependency) |
| `pydeck` | >=0.8 | Deck.gl bindings (Streamlit dependency) |

## CLI
| Package | Version | Purpose |
|---------|---------|---------|
| `click` | >=8.0.0 | CLI argument parsing |
| `rich` | >=13.0.0 | Terminal formatting (tables, panels, markdown) |

## Development & Testing
| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=7.0.0 | Test framework |
| `pytest-asyncio` | >=0.21.0 | Async test support |
| `pytest-mock` | >=3.10.0 | Mocking support |

## Infrastructure

### Development Machine
| Spec | Value |
|------|-------|
| OS | Windows 11 |
| IDE | VS Code |
| Shell | cmd.exe / PowerShell |

### Production (Tencent VPS)
| Spec | Value |
|------|-------|
| vCPU | 2 cores |
| RAM | 2 GB |
| Storage | 40 GB |
| OS | Linux (Ubuntu recommended) |
| Port | 8501 (Streamlit) |
| Process Manager | `screen` or `systemd` |
| Reverse Proxy | Nginx (if multiple apps) |

## API Contract

### Sumopod (OpenAI-compatible)

**Base URL:** `https://api.sumopod.com/v1` (configurable via `SUMODOP_BASE_URL`)

**Authentication:** Bearer token via `SUMODOP_API_KEY`

**Default Model:** `gpt-4o-mini` (configurable via `SUMODOP_MODEL`)

**Endpoints Used:**
- `POST /chat/completions` - All LLM interactions

**Request Format:**
```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**Response Format:**
```json
{
  "choices": [
    {
      "message": {
        "content": "..."
      }
    }
  ]
}
```

## Environment Variables
| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `SUMODOP_API_KEY` | — | Yes | API authentication key |
| `SUMODOP_BASE_URL` | `https://api.sumopod.com/v1` | No | API endpoint URL |
| `SUMODOP_MODEL` | `gpt-4o-mini` | No | Model identifier |