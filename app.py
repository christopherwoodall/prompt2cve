import gradio as gr


def greet(name):
    return "Hello " + name + "!"


demo = gr.Interface(fn=greet, inputs="text", outputs="text")

if __name__ == "__main__":
    # Launch args -
    #   https://github.com/gradio-app/gradio/issues/260#issuecomment-1520933912
    demo.launch(server_name="0.0.0.0", server_port=7860)