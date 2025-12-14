## ⚠️ **API Keys Required**

Climate Signal needs API keys to fetch data. Please follow these steps:

### **1. Get Free API Keys:**

**OpenWeatherMap (Required):**
- Visit: https://openweathermap.org/api
- Sign up for free account
- Copy your API key

**Alpha Vantage (Required):**
- Visit: https://www.alphavantage.co/support/#api-key
- Get free API key (no credit card)
- Copy your API key

**Gemini AI (Optional - for AI Insights):**
- Visit: https://makersuite.google.com/app/apikey
- Sign in with Google
- Create API key

### **2. Add Keys to `.env` File:**

Open `z:/Projects/Kiro/.env` and add your keys:

```env
# Required API Keys
OPENWEATHERMAP_API_KEY=your_openweathermap_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Optional (AI Insights will use fallback if not provided)
GEMINI_API_KEY=your_gemini_key_here
```

### **3. Restart Backend:**

After adding keys, restart the Flask server:
```bash
cd z:/Projects/Kiro/backend
python -m flask run
```

### **4. Test the App:**

Open http://localhost:3000 and try:
- City: New York
- Stock: AAPL
- Date Range: 30 Days
- Click "Analyze Correlation"

---

**Note:** All APIs have generous free tiers perfect for testing!
