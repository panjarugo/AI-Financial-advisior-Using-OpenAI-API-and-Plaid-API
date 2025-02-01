import gradio as gr
from datetime import datetime
import base64
import requests
from PIL import Image
from io import BytesIO

class FinanceAdvisor:
    def __init__(self):
        self.categories = {
            'budgeting': {
                'keywords': ['budget', 'spending plan', 'allocate money', 'track spending'],
                'icon': '💰',
                'tooltip': 'Budgeting and Expense Tracking'
            },
            'saving': {
                'keywords': ['save money', 'savings', 'emergency fund', 'save for'],
                'icon': '🏦',
                'tooltip': 'Savings and Emergency Fund'
            },
            'debt': {
                'keywords': ['debt', 'loan', 'credit card', 'mortgage'],
                'icon': '💳',
                'tooltip': 'Debt Management'
            },
            'investing': {
                'keywords': ['invest', 'stock market', 'mutual funds', 'etf'],
                'icon': '📈',
                'tooltip': 'Investment Strategies'
            },
            'income': {
                'keywords': ['income', 'salary', 'raise', 'side hustle'],
                'icon': '💵',
                'tooltip': 'Income Growth'
            }
        }
        
        self.responses = {
            'budgeting': {
                'general': """💰 Budgeting Guide:
1. Track all income sources
2. List fixed expenses (rent, utilities)
3. Calculate variable expenses
4. Use the 50/30/20 rule:
   - 50% for needs
   - 30% for wants
   - 20% for savings
5. Use budgeting apps or spreadsheets
6. Review and adjust monthly""",
                
                'specific': {
                    'track spending': "📱 Tracking Tools:\n- Mint\n- YNAB\n- Personal Capital\n- Spreadsheet templates",
                    'monthly plan': "📅 Monthly Budget Steps:\n1. Calculate income\n2. List expenses\n3. Set saving goals\n4. Allow flexibility"
                }
            },
            
            'saving': {
                'general': """🏦 Saving Strategies:
1. Automate savings
2. Build emergency fund
3. Use high-yield accounts
4. Employer matching
5. Cut subscriptions
6. Mindful spending""",
                
                'specific': {
                    'emergency fund': "🆘 Emergency Fund:\n3-6 months of expenses in accessible account",
                    'retirement': "👵 Retirement Planning:\n- 401(k)\n- IRA\n- HSA\n- Social Security"
                }
            }
        }

    def create_category_buttons(self):
        buttons_html = ""
        for category, info in self.categories.items():
            buttons_html += f"""
            <button 
                onclick="document.getElementById('input-text').value='{info['tooltip']}'; document.getElementById('submit-btn').click();"
                class="category-btn"
                title="{info['tooltip']}"
            >
                {info['icon']} {category.title()}
            </button>
            """
        return buttons_html

    def generate_response(self, user_input):
        if not user_input.strip():
            buttons = self.create_category_buttons()
            return f"""
            <div class="advisor-response">
                <h3>Welcome to Your Personal Finance Advisor! 🎯</h3>
                <p>Click a category to learn more:</p>
                <div class="category-buttons">
                    {buttons}
                </div>
            </div>
            """

        matched_categories = self.categorize_query(user_input)
        response = self.get_response_for_categories(matched_categories, user_input)
        
        return f"""
        <div class="advisor-response">
            {response}
            <div class="category-buttons">
                {self.create_category_buttons()}
            </div>
        </div>
        """

    def categorize_query(self, query):
        query = query.lower()
        return [
            category for category, info in self.categories.items()
            if any(keyword in query for keyword in info['keywords'])
        ]

    def get_response_for_categories(self, categories, query):
        if not categories:
            return f"""
            <h3>🤔 Let me help you with your financial questions!</h3>
            <p>Click any category below to learn more:</p>
            """
        
        response = ""
        for category in categories:
            if category in self.responses:
                specific = self.get_specific_response(category, query)
                if specific:
                    response += f"<div class='response-section'>{specific}</div>"
                else:
                    response += f"<div class='response-section'>{self.responses[category]['general']}</div>"
        
        return response

    def get_specific_response(self, category, query):
        if category in self.responses:
            for key, response in self.responses[category].get('specific', {}).items():
                if key in query.lower():
                    return response
        return None

def custom_css():
    return """
    <style>
    .advisor-response {
        font-family: 'Arial', sans-serif;
        padding: 20px;
        border-radius: 10px;
        background: #f8f9fa;
    }
    .category-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
    }
    .category-btn {
        padding: 8px 16px;
        border: none;
        border-radius: 20px;
        background: #007bff;
        color: white;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 14px;
    }
    .category-btn:hover {
        background: #0056b3;
        transform: translateY(-2px);
    }
    .response-section {
        margin: 15px 0;
        padding: 15px;
        border-left: 4px solid #007bff;
        background: white;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """

def create_interface():
    advisor = FinanceAdvisor()
    
    with gr.Blocks(css=custom_css()) as iface:
        gr.HTML("<h1>🏦 Personal Finance AI Advisor</h1>")
        
        with gr.Row():
            input_text = gr.Textbox(
                label="Your Financial Question",
                placeholder="Ask about budgeting, saving, investing, or debt management...",
                elem_id="input-text"
            )
        
        with gr.Row():
            submit_btn = gr.Button("Get Advice", elem_id="submit-btn")
        
        with gr.Row():
            output = gr.HTML(label="AI Financial Advice")
        
        # Set initial state
        input_text.change(advisor.generate_response, inputs=[input_text], outputs=[output])
        submit_btn.click(advisor.generate_response, inputs=[input_text], outputs=[output])
        
        # Show initial welcome message
        output.value = advisor.generate_response("")

    return iface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch(share=True)