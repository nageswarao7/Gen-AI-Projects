# 🏠 CoinedOne Anti-Calculator – UAE Mortgage Assistant

**AI First Engineer (Founder's Office) Assignment Submission**  
**Challenge**: "The Anti-Calculator" – Build an AI agent that acts like a smart friend to guide UAE expats through the mortgage maze (buy vs. rent decision).

## Live Demo
**Test the bot immediately**: https://gen-ai-projects-u8qggqetagxa2leqbecarp.streamlit.app/ 


## Repository
https://github.com/nageswarao7/Gen-AI-Projects/tree/main/uae-mortgage-advisor

## Project Overview
A fully conversational AI mortgage advisor that helps UAE expats decide whether to **buy or rent** — replacing cold, emotionally useless calculators with warm, empathetic guidance.

Key features:
- Natural conversation that feels like chatting with a smart friend
- Gracefully collects income, property price, current rent, and planned stay duration without robotic surveys
- Enforces all UAE expat rules (20% min down payment, ~7% upfront fees, 4.5% rate, 25-year max tenure)
- Delivers personalized buy vs. rent recommendation with clear reasoning
- **Zero hallucination on numbers** — all math handled via deterministic function calling
- Ends with compelling lead capture

Built and shipped in under 24 hours.

## Architecture & Technology Choices
- **LLM**: Gemini 2.5 Flash (`gemini-2.5-flash`)  
  → Chosen for excellent function calling reliability, low latency, strong natural language tone, and cost efficiency.

- **Framework**: Streamlit + Google Generative AI SDK (`google-genai`)  
  → Used the official SDK directly (no LangChain, no Vercel AI SDK) for maximum control over tool registration, conversation history, and function call flow. This ensures reliable tool usage and easy debugging.

- **Function Calling / Tools**: Native Gemini tool integration  
  → Critical for solving the hallucination problem — the LLM never calculates numbers itself.

- **Deployment**: Streamlit Community Cloud (instant public URL)

- **Security**: API key loaded securely from `.env` (never exposed)

## The Math – Solving the Hallucination Problem
All calculations are performed **exclusively** in deterministic Python functions. The LLM is strictly prohibited from doing math.

### Registered Tools (specific code block handling tool calls)
```python
tools_map = {
    "calculate_mortgage_emi": calculate_mortgage_emi,
    "calculate_upfront_costs": calculate_upfront_costs,
    "calculate_loan_details": calculate_loan_details,
    "buy_vs_rent_analysis": buy_vs_rent_analysis  # Main decision engine
}
```

These functions are passed directly to Gemini via:
```python
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=list(tools_map.values()),
    temperature=0.3
)
```

When the user provides sufficient data, Gemini calls one of these tools (most commonly `buy_vs_rent_analysis`). The UI explicitly shows:
```
⚙️ Calculating: Using `buy_vs_rent_analysis`...
📊 Calculation Result: (full JSON output)
```

This proves every financial number comes from code — **zero hallucination**.

### Enforced Rules (as per assignment cheat sheet)
- Max LTV: 80% → 20% minimum down payment
- Upfront costs: ~7% (4% transfer + 2% agency + 1% misc)
- Interest rate: 4.5%
- Max tenure: 25 years
- Buy vs. Rent logic:
  - <3 years → **RENT** (transaction costs dominate)
  - ≥5 years + EMI ≤40% income → **BUY**
  - EMI >40% income → **RENT**
  - 3–5 years → **BORDERLINE**

## Product Sense
- Empathetic, human tone throughout
- Natural data collection (no form-like questioning)
- Handles vague inputs (e.g., "2M in Marina")
- Clear warnings about hidden fees
- Strong conversion: ends with lead capture prompt

## Velocity & Tooling (Speed Run)
- **Primary tool**: Cursor  
  → Used extensively for writing functions, debugging function calling, refining the system prompt, and rapid UI iteration.
- **Secondary tool**: Claude  
  → Helped draft the initial system instruction and conversation flow.
- **Total build time**: ~18–20 hours

Aggressively leveraged AI-native tools to ship a polished, reliable product at high velocity.

## How to Run Locally
```bash
git clone https://github.com/nageswarao7/Gen-AI-Projects.git
cd uae-mortgage-advisor

pip install -r requirements.txt

# Create .env file
"GOOGLE_API_KEY=your_gemini_api_key_here" > .env

streamlit run app.py
```

## Repository Files
- `app.py` – Full application code
- `requirements.txt`
- `README.md` – This walkthrough

Thank you for the thoughtful challenge. I'm excited about building more AI-native products at CoinedOne.

— Nageswara Rao Vutla