from flask import Flask, request, jsonify
from state import appointment_submitted, submitted_data, history
from agent.appointment_agent import agent_executor
# history = []  # Initialize the history list

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.json.get("message")
    history.append({"role": "user", "content": user_input})
    if not user_input:
        return jsonify({"error": "No input message provided"}), 400

    try:
        response = agent_executor.run(history)
        history.append({"role": "assistant", "content": response})
        # response = get_agent_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route("/success")
def success():
    email = request.args.get('email')
    name = request.args.get('name')
    submission_uuid = request.args.get('submission_uuid')

    print(f"✅ Appointment Process Done!")
    print(f"📧 Email: {email}")
    print(f"🙍 Name: {name}")
    print(f"🆔 Submission UUID: {submission_uuid}")
    
    submitted_data['email'] = email
    submitted_data['name'] = name
    submitted_data['submission_uuid'] = submission_uuid

    global submitted
    submitted = True
    appointment_submitted.set()
    print("✅ Process done successfully!")
    return """
    <html>
    <head>
        <title>Appointment Confirmed</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
                margin: 0;
            }
            .message-box {
                text-align: center;
                padding: 30px 40px;
                border-radius: 12px;
                background-color: white;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            h2 {
                color: #2e7d32;
            }
        </style>
    </head>
    <body>
        <div class="message-box">
            <h2>✅ Thank you for your Time!</h2>
            <p>You may now close this window.</p>
        </div>
    </body>
    </html>
    """



if __name__ == "__main__":
    app.run(debug=True)
