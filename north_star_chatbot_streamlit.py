"""
North Star Support Bot - Streamlit Implementation
Complete customer support chatbot for outdoor apparel e-commerce
All requirements met: Order tracking, returns, recommendations, human handoff, fallback handling
"""

import streamlit as st
from datetime import datetime
import re

# Page config
st.set_page_config(
    page_title="North Star Support Bot",
    page_icon="🏕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== MOCK DATA ====================
ORDERS = {
    "111": {
        "status": "Shipped",
        "details": "Your order is on its way! Arriving tomorrow.",
        "emoji": "✅"
    },
    "222": {
        "status": "Processing",
        "details": "We're getting your gear ready. Ships in 24 hours.",
        "emoji": "⏳"
    },
    "333": {
        "status": "Delivered",
        "details": "Your package has been delivered. Hope you love it!",
        "emoji": "📦"
    },
}

RETURN_POLICY = """
🔄 **North Star Return Policy**

✓ **30-day returns accepted**
✓ **Items must be unused**
✓ **Original packaging required**

**Shipping Options:**
- Standard: 3-5 days
- Expedited: 1-2 days

Ready to process a return? Visit our returns portal: **northstar.com/returns**
"""

PRODUCT_CATEGORIES = {
    "tents": "Tents & Shelters",
    "sleeping": "Sleeping Bags & Pads",
    "backpacks": "Backpacks",
    "clothing": "Outdoor Clothing",
    "gear": "Camping Gear",
    "footwear": "Hiking Footwear"
}

# ==================== INITIALIZE SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.awaiting_clarification = False
    st.session_state.clarification_type = None

# ==================== INTENT RECOGNITION ====================
def recognize_intent(message):
    """Recognize user intent from message"""
    message_lower = message.lower().strip()
    
    # Order tracking intents
    order_keywords = ["order", "track", "package", "shipped", "delivery", "where", "status"]
    if any(keyword in message_lower for keyword in order_keywords):
        return "order_tracking"
    
    # Return/exchange intents
    return_keywords = ["return", "exchange", "refund", "send back", "wrong", "damaged"]
    if any(keyword in message_lower for keyword in return_keywords):
        return "returns_exchanges"
    
    # Product recommendation intents
    rec_keywords = ["recommend", "suggest", "what should", "help me find", "looking for", "need"]
    if any(keyword in message_lower for keyword in rec_keywords):
        return "product_recommendation"
    
    # Human handoff intents
    handoff_keywords = ["agent", "support", "speak to", "human", "help", "representative"]
    if any(keyword in message_lower for keyword in handoff_keywords):
        if "human" in message_lower or "agent" in message_lower or "speak" in message_lower:
            return "human_handoff"
    
    # Greeting intents
    greeting_keywords = ["hello", "hi", "hey", "start", "help"]
    if any(keyword in message_lower for keyword in greeting_keywords):
        return "greeting"
    
    return "unknown"

# ==================== HANDLER FUNCTIONS ====================
def handle_greeting():
    """Handle greeting and show main options"""
    return {
        "response": """🏕️ Welcome to North Star Support! I'm here to help with outdoor adventures.

How can I assist you today?
• 📦 **Track an order**
• 🔄 **Return or exchange items**
• 🎒 **Get product recommendations**
• 👤 **Speak to a live agent**""",
        "intent": "greeting"
    }

def handle_order_tracking(message):
    """Handle order tracking"""
    # Extract order numbers
    order_numbers = re.findall(r'\d{3}', message)
    
    if order_numbers:
        order_num = order_numbers[0]
        if order_num in ORDERS:
            order_info = ORDERS[order_num]
            return {
                "response": f"""{order_info['emoji']} **Order #{order_num}**
Status: {order_info['status']}
{order_info['details']}""",
                "intent": "order_tracking",
                "resolved": True
            }
        else:
            return {
                "response": f"""❌ **Order #{order_num} not found.**
Please check your order number and try again.

Valid orders: 111, 222, 333""",
                "intent": "order_tracking",
                "ask_clarification": True
            }
    else:
        return {
            "response": """I'd be happy to track your order! 📦

What's your **order number**? You can find it in your confirmation email.
(Example: 111, 222, 333)""",
            "intent": "order_tracking",
            "ask_clarification": True
        }

def handle_returns(message):
    """Handle returns and exchanges"""
    return {
        "response": RETURN_POLICY,
        "intent": "returns_exchanges",
        "resolved": True
    }

def handle_product_recommendation(message):
    """Handle product recommendations"""
    if not st.session_state.awaiting_clarification or st.session_state.clarification_type != "recommendation":
        return {
            "response": """🎒 I'd love to help you find the perfect gear!

What **activity** are you gearing up for?
• 🏕️ Car camping
• 🥾 Hiking
• ⛺ Backpacking
• 🧗 Adventure sports
• 🌲 General outdoor activities""",
            "intent": "product_recommendation",
            "ask_clarification": True
        }
    
    # User has answered the clarifying question
    message_lower = message.lower()
    
    if "tent" in message_lower or "camping" in message_lower or "shelter" in message_lower:
        category = "Tents & Shelters"
    elif "sleep" in message_lower or "bag" in message_lower or "pad" in message_lower:
        category = "Sleeping Bags & Pads"
    elif "back" in message_lower or "pack" in message_lower:
        category = "Backpacks"
    elif "cloth" in message_lower or "wear" in message_lower:
        category = "Outdoor Clothing"
    elif "shoe" in message_lower or "boot" in message_lower or "foot" in message_lower:
        category = "Hiking Footwear"
    else:
        category = "Camping Gear"
    
    st.session_state.awaiting_clarification = False
    
    return {
        "response": f"""👌 **Based on that, I'd recommend:**

Check out our **{category}** section!

Our {category.lower()} are highly rated and perfect for your adventure!

**Need more help?**
- Ask about returns
- Track an order
- Speak to an agent""",
        "intent": "product_recommendation",
        "resolved": True
    }

def handle_human_handoff(message):
    """Handle human handoff"""
    return {
        "response": """👤 **Connecting you to a live agent...**

[You are now in a conversation with a North Star Support Agent]

**Agent:** Hi there! 👋 Thanks for your patience. How can I help you today?""",
        "intent": "human_handoff",
        "handoff": True
    }

def handle_unknown(message):
    """Handle unknown intents with helpful fallback"""
    return {
        "response": """I didn't quite catch that. 🤔

I can help you with:
• 📦 **Order tracking** - Check your order status
• 🔄 **Returns & exchanges** - Learn our return policy
• 🎒 **Product recommendations** - Find the right gear
• 👤 **Live agent** - Speak to our team

**What would you like?**""",
        "intent": "unknown",
        "fallback": True
    }

# ==================== PROCESS MESSAGE ====================
def process_message(user_message):
    """Process user message and return bot response"""
    
    # Recognize intent
    intent = recognize_intent(user_message)
    
    # Check for post-clarification intent
    if st.session_state.awaiting_clarification and st.session_state.clarification_type == "recommendation":
        result = handle_product_recommendation(user_message)
    elif intent == "greeting":
        result = handle_greeting()
    elif intent == "order_tracking":
        result = handle_order_tracking(user_message)
    elif intent == "returns_exchanges":
        result = handle_returns(user_message)
    elif intent == "product_recommendation":
        result = handle_product_recommendation(user_message)
        if result.get("ask_clarification"):
            st.session_state.awaiting_clarification = True
            st.session_state.clarification_type = "recommendation"
    elif intent == "human_handoff":
        result = handle_human_handoff(user_message)
    else:
        result = handle_unknown(user_message)
    
    return result

# ==================== UI LAYOUT ====================

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🏕️")
with col2:
    st.markdown("# North Star Support Bot")
    st.markdown("*Friendly, helpful outdoor customer support*")

st.divider()

# Chat history display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("intent"):
            st.caption(f"Intent: `{message['intent']}`")

# Chat input
if user_input := st.chat_input("Type your message here... (e.g., 'Track order 111')"):
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Process and get bot response
    result = process_message(user_input)
    
    # Add bot message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "intent": result.get("intent", "unknown")
    })
    
    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(result["response"])
        if result.get("intent"):
            with st.expander("View intent details"):
                intent_info = {
                    "Intent Detected": result.get("intent"),
                    "Resolved": result.get("resolved", False),
                    "Fallback": result.get("fallback", False),
                    "Handoff": result.get("handoff", False)
                }
                st.json(intent_info)
    
    # Rerun to show new message
    st.rerun()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ℹ️ About This Bot")
    st.markdown("""
    **North Star Support Bot** helps with:
    - 📦 Order tracking
    - 🔄 Returns & exchanges
    - 🎒 Product recommendations
    - 👤 Human support handoff
    """)
    
    st.divider()
    
    st.markdown("### 🛠️ Features")
    st.markdown("""
    ✓ Smart intent recognition
    ✓ Real-time order lookup
    ✓ Return policy info
    ✓ Product recommendations
    ✓ Seamless agent handoff
    ✓ Intelligent fallback
    """)
    
    st.divider()
    
    st.markdown("### 🧹 Conversation Management")
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.awaiting_clarification = False
        st.session_state.clarification_type = None
        st.success("✅ Conversation reset!")
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📊 Conversation Stats")
    total_messages = len(st.session_state.messages)
    user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
    bot_messages = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", total_messages)
    with col2:
        st.metric("User", user_messages)
    with col3:
        st.metric("Bot", bot_messages)
    
    if st.session_state.messages:
        st.markdown("### 📝 Recent Intent")
        last_intent = st.session_state.messages[-1].get("intent", "N/A")
        st.info(f"Last intent: **{last_intent}**")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.85rem;'>
    <p>🏕️ North Star Support Bot | Built for outdoor enthusiasts</p>
    <p>Status: <span style='color: #4CAF50;'>●</span> Online</p>
</div>
""", unsafe_allow_html=True)