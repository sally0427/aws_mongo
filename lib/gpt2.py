

def gpt(text):
    from transformers import pipeline
    from transformers import BertTokenizer, GPT2LMHeadModel

    # tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
    # model = AutoModelWithLMHead.from_pretrained('ckiplab/gpt2-base-chinese')
    tokenizer = BertTokenizer.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    model = GPT2LMHeadModel.from_pretrained("uer/gpt2-chinese-cluecorpussmall")

    text_generation = pipeline('text-generation', model=model, tokenizer=tokenizer)

    prefix_text = text

    generated_text= text_generation(prefix_text, max_length=100, do_sample=False)[0]
    print(generated_text['generated_text'])

# def gpt2(text):
