from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime

app = Flask(__name__)

# ---------------- FAQ DATA ---------------- #

faq_data = [

    {
        "question":"What is Artificial Intelligence?",
        "answer":"Artificial Intelligence (AI) enables machines to simulate human intelligence."
    },

    {
        "question":"What is Machine Learning?",
        "answer":"Machine Learning is a branch of AI that learns from data."
    },

    {
        "question":"What is Deep Learning?",
        "answer":"Deep Learning uses multi-layer neural networks."
    },

    {
        "question":"What is Python?",
        "answer":"Python is a powerful programming language used for AI, Web Development and Automation."
    },

    {
        "question":"Who developed Python?",
        "answer":"Python was created by Guido van Rossum."
    },

    {
        "question":"What is Flask?",
        "answer":"Flask is a lightweight Python web framework."
    }

]

questions = [item["question"] for item in faq_data]

vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(questions)

# ---------------- CHATBOT FUNCTION ---------------- #

def chatbot(message):

    user_vector = vectorizer.transform([message])

    similarity = cosine_similarity(user_vector,question_vectors)

    index = similarity.argmax()

    score = similarity[0][index]

    if score < 0.30:

        return {
            "answer":"Sorry! I couldn't understand your question.",
            "confidence":round(score*100,2)
        }

    return{
        "answer":faq_data[index]["answer"],
        "confidence":round(score*100,2)
    }

# ---------------- HTML ---------------- #

HTML = """

<!DOCTYPE html>

<html>

<head>

<title>Professional AI FAQ Chatbot</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>
body{

margin:0;
padding:0;

font-family:'Segoe UI',sans-serif;

background:linear-gradient(-45deg,#0f172a,#1e3a8a,#2563eb,#38bdf8);

background-size:400% 400%;

animation:bg 12s ease infinite;

height:100vh;

display:flex;

justify-content:center;

align-items:center;

}

@keyframes bg{

0%{background-position:0% 50%;}

50%{background-position:100% 50%;}

100%{background-position:0% 50%;}

}

.container{

width:92%;

max-width:900px;

height:90vh;

background:rgba(255,255,255,.12);

backdrop-filter:blur(18px);

border-radius:25px;

overflow:hidden;

box-shadow:0 0 35px rgba(0,0,0,.35);

display:flex;

flex-direction:column;

}

.header{

background:rgba(255,255,255,.15);

padding:22px;

text-align:center;

color:white;

font-size:30px;

font-weight:bold;

letter-spacing:1px;

}

.subtitle{

font-size:14px;

margin-top:6px;

color:#dbeafe;

}

#chat{

flex:1;

overflow-y:auto;

padding:20px;

background:rgba(255,255,255,.08);

}

.user{

max-width:70%;

margin-left:auto;

margin-bottom:15px;

padding:14px;

background:#2563eb;

color:white;

border-radius:18px 18px 5px 18px;

animation:fade .3s;

}

.bot{

max-width:70%;

margin-right:auto;

margin-bottom:15px;

padding:14px;

background:white;

color:#111827;

border-radius:18px 18px 18px 5px;

animation:fade .3s;

}

small{

display:block;

margin-top:8px;

opacity:.75;

font-size:12px;

}

.input-area{

display:flex;

padding:18px;

background:rgba(255,255,255,.12);

gap:10px;

}

input{

flex:1;

padding:15px;

border:none;

outline:none;

border-radius:12px;

font-size:16px;

}

button{

padding:14px 22px;

border:none;

border-radius:12px;

background:#2563eb;

color:white;

font-size:16px;

cursor:pointer;

transition:.3s;

}

button:hover{

background:#1d4ed8;

transform:scale(1.05);

}

.footer{

padding:12px;

text-align:center;

background:rgba(255,255,255,.08);

color:white;

font-size:14px;

}

@keyframes fade{

from{

opacity:0;

transform:translateY(15px);

}

to{

opacity:1;

transform:translateY(0);

}

}

</style>

</head>

<body>

<div class="container">

<div class="header">

🤖 AI FAQ CHATBOT

<div class="subtitle">

Powered by Flask • NLP • TF-IDF

</div>

</div>

<div id="chat">

<div class="bot">

👋 Hello!

I am your AI FAQ Assistant.

Ask me anything about Python, AI, Machine Learning or Flask.

</div>
</div>

<div class="input-area">

<input
type="text"
id="message"
placeholder="Ask your question here..."
onkeypress="if(event.key==='Enter') sendMessage()">

<button onclick="sendMessage()">
Send
</button>

<button onclick="clearChat()">
Clear
</button>

</div>

<div class="footer">

Professional AI FAQ Chatbot © 2026

</div>

</div>

<script>

function getTime(){

const now=new Date();

return now.toLocaleTimeString([],{

hour:'2-digit',

minute:'2-digit'

});

}

function sendMessage(){

let input=document.getElementById("message");

let text=input.value.trim();

if(text=="") return;

let chat=document.getElementById("chat");

chat.innerHTML+=`

<div class="user">

${text}

<small>${getTime()}</small>

</div>

`;

chat.innerHTML+=`

<div class="bot" id="typing">

🤖 Typing...

</div>

`;

chat.scrollTop=chat.scrollHeight;

fetch("/chat",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

message:text

})

})

.then(response=>response.json())

.then(data=>{

document.getElementById("typing").remove();

chat.innerHTML+=`

<div class="bot">

${data.answer}

<small>

Confidence : ${data.confidence}%<br>

${getTime()}

</small>

</div>

`;

chat.scrollTop=chat.scrollHeight;

});

input.value="";

}

function clearChat(){

document.getElementById("chat").innerHTML=`

<div class="bot">

👋 Hello!

I am your AI FAQ Assistant.

Ask me anything about Python, AI, Machine Learning or Flask.

</div>

`;

}

</script>

</body>

</html>

"""
@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if user_message == "":

        return jsonify({

            "answer":"Please enter a question.",

            "confidence":0

        })

    result = chatbot(user_message)

    return jsonify({

        "answer":result["answer"],

        "confidence":result["confidence"],

        "time":datetime.datetime.now().strftime("%I:%M %p")

    })


@app.route("/about")
def about():

    return jsonify({

        "project":"Professional AI FAQ Chatbot",

        "developer":"Student Project",

        "technology":[

            "Python",

            "Flask",

            "HTML",

            "CSS",

            "JavaScript",

            "TF-IDF",

            "Cosine Similarity"

        ]

    })


if __name__ == "__main__":

    print("="*50)

    print(" Professional AI FAQ Chatbot Started ")

    print("="*50)

    print("Open Browser:")

    print("http://127.0.0.1:5000")

    print("="*50)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
    