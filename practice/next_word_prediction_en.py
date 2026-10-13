import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. Load the classic light-weight English GPT-2 model and its tokenizer
model_name = "gpt2"
print(f"Loading English GPT-2 model '{model_name}', please wait...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# 2. Set an incomplete English prompt
prompt = "Artificial intelligence will change the world by"
print("\n" + "=" * 75)
print(f"[Initial Prompt]: {prompt}")
print("=" * 75)

# ⚙️ Hyperparameters
MAX_LENGTH = 150  # Force the model to expand up to 150 tokens
TEMPERATURE = 0.8  # Temperature to maintain creativity over long generation
TOP_K = 10  # Restrict sample pool to top 10 token candidates
eos_token_id = tokenizer.eos_token_id

# Properly initialize the input IDs as a PyTorch Tensor
input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]

print(f"🧠 Black Magic Activated: Forcing GPT-2 to write a long text by denying its right to stop...\n")

for step in range(MAX_LENGTH):
    with torch.no_grad():
        outputs = model(input_ids)
        next_token_logits = outputs.logits[0, -1, :]

        # Calculate raw probability distribution across the entire vocabulary
        raw_probs = F.softmax(next_token_logits, dim=-1)

        # Apply temperature scaling
        scaled_logits = next_token_logits / TEMPERATURE

        # 🚨 ========================================================
        # 🔥 [Strategy 2: Strip the Stop Token Right here]
        # Force the End-of-Sequence (EOS) token logit score to negative infinity.
        # This completely guarantees a 0% chance of being selected during sampling.
        # ========================================================
        scaled_logits[eos_token_id] = -float("Inf")

        # Top-K filtering
        top_k_values, _ = torch.topk(scaled_logits, TOP_K)
        min_values = top_k_values[-1]
        filtered_logits = torch.where(
            scaled_logits < min_values,
            torch.ones_like(scaled_logits) * -float("Inf"),
            scaled_logits
        )
        probs_for_sampling = F.softmax(filtered_logits, dim=-1)

        # Multinomial sampling to pick the winning token
        next_token_id = torch.multinomial(probs_for_sampling, num_samples=1)
        chosen_id = next_token_id.item()

        # --- Calculate Token Statistics ---
        chosen_raw_prob = raw_probs[chosen_id].item() * 100
        raw_sorted_indices = torch.argsort(next_token_logits, descending=True)

        # Extract rank securely using a clean tensor lookup
        chosen_rank = (raw_sorted_indices == chosen_id).nonzero().item() + 1

        # Decode the single token string
        decoded_word = tokenizer.decode([chosen_id])
        display_word = decoded_word.replace('\n', '\\n').replace('\r', '\\r')

        # Real-time console monitor
        print(f"Step {step + 1:03d} ──> Token Chosen: [ {display_word.strip():<10} ] "
              f"| Vocab ID: {chosen_id:<6} "
              f"| Raw Prob: {chosen_raw_prob:>6.2f}% "
              f"| Model Rank: Top {chosen_rank}")

        # Autoregressive concatenation: append token back to inputs for the next loop
        input_ids = torch.cat([input_ids, next_token_id.unsqueeze(0)], dim=-1)

print("\n" + "=" * 75)

# ─── 🛠️ Bulletproof Data Sanitization and Formatting ───

# 1. Flatten the multi-dimensional tensor completely to a 1D pure Python integer list
flat_token_ids = [int(x) for x in input_ids[0].tolist()]

# 2. Decode the whole token list into human-readable text
raw_decoded = tokenizer.decode(flat_token_ids, skip_special_tokens=True)

# 3. Defensive unpacking mechanism against implicit batch wrapper returns
if type(raw_decoded) is list:
    final_text = "".join([str(item) for item in raw_decoded])
else:
    final_text = str(raw_decoded)

# 4. Clean up any literal remnants like ['Your Generated Text String Here']
final_text = final_text.lstrip("['\"").rstrip("]'\"")

# 5. Locate the last English structural punctuation index for a tidy post-production trim
punc_indices = [
    final_text.rfind('.'), final_text.rfind('?'), final_text.rfind('!')
]
last_punctuation = max(punc_indices)

if last_punctuation != -1:
    final_text = final_text[:last_punctuation + 1]

print(f"✨ [Final Output - Forced Continuous Generation Text]:\n{final_text}")
print("=" * 75)
