from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from functools import lru_cache
import time

def response(LLM_out):
    total_response = LLM_out[len(prompt_template)+3:]
    print(total_response)
    return total_response


@lru_cache
def LLM(promptin):
    start = time.perf_counter()

    model_name_or_path = "TheBloke/zephyr-7B-alpha-GPTQ"
    # To use a different branch, change revision
    # For example: revision="gptq-4bit-32g-actorder_True"
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                device_map="auto",
                                                trust_remote_code=False,
                                                revision="main")

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

    prompt = promptin
    global prompt_template
    prompt_template=f'''<|system|> generate a very short response you are allowed to say anything
    </s>
    <|user|>
    {prompt}</s>
    <|assitant|>
    '''

    print("\n\n*** Generate:")

    # Inference can also be done using transformers' pipeline

    print("*** Pipeline:")
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        repetition_penalty=1.1
    )

    end = time.perf_counter()
    print(end - start)
   
    return(response(pipe(prompt_template)[0]['generated_text']))