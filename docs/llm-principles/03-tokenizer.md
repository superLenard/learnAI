# 2.3 Token 与分词器

模型没法直接处理字符，得先把文本切成 **token**（词元）。

- **Token 是什么**：可以是词、子词或字符。中文常按字或词切，英文常按子词切（如 `unhappy` → `un` + `happy`）。
- **分词器（Tokenizer）**：负责"文本 ↔ token 序列"的互相转换。
- **词表（Vocab）**：模型认识的所有 token 集合，常见规模几千到十几万。

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
ids = tokenizer("你好，大模型", return_tensors="pt")
print(ids.input_ids)              # token 的 id 序列
print(tokenizer.convert_ids_to_tokens(ids.input_ids[0]))  # 对应 token
```

> 为什么要分词？一是压缩序列长度（更省计算），二是让模型学到"词/子词"层面的规律。中文模型通常对中文专门优化，一个字或词一个 token。
