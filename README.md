# 🤔 My Thinker Buddy

**Chain-of-Thought Reasoning Engine** — A multi-framework analytical system that processes questions through structured reasoning chains using an OpenAI-compatible API (sumopod).

## 🧠 How It Works

1. **You ask a question** — e.g., "Why are customers churning in our SaaS product?"
2. **Auto-detect best framework** — The LLM classifies your question and selects the most suitable analytical framework
3. **Chain-of-Thought execution** — The framework runs step-by-step, with each LLM call building on previous outputs
4. **Structured result** — You get a complete reasoning chain showing how the answer was derived

## 📋 Available Frameworks

| Framework | Steps | Best For |
|-----------|-------|----------|
| **Fishbone Diagram** | 4 | Root cause analysis, manufacturing, business processes |
| **Fault Tree Analysis** | 4 | System failures, safety incidents, reliability engineering |
| **Iceberg Model** | 4 | Systemic issues, organizational challenges, deep patterns |
| **Apollo RCA** | 5 | Thorough incident investigation, causal relationships |
| **STAMP** | 5 | Complex socio-technical systems, safety-critical domains |
| **Swiss Cheese Model** | 4 | Layered defense systems, healthcare, aviation safety |
| **Cynefin Framework** | 4 | Problem classification, strategy, decision-making |
| **DMAIC** | 5 | Process improvement, Six Sigma, quality control |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env.example` to `.env` and fill in your sumopod API credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
SUMODOP_API_KEY=your_api_key_here
SUMODOP_BASE_URL=https://api.sumopod.com/v1
SUMODOP_MODEL=gpt-4o-mini
```

### 3. Run the Web UI (Streamlit)

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### 4. Or Use the CLI

```bash
# Auto-detect framework
python main.py analyze "Why did the production line stop?" --api-key YOUR_KEY

# Specify a framework
python main.py analyze "What caused the system failure?" --fault_tree --api-key YOUR_KEY

# JSON output
python main.py analyze "How to improve customer retention?" --json --api-key YOUR_KEY

# List available frameworks
python main.py frameworks
```

## 🖥️ Web UI Features

- **Auto-detect** or manually select a framework
- **Step-by-step display** of the reasoning chain
- **Progress tracking** showing completion status
- **Export results** as Markdown or JSON
- **Configurable** API endpoint, model, and key

## 📁 Project Structure

```
my-thinker-buddy/
├── app.py                    # Streamlit web UI
├── main.py                   # CLI entry point
├── Dockerfile                # 🐳 Docker build recipe (new)
├── docker-compose.yml        # 🐳 Docker run config (new)
├── docker-compose-with-n8n.yml # 🐳 n8n side-by-side example (new)
├── .dockerignore             # 🐳 Files to exclude from image (new)
├── requirements.txt
├── .env.example              # Copy to .env and add your API key
├── README.md
├── nginx/
│   └── default.conf          # 🌐 Sample Nginx config for domain (new)
├── src/
│   ├── __init__.py
│   ├── llm_adapter.py        # OpenAI-compatible API wrapper
│   ├── framework_selector.py # Auto-detect + manual override
│   ├── orchestrator.py       # Chain execution engine
│   ├── formatter.py          # Output formatting
│   └── frameworks/
│       ├── __init__.py
│       ├── base.py           # Abstract base class
│       ├── fishbone.py       # Fishbone Diagram
│       ├── fault_tree.py     # Fault Tree Analysis
│       ├── iceberg.py        # Iceberg Model
│       ├── apollo_rca.py     # Apollo Root Cause Analysis
│       ├── stamp.py          # STAMP
│       ├── swiss_cheese.py   # Swiss Cheese Model
│       ├── cynefin.py        # Cynefin Framework
│       └── dmaic.py          # DMAIC
└── tests/
    ├── __init__.py
    └── test_frameworks.py    # 25+ tests
```

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 🐳 Deploy to Your Own Server (Docker)

> **Don't want to deal with servers?** You can also run the app locally on your computer with `streamlit run app.py` (see Quick Start above).

This guide walks you through deploying My Thinker Buddy on a **shared VPS** — a single server that runs multiple apps (like n8n, websites, or this tool) side-by-side.

**Who is this for?**
- 📊 **Data analysts** who want a team-accessible reasoning tool
- 🎯 **Marketing strategists** who need it available 24/7
- 💻 **Developers** who want a clean, containerized deployment

**What you'll learn:**
- How to package the app so it runs the same on any server
- How to run it alongside other apps (like n8n) without conflicts
- How to access it from anywhere using just a web browser

---

### 🧰 What is Docker? (Plain English)

Imagine you're packing a lunchbox. You put your sandwich, drink, and snack inside. No matter where you go — the office, a park, a friend's house — your lunch is the same.

**Docker is like a lunchbox for your app.** It packs the app + everything it needs (Python, libraries, settings) into a single box called a **container**. This means:

- ✅ It runs the same way on any computer or server
- ✅ You can run many apps side-by-side without them interfering
- ✅ If something breaks, you just restart the container — no re-installing

---

### 📋 What You'll Need

Before starting, make sure you have:

| Item | Where to get it |
|------|----------------|
| ☁️ **A VPS (server)** | Any provider: DigitalOcean, Linode, AWS, Azure, or your own computer |
| 🐳 **Docker** | [Install Docker](https://docs.docker.com/get-docker/) (free) |
| 🔑 **API key** | From your sumopod account (or any OpenAI-compatible provider) |
| 🌐 **A domain** (optional) | For using `thinker-buddy.yourdomain.com` instead of `IP:8501` |

> **💡 Tip:** If you're on **Windows**, install [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/). If you're on **Ubuntu/Linux**, we'll install it in the next step.

---

### Step 1: Install Docker

#### 🐧 For Ubuntu / Linux VPS

Copy and paste these commands one by one into your server's terminal:

```bash
# Update your package list
sudo apt update

# Install Docker
sudo apt install docker.io -y

# Install Docker Compose (for running multi-app setups)
sudo apt install docker-compose-v2 -y

# Start Docker automatically on boot
sudo systemctl enable --now docker

# Verify it's working
docker --version
```

**What you should see:** A version number like `Docker version 24.0.7`.

#### 🪟 For Windows VPS

1. Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Open Docker Desktop (it will start automatically)
3. Open **Command Prompt** or **PowerShell** and type:
   ```bash
   docker --version
   ```
4. You should see a version number — that means Docker is ready.

---

### Step 2: Get the Project Files

You have two options:

#### Option A: Download as ZIP (easier for non-developers)

1. Go to the [My Thinker Buddy GitHub page](https://github.com/YOUR_USERNAME/my-thinker-buddy)
2. Click the green **"Code"** button → **"Download ZIP"**
3. Upload the ZIP to your server, or unzip it on your computer and upload the folder

#### Option B: Clone with Git (for developers)

```bash
git clone https://github.com/YOUR_USERNAME/my-thinker-buddy.git
cd my-thinker-buddy
```

---

### Step 3: Configure Your API Key

The app needs an API key to work. Here's how to set it up:

1. **Copy the example config file:**
   ```bash
   cp .env.example .env
   ```

2. **Open the `.env` file** in any text editor (Notepad, VS Code, nano, vim).

3. **Fill in your details:**
   ```
   SUMODOP_API_KEY=sk-your-actual-api-key-here
   SUMODOP_BASE_URL=https://api.sumopod.com/v1
   SUMODOP_MODEL=gpt-4o-mini
   ```

   | Setting | What to put |
   |---------|-------------|
   | `SUMODOP_API_KEY` | Your actual API key from sumopod (starts with `sk-...`) |
   | `SUMODOP_BASE_URL` | The API endpoint (usually leave as default) |
   | `SUMODOP_MODEL` | Which AI model to use (e.g., `gpt-4o-mini`, `gpt-4o`) |

> **🔒 Security note:** The `.env` file contains your secret API key. Never share it or commit it to GitHub. The `.gitignore` and `.dockerignore` files already exclude it automatically.

---

### Step 4: Build and Start the App 🚀

Now for the exciting part — let's get your app running!

**What this command does:**
- Downloads all the necessary packages
- Packs everything into a container (remember the lunchbox analogy?)
- Starts the app so you can use it

```bash
docker compose up -d
```

**What you should see:** Text will scroll by as Docker downloads and builds everything. When it's done, you'll get your cursor back.

**Check if it's running:**
```bash
docker compose ps
```

You should see `my-thinker-buddy` listed with a status of **"Up"** (meaning running).

> **💡 Tip:** The first time you run this, it may take 1-3 minutes to download everything. After that, it starts instantly.

---

### Step 5: Open the App

Open your web browser and go to:

```
http://YOUR_SERVER_IP:8501
```

Replace `YOUR_SERVER_IP` with your server's actual IP address (e.g., `http://123.456.78.90:8501`).

**You should see:** The My Thinker Buddy web interface! 🎉

> **💡 Tip:** If you're running this on your **local computer** (not a VPS), use `http://localhost:8501` instead.

---

### Step 6: Keep It Running

#### Auto-start on boot

Docker is configured to restart the app automatically if:
- The server reboots
- The app crashes unexpectedly

You don't need to do anything extra — it's already set up in the `docker-compose.yml` file.

#### Useful commands

| What you want to do | Command |
|---------------------|---------|
| **See live logs** (what's happening right now) | `docker compose logs -f` |
| **Stop the app** | `docker compose down` |
| **Restart the app** | `docker compose restart` |
| **Check if it's running** | `docker compose ps` |
| **Update to the latest version** | See "Updating" below |

Press **Ctrl+C** to stop viewing logs and return to the command prompt.

#### Updating to a new version

When there's an update to My Thinker Buddy:

```bash
# 1. Pull the latest code
git pull

# 2. Rebuild and restart
docker compose up -d --build
```

That's it! The app will be updated with zero downtime.

---

### 🧩 Running Multiple Apps (n8n + Thinker Buddy)

This is where Docker really shines. You can run My Thinker Buddy alongside n8n (or any other app) on the same server.

#### Option A: Use the included example file

We've included a ready-made file that runs both apps:

```bash
docker compose -f docker-compose-with-n8n.yml up -d
```

This starts:
- **My Thinker Buddy** on port `8501`
- **n8n** on port `5678`

#### Option B: Add n8n to your existing setup

Edit your `docker-compose.yml` file and add the n8n service:

```yaml
services:
  thinker-buddy:
    # ... (existing config, don't change this)

  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

Then run:
```bash
docker compose up -d
```

#### Option C: Add any other app

Follow the same pattern for any Docker app:

```yaml
services:
  thinker-buddy:
    # ... existing config

  your-other-app:
    image: some-image-name
    container_name: my-other-app
    restart: unless-stopped
    ports:
      - "PORT_ON_SERVER:PORT_IN_CONTAINER"
```

> **💡 Tip:** Make sure each app uses a **different port** on the left side of the colon. For example: `8501:8501`, `5678:5678`, `3000:3000`.

#### Resource limits (important for shared VPS)

On a shared VPS, you want to make sure one app doesn't hog all the CPU or memory. Uncomment these lines in `docker-compose.yml` to limit resources:

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'      # Max 50% of one CPU core
      memory: 512M     # Max 512 MB of RAM
```

This ensures Thinker Buddy and n8n play nicely together.

---

### 🌐 Going Further: Use a Domain Name (Optional)

> **🔧 For advanced users.** If you just want the app working, you can skip this section and use `http://YOUR_SERVER_IP:8501`.

If you have a domain name, you can access your app at `http://thinker-buddy.yourdomain.com` instead of remembering an IP address and port number.

#### Step 1: Point your domain to your server

In your domain registrar's DNS settings, add an **A record**:
- **Name:** `thinker-buddy` (or whatever subdomain you want)
- **Value:** Your server's IP address

#### Step 2: Install Nginx

```bash
sudo apt install nginx -y
```

#### Step 3: Use the included Nginx config

We've included a sample config file at `nginx/default.conf`. Copy and adapt it:

```bash
sudo cp nginx/default.conf /etc/nginx/sites-available/thinker-buddy
```

Edit the file and replace `thinker-buddy.yourdomain.com` with your actual domain.

```bash
sudo nano /etc/nginx/sites-available/thinker-buddy
```

Enable the site and reload:

```bash
sudo ln -s /etc/nginx/sites-available/thinker-buddy /etc/nginx/sites-enabled/
sudo nginx -t          # Test the config
sudo nginx -s reload   # Apply changes
```

#### Step 4: Add HTTPS (free SSL certificate)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d thinker-buddy.yourdomain.com
```

Follow the prompts. Certbot will automatically set up HTTPS for you.

---

### 🔧 Troubleshooting

#### "Port 8501 is already in use"

This means another app is already using port 8501. Change the port in `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"   # Use port 8502 on your server instead
```

Then access the app at `http://YOUR_SERVER_IP:8502`.

#### "Container keeps restarting"

Check the logs to see what's wrong:

```bash
docker compose logs -f
```

Common causes:
- Missing or incorrect API key in `.env`
- The `.env` file doesn't exist (copy from `.env.example`)

#### "I can't access the app from my browser"

1. Make sure the container is running: `docker compose ps`
2. Check your server's firewall allows port 8501:
   ```bash
   # For Ubuntu with UFW
   sudo ufw allow 8501
   ```
3. If using a cloud provider (AWS, Azure, DigitalOcean), check the **security group / firewall settings** in their dashboard — you may need to add a rule allowing port 8501.

#### "The app is slow"

On a shared VPS, other apps may be using resources. Enable resource limits (see "Resource limits" section above) to give each app its fair share.

---

### 📁 Files in This Folder (Docker-related)

| File | What it does |
|------|-------------|
| `Dockerfile` | The recipe for building the app container |
| `docker-compose.yml` | How to run the app (single app) |
| `docker-compose-with-n8n.yml` | How to run alongside n8n (reference) |
| `.dockerignore` | Files to exclude from the container (keeps it small) |
| `nginx/default.conf` | Sample Nginx config for domain names (optional) |

---

## 🔧 Configuration

All configuration is via `.env` file or environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SUMODOP_API_KEY` | — | Your API key (required) |
| `SUMODOP_BASE_URL` | `https://api.sumopod.com/v1` | API endpoint |
| `SUMODOP_MODEL` | `gpt-4o-mini` | Model name |

## 📝 Example

**Question:** "Why a retail company purchase insurance and how to identify the one will renew"

The system will:
1. Auto-detect the best framework (likely Fishbone or Apollo RCA)
2. Execute each step, building context progressively
3. Return a complete reasoning chain with actionable insights

## 🏗️ Architecture

```
User Question → Framework Selector (LLM) → Best Framework
                                              ↓
    Step 1 → LLM → output ──┐
                              ↓
    Step 2 → LLM → output ──┤ (context from previous steps)
                              ↓
    Step 3 → LLM → output ──┤
                              ↓
    ... → Final Result → Formatted Output
```

## 📄 License

MIT