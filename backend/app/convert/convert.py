
#convert the model
from bigdl.llm import llm_convert
model_path = "/home/aowang/Bigit-local/backend/llms/chatglm-6b"
model_path_output = "/home/aowang/Bigit-local/backend/llms/chatglm-6b-low"
bigdl_llm_path = llm_convert(model=model_path,
        outfile=model_path_output, outtype='int4', model_family="chatglm")

# #load the converted model
# #switch to ChatGLMForCausalLM/GptneoxForCausalLM/BloomForCausalLM/StarcoderForCausalLM to load other models
# from bigdl.llm.transformers import LlamaForCausalLM
# llm = LlamaForCausalLM.from_pretrained("/path/to/output/model.bin", native=True, ...)
  
# #run the converted model
# input_ids = llm.tokenize(prompt)
# output_ids = llm.generate(input_ids, ...)
# output = llm.batch_decode(output_ids)