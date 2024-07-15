from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_aws.chat_models import ChatBedrock
from langchain_aws.embeddings import BedrockEmbeddings
from vertexai.generative_models import GenerativeModel
import vertexai
import os

model_kwargs = {"temperature": 0.01}


claude_config = {
    "credentials_profile_name": "default",  # E.g "default"
    "region_name": "us-east-1",  # E.g. "us-east-1"
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0", 
}

gpt_config = {
    "model_endpoint": "https://ai-capdev-oai-eastus-gcc2.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_id": "gpt-4o"
}

gemini_config = {
    "project_id": "gvt0031-gcp-152-govtext-ds",
    "location": "asia-southeast1",
    "model_id": "gemini-1.5-flash-001"
}


class LLMHelper:
    def __init__(self, model_type):
        if model_type not in ["gemini", "claude", "gpt"]:
            raise ValueError("Model type must be one of \"gemini\", \"claude\", or \"gpt\" ")
        
        self.model_type = model_type

        # use gemini without api key, login using gcloud auth application-default login
        if model_type == "gemini":
            vertexai.init(project=gemini_config["project_id"], location=gemini_config["location"])
            self.model = GenerativeModel(model_name="gemini-1.5-flash-001", generation_config=model_kwargs)


        elif model_type == "gpt":
            # To pass "AZURE_OPENAI_API_KEY" as an environment parameter when using

            os.environ["AZURE_OPENAI_ENDPOINT"] = gpt_config["model_endpoint"]
            
            self.model = AzureChatOpenAI(
                openai_api_version=gpt_config["api_version"],
                azure_deployment=gpt_config["model_id"],
                **model_kwargs,
            )
            
        elif model_type == "claude":
            self.model = ChatBedrock(
                credentials_profile_name=claude_config["credentials_profile_name"],
                region_name=claude_config["region_name"],
                endpoint_url=f"https://bedrock-runtime.{claude_config['region_name']}.amazonaws.com",
                model_id=claude_config["model_id"],
                model_kwargs=model_kwargs,
            )

    def generate(self, prompt):
        if self.model_type == "gemini":
            return self.model.generate_content(prompt).text
        # langchain generation
        else:
            message = HumanMessage(
                content=prompt
            )
            return self.model.invoke([message]).content














