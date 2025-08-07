import ollama
from typing import List, Dict
import textwrap

def format_policy_clauses(clauses: List[str]) -> str:
    """
    Formats a list of policy clauses for the prompt.
    """
    return "\n\n".join([f"Clause {i+1}: {clause}" for i, clause in enumerate(clauses)])


def build_prompt(query_dict: Dict[str, str], clauses: List[str]) -> Dict[str, str]:
    """
    Builds a structured system and user prompt for the LLM.
    """
    system_prompt = (
        "You are an expert assistant that explains health insurance clauses to users.\n"
        "You must respond ONLY based on the provided policy clauses.\n"
        "Avoid speculation. Do not use external knowledge.\n"
        "Be concise and include the most relevant clause number in your justification."
    )

    query_info = "\n".join([
        f"- Age: {query_dict.get('age', 'Not provided')}",
        f"- Procedure: {query_dict.get('procedure', 'Not specified')}",
        f"- Location: {query_dict.get('location', 'Unknown')}",
        f"- Policy Duration: {query_dict.get('policy_duration', 'Unknown')}",
        f"- Intent: {query_dict.get('intent', 'General query')}"
    ])

    user_prompt = (
        f"User Query Metadata:\n{query_info}\n\n"
        f"Relevant Policy Clauses:\n{format_policy_clauses(clauses)}\n\n"
        "Based on the clauses above, does the policy likely cover the user's scenario?\n"
        "Give a Yes/No answer followed by a 1-line justification. Mention the most relevant clause if possible."
    )

    return {"system": system_prompt, "user": user_prompt}


def generate_answer(
    query_dict: Dict[str, str],
    top_k_clauses: List[str],
    model: str = "llama3"
) -> str:
    """
    Calls the LLM to generate a human-like, clause-based response.
    """
    prompt = build_prompt(query_dict, top_k_clauses)

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ]
        )
        return textwrap.fill(response['message']['content'], width=100)

    except Exception as e:
        return f"❌ Error generating answer: {e}"
