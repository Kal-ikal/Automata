from flask import Flask, request, render_template, redirect
import os

# Debug print untuk melihat direktori kerja dan path template
print("Current Working Directory:", os.getcwd())
print("Template Path:", os.path.join(os.getcwd(), 'pages', 'web.html'))

app = Flask(__name__, template_folder='pages')

def generate_er_from_fsa(states, transitions, initial_state, final_states):
    return f"Generated ER based on user-defined FSA with states: {states}, transitions: {transitions}, initial state: {initial_state}, final states: {final_states}"

def generate_production_rules(states, transitions):
    production_rules = "Production Rules:\n"
    for state in states:
        if state in transitions:
            for symbol, next_state in transitions[state].items():
                production_rules += f"{state} -> {symbol}{next_state}\n"
    return production_rules

@app.route('/')
def index():
    return redirect('/er')  # Redirect ke halaman /er

@app.route('/er', methods=['GET', 'POST'])
def er_view():
    if request.method == 'POST':
        try:
            states = request.form['states'].split(',')
            input_symbols = request.form['input_symbols'].split(',')
            transitions_input = request.form.getlist('transitions')
            initial_state = request.form['initial_state']
            final_states = request.form['final_states'].split(',')
            
            transitions = {}
            for transition in transitions_input:
                from_state, symbol, to_state = transition.split(',')
                if from_state not in transitions:
                    transitions[from_state] = {}
                transitions[from_state][symbol] = to_state

            # Debug print untuk semua variabel
            print("States:", states)
            print("Input Symbols:", input_symbols)
            print("Transitions:", transitions)
            print("Initial State:", initial_state)
            print("Final States:", final_states)

            er = generate_er_from_fsa(states, transitions, initial_state, final_states)
            production_rules = generate_production_rules(states, transitions)
            
            return render_template('pages/web.html', er=er, production_rules=production_rules)
        except Exception as e:
            print("Error:", e)  # Mencetak error
            return render_template('pages/web.html', er=None, production_rules=None)  # Menampilkan halaman tanpa data
    return render_template('web.html')


if __name__ == '__main__':
    app.run(debug=True)
