import gradio as gr
import requests
import json

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

def make_request(history):
    data = {"model":"chinese_task", "prompt":history[-1][0]}

    response = requests.post(url, headers=headers, json=data, stream=True)
    history[-1][1] = ""
    for line in response.iter_lines():
        if line:
            val = json.loads(line.decode('utf-8'))['response']

            for ch in val:
                history[-1][1] += ch
                print(ch)
                yield history
            # print(response_json['response'])
            # yield chunk.decode("utf-8")


with gr.Blocks(theme="gradio/monochrome") as demo:

    def user(user_message, history):
        return "", history + [[user_message, None]]
    
    gr.Markdown("""<h1 style="text-align: center;"> task breakdown/任务分解 via Chinese-Llama2</h1>
               This is build running on macos system locally.  
               The system prompt is
               ```<br/> FROM llama2-chinese
PARAMETER temperature 1
<br/>
PARAMETER num_ctx 4096
<br/>
SYSTEM Your responsibilty is to take the task given to you by the user, and return a detailed task breakdown in Simplified Chinese. 
                The user does not know English, so never ever answer unless necessary in English.```

                """)
    #msg = gr.Textbox(label="Task to Breakdown / 任务分解", lines=5, placeholder="Enter your task here. / 在此输入你的任务。")
    #mkdn = gr.Markdown("When you are done, click the button below. / 完成后，点击下面的按钮。")
    chatbot=gr.Chatbot()
    msg = gr.Textbox()
    button = gr.Button(label="Breakdown / 分解")

    button.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        make_request, 
        chatbot, 
        chatbot
    )

    
if __name__ == "__main__":
    demo.queue().launch(server_port=9980, debug=True, server_name="0.0.0.0")