from flask import Flask, request, render_template
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
import graphviz
import os

app = Flask(__name__)

# Fungsi untuk menggambar NFA/DFA menggunakan Graphviz
def draw_automaton(transitions, initial_state, final_states, filename):
    dot = graphviz.Digraph()

    # Tambahkan node untuk setiap state
    for state in transitions:
        state = str(state)  # Pastikan state berupa string
        if state in final_states:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state)

    # Tambahkan node untuk initial state
    dot.node("start", shape="none", label="")
    dot.edge("start", str(initial_state))  # Pastikan initial_state berupa string

    # Tambahkan edge untuk setiap transisi
    for from_state, symbols in transitions.items():
        from_state = str(from_state)  # Pastikan from_state berupa string
        for symbol, to_states in symbols.items():
            symbol = str(symbol)  # Pastikan simbol berupa string
            if isinstance(to_states, set):
                for to_state in to_states:
                    dot.edge(from_state, str(to_state), label=symbol)  # Pastikan to_state berupa string
            else:
                dot.edge(from_state, str(to_states), label=symbol)  # Pastikan to_states berupa string

    # Simpan gambar automata
    filepath = os.path.join("static", filename)
    dot.render(filepath, format="png", cleanup=True)
    return f"{filename}.png"


# Route untuk halaman utama (home)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk memproses input form
@app.route('/process', methods=['POST'])
def process():
    try:
        # Mengambil dan memisahkan input states dan input_symbols dari user
        states = set(request.form['states'].split(','))
        input_symbols = set(request.form['input_symbols'].split(','))

        # Ambil transisi dari input sebagai daftar
        transitions_raw = request.form.getlist('transitions')
        transitions = {}

        # Proses setiap transisi yang diinputkan user
        for transition in transitions_raw:
            if transition.strip():  # Memastikan tidak ada input kosong
                from_state, symbol, to_state = transition.split(',')
                if from_state not in transitions:
                    transitions[from_state] = {}
                if symbol not in transitions[from_state]:
                    transitions[from_state][symbol] = set()
                transitions[from_state][symbol].add(to_state)

        # Ambil initial state dan final states dari input user
        initial_state = request.form['initial_state']
        final_states = set(request.form['final_states'].split(','))

        # Debugging print untuk memastikan semua input terbaca dengan benar
        print("States:", states)
        print("Input Symbols:", input_symbols)
        print("Transitions:", transitions)
        print("Initial State:", initial_state)
        print("Final States:", final_states)

        # Buat NFA dari input user
        nfa = NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )

        # Konversi NFA ke DFA
        dfa = DFA.from_nfa(nfa)

        # Gambar NFA dan DFA
        nfa_image = draw_automaton(transitions, initial_state, final_states, "nfa_diagram")
        dfa_image = draw_automaton(dfa.transitions, dfa.initial_state, dfa.final_states, "dfa_diagram")

        # Render hasil ke template result.html
        return render_template('result.html', 
                               states=states, 
                               input_symbols=input_symbols, 
                               transitions=transitions, 
                               initial_state=initial_state, 
                               final_states=final_states, 
                               nfa_image=nfa_image, 
                               dfa_image=dfa_image)
    except Exception as e:
        # Print error untuk membantu debugging
        print(f"Error: {e}")
        return f"Terjadi kesalahan: {e}"

if __name__ == '__main__':
    app.run(debug=True)
