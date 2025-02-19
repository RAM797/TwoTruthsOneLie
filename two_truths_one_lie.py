import json
import re
import concurrent.futures
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI


executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


prompt_template = """
You are a trivia game generator. Generate 3 statements around a random or interesting topic.
Exactly 2 statements must be TRUE, and exactly 1 statement must be FALSE.

Important requirements:
- The false statement should be subtle and sound plausible, not obviously incorrect.
- The two true statements should be correct but somewhat obscure.
- Do NOT pick overly well-known facts (e.g., “The sky is blue”)

For each statement, also provide a short explanation that can be revealed after the user guesses.

Format your response strictly as valid JSON with the following structure:

{{
  "facts": [
    {{
      "statement": "<string>",
      "truth_value": "<True or False>",
      "explanation": "<string>"
    }},
    {{
      "statement": "<string>",
      "truth_value": "<True or False>",
      "explanation": "<string>"
    }},
    {{
      "statement": "<string>",
      "truth_value": "<True or False>",
      "explanation": "<string>"
    }}
  ]
}}

Here is a good example for you to follow:

{{
  "facts": [
    {{
      "statement": "The French invented French fries in the 17th century.",
      "truth_value": "False",
      "explanation": "Despite the name, French fries are widely believed to have originated in Belgium. The exact timeline is debated, but they are not definitively traced back to France in the 17th century."
    }},
    {{
      "statement": "Some power outages in the United States are caused by squirrels.",
      "truth_value": "True",
      "explanation": "Squirrels sometimes chew through power lines or damage transformers, which can lead to localized power outages."
    }},
    {{
      "statement": "The Australians declared war on emus twice.",
      "truth_value": "True",
      "explanation": "In 1932, the Australian government launched a military campaign (known as the Great Emu War) against emus damaging farmland. This campaign involved at least two major attempts to reduce the emu population."
    }}
  ]
}}

Format your response strictly as valid JSON, and do not wrap your output in triple backticks or any other Markdown formatting.
"""

chain_prompt = PromptTemplate(template=prompt_template, input_variables=[])
llm = ChatOpenAI(
    model_name="gpt-4o",  # using your GPT-4o model
    temperature=0.8,
    max_tokens=500
)
fact_chain = LLMChain(llm=llm, prompt=chain_prompt)


def clean_and_parse_json(raw_response: str):
    """
    Remove any code fences from the LLM output and parse as JSON.
    """
    cleaned = re.sub(r"```(?:json)?", "", raw_response)
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()
    return json.loads(cleaned)

def generate_three_facts():
    response = fact_chain.run({})
    print("Raw response:", response)
    try:
        data = clean_and_parse_json(response)
        return data["facts"]
    except json.JSONDecodeError as e:
        st.error("JSON decoding error: " + str(e))
        return []


def update_next_facts():
    """Submit the fact generation to our thread pool executor"""
    future = executor.submit(generate_three_facts)
    return future.result()


def initialize_state():
    if "current_facts" not in st.session_state:
        st.session_state.current_facts = generate_three_facts()
    if "next_facts" not in st.session_state:
        st.session_state.next_facts = update_next_facts()
    if "selected_fact_index" not in st.session_state:
        st.session_state.selected_fact_index = None
    if "revealed" not in st.session_state:
        st.session_state.revealed = False

initialize_state()


def load_new_facts():
    st.session_state.selected_fact_index = None
    st.session_state.revealed = False
    st.session_state.current_facts = st.session_state.next_facts
    st.session_state.next_facts = update_next_facts()
    
def main():
    st.title("2 Truths and 1 Lie")
    st.write("Try to spot the lie among these three statements!")

    for idx, fact in enumerate(st.session_state.current_facts):
        if st.button(f"{fact['statement']}", key=f"option_{idx}"):
            st.session_state.selected_fact_index = idx
            st.session_state.revealed = True

    if st.session_state.revealed and st.session_state.selected_fact_index is not None:
        chosen_fact = st.session_state.current_facts[st.session_state.selected_fact_index]
        if chosen_fact["truth_value"].lower() == "false":
            st.balloons()
            st.success("Correct! You found the lie.")
        else:
            st.error("Oops! That one is actually true.")
        
        st.write("---")
        st.write("### Explanations")
        for i, fact in enumerate(st.session_state.current_facts):
            truth_label = "True" if fact["truth_value"].lower() == "true" else "False"
            st.write(f"**Option {i+1} ({truth_label}):** {fact['explanation']}")
    
    st.write("---")
    if st.button("Skip / Next Question", key="skip"):
        load_new_facts()

if __name__ == "__main__":
    main()
