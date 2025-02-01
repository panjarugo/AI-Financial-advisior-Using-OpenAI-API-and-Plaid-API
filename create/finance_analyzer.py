
from flask import Flask, render_template_string, request
from datetime import datetime
import csv
import random
import openai  # Uncomment when using real API

app = Flask(__name__)

# Configure OpenAI API (Add your key)
# openai.api_key = "sk-your-key-here"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>💰 Smart Finance Analyzer</title>
    <style>
        :root {
            --primary: #6c5ce7;
            --background: #2d2d39;
            --surface: #3a3a48;
            --text: #ffffff;
            --danger: #ff4757;
            --success: #2ed573;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        body {
            background: var(--background);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            animation: fadeIn 0.5s ease;
        }

        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            background: linear-gradient(45deg, #6c5ce7, #a66efa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .upload-section {
            background: var(--surface);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 3rem;
        }

        .custom-upload {
            position: relative;
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .custom-upload input[type="file"] {
            opacity: 0;
            position: absolute;
            width: 1px;
            height: 1px;
        }

        .upload-label {
            background: var(--primary);
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .upload-label:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
        }

        .result-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--surface);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .result-table th,
        .result-table td {
            padding: 1.2rem;
            text-align: left;
        }

        .result-table th {
            background: var(--primary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-table tr:nth-child(even) {
            background: rgba(255,255,255,0.03);
        }

        .net-positive { color: var(--success); font-weight: bold; }
        .net-negative { color: var(--danger); font-weight: bold; }

        /* AI Advice Section */
        .ai-advice {
            margin-top: 2rem;
            background: var(--surface);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .advice-card {
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            display: flex;
            gap: 1rem;
            align-items: start;
            border-left: 4px solid;
        }

        .advice-critical { border-color: var(--danger); background: rgba(255, 71, 87, 0.1); }
        .advice-warning { border-color: #ffa502; background: rgba(255, 165, 2, 0.1); }
        .advice-recommendation { border-color: var(--success); background: rgba(46, 213, 115, 0.1); }
        .advice-investment { border-color: var(--primary); background: rgba(108, 92, 231, 0.1); }

        .advice-icon { font-size: 1.5rem; flex-shrink: 0; }
        .advice-content h3 { margin-bottom: 0.5rem; }
        .advice-content p { line-height: 1.6; color: rgba(255,255,255,0.9); }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--background); }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }

        @media (max-width: 768px) {
            body { padding: 1rem; }
            .result-table th, .result-table td { padding: 0.8rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Finance Analyzer</h1>
        
        <div class="upload-section">
            <form method="post" enctype="multipart/form-data">
                <div class="custom-upload">
                    <input type="file" name="file" id="fileInput" accept=".csv,.txt" required>
                    <label for="fileInput" class="upload-label">📁 Choose File</label>
                    <input type="submit" value="🚀 Analyze" class="upload-label">
                </div>
            </form>
        </div>

        {% if summary %}
        <div class="results-section">
            <table class="result-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Total Spent</th>
                        <th>Total Saved</th>
                        <th>Net Flow</th>
                    </tr>
                </thead>
                <tbody>
                    {% for day in summary %}
                    <tr>
                        <td>{{ day.date }}</td>
                        <td class="net-negative">▼ ₹{{ "%.2f"|format(day.spent) }}</td>
                        <td class="net-positive">▲ ₹{{ "%.2f"|format(day.saved) }}</td>
                        <td class="{{ 'net-positive' if (day.saved - day.spent) > 0 else 'net-negative' }}">
                            ₹{{ "%.2f"|format(day.saved - day.spent) }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        {% if ai_advice %}
        <div class="ai-advice">
            <h2>AI Financial Advisor Suggestions</h2>
            {% for advice in ai_advice %}
            <div class="advice-card advice-{{ advice.type }}">
                <div class="advice-icon">
                    {% if advice.type == 'critical' %}⚠
                    {% elif advice.type == 'investment' %}📈
                    {% else %}💡{% endif %}
                </div>
                <div class="advice-content">
                    <h3>{{ advice.title }}</h3>
                    <p>{{ advice.content }}</p>
                </div>
            </div>
            {% endfor %}
            
            <div class="advice-card advice-recommendation">
                <div class="advice-icon">🤖</div>
                <div class="advice-content">
                    <h3>Powered by FinanceGPT</h3>
                    <p>Enable real AI analysis: 
                        <a href="#" style="color: var(--primary); text-decoration: underline;">
                            Connect OpenAI API
                        </a>
                    </p>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileName = e.target.files[0].name;
            document.querySelector('.upload-label').textContent = '📁 ' + fileName;
        });
    </script>
</body>
</html>
'''

def mock_transaction_api(transaction_id):
    return {
        'date': datetime(2023, random.randint(1,12), random.randint(1,28)).strftime('%Y-%m-%d'),
        'amount': round(random.uniform(10, 1000), 2),
        'type': random.choice(['debit', 'credit'])
    }

def process_upload(file):
    transaction_ids = []
    content = file.stream.read().decode('utf-8')
    
    if file.filename.endswith('.csv'):
        reader = csv.reader(content.splitlines())
        for row in reader:
            if row:
                transaction_ids.append(row[0].strip())
    else:
        transaction_ids = [line.strip() for line in content.splitlines() if line.strip()]
    
    return transaction_ids

def generate_ai_advice(summary):
    """Generate financial advice (Replace with actual API call)"""
    total_spent = sum(day['spent'] for day in summary)
    total_saved = sum(day['saved'] for day in summary)
    
    # Mock AI analysis
    advice = [
        {
            'type': 'warning',
            'title': '🚨 High Spending Alert',
            'content': f'You\'re spending {(total_spent/(total_saved + total_spent)):.0%} of income'
        },
        {
            'type': 'investment',
            'title': '📈 Investment Tip',
            'content': f'Invest ₹{total_saved * 0.15:.2f} monthly in index funds'
        }
    ]
    
    # Uncomment for real OpenAI integration
    '''
    prompt = f"Act as financial advisor analyzing: Income ₹{total_spent + total_saved}, Expenses ₹{total_spent}, Savings ₹{total_saved}. Give 3 concise recommendations."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # Parse response into advice format
    '''
    
    return advice

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    ai_advice = None
    
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            transaction_ids = process_upload(file)
            transactions = [mock_transaction_api(tid) for tid in transaction_ids]
            
            daily_totals = {}
            for t in transactions:
                date = t['date']
                if date not in daily_totals:
                    daily_totals[date] = {'spent': 0, 'saved': 0}
                
                if t['type'] == 'debit':
                    daily_totals[date]['spent'] += t['amount']
                else:
                    daily_totals[date]['saved'] += t['amount']
            
            summary = sorted([{'date': date, **values} for date, values in daily_totals.items()], 
                           key=lambda x: x['date'])
            
            if summary:
                ai_advice = generate_ai_advice(summary)

    return render_template_string(HTML_TEMPLATE, summary=summary, ai_advice=ai_advice)

if __name__ == '__main__':
    app.run(debug=True)



