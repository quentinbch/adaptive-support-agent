import gradio as gr
from src.agent import AdaptiveAgent

# 1. Instantiate the Agent
agent = AdaptiveAgent()


# 2. Interaction Logic
def interact_with_agent(message, history):
	# Call the structured agent
	response, level, strategy = agent.process_request(message)

	# Update chat history
	history.append((message, response))

	# Return updates: Chatbot, Input (cleared), Level Label, Strategy Label
	return history, "", level, strategy


# 3. UI Layout
with gr.Blocks(title="Adaptive Agent Demo") as demo:
	gr.Markdown("# 🦎 Adaptive AI Agent")
	gr.Markdown(
		"> **Context:** This prototype demonstrates an agent's ability to **infer implicit preferences** (technical level) and **adapt its strategy** in real-time.")

	with gr.Row():
		# Left Column: Chat Interface
		with gr.Column(scale=2):
			chatbot = gr.Chatbot(label="Support Session", height=450)
			msg = gr.Textbox(label="Your Message",
			                 placeholder="Try: 'The screen is black...' vs '500 Error on API endpoint...'")
			clear_btn = gr.Button("New Session")

		# Right Column: Debug / Internal State Visualization
		with gr.Column(scale=1, variant="panel"):
			gr.Markdown("### 🔍 Adaptation Engine")
			gr.Markdown("*Real-time visualization of dynamic profiling*")

			lbl_level = gr.Textbox(label="Detected Level (Profiling)", value="Waiting...", interactive=False)
			lbl_strategy = gr.TextArea(label="Injected System Instruction (Prompt Tuning)", value="...",
			                           interactive=False, lines=10)

	# Event Wiring
	msg.submit(interact_with_agent, [msg, chatbot], [chatbot, msg, lbl_level, lbl_strategy])
	clear_btn.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
	demo.launch()