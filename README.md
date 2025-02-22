# **Tool-Calling Agent with Custom Memory System**  

This repository implements a **tool-calling AI agent** using **LangChain**, **OpenAI GPT models**, and a **custom memory system** for efficient conversation history management.  

🚀 **Key Features:**  
- Uses **LangChain** to interact with OpenAI's GPT models.  
- Implements a **custom memory system** to store only **Human, AI, and Tool messages**, reducing token usage.  
- Supports **dynamic tool calling** for operations like addition, multiplication, and managing to-dos.  
- Optimized to **avoid duplicate API calls**, minimizing costs and improving response speed.  

---

## **🛠️ Setup & Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/PinsaraPerera/langchain_function_calling.git
cd langchain_function_calling
```

### **2️⃣ Install Dependencies**  
```bash
uv sync
```

### **3️⃣ Set Up Environment Variables**  
Create a `.env` file in the project root and add your OpenAI API key:  
```env
OPENAI_API_KEY=your_openai_api_key

DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""
```

### **4️⃣ Set Up the Database**  
Ensure that your database tables are created before running the script:  
```python
from src.db.base import Base
from src.db.session import engine

Base.metadata.create_all(bind=engine)
```

---

## **🚀 Running the Agent**  
Start the interactive agent by running:  
```bash
uv run main.py
```

### **💬 Example Usage**  
```bash
Enter your input: Hello!
AI: Hello! How can I assist you today?

Enter your input: Create a to-do item: "Buy groceries"
Tool: To-do item "Buy groceries" has been added.
AI: I have added "Buy groceries" to your to-do list.

Enter your input: Add 5 and 3
Tool: 5 + 3 = 8
AI: The result is 8.

Enter your input: What tasks are on my to-do list?
Tool: Your current to-do items: ["Buy groceries"]
AI: Here is your to-do list: ["Buy groceries"]

Enter your input: Analyze my recent tasks and summarize them.
Tool: Your recent tasks include: ["Buy groceries"]. Summary: "You have 1 pending task."
AI: You have one pending task: "Buy groceries."

Enter your input: Remove "Buy groceries" from my to-do list
Tool: The item "Buy groceries" has been removed.
AI: "Buy groceries" has been successfully removed from your to-do list.

Enter your input: exit

```

---

## **⚡ Key Components**  

### **🔹 Custom Memory System** (`memory.py`)  
- Stores only **Human, AI, and Tool messages**.  
- Reduces token usage by preventing unnecessary message repetition.  

### **🔹 Tool Calling System** (`tools/`)  
- Supports dynamic tool invocation:  
  - `add_tool`: Adds two numbers.  
  - `multiply_tool`: Multiplies two numbers.  
  - `create_todo`: Creates a to-do item.  
  - `get_todo`: Retrieves to-do items.  
  - `remove_todo`: Removes a to-do item.  

### **🔹 Token Tracking System** (`tokens.json`)  
- Tracks **prompt tokens, completion tokens, and total usage** to optimize API calls.  

---

## **🛠️ Future Improvements**  
✅ Add persistent database storage for conversation history.  
✅ Implement logging and debugging tools.  
✅ Expand toolset with more advanced operations.  

---

## **🤝 Contributing**  
1. Fork the repository.  
2. Create a new branch: `git checkout -b feature-branch`  
3. Commit your changes: `git commit -m "Added new feature"`  
4. Push to the branch: `git push origin feature-branch`  
5. Open a pull request.  

---

## **📜 License**  
This project is licensed under the **MIT License**.  

---

## **📧 Contact**  
For questions or suggestions, feel free to reach out via GitHub issues. 🚀  

