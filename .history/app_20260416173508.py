from flask import Flask, render_template, request

app = Flask(__name__)

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

    return render_template('index.html', result=result, error=error, values=values)

if __name__ == '__main__':
    app.run(debug=True)
