from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Password Checker</title>
  <style>
    body { font-family: Arial; max-width: 400px; margin: 80px auto; text-align: center; }
    input { padding: 10px; width: 100%; font-size: 16px; box-sizing: border-box; }
    #result { margin-top: 20px; font-size: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <h2>Password Strength Checker</h2>
  <input type="text" id="pw" placeholder="Password likhein" oninput="check()">
  <div id="result"></div>
  <script>
    async function check() {
      const pw = document.getElementById('pw').value;
      const res = await fetch('/check', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password: pw})
      });
      const data = await res.json();
      document.getElementById('result').innerText = data.strength;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/check", methods=["POST"])
def check():
    pw = request.get_json().get("password", "")
    score = 0
    if len(pw) >= 8: score += 1
    if any(c.islower() for c in pw): score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(not c.isalnum() for c in pw): score += 1

    if not pw:
        strength = ""
    elif score <= 2:
        strength = "Weak 🔴"
    elif score <= 4:
        strength = "Medium 🟠"
    else:
        strength = "Strong 🟢"
    return jsonify(strength=strength)

if __name__ == "__main__":
    app.run(debug=True)