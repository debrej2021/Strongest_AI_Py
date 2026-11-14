import datetime
import random
import re
import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(0)
random.seed(0)

# =====================================================================
# STEP 1: THE HANDS - tools the agent can use
# =====================================================================
def tool_calculate(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if not expression or not all(c in allowed for c in expression):
        return "Error: Invalid characters"
    if "**" in expression or len(expression) > 30:      # block 9**9**9 style hangs
        return "Error: Expression not allowed"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def tool_current_time(_: str = "") -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

TOOL_REGISTRY = {"calc": tool_calculate, "time": tool_current_time}

# =====================================================================
# STEP 2: THE WORDS - training examples + tokenizer
# =====================================================================
# The brain only learns WHICH tool. "$" is a slot: "the maths in the question".
calc_phrases = ["compute {}", "what is {}?", "calculate {}", "add {}", "solve {}", "how much is {}?"]
time_phrases = ["what is the time?", "what is the time now?", "tell me the time",
                "time please", "current time?", "what time is it?"]

examples = []
for _ in range(40):
    a, b = random.randint(0, 99), random.randint(0, 99)
    expr = f"{a}{random.choice('+-*/')}{b}"
    examples.append(f"Q: {random.choice(calc_phrases).format(expr)} -> ACT:calc[$] |")
for p in time_phrases:
    examples += [f"Q: {p} -> ACT:time[] |"] * 4

vocab = sorted(set("".join(examples)) | set("0123456789"))   # make sure every digit exists
vocab_size = len(vocab)
char_to_ix = {ch: i for i, ch in enumerate(vocab)}
ix_to_char = {i: ch for ch, i in char_to_ix.items()}

def encode(text: str) -> torch.Tensor:
    return torch.tensor([char_to_ix[ch] for ch in text if ch in char_to_ix], dtype=torch.long)

# =====================================================================
# STEP 3: THE BRAIN - a tiny next-character predictor
# =====================================================================
class TinyLLM(nn.Module):
    def __init__(self, vocab_size, embed_dim=32, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)              # (1, T)          -> (1, T, 32)
        x, hidden = self.rnn(x, hidden)    # (1, T, 32)      -> (1, T, 128)
        logits = self.fc(x)                # (1, T, 128)     -> (1, T, vocab_size)
        return logits, hidden

model = TinyLLM(vocab_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

# =====================================================================
# STEP 4: TRAINING + GREEDY GENERATION
# =====================================================================
model.train()
for epoch in range(1, 31):
    random.shuffle(examples)
    total = 0.0
    for ex in examples:                            # one example at a time, fresh memory
        seq = encode(ex).unsqueeze(0)              # (1, T)
        inputs, targets = seq[:, :-1], seq[:, 1:]  # predict the next character
        optimizer.zero_grad()
        logits, _ = model(inputs)
        loss = criterion(logits.view(-1, vocab_size), targets.view(-1))
        loss.backward()
        optimizer.step()
        total += loss.item()
    if epoch % 10 == 0:
        print(f"Epoch {epoch:2d}/30 | Avg loss: {total / len(examples):.4f}")

def generate_action(prompt: str, max_chars: int = 20) -> str:
    model.eval()
    with torch.no_grad():
        logits, hidden = model(encode(prompt).unsqueeze(0))   # read the whole prompt
        generated = ""
        for _ in range(max_chars):
            next_ix = torch.argmax(logits[0, -1]).item()       # most likely next char
            char = ix_to_char[next_ix]
            if char == "|":                                    # stop symbol
                break
            generated += char
            logits, hidden = model(torch.tensor([[next_ix]]), hidden)
    return generated.strip()

# =====================================================================
# STEP 5: THE CONTROLLER - think, act, observe (single step)
# =====================================================================
def extract_expression(text: str) -> str:
    chunks = re.findall(r"[\d+\-*/(). ]+", text)
    chunks = [c.strip() for c in chunks if any(ch.isdigit() for ch in c)]
    return max(chunks, key=len) if chunks else ""

class MinimalAgent:
    def __init__(self, tools: dict):
        self.tools = tools

    def run(self, user_query: str) -> str:
        prediction = generate_action(f"Q: {user_query} -> ")            # THINK
        match = re.search(r"ACT:(\w+)\[(.*?)\]", prediction)
        if not match:
            return f"{user_query!r:24} -> {prediction!r} (no tool)"
        tool_name, tool_arg = match.groups()
        if tool_name not in self.tools:
            return f"{user_query!r:24} -> unknown tool {tool_name!r}"
        if tool_arg == "$":                                             # fill the slot
            tool_arg = extract_expression(user_query)
        observation = self.tools[tool_name](tool_arg)                   # ACT
        return f"{user_query!r:24} -> {prediction:14} -> {observation}"  # OBSERVE

# =====================================================================
# STEP 6: TEST - seen AND unseen questions
# =====================================================================
if __name__ == "__main__":
    agent = MinimalAgent(TOOL_REGISTRY)
    for q in ["compute 25+15", "what is the time?",            # like training
              "compute 3+4", "what is 6*9?", "add 120+35",     # new numbers
              "tell me the time", "time now?", "solve (8-3)*2"]:
        print(agent.run(q))
