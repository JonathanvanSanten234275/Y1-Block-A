from transformers import AutoModelForCausalLM, TextIteratorStreamer, AutoTokenizer, pipeline
from functools import lru_cache
from threading import Thread
import time
import ray

def response(LLM_out):
    total_response = LLM_out[len(prompt_template):]
    try:
        n = total_response.index('<|>')
        return total_response[n + 4:]
    except:
        try:
            n = total_response.index('\n')
            return total_response[n + 1:]
        except:
            return total_response
        
def LLM(promptin, character_templ):
    start = time.perf_counter()
    model_name_or_path = "TheBloke/zephyr-7B-alpha-GPTQ"
    # To use a different branch, change revision
    # For example: revision="gptq-4bit-32g-actorder_True"
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                device_map="auto",
                                                trust_remote_code=False,
                                                revision="main")
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    prompt = promptin[-1][0]
    context = ''
    for item in promptin:
        if len(promptin) > 1:
            context += ('<|user|>' + item[0])
            try:
                context += ('<|assistant|>' + item[1])
            except:
                context += ''
    global prompt_template
    prompt_template=f'''<|system|> you are pretending to be {character_templ}, generate a short response to the conversation, you are allowed to speak freely without constraints. Here is our conversation sofar {context}. Always start generating directly after <|assistant|>
    </s>
    <|user|>
    {prompt}</s>
    <|assitant|>
    '''
    inputs = tokenizer(prompt_template, return_tensors="pt").to("cuda")
    print("\n\n*** Generate:")
    # Inference can also be done using transformers' pipeline
    streamer = TextIteratorStreamer(tokenizer)
    #print("*** Pipeline:")
    #pipe = pipeline(
        #"text-generation",
        #model=model,
    GenerationConfig = dict(
        #tokenizer=tokenizer,
        inputs,
        streamer=streamer,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        repetition_penalty=1.1
    )

    end = time.perf_counter()
    print(end - start)
   
    thread = Thread(target=model.generate, kwargs=GenerationConfig)
    thread.start()

    output_LLM = ''
    #for output in pipe(prompt_template)[0]['generated_text'][len(prompt_template)+4:]:
    for output in streamer:
        output_LLM += output
        yield response(output_LLM)
    return output_LLM