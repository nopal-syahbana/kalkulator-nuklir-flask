from flask import Flask, render_template, request

app = Flask(__name__)

# Variabel untuk menyimpan log perhitungan
logs = []

def jarak_aman(aktivitas, gamma, laju_paparan, ketebalan, hvl):
    """
    Menghitung jarak aman dari sumber radiasi sesuai dengan rumus yang diberikan.
    """
    import math
    exponent = ketebalan / hvl
    main_factor = (gamma * aktivitas / laju_paparan)
    jarak = math.sqrt(main_factor * (0.5 ** exponent))
    return round(jarak, 2)  # Membatasi hasil dengan 2 digit setelah koma

@app.route('/', methods=['GET', 'POST'])
def index():
    result_supervisi = None
    result_pengendalian = None
    if request.method == 'POST':
        try:
            aktivitas = float(request.form['aktivitas'])
            laju_paparan_supervisi = float(request.form['laju_paparan_supervisi'])
            laju_paparan_pengendalian = float(request.form['laju_paparan_pengendalian'])
            isotop = request.form['isotop']

            # Nilai gamma berdasarkan isotop yang dipilih
            isotop_values = {
                'Ir-192': 500,
                'Au-198': 416,
                'Cs-137': 662,
                'I-131': 364
            }
            gamma = isotop_values[isotop]
            ketebalan = 20  # Ketebalan kolimator tungsten dalam mm
            hvl = 3  # Half-Value Layer dalam mm

            # Hitung jarak aman untuk supervisi
            result_supervisi = jarak_aman(aktivitas, gamma, laju_paparan_supervisi, ketebalan, hvl)
            # Hitung jarak aman untuk pengendalian
            result_pengendalian = jarak_aman(aktivitas, gamma, laju_paparan_pengendalian, ketebalan, hvl)

            # Tambahkan log hasil perhitungan
            logs.append({
                "isotop": isotop,
                "aktivitas": round(aktivitas, 2),
                "laju_paparan_supervisi": round(laju_paparan_supervisi, 2),
                "result_supervisi": result_supervisi,
                "laju_paparan_pengendalian": round(laju_paparan_pengendalian, 2),
                "result_pengendalian": result_pengendalian
            })
            
        except ValueError:
            result_supervisi = "Input tidak valid. Pastikan memasukkan angka yang benar."
            result_pengendalian = "Input tidak valid. Pastikan memasukkan angka yang benar."
    
    return render_template('index.html', result_supervisi=result_supervisi, result_pengendalian=result_pengendalian, logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
