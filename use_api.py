

from dotenv import load_dotenv
import os
import openai


# get all txt files
def find_txt_files(directory):
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

txt_files = find_txt_files("web_text")


load_dotenv("local.env")  # put the key in the .env file

client = openai.OpenAI(
    api_key=os.getenv("LITELLM_API_KEY"),
    base_url="https://cmu.litellm.ai",
)


#path = 'web_text/wiki/Pittsburgh.txt'
for txt_file in txt_files[:3]:
    with open(txt_file, "r") as file:
        text = file.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini", #Allowed:['gpt-4o-mini', 'gpt-4o', 'text-embedding-3-small', 'text-embedding-3-large']"
        messages=[
            {"role": "system", "content": "You are an assistant that use the material below to generate a Q&A in the following format. Q: (Some question)\nA:(Some answer)\n\nQ: (Some question)\nA:(Some answer)..."},
            {"role": "user", "content": f"Generate the Q&As based on the text:\n\n{text}"}
        ]
    )

    filename = f"annotations/{txt_file.strip('/.txt').split('/')[-1]}_annotation.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.choices[0].message.content)