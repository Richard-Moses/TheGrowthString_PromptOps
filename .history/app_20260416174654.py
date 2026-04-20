from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Arithmetic Calculator</title>
    <style>
      :root {
        color-scheme: light;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f3f5f9;
        color: #111827;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        min-height: 100vh;
        background: radial-gradient(circle at top left, rgba(49, 130, 206, 0.16), transparent 32%),
          radial-gradient(circle at bottom right, rgba(168, 85, 247, 0.14), transparent 26%);
      }

      .page-shell {
        max-width: 760px;
        margin: 0 auto;
        padding: 2rem 1rem 3rem;
      }

      .hero {
        padding: 2rem 2rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 28px;
        box-shadow: 0 24px 80px rgba(15, 23, 42, 0.08);
        margin-bottom: 1.75rem;
      }

      .eyebrow {
        margin: 0 0 0.75rem;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #6366f1;
      }

      .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 2.5vw, 3rem);
        line-height: 1.05;
      }

      .hero p {
        margin: 1rem 0 0;
        color: #4b5563;
        max-width: 34rem;
      }

      .card {
        padding: 2rem;
        background: #ffffff;
        border-radius: 28px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.06);
      }

      .calculator-form {
        display: grid;
        gap: 1rem;
      }

      .field-row {
        display: grid;
        gap: 0.55rem;
      }

      label {
        display: block;
        font-size: 0.95rem;
        font-weight: 600;
        color: #374151;
      }

      input,
      select {
        width: 100%;
        border: 1px solid #d1d5db;
        border-radius: 14px;
        padding: 0.95rem 1rem;
        font-size: 1rem;
        color: #111827;
        background: #f9fafb;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }

      input:focus,
      select:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
      }

      .primary-button {
        width: 100%;
        padding: 1rem 1.1rem;
        border: none;
        border-radius: 14px;
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }

      .primary-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.18);
      }

      .message {
        margin-top: 1.25rem;
        padding: 1.2rem 1.25rem;
        border-radius: 18px;
        display: grid;
        gap: 0.4rem;
      }

      .message-label {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }

      .result {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
      }

      .error {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
      }

      @media (max-width: 600px) {
        .page-shell {
          padding: 1.25rem;
        }

        .hero,
        .card {
          border-radius: 22px;
        }
      }
    </style>
  </head>
  <body>
    <div class="page-shell">
      <header class="hero">
        <div>
          <p class="eyebrow">Simple Math Tool</p>
          <h1>Arithmetic Calculator</h1>
          <p>Enter two numbers and choose an operation to compute the result instantly.</p>
        </div>
      </header>

      <main class="card">
        <form method="post" class="calculator-form">
          <div class="field-row">
            <label for="a">Number A</label>
            <input type="text" id="a" name="a" value="{{ values.a }}" placeholder="Enter first number" required>
          </div>

          <div class="field-row">
            <label for="b">Number B</label>
            <input type="text" id="b" name="b" value="{{ values.b }}" placeholder="Enter second number" required>
          </div>

          <div class="field-row">
            <label for="operation">Operation</label>
            <select id="operation" name="operation">
              <option value="add" {% if values.operation == 'add' %}selected{% endif %}>Add</option>
              <option value="subtract" {% if values.operation == 'subtract' %}selected{% endif %}>Subtract</option>
              <option value="multiply" {% if values.operation == 'multiply' %}selected{% endif %}>Multiply</option>
              <option value="divide" {% if values.operation == 'divide' %}selected{% endif %}>Divide</option>
            </select>
          </div>

          <button type="submit" class="primary-button">Calculate</button>
        </form>

        {% if result is not none %}
          <div class="message result">
            <span class="message-label">Result</span>
            <strong>{{ result }}</strong>
          </div>
        {% endif %}

        {% if error %}
          <div class="message error">
            <span class="message-label">Error</span>
            <strong>{{ error }}</strong>
          </div>
        {% endif %}
      </main>
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    values = {'a': '', 'b': '', 'operation': 'add'}

    if request.method == 'POST':
        values['a'] = request.form.get('a', '').strip()
        values['b'] = request.form.get('b', '').strip()
        values['operation'] = request.form.get('operation', 'add')

        try:
            a = float(values['a'])
            b = float(values['b'])

            if values['operation'] == 'add':
                result = a + b
            elif values['operation'] == 'subtract':
                result = a - b
            elif values['operation'] == 'multiply':
                result = a * b
            elif values['operation'] == 'divide':
                if b == 0:
                    raise ValueError('Cannot divide by zero')
                result = a / b
            else:
                error = 'Unknown operation selected.'
        except ValueError as exc:
            error = f'Invalid input: {exc}'

    return render_template_string(HTML_TEMPLATE, result=result, error=error, values=values)

if __name__ == '__main__':
    app.run(debug=True)
