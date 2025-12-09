
natural_elegance = """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Serif:wght@400;700&family=Noto+Serif+Devanagari:wght@400;700&family=Noto+Serif+Telugu:wght@400;700&family=Noto+Serif+Kannada:wght@400;700&family=Noto+Serif+Malayalam:wght@400;700&family=Noto+Serif+Tamil:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* --- CSS Variable Definitions: "Natural Elegance" Premium Theme --- */
        :root {
            --primary-color: #2E7D32; /* Rich Forest Green */
            --primary-light: #4CAF50; /* Vibrant Green */
            --primary-dark: #1B5E20; /* Deep Green */
            --secondary-color: #8D6E63; /* Earthy Brown */
            --accent-color: #FFC107; /* Golden Harvest */
            --background-color: #F5F7F5; /* Very Light Green-Grey Mist */
            --card-background: #FFFFFF;
            --text-primary: #1A1A1A; /* Almost Black */
            --text-secondary: #555555;
            --border-color: #E0E0E0;
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Noto Serif', 'Noto Serif Devanagari', 'Noto Serif Telugu', 'Noto Serif Kannada', 'Noto Serif Malayalam', 'Noto Serif Tamil', serif;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 8px rgba(0,0,0,0.08);
            --shadow-lg: 0 8px 16px rgba(0,0,0,0.12);
            --radius-md: 12px;
            --radius-lg: 20px;
        }

        /* --- General Body & App Styling --- */
        html, body, .stApp {
            background-color: var(--background-color);
            color: var(--text-primary);
            font-family: var(--font-body);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary-dark);
            font-family: var(--font-heading);
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        p, label, .stMarkdown {
            color: var(--text-secondary);
            font-family: var(--font-body);
            line-height: 1.6;
            font-size: 1.05rem;
        }

        /* --- Main Title with Leaf Icon --- */
        .main-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 3rem 0 1rem 0;
            background: linear-gradient(135deg, rgba(46, 125, 50, 0.1) 0%, rgba(255, 255, 255, 0) 100%);
            border-radius: var(--radius-lg);
            margin-bottom: 2rem;
            border: 1px solid rgba(46, 125, 50, 0.1);
        }
        .main-title h1 {
            font-size: 3.5rem;
            margin: 0;
            background: linear-gradient(45deg, var(--primary-dark), var(--primary-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 3rem;
            font-weight: 400;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        /* --- Sidebar Styling --- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid var(--border-color);
        }
        [data-testid="stSidebar"] h2 {
            color: var(--primary-dark);
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
            display: inline-block;
        }

        /* --- Tabs Styling: Modern Pills --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background-color: transparent;
            border-bottom: none;
            margin-bottom: 2rem;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 24px;
            font-family: var(--font-heading);
            font-weight: 600;
            color: var(--text-secondary);
            background-color: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--primary-color);
            border-color: var(--primary-color);
            transform: translateY(-2px);
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color) !important;
            color: #FFFFFF !important;
            border-color: var(--primary-color) !important;
            box-shadow: var(--shadow-md);
        }

        /* --- Form, Inputs & Buttons Styling --- */
        .stTextInput input, .stTextArea textarea, .stFileUploader section {
            background-color: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.15);
        }
        
        /* Primary Action Button */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: #FFFFFF;
            border: none;
            border-radius: 50px;
            padding: 14px 32px;
            width: 100%;
            font-family: var(--font-heading);
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
            background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
        }
        
        /* Secondary Button */
        .stButton>button {
            border: 2px solid var(--primary-color);
            background-color: transparent;
            color: var(--primary-color);
            border-radius: 50px;
            padding: 10px 24px;
            font-weight: 600;
            font-family: var(--font-heading);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: var(--primary-color);
            color: white;
            box-shadow: var(--shadow-md);
        }

        /* --- Response Card Styling --- */
        .response-card {
            background-color: var(--card-background);
            border-radius: var(--radius-md);
            padding: 2.5rem;
            margin-top: 2.5rem;
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }
        .response-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary-light), var(--primary-dark));
        }
        .response-card h3 {
            color: var(--primary-dark);
            font-size: 1.6rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .response-card p {
            color: var(--text-primary);
            font-size: 1.1rem;
            line-height: 1.8;
        }

        /* --- Section Headers --- */
        .section-header {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-dark);
            margin-top: 1rem;
            margin-bottom: 1rem;
            text-align: center;
        }

        /* --- Footer --- */
        .footer { 
            text-align: center; 
            color: var(--text-secondary); 
            margin-top: 5rem; 
            padding: 3rem 0; 
            border-top: 1px solid var(--border-color);
            font-size: 0.9rem;
        }
        
        /* --- Custom Scrollbar --- */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1; 
        }
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8; 
        }
    </style>
"""
