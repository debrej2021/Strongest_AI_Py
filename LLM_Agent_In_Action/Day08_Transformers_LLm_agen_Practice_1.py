"""
agent_from_scratch.py
======================
An educational, complete implementation of an autonomous AI Agent built
from first principles using a custom PyTorch character-level RNN.

Key Concepts Demonstrated:
1. Neural Engine: A character-level Recurrent Neural Network (LLM).
2. Protocol Alignment: Training the model to output tool-call commands.
3. Tool Registry: External deterministic functions (the agent's "hands").
4. ReAct Controller: Reason -> Parse -> Act -> Observe execution loop.
"""

import datetime
import re
import torch
import torch.nn as nn
import torch.optim as optim

# =====================================================================
# STEP 1: DEFINE EXTERNAL TOOLS (The "Hands")
# =====================================================================
# Language models struggle with precise arithmetic and real-time state.
# We create deterministic Python functions to handle these tasks reliably.


def tool_calculate(expression: str) -> str:
    """Evaluates mathematical expressions safely using Python's parser.

    The model only needs to formulate the equation; Python calculates it.
    """
    try:
        # Whitelist permitted characters to prevent arbitrary code execution
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            return "Error: Unsupported characters in calculation."

        # Compute the verified numeric result
        result = eval(expression)
        return str(result)
    except Exception as err:
        return f"Calculation Error: {err}"


def tool_get_time(_: str = "") -> str:
    """Queries your operating system clock to fetch current local time."""
    return datetime.datetime.now().strftime("%H:%M:%S")


# Registry dictionary: maps string tool names to actual Python callables
TOOL_REGISTRY = {
    "calc": tool_calculate,
    "time": tool_get_time,
}


# =====================================================================
# STEP 2: TRAINING DATA & SYNTAX PROTOCOL
# =====================================================================
# Modern LLMs are trained to follow structured formatting (like JSON).
# For our micro-model, we define a compact string protocol:
#   Input:  "Q: <query> -> "
#   Action: "ACT:<tool_name>[<tool_argument>]"
#   Stop:   "|" (tells generation when to halt)

training_corpus = (
    "Q: what is the time? -> ACT:time[] | "
    "Q: compute 25+15 -> ACT:calc[25+15] | "
    "Q: current time -> ACT:time[] | "
    "Q: calculate 8*9 -> ACT:calc[8*9] | "
)

# Extract all unique characters to build our vocabulary table
vocabulary = sorted(list(set(training_corpus)))
vocab_size = len(vocabulary)

# Character-level mappings (Tokenizer)
char_to_ix = {ch: idx for idx, ch in enumerate(vocabulary)}
ix_to_char = {idx: ch for idx, ch in enumerate(vocabulary)}

# Convert full corpus string into numerical tensor IDs
training_tensor = torch.tensor(
    [char_to_ix[c] for c in training_corpus], dtype=torch.long
)


# =====================================================================
# STEP 3: NEURAL NETWORK ARCHITECTURE (The "Brain")
# =====================================================================
class TinyLLM(nn.Module):

    def __init__(self, vocab_size: int, embed_dim: int = 32, hidden_dim: int = 64):
        super().__init__()
        # Layer 1: Vector lookup table converting token ID -> dense coordinates
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # Layer 2: Recurrent layer preserving sequence history across steps
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)

        # Layer 3: Projection head converting hidden state -> raw scores (logits) per token
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden_state=None):
        # x shape: (batch_size, sequence_length)
        embedded = self.embedding(x)
        rnn_out, hidden_state = self.rnn(embedded, hidden_state)
        logits = self.fc(rnn_out)
        return logits, hidden_state


# Initialize network, loss function, and optimizer
model = TinyLLM(vocab_size=vocab_size)
optimizer = optim.Adam(model.parameters(), lr=0.01)

# nn.CrossEntropyLoss automatically applies Log-Softmax internally,
# so our model outputs raw unnormalized logits directly.
criterion = nn.CrossEntropyLoss()


# =====================================================================
# STEP 4: MODEL TRAINING (Next-Character Prediction)
# =====================================================================
# Inputs: characters from index 0 to N-1
# Targets: characters from index 1 to N (shifted one position forward)
inputs = training_tensor[:-1].unsqueeze(0)
targets = training_tensor[1:].unsqueeze(0)

print("Starting training: teaching TinyLLM tool-use protocol...")
model.train()

for epoch in range(1, 351):
    optimizer.zero_grad()  # Reset gradients from previous step

    logits, _ = model(inputs)

    # Flatten batch and sequence dimensions for CrossEntropyLoss calculation
    loss = criterion(logits.view(-1, vocab_size), targets.view(-1))

    loss.backward()  # Compute gradients via backpropagation
    optimizer.step()  # Update neural network weights

    if epoch % 70 == 0:
        print(f"Epoch {epoch:3d}/350 | Loss: {loss.item():.4f}")

print("Training complete. Model weights ready.\n" + "=" * 60)


# =====================================================================
# STEP 5: INFERENCE ENGINE (Deterministic Greedy Decoding)
# =====================================================================
def generate_action(prompt: str, max_chars: int = 30) -> str:
    """Takes a user prompt, primes the RNN, and generates tokens until

    it encounters the stop character '|' or hits max_chars.
    """
    model.eval()

    # Discard any characters unseen during training
    token_ids = [char_to_ix[c] for c in prompt if c in char_to_ix]
    if not token_ids:
        return ""

    input_tensor = torch.tensor([token_ids], dtype=torch.long)
    hidden_state = None
    generated_text = ""

    with torch.no_grad():
        # Step A: Prime the RNN state with prompt tokens
        logits, hidden_state = model(input_tensor, hidden_state)

        # Greedy choice: pick the single character with highest score (argmax)
        next_char_id = torch.argmax(logits[0, -1, :]).item()
        generated_text += ix_to_char[next_char_id]

        current_token = torch.tensor([[next_char_id]], dtype=torch.long)

        # Step B: Autoregressively roll out remaining characters
        for _ in range(max_chars):
            logits, hidden_state = model(current_token, hidden_state)
            next_char_id = torch.argmax(logits[0, -1, :]).item()
            char = ix_to_char[next_char_id]

            # Stop generating if the model outputs our delimiter token '|'
            if char == "|":
                break

            generated_text += char
            current_token = torch.tensor([[next_char_id]], dtype=torch.long)

    return generated_text.strip()


# =====================================================================
# STEP 6: AGENT CONTROLLER (The ReAct Loop)
# =====================================================================
class MinimalAgent:
    """Autonomous agent wrapping our language model with tool-execution capabilities.

    Execution cycle:
      1. REASON  -> Model generates action intent.
      2. PARSE   -> Agent parses function name and arguments.
      3. ACT     -> Agent executes Python function.
      4. OBSERVE -> Agent captures output to answer the user.
    """

    def __init__(self, tools: dict):
        self.tools = tools

    def run(self, user_query: str) -> str:
        print(f"-> [User Query]: '{user_query}'")

        # 1. REASON: Query the neural model to predict an action
        prompt = f"Q: {user_query} -> "
        raw_prediction = generate_action(prompt)
        print(f"   [LLM Decision]: {raw_prediction}")

        # 2. PARSE: Search output for protocol regex: ACT:tool_name[arguments]
        pattern = r"ACT:(\w+)\[(.*?)\]"
        match = re.search(pattern, raw_prediction)

        if match:
            tool_name, tool_arg = match.groups()
            print(f"   [Action Parser]: Detected '{tool_name}' with parameter '{tool_arg}'")

            # 3. ACT: Execute registered tool
            if tool_name in self.tools:
                observation = self.tools[tool_name](tool_arg)
                print(f"   [Tool Output]: {observation}")

                # 4. OBSERVE: Return finalized verified response
                final_answer = f"The answer is {observation}."
            else:
                final_answer = f"Error: Tool '{tool_name}' not available."
        else:
            # Fallback if no tool call was emitted
            final_answer = raw_prediction

        print(f"<- [Final Response]: {final_answer}\n" + "-" * 60)
        return final_answer


# =====================================================================
# STEP 7: TEST EXECUTION
# =====================================================================
if __name__ == "__main__":
    agent = MinimalAgent(tools=TOOL_REGISTRY)

    # Test Case 1: Arithmetic reasoning task
    agent.run("compute 25+15")

    # Test Case 2: System environment query task
    agent.run("what is the time?")