# 2.8 动手：用 transformers 跑一个小模型

用 Hugging Face 的 `transformers` 加载一个很小（0.5B）的开源模型，直观感受"预测下一个词"：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "中国的首都是"
inputs = tokenizer(prompt, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=30)
print(tokenizer.decode(out[0], skip_special_tokens=True))
```

输出类似：

```text
中国的首都是北京
```

> 建议把模型换成 `Qwen/Qwen2.5-7B-Instruct`（需显卡）试试效果差异；没有显卡就用 0.5B 先在 CPU 上跑通流程。
