import gradio as gr
from difflib import SequenceMatcher

def text_similarity(text1, text2):
    """
    比较两句话的相似度
    Args:
        text1: 第一个文本字符串
        text2: 第二个文本字符串
    Returns:
        0到1之间的浮点数，表示两句话的相似度，1表示完全相似，0表示完全不同
    """

    similarity = SequenceMatcher(None, text1, text2).ratio()
    print(f"{text1} {text2} 相似度: {similarity:.0%}")
    return similarity

demo = gr.Interface(
    fn=text_similarity,
    inputs=[gr.Textbox("我喜欢苹果"), gr.Textbox("你喜欢吃苹果吗？")],
    outputs=[gr.Number()],
    title="文本相似度比较",
    description="比较两句话的相似度"
)

if __name__ == "__main__":
    demo.launch(mcp_server=True)