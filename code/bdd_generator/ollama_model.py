import ollama

def generate_bdd_scenarios(context_file):
    with open(context_file, "r") as file:
        context = file.read()
    
    prompt = f"Convert the following financial transaction system context into BDD Gherkin format:\n\n{context}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    return response['message']['content']

if __name__ == "__main__":
    bdd_scenarios = generate_bdd_scenarios("bdd_generator/context.txt")
    with open("bdd_generator/generated_bdd.feature", "w") as file:
        file.write(bdd_scenarios)
    print("BDD scenarios generated successfully!")
