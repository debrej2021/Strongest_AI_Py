import re
import datetime
import torch
import torch.nn as nn   
import torch.optim as optim

from tiny_llm_agent import extract_expression

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

# =====================================================================
def tool_current_time(_: str = "") -> str:
    return datetime.datetime.now().strftime("%H:%M:%S") 

# =====================================================================
TOOL_REGISTRY = {"calc": tool_calculate, "time": tool_current_time}

# =====================================================================
#Training text and vocabulary
# =====================================================================
training_text = "Q: what is the time? -> ACT:time[] | Q: compute 25+15 -> ACT:calc[25+15] | Q: what is 7*8? -> ACT:calc[7*8] | Q: what is the time now? -> ACT:time[] | "
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
print(f"Character '{example_char}' has ID {example_ix}")
print(f"ID {example_ix} corresponds to character '{ix_to_char[example_ix]}'")

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

 #Instantiate the model with the vocabulary size and print the model architecture.
model = TinyLLM(vocab_size)
print(model)

cross_entropy_loss = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

#Training loop and action generation
inputs = text_tensor[:-1].unsqueeze(0)  # (1, T-1)
targets = text_tensor[1:].unsqueeze(0)    # (1, T-1)
model.train()   

#Start the training loop for 30 epochs, shuffling the training examples each epoch, and calculating the average loss.
for epoch in range(1, 351):
    optimizer.zero_grad()
    logits, _ = model(inputs)
    loss = cross_entropy_loss(logits.view(-1, vocab_size), targets.view(-1))
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch:3d}/350 | Loss: {loss.item():.4f}")

    #Greedy action generation: After training, the model can generate actions based on a given prompt. The generate_action function takes a prompt string and generates a sequence of characters until it reaches a stop symbol or the maximum number of characters.
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
        prompt = f"Q: {user_query} -> "
        prediction = generate_action(prompt)
        match = re.search(r"ACT:(\w+)\[(.*?)\]", prediction)
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
    #Test the agent with a series of queries, including both valid and invalid tool requests, to demonstrate its reasoning, acting, and observing capabilities.
if __name__ == "__main__":
    agent = MinimalAgent(TOOL_REGISTRY)

    test_queries = [
        "what is the time?",
        "compute 25+15",
        "what is 7*8?",
        "what is the time now?",
        "compute 9**9**9",  # Invalid expression
        "unknown tool test"  # No tool detected
    ]

    for query in test_queries:
        agent.run(query)