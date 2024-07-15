from llm_utils.llms import LLMHelper

def test_prompts():
    prompt = "Tell me a joke."
    
    gemini_helper = LLMHelper(model_type="gemini")
    print(gemini_helper.generate(prompt))


    gpt_helper = LLMHelper(model_type="gpt")
    print(gpt_helper.generate(prompt))

    claude_helper = LLMHelper(model_type="claude")
    print(claude_helper.generate(prompt))

if __name__ == "__main__":
    test_prompts()