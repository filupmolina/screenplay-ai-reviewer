# Screenplay App Upgrade Guide

**Two critical upgrades needed:**
1. Get full Claude model access (currently Haiku-only)
2. Add PDF parsing MCP server for better screenplay extraction

---

## Part 1: Upgrade API Key for Full Model Access

### Current Problem
Your API key may be workspace-restricted to Haiku models only.

**What works:**
- ✅ claude-3-haiku-20240307
- ✅ claude-3-5-haiku-20241022

**What's blocked:**
- ❌ claude-3-5-sonnet (better quality, recommended)
- ❌ claude-3-opus (most capable)

### Solution: Create New Personal API Key

**Step 1: Go to Anthropic Console**
Open: https://console.anthropic.com/settings/keys

**Step 2: Create New Key**
1. Click "Create Key" button
2. **Important:** Make sure you're in your **personal workspace**, not a team workspace
3. Name it: "screenplay-personal-key" or similar
4. Click Create

**Step 3: Add Billing (if not already set up)**
If prompted, add payment method:
- Go to: https://console.anthropic.com/settings/billing
- Add credit card
- You'll be charged only for usage (pay-as-you-go)
- Sonnet pricing: ~$3 per 1M input tokens, $15 per 1M output tokens
- For screenplay analysis, expect $0.10-0.50 per script

**Step 4: Update Your .env File**
```bash
cd /Users/filupmolina/Downloads/claude\ code/screenplay
```

Open `.env` and replace the key:
```bash
# Old (Haiku-only)
# ANTHROPIC_API_KEY=your-api-key-here

# New (Full access)
ANTHROPIC_API_KEY=<your-new-key-here>
```

**Step 5: Update Backend to Use Sonnet**
Edit `backend/services/ai_provider.py`:

Change line 4:
```python
# OLD
def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-haiku-20241022"):

# NEW
def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
```

Or better - use environment variable:
```python
def __init__(self, api_key: Optional[str] = None, model: str = None):
    self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
```

Then add to `.env`:
```bash
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Step 6: Test It**
```bash
cd backend
python3 << 'EOF'
import os
from anthropic import Anthropic

# Load your new key
from dotenv import load_dotenv
load_dotenv()

client = Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say 'Sonnet works!' if you can read this."}]
)

print(f"✅ Success! Response: {response.content[0].text}")
EOF
```

Expected output: `✅ Success! Response: Sonnet works!`

---

## Part 2: Install PDF Parsing MCP Server

### Current Problem
Screenplay app uses basic PDF parsing which can miss formatting, fail on complex PDFs, or lose screenplay structure.

### Solution: Install MCP PDF Server

**Best option for screenplay app:** `pdf-reader-mcp` by Sylph Lab (Node.js, most reliable)

**Step 1: Install the MCP Server**
```bash
# Install globally
npm install -g @sylphxltd/pdf-reader-mcp

# Or clone and run locally
cd ~/Projects  # or wherever you keep projects
git clone https://github.com/sylphxltd/pdf-reader-mcp.git
cd pdf-reader-mcp
npm install
npm run build
```

**Step 2: Configure Claude Code to Use It**

Create MCP config file:
```bash
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/mcp.json << 'EOF'
{
  "mcpServers": {
    "pdf-reader": {
      "command": "npx",
      "args": ["-y", "@sylphxltd/pdf-reader-mcp"],
      "env": {}
    }
  }
}
EOF
```

**Step 3: Test MCP Server**
Restart Claude Code CLI, then the PDF reader tools should be available:
- `read_pdf` - Extract text from PDFs
- `get_pdf_metadata` - Get PDF info
- `count_pages` - Get page count

**Step 4: Update Screenplay Backend to Use MCP**

Instead of parsing PDFs in Python, we can use the MCP server.

Create new file `backend/services/pdf_mcp.py`:
```python
import subprocess
import json
from typing import Dict, Any

class PDFMCPReader:
    """Use MCP PDF server for better parsing"""

    def read_pdf(self, file_path: str) -> str:
        """Extract text from PDF using MCP server"""
        result = subprocess.run(
            ["npx", "-y", "@sylphxltd/pdf-reader-mcp", "read_pdf", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"PDF parsing failed: {result.stderr}")

        data = json.loads(result.stdout)
        return data.get("text", "")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get PDF metadata"""
        result = subprocess.run(
            ["npx", "-y", "@sylphxltd/pdf-reader-mcp", "get_metadata", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Metadata extraction failed: {result.stderr}")

        return json.loads(result.stdout)
```

**Step 5: Update Parser to Use MCP**

Edit `backend/services/parser.py`:
```python
from services.pdf_mcp import PDFMCPReader

class FountainParser:
    def __init__(self):
        self.pdf_reader = PDFMCPReader()

    def parse_pdf(self, file_path: str) -> str:
        """Parse PDF using MCP server"""
        try:
            return self.pdf_reader.read_pdf(file_path)
        except Exception as e:
            # Fallback to old method if MCP fails
            logger.warn(f"MCP PDF reading failed, using fallback: {e}")
            return self._fallback_pdf_parse(file_path)
```

---

## Testing Both Upgrades

**Test 1: Verify Sonnet Access**
```bash
cd /Users/filupmolina/Downloads/claude\ code/screenplay/backend
python3 -c "
from services.ai_provider import AnthropicProvider
provider = AnthropicProvider()
print(f'Using model: {provider.model}')
response = provider.chat([{'role': 'user', 'content': 'Hi'}])
print(f'Response: {response.content}')
"
```

Expected: Should say "Using model: claude-3-5-sonnet-20241022"

**Test 2: Verify PDF MCP**
```bash
# Create a simple test PDF (or use existing screenplay)
echo "Testing MCP PDF reader..."
npx -y @sylphxltd/pdf-reader-mcp read_pdf "/Users/filupmolina/Downloads/claude code/screenplay/Bad Hombres by Filup Molina.pdf"
```

Expected: Should output JSON with extracted text

---

## Cost Comparison

**Haiku vs Sonnet for screenplay analysis:**

Assuming 100-page screenplay ≈ 40,000 tokens:
- **Haiku:** $0.01 input + ~$0.05 output = **$0.06 per script**
- **Sonnet:** $0.12 input + ~$0.60 output = **$0.72 per script**

**Worth it?** Yes - Sonnet gives much better:
- Character analysis
- Scene-by-scene feedback
- Story structure insights
- Emotional tracking

For serious screenplay review, Sonnet is worth the 12x cost increase.

---

## Rollback Plan

If anything goes wrong:

**Revert API key:**
```bash
# Put old key back in .env
ANTHROPIC_API_KEY=your-api-key-here
```

**Revert model:**
```python
# In ai_provider.py
model: str = "claude-3-5-haiku-20241022"
```

**Remove MCP:**
```bash
rm ~/.config/claude-code/mcp.json
```

---

## Questions?

If issues:
1. Check console.anthropic.com for key status
2. Verify billing is set up
3. Test with curl/python before updating app
4. Check MCP logs for PDF parsing errors

---

**Next steps:**
1. Create new API key (5 min)
2. Update .env and ai_provider.py (2 min)
3. Test Sonnet access (1 min)
4. Install PDF MCP server (5 min)
5. Test screenplay upload (2 min)

**Total time: ~15 minutes to upgrade both**
