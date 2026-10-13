import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 载入懂得礼貌闭嘴的 Chat 聊天模型
model_name = "Qwen/Qwen1.5-0.5B-Chat"
print(f"正在加载中文 Chat 模型 {model_name}，请稍候...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# 2. 设定初始中文前文
prompt = "人工智能在未来将会彻底改变人类的"
print("\n" + "=" * 75)
print(f"【初始前文】: {prompt}")
print("=" * 75)

# ⚙️ 核心参数
MAX_LENGTH = 100  # 硬性上限放宽到 100 步，强迫模型在此范围内展开
TEMPERATURE = 0.8  # 温度，赋予长续写所需的创造力
TOP_K = 10
eos_token_id = tokenizer.eos_token_id

# 初始化 Tensor 格式原生 input_ids
input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]

print(f"🧠 激活黑魔法：剥夺 AI 的闭嘴权，强迫其展开长篇大论...\n")

for step in range(MAX_LENGTH):
    with torch.no_grad():
        outputs = model(input_ids)
        next_token_logits = outputs.logits[0, -1, :]

        # 计算全局词表的真实原生概率分布
        raw_probs = F.softmax(next_token_logits, dim=-1)

        # 应用温度
        scaled_logits = next_token_logits / TEMPERATURE

        # 🚨 ========================================================
        # 🔥【策略二：剥夺闭嘴权的黑魔法核心行】
        # ========================================================
        scaled_logits[eos_token_id] = -float("Inf")

        # 过滤前 10 个候选 Token
        top_k_values, _ = torch.topk(scaled_logits, TOP_K)
        min_values = top_k_values[-1]
        filtered_logits = torch.where(
            scaled_logits < min_values,
            torch.ones_like(scaled_logits) * -float("Inf"),
            scaled_logits
        )
        probs_for_sampling = F.softmax(filtered_logits, dim=-1)

        # 摇号抽奖，决定最终胜出的 Token ID
        next_token_id = torch.multinomial(probs_for_sampling, num_samples=1)
        chosen_id = next_token_id.item()

        # ─── 计算选中词的“战况指标” ───
        chosen_raw_prob = raw_probs[chosen_id].item() * 100
        raw_sorted_indices = torch.argsort(next_token_logits, descending=True)

        # 严格使用二维索引层级提取张量中的名次
        chosen_rank = (raw_sorted_indices == chosen_id).nonzero().item() + 1

        # 解码这一个 Token 字符串
        decoded_word = tokenizer.decode([chosen_id])
        display_word = decoded_word.replace('\n', '\\n').replace('\r', '\\r')

        # 实时打印数据监控
        print(f"步数 {step + 1:03d} ──> 选中碎片: [ {display_word.strip():<8} ] "
              f"| 词表 ID: {chosen_id:<6} "
              f"| 字典原始概率: {chosen_raw_prob:>6.2f}% "
              f"| 模型预测名次: Top {chosen_rank}")

        # 拼接 Tensor 前文，继续下一次预测循环
        input_ids = torch.cat([input_ids, next_token_id.unsqueeze(0)], dim=-1)

print("\n" + "=" * 75)

# ─── 🛠️ 终极地毯式修复：毁灭性粉碎 ['str'] 列表 Bug ───

# 1. 显式地将 input_ids 降维并完全拍扁成最普通的一维纯整数列表
flat_token_ids = [int(x) for x in input_ids[0].tolist()]

# 2. 将全量 token 序列解码为人类语言
raw_decoded = tokenizer.decode(flat_token_ids, skip_special_tokens=True)

# 3. 🔥【终极防御重构】：不用 isinstance 判断，直接用强制转换和空字符串连接法
# 如果是列表，通过 "".join 强行把里面的每一项拼接成字符串；如果是单条字符串，也会被强制处理
if type(raw_decoded) is list:
    final_text = "".join([str(item) for item in raw_decoded])
else:
    final_text = str(raw_decoded)

# 4. 🔥【降维打击隐患】：防止 final_text 依然残留类似于 "['文本']" 的方括号字符串杂质
final_text = final_text.lstrip("['\"").rstrip("]'\"")

# 5. 寻找文本中最后一个中文或英文标点符号的位置进行截断
punc_indices = [
    final_text.rfind('。'), final_text.rfind('？'), final_text.rfind('！'),
    final_text.rfind('.'), final_text.rfind('?'), final_text.rfind('!')
]
last_punctuation = max(punc_indices)

if last_punctuation != -1:
    final_text = final_text[:last_punctuation + 1]

print(f"✨【强行逼迫长篇展开后的自回归文本】:\n{final_text}")
print("=" * 75)
