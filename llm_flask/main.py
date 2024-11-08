import os
from flask import Flask, Response, request
import threading
import queue

from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
@app.route('/')
def index():
    
    return Response('''
<!DOCTYPE html>
<html>
<head><title>Flask Streaming Langchain Example</title></head>
<body>
    <form id="form">
        <input name="prompt" value=""/>
        <input type="submit"/>
    </form>
    <div id="output"></div>
    <script>
        const formEl = document.getElementById('form');
        const outputEl = document.getElementById('output');
        let aborter = new AbortController();
        async function run() {
            aborter.abort();  // cancel previous request
            outputEl.innerText = '';
            aborter = new AbortController();
            const prompt = new FormData(formEl).get('prompt');
            try {
                const response = await fetch(
                    '/chain', {
                        signal: aborter.signal,
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            prompt
                        }),
                    }
                );
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) { break; }
                    const decoded = decoder.decode(value, {stream: true});
                    outputEl.innerText += decoded;
                }
            } catch (err) {
                console.error(err);
            }
        }
        run();  // run on initial prompt
        formEl.addEventListener('submit', function(event) {
            event.preventDefault();
            run();
        });
    </script>
</body>
</html>
''', mimetype='text/html')

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)

def llm_thread(g, prompt):
    try:
        chat = ChatOpenAI(
            verbose=True,
            streaming=True,
            callbacks=[ChainStreamHandler(g)],
            temperature=0.7,
        )
        chat([HumanMessage(content=prompt)])
    finally:
        g.close()


def chain(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


@app.route('/chain', methods=['POST'])
def _chain():
    return Response(chain(request.json['prompt']), mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True, debug=True)