# 🏕️ North Star Support Bot

A customer support chatbot for outdoor apparel and camping gear, built with Streamlit.

## Features

- ✅ **Order Tracking** - Track order status (orders 111, 222, 333)
- ✅ **Return & Exchanges** - View return policy and shipping options
- ✅ **Product Recommendations** - Get personalized product suggestions
- ✅ **Human Handoff** - Seamless transition to live agent support
- ✅ **Smart Fallback** - Graceful handling of unknown inputs

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Mac, Windows, or Linux

### Installation

1. Clone the repository
```bash
git clone https://github.com/YourUsername/north_star_chatbot.git
cd north_star_chatbot
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate     # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the chatbot
```bash
streamlit run north_star_chatbot_streamlit.py
```

5. Open browser to `http://localhost:8501`

## Testing

Try these messages:
- "Track my order 111" → Shows shipping status
- "What's your return policy?" → Shows policy details
- "Recommend a tent" → Product recommendation
- "I need an agent" → Human handoff
- "asdfghjkl" → Fallback handling

## Project Requirements Met

✅ All 4 core use cases implemented  
✅ Intent recognition with variation handling  
✅ Accurate mock data (orders 111/222/333)  
✅ Fallback handling for unknown inputs  
✅ Professional UI with Streamlit  
✅ Comprehensive documentation  

## Tech Stack

- **Framework:** Streamlit
- **Language:** Python 3.8+
- **Dependencies:** See requirements.txt

## Demo

Video demo available showing all features:
- Order tracking (all statuses)
- Return policy explanation
- Product recommendations
- Human agent handoff
- Fallback scenario handling

Duration: 2-3 minutes

## Author

[Your Name] - Upwork Talent Accelerator Project

## License

MIT (or no license - your choice)
