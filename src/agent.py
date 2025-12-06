from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src import config, prompts
import time


class AdaptiveAgent:
	def __init__(self):
		print(f"Loading model {config.LLM_MODEL_NAME}...")
		self.llm = ChatOllama(model=config.LLM_MODEL_NAME, temperature=config.TEMPERATURE)
		print("Model loaded and ready.")

	def _detect_user_profile(self, user_input: str) -> str:
		"""
		OBSERVATION PHASE: Analyzes the user's technical level.
		This step is synchronous (blocking) because we need the result before generating.
		"""
		print("Phase 1: Analyzing user profile...")
		start_time = time.time()

		prompt = ChatPromptTemplate.from_messages([
			("system", prompts.ANALYSIS_SYSTEM_PROMPT),
			("user", "{text}")
		])
		chain = prompt | self.llm | StrOutputParser()

		# We wait for the classification result
		detected_level = chain.invoke({"text": user_input}).strip().upper()

		duration = time.time() - start_time
		print(f"Analysis finished in {duration:.2f}s. Result: {detected_level}")

		# Safety fallback
		if detected_level not in prompts.STRATEGIES:
			return "NEUTRAL"
		return detected_level

	def process_request_stream(self, user_input: str):
		"""
		Orchestration with STREAMING.
		Returns a generator (stream) instead of a full text.
		"""
		# 1. Dynamic Profiling (Blocking)
		level = self._detect_user_profile(user_input)

		# 2. Select Strategy (Contextual Prompt Adaptation)
		system_instruction = prompts.STRATEGIES.get(level, prompts.STRATEGIES["NEUTRAL"])

		print(f"Phase 2: Streaming response with strategy [{level}]...")

		# 3. Prepare Generation Chain
		response_prompt = ChatPromptTemplate.from_messages([
			("system", system_instruction),
			("user", "{text}")
		])

		chain = response_prompt | self.llm | StrOutputParser()

		# Return the stream object, the level, and the strategy
		return chain.stream({"text": user_input}), level, system_instruction