import datetime
import re
import torch
import torch.nn as nn
import torch.optim as optim

from asyncio_ml_mini import train

# Whitelist allowed characters for safe calculation
def tool_calculate(expression: str) -> str:
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Returns the current time formatted as HH:MM:SS    
def tool_current_time(_: str = "") -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

# A dictionary mapping tool names to functions
TOOL_REGISTRY = {
    "calc": tool_calculate,
    "time": tool_current_time
}
##STEP 1: Define the training text and build the vocabulary
#Define training_text: A string containing 3 to 4 examples following the format:
training_text = "Q: what is the time? -> ACT:time[] | Q: compute 25+15 -> ACT:calc[25+15] | Q: what is 7*8? -> ACT:calc[7*8] | Q: what is the time now? -> ACT:time[] | "

#Build the Vocabulary:
#Get all unique characters from training_text sorted into a list.
#Store the vocabulary length as vocab_size.
vocab = sorted(set(training_text))
vocab_size = len(vocab)

#Create the Tokenizer Dictionaries:
#char_to_ix: Maps each character to an integer ID ({' ': 0, '+': 1, ...}).
#ix_to_char: Maps each integer ID back to its character ({0: ' ', 1: '+', ...}).
char_to_ix = {ch: i for i, ch in enumerate(vocab)}
ix_to_char = {i: ch for i, ch in enumerate(vocab)}
#Example usage:
example_char = 'Q'
example_ix = char_to_ix[example_char]
print(f"Character '{example_char}' is mapped to index {example_ix}")
print(f"Index {example_ix} is mapped back to character '{ix_to_char[example_ix]}'")

##STEP 2: Convert text to a tensor
#Convert the entire training_text into a PyTorch 1D tensor of token IDs with dtype=torch.long.
text_tensor = torch.tensor([char_to_ix[ch] for ch in training_text], dtype=torch.long)
print(f"Text tensor: {text_tensor}")

#Step 3 :Neural Network Architecture (The "Brain")
#Define a class TinyLLM inheriting from nn.Module.
#In __init__(self, vocab_size, embed_dim=32, hidden_dim=64)
#Call super().__init__().
#self.embedding: An nn.Embedding(vocab_size, embed_dim) layer.
#self.rnn: An nn.RNN(embed_dim, hidden_dim, batch_first=True) layer.
#self.fc: A linear layer mapping hidden_dim to vocab_size.
#Pass input tensor x through the embedding layer.
#Pass the embedded representations and hidden into the RNN.
#Pass the RNN output through the linear layer (self.fc).
#Return both the raw logits and the new hidden state.
class TinyLLM(nn.Module):
    def __init__(self, vocab_size, hidden_size=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.rnn = nn.RNN(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)
        x, hidden = self.rnn(x, hidden)
        logits = self.fc(x)
        return logits, hidden  # Return both logits and hidden
#Instantiate the model:
model = TinyLLM(vocab_size)
print(model)
#Define criterion = nn.CrossEntropyLoss()
criterion = nn.CrossEntropyLoss()
#Define optimizer = optim.Adam(model.parameters(), lr=0.01)
optimizer = optim.Adam(model.parameters(), lr=0.01)

#Example forward pass:
# input_tensor = text_tensor.unsqueeze(0)  # Add batch dimension
# logits, hidden = model(input_tensor)
# print(f"Logits shape: {logits.shape}")

#Step 4: Training Loop & Greedy Action Generator
# =====================================================================
# STEP 4: Training Loop & Greedy Action Generator
# =====================================================================

# 1. Prepare Inputs and Targets (Offset by 1 character)
inputs = text_tensor[:-1].unsqueeze(0)
targets = text_tensor[1:].unsqueeze(0)

# 2. Train the Model
print("Training TinyLLM to recognize tool patterns...")
model.train()
for epoch in range(1, 351):
    optimizer.zero_grad()
    logits, _ = model(inputs)
    loss = criterion(logits.view(-1, vocab_size), targets.view(-1))
    loss.backward()
    optimizer.step()

    if epoch % 50 == 0:
        print(f"Epoch {epoch:3d}/350 | Loss: {loss.item():.4f}")

print("Training finished!\n" + "=" * 50)

# 3. Greedy Action Generator
def generate_action(prompt: str, max_chars: int = 30) -> str:
    model.eval()

    # Filter prompt characters to only those known in vocab
    token_ids = [char_to_ix[ch] for ch in prompt if ch in char_to_ix]
    if not token_ids:
        return ""

    input_tensor = torch.tensor([token_ids], dtype=torch.long)
    hidden = None
    generated = ""

    with torch.no_grad():
        # Prime the RNN memory with the entire prompt
        logits, hidden = model(input_tensor, hidden)
        next_char_ix = torch.argmax(logits[0, -1, :]).item()
        char = ix_to_char[next_char_ix]
        generated += char

        current_token = torch.tensor([[next_char_ix]], dtype=torch.long)

        # Autoregressively generate next characters one by one
        for _ in range(max_chars):
            logits, hidden = model(current_token, hidden)
            next_char_ix = torch.argmax(logits[0, -1, :]).item()
            char = ix_to_char[next_char_ix]

            if char == "|":
                break

            generated += char
            current_token = torch.tensor([[next_char_ix]], dtype=torch.long)

    return generated.strip()

#Step 5: The Agent Controller (The ReAct Loop)
#Create a class MinimalAgent.
#Inside __init__(self, tools): store self.tools = tools.
#Inside run(self, user_query: str):
#Build the formatted prompt.
#Call generate_action(prompt).
#Use re.search to inspect the response.
#If a tool is detected, run it from self.tools and format the answer.
#If no tool is detected, return the model's text directly.
class MinimalAgent:
    def __init__(self, tools: dict):
        self.tools = tools

    def run(self, user_query: str) -> str:
        print(f"-> [User Query]: '{user_query}'")

        # 1. REASON: Align prompt exactly with Step 2's training format
        prompt = f"Q: {user_query} -> "
        prediction = generate_action(prompt)
        print(f"   [LLM Output]: {prediction}")

        # 2. PARSE: Extract tool name and the argument inside the brackets
        pattern = r"ACT:(\w+)\[(.*?)\]"
        match = re.search(pattern, prediction)

        if match:
            tool_name, tool_arg = match.groups()
            print(f"   [Parser]: Detected tool '{tool_name}' with arg '{tool_arg}'")

            # 3. ACT: Execute the matched tool with its specific argument
            if tool_name in self.tools:
                observation = self.tools[tool_name](tool_arg)
                print(f"   [Observation]: {observation}")

                # 4. OBSERVE: Format the final response
                final_answer = f"Result: {observation}"
            else:
                final_answer = f"Error: Tool '{tool_name}' is not registered."
        else:
            final_answer = prediction

        print(f"<- [Final Response]: {final_answer}\n" + "-" * 50)
        return final_answer


# =====================================================================
# STEP 6: TEST THE AGENT
# =====================================================================
if __name__ == "__main__":
    agent = MinimalAgent(tools=TOOL_REGISTRY)

    # Test 1: Math calculation task
    agent.run("compute 25+15")

    # Test 2: System time query task
    agent.run("what is the time?")
    #Test it by instantiating agent = MinimalAgent(TOOL_REGISTRY) and running:
    #agent.run("compute 25+15")
    #agent.run("what is the time?")
    #Example usage:
    #TOOL_REGISTRY = {
    #    "calculator": lambda query: str(eval(query.split("compute")[-1])),
    #    "time": lambda query: "12:00 PM"
    #}
    #agent = MinimalAgent(TOOL_REGISTRY)
    #print(agent.run("compute 25+15"))
    #print(agent.run("what is the time?"))

#    