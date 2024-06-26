import requests

def file_reader(file: str, encoding = "utf-8"):
    with open(file, "r", -1, encoding) as f:
        message = []

        for line in f:
            new_line = line.strip()
            message.append(new_line)
            message.append("\n")

        return ''.join(message)

def file_writer(file: str, text: str, text_binary = 't'):
    if text_binary == 't':
        with open(file, "w", -1, "utf-8") as f:
            f.write(text)
    elif text_binary == 'b':
        with open(file, "wb") as f:
            if 'http' in text:
                responce = requests.get(text).content
                f.write((responce))
            else:
                f.write(text)
    else:
        raise ValueError("Wrong parameters: text_binary")