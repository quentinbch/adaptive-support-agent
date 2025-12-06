import gradio as gr
from src.agent import AdaptiveAgent

# 1. Instantiate the Agent
agent = AdaptiveAgent()


# 2. Interaction Logic
def interact_with_agent(message, history):
	# Initialize history if it's None
	if history is None:
		history = []

	# Call the agent in streaming mode
	response_generator, level, strategy = agent.process_request_stream(message)

	# 1. Add USER message
	history.append({"role": "user", "content": message})

	# 2. Add ASSISTANT message
	history.append({"role": "assistant", "content": ""})

	partial_response = ""

	for chunk in response_generator:
		partial_response += chunk

		# Update the CONTENT of the last message
		history[-1]["content"] = partial_response

		yield history, "", level, strategy


# 3. User Interface
with gr.Blocks(title="Adaptive Agent") as demo:
	gr.Markdown("# 🦎 Adaptive AI Agent")
	gr.Markdown(
		"> **Context:** This prototype demonstrates an agent's ability to **infer implicit preferences** (technical level) and **adapt its strategy** in real-time.")

	with gr.Row():
		# Left Column: Chat
		with gr.Column(scale=2):
			chatbot = gr.Chatbot(
				label="Support Session",
				height=450
			)
			msg = gr.Textbox(label="Your Message",
			                 placeholder="Try: 'The screen is black...' or '500 Error on API endpoint...'")
			clear_btn = gr.Button("New Session")

		# Right Column: Debug / Visualization
		with gr.Column(scale=1, variant="panel"):
			gr.Markdown("### 🔍 Adaptation Engine")
			gr.Markdown("*Real-time visualization of dynamic profiling*")

			lbl_level = gr.Textbox(label="Detected Level (Profiling)", value="Waiting...", interactive=False)
			lbl_strategy = gr.TextArea(label="System Instruction (Prompt Tuning)", value="...", interactive=False,
			                           lines=10)

	# Event Wiring
	msg.submit(interact_with_agent, [msg, chatbot], [chatbot, msg, lbl_level, lbl_strategy])


	# Reset button logic
	def reset_chat():
		return [], "", "Waiting...", "..."


	clear_btn.click(reset_chat, outputs=[chatbot, msg, lbl_level, lbl_strategy])

if __name__ == "__main__":
	demo.launch()