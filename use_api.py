

from dotenv import load_dotenv
import os
import openai



def find_txt_files():
    files = []
    for file in os.listdir(os.getcwd()+"/web_text"):
        if file.endswith(".txt") and len(file)>4:
            print(os.path.join(os.getcwd()+"/web_text", file))
            files.append(os.path.join(os.getcwd()+"/web_text", file))
    return files

txt_files = find_txt_files()
print(txt_files)

load_dotenv("local.env")  # put the key in the .env file

client = openai.OpenAI(
    api_key=os.getenv("LITELLM_API_KEY"),
    base_url="https://cmu.litellm.ai",
)


#path = 'web_text/wiki/Pittsburgh.txt'
for txt_file in txt_files:
    # Open the file with UTF-8 encoding
    with open(txt_file, 'r', encoding='utf-8') as file:
        text = file.read()


    response = client.chat.completions.create(
        model="gpt-4o-mini", #Allowed:['gpt-4o-mini', 'gpt-4o', 'text-embedding-3-small', 'text-embedding-3-large']"
        messages=[
            {"role": "system", "content": "You are an assistant that use the material below to generate a Q&A in the following format. Q: (Some question)\nA:(Some answer)\n\nQ: (Some question)\nA:(Some answer)..."},
            {"role": "user", "content": f"Generate the Q&As based on the text:\n\n{text}"}
        ]
    )

    filename = f"annotations/{txt_file.strip('/.txt').split('/')[-1]}_annotation.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.choices[0].message.content)