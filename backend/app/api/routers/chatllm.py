import argparse

from bigdl.llm.langchain.llms import *
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def main():
    
    question = '你是谁'
    model_path = "/home/aowang/Bigit-local/backend/llms/chatglm-6b-low/bigdl_llm_chatglm_q4_0.bin"
    model_family = 'chatglm'
    n_threads = 2
    template ="""{question}"""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    model_family_to_llm = {
        "llama": LlamaLLM,
        "gptneox": GptneoxLLM,
        "bloom": BloomLLM,
        "starcoder": StarcoderLLM,
        "chatglm": ChatGLMLLM
    }

    if model_family in model_family_to_llm:
        langchain_llm = model_family_to_llm[model_family]
    else:
        raise ValueError(f"Unknown model family: {model_family}")
    
    llm = langchain_llm(
        model_path=model_path,
        n_threads=n_threads,
        callback_manager=callback_manager, 
        verbose=True
    )

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    llm_chain.run(question)


if __name__ == '__main__':

    
    main()