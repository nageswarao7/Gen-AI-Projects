"""
UAE Mortgage Assistant - Streamlit App with Gemini Function Calling
"""

import streamlit as st
from google import genai
from google.genai import types
import os
import math
from dotenv import load_dotenv

load_dotenv()

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="UAE Mortgage Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============= CUSTOM CSS =============
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-out;
    }
    .user-message {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        margin-right: 20%;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ============= CONSTANTS =============
MAX_LTV = 0.8
TRANSFER_FEE = 0.04
AGENCY_FEE = 0.02
MISC_FEES = 0.01
STANDARD_RATE = 4.5
MAX_TENURE = 25

# ============= DETERMINISTIC MATH FUNCTIONS =============
def calculate_mortgage_emi(principal: float, annual_rate: float, years: int) -> dict:
    """Calculate EMI - NO LLM HALLUCINATION"""
    if years > MAX_TENURE:
        return {"error": f"Tenure cannot exceed {MAX_TENURE} years."}
   
    monthly_rate = annual_rate / (12 * 100)
    num_payments = years * 12
   
    if monthly_rate == 0:
        emi = principal / num_payments
    else:
        numerator = monthly_rate * math.pow(1 + monthly_rate, num_payments)
        denominator = math.pow(1 + monthly_rate, num_payments) - 1
        emi = principal * (numerator / denominator)
   
    total_payment = emi * num_payments
    total_interest = total_payment - principal
   
    return {
        "monthly_emi_aed": round(emi, 2),
        "total_payment_aed": round(total_payment, 2),
        "total_interest_aed": round(total_interest, 2),
        "loan_amount": round(principal, 2),
        "tenure_years": years,
        "interest_rate": annual_rate
    }

def calculate_upfront_costs(property_price: float) -> dict:
    """Calculate all upfront costs"""
    transfer = property_price * TRANSFER_FEE
    agency = property_price * AGENCY_FEE
    misc = property_price * MISC_FEES
    total = transfer + agency + misc
   
    return {
        "transfer_fee_aed": round(transfer, 2),
        "agency_fee_aed": round(agency, 2),
        "misc_fees_aed": round(misc, 2),
        "total_upfront_aed": round(total, 2),
        "percentage_of_price": round((total / property_price) * 100, 2),
        "note": "These are the hidden costs most buyers forget!"
    }

def calculate_loan_details(property_price: float, down_payment_percent: float,
                          tenure_years: int) -> dict:
    """Calculate complete loan details"""
    min_down_payment = 20
    actual_down_payment = max(down_payment_percent, min_down_payment)
   
    down_payment_amount = property_price * (actual_down_payment / 100)
    loan_amount = property_price - down_payment_amount
   
    max_loan = property_price * MAX_LTV
    loan_amount = min(loan_amount, max_loan)
   
    emi_result = calculate_mortgage_emi(loan_amount, STANDARD_RATE, tenure_years)
   
    return {
        "property_price_aed": round(property_price, 2),
        "down_payment_percent": actual_down_payment,
        "down_payment_amount_aed": round(down_payment_amount, 2),
        "loan_amount_aed": round(loan_amount, 2),
        "monthly_emi_aed": emi_result["monthly_emi_aed"],
        "total_interest_aed": emi_result["total_interest_aed"],
        "interest_rate": STANDARD_RATE,
        "tenure_years": tenure_years,
        "note": "Expats can borrow maximum 80% (20% down payment is mandatory)"
    }

def buy_vs_rent_analysis(property_price: float, monthly_rent: float,
                        stay_duration_years: int, monthly_income: float) -> dict:
    """Comprehensive buy vs rent analysis"""
   
    upfront = calculate_upfront_costs(property_price)
    loan = calculate_loan_details(property_price, 20, MAX_TENURE)
   
    monthly_maintenance = property_price * 0.001
    monthly_buying_cost = loan["monthly_emi_aed"] + monthly_maintenance
   
    total_rent_paid = monthly_rent * stay_duration_years * 12
    down_payment = property_price * 0.2
    total_buying_cost = upfront["total_upfront_aed"] + down_payment + (monthly_buying_cost * stay_duration_years * 12)
   
    emi_to_income_ratio = (loan["monthly_emi_aed"] / monthly_income) * 100 if monthly_income > 0 else 999
    is_affordable = emi_to_income_ratio <= 40
   
    if stay_duration_years < 3:
        recommendation = "RENT"
        reason = "Short stay duration. Transaction costs (7% upfront) make buying uneconomical."
    elif stay_duration_years >= 5 and is_affordable:
        recommendation = "BUY"
        reason = "Long stay duration and affordable EMI. Building equity beats paying rent."
    elif not is_affordable:
        recommendation = "RENT"
        reason = f"EMI would be {round(emi_to_income_ratio, 1)}% of income (should be <40%). Financially risky."
    else:
        recommendation = "BORDERLINE"
        reason = "Medium stay (3-5 years). Consider job stability and life plans carefully."
   
    return {
        "recommendation": recommendation,
        "reason": reason,
        "property_price_aed": property_price,
        "monthly_rent_aed": monthly_rent,
        "stay_duration_years": stay_duration_years,
        "monthly_income_aed": monthly_income,
        "upfront_costs_aed": upfront["total_upfront_aed"],
        "down_payment_aed": down_payment,
        "monthly_emi_aed": loan["monthly_emi_aed"],
        "monthly_maintenance_aed": round(monthly_maintenance, 2),
        "total_monthly_buying_cost_aed": round(monthly_buying_cost, 2),
        "total_rent_over_period_aed": round(total_rent_paid, 2),
        "total_buying_cost_over_period_aed": round(total_buying_cost, 2),
        "savings_if_buy_aed": round(total_rent_paid - total_buying_cost, 2),
        "emi_to_income_ratio_percent": round(emi_to_income_ratio, 2),
        "is_affordable": is_affordable
    }

# ============= TOOLS MAPPING =============
tools_map = {
    "calculate_mortgage_emi": calculate_mortgage_emi,
    "calculate_upfront_costs": calculate_upfront_costs,
    "calculate_loan_details": calculate_loan_details,
    "buy_vs_rent_analysis": buy_vs_rent_analysis
}

# ============= SYSTEM PROMPT =============
SYSTEM_INSTRUCTION = """You are a friendly mortgage advisor for expats in the UAE. Your name is "Smart Friend" and you help them decide: buy or rent?
KEY RULES:
1. NEVER calculate numbers yourself - ALWAYS use the provided tool functions for any calculations
2. Be warm, conversational, and empathetic - not robotic or formal
3. Gather information naturally through conversation: monthly income, property price they're considering, current rent, how long they plan to stay
4. Explain concepts simply without jargon overload
5. After providing analysis, encourage them to share contact details to connect with mortgage advisors
UAE MORTGAGE FACTS (mention these naturally):
- Expats can borrow maximum 80% (need 20% down payment minimum)
- Upfront costs are ~7% of property price (transfer fee 4%, agency 2%, misc 1%) - most buyers forget this!
- Standard interest rate: 4.5% annual
- Maximum tenure: 25 years
- Affordability rule: EMI should be less than 40% of monthly income
BUY vs RENT DECISION LOGIC:
- Stay duration < 3 years: Recommend RENT (transaction costs kill the profit)
- Stay duration > 5 years: Recommend BUY (building equity beats paying rent)
- EMI > 40% of income: Recommend RENT (too financially risky)
- Medium duration (3-5 years): BORDERLINE - consider job stability and life plans
CONVERSATION FLOW:
1. Greet warmly and understand their situation
2. Ask natural questions to collect data (don't feel like a survey form)
3. Once you have property price, rent, income, and stay duration, use the buy_vs_rent_analysis tool
4. Present the recommendation clearly with reasoning
5. End with: "Want me to connect you with mortgage advisors who can get you the best rates? Just share your name and email!"
CRITICAL: Always use tools for calculations. Never guess or estimate numbers yourself."""

# ============= HELPER FUNCTIONS =============
def get_text(part):
    """Safely extracts text from a Part object or string."""
    if isinstance(part, str):
        return part
    if hasattr(part, 'text'):
        return part.text
    return str(part)

# ============= SESSION STATE INITIALIZATION =============
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "model",
                "parts": [types.Part(text="👋 Hey there! I'm your friendly mortgage advisor for the UAE.\n\nI help expats like you figure out whether buying or renting makes more sense. No confusing jargon, just honest advice.\n\nWhat brings you here today?")]
            }
        ]

# ============= CONFIGURE GEMINI =============
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file. Please create a .env file with GOOGLE_API_KEY=your_key")
    st.stop()

client = genai.Client(api_key=api_key)

# ============= MAIN APP =============
def main():
    initialize_session_state()
   
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: white;'>
        <h1>🏠 UAE Mortgage Assistant</h1>
        <p style='font-size: 1.2rem;'>Should you buy or rent? Let's figure it out together.</p>
    </div>
    """, unsafe_allow_html=True)
   
    # Sidebar (now minimal - no API key input)
    with st.sidebar:
        st.header("ℹ️ Info")
        st.markdown("### 📊 UAE Mortgage Facts")
        st.markdown("- **Max Loan:** 80% (20% down)")
        st.markdown("- **Upfront Costs:** ~7% of price")
        st.markdown("- **Interest Rate:** 4.5% p.a.")
        st.markdown("- **Max Tenure:** 25 years")
        st.markdown("- **EMI Rule:** <40% of income")
       
        st.markdown("---")
        st.markdown("### 💡 Try saying:")
        st.markdown("- \"I make 25k/month\"")
        st.markdown("- \"Looking at 2M property\"")
        st.markdown("- \"Currently paying 8k rent\"")
        st.markdown("- \"Planning to stay 4 years\"")
       
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = [
                {
                    "role": "model",
                    "parts": [types.Part(text="👋 Hey there! I'm your friendly mortgage advisor for the UAE.\n\nI help expats like you figure out whether buying or renting makes more sense. No confusing jargon, just honest advice.\n\nWhat brings you here today?")]
                }
            ]
            st.rerun()
   
    # Display Chat History
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
       
        with st.chat_message(role):
            # Show tool outputs
            if "function_response" in msg:
                st.success(f"📊 **Calculation Result:**\n```json\n{msg['function_response']['response']}\n```")
            # Show text messages
            elif "parts" in msg:
                text = get_text(msg["parts"][0])
                st.markdown(text)
   
    # Chat Input
    if prompt := st.chat_input("Type your message here... (e.g., 'I make 20k/month and want to buy in Marina')"):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "parts": [types.Part(text=prompt)]
        })
       
        with st.chat_message("user"):
            st.markdown(prompt)
       
        # Prepare API history
        api_history = []
        for m in st.session_state.messages:
            if m["role"] == "tool":
                api_history.append(types.Content(
                    role="tool",
                    parts=[types.Part.from_function_response(
                        name=m["function_response"]["name"],
                        response=m["function_response"]["response"]
                    )]
                ))
            else:
                txt = get_text(m["parts"][0])
                api_history.append(types.Content(
                    role=m["role"],
                    parts=[types.Part(text=txt)]
                ))
       
        # Generate response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
           
            try:
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=list(tools_map.values()),
                    temperature=0.3
                )
               
                # First API call
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=api_history,
                    config=config
                )
               
                # Handle function calling
                if response.function_calls:
                    call = response.function_calls[0]
                    func_name = call.name
                    func_args = {k: v for k, v in call.args.items()}
                   
                    st.info(f"⚙️ **Calculating:** Using `{func_name}` with parameters...")
                   
                    # Execute function
                    if func_name in tools_map:
                        result = tools_map[func_name](**func_args)
                       
                        st.success(f"📊 **Calculation Result:**\n```json\n{result}\n```")
                       
                        # Add tool response to history
                        st.session_state.messages.append({
                            "role": "tool",
                            "function_response": {
                                "name": func_name,
                                "response": result
                            }
                        })
                       
                        # Send tool output back to model
                        api_history.append(types.Content(
                            role="model",
                            parts=[types.Part.from_function_calls(name=func_name, args=call.args)]
                        ))
                        api_history.append(types.Content(
                            role="tool",
                            parts=[types.Part.from_function_response(name=func_name, response=result)]
                        ))
                       
                        # Get final response
                        final_response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=api_history,
                            config=config
                        )
                       
                        final_text = final_response.text
                        response_placeholder.markdown(final_text)
                       
                        st.session_state.messages.append({
                            "role": "model",
                            "parts": [types.Part(text=final_text)]
                        })
                    else:
                        response_placeholder.error(f"Unknown function: {func_name}")
                else:
                    # No tool call, just text response
                    text = response.text
                    response_placeholder.markdown(text)
                   
                    st.session_state.messages.append({
                        "role": "model",
                        "parts": [types.Part(text=text)]
                    })
               
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}\n\nPlease check your API key and try again."
                response_placeholder.error(error_msg)
   
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: white; font-size: 0.9rem;'>
        <p>Built with ❤️ using Streamlit + Gemini 2.5 Flash | AI First Engineer Assignment</p>
        <p>🚀 Function calling ensures accurate calculations - zero hallucination!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()