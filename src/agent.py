from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src import config, prompts


class AdaptiveAgent:
	def __init__(self):
		# Initialize LLM with config
		self.llm = ChatOllama(model=config.LLM_MODEL_NAME, temperature=config.TEMPERATURE)
		print(f"✅ Agent initialized with model: {config.LLM_MODEL_NAME}")

	def _detect_user_profile(self, user_input: str) -> str:
		"""
		OBSERVATION PHASE: Infers the user's technical level (Implicit Preference Learning).
		"""
		prompt = ChatPromptTemplate.from_messages([
			("system", prompts.ANALYSIS_SYSTEM_PROMPT),
			("user", "{text}")
		])
		chain = prompt | self.llm | StrOutputParser()

		# Clean up response (remove potential whitespace)
		detected_level = chain.invoke({"text": user_input}).strip().upper()

		# Safety fallback if LLM hallucinates a different word
		if detected_level not in prompts.STRATEGIES:
			return "NEUTRAL"
		return detected_level

	def process_request(self, user_input: str):
		"""
		Orchestration: Analyze -> Adapt -> Generate
		Returns: (response_text, detected_level, used_strategy)
		"""
		# 1. Dynamic Profiling
		level = self._detect_user_profile(user_input)

		# 2. Strategy Selection (Contextual Prompt Adaptation)
		system_instruction = prompts.STRATEGIES.get(level, prompts.STRATEGIES["NEUTRAL"])

		# 3. Response Generation
		response_prompt = ChatPromptTemplate.from_messages([
			("system", system_instruction),
			("user", "{text}")
		])

		chain = response_prompt | self.llm | StrOutputParser()
		response = chain.invoke({"text": user_input})

		return response, level, system_instruction