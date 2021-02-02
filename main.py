import json
import click


def strip_text(s: str):
    s = s.strip()
    return s


@click.command("TelegramWordCloud - main.py")
@click.option("--ignore", "-i", help="Ignore messages sends from these account.", multiple=True)
def main(ignore: list):
    print("ignore messages from: ", ", ".join(ignore))
    with open("result.json", "r", encoding="UTF-8") as messages:
        data = json.load(messages)["messages"]

        with open("data", "w", encoding="UTF-8") as output:
            result = []
            for entry in data:
                if str(entry["type"]) == "message":
                    if "via_bot" in entry or "media_type" in entry or str(entry["from"]) in ignore:
                        continue

                    text = entry["text"]
                    if type(text) == list:
                        inner_result = []
                        for text_entry in text:
                            if type(text_entry) == dict:
                                inner_type = str(text_entry["type"])
                                inner_text = strip_text(str(text_entry["text"]))
                                if inner_type not in ['italic', 'bold', 'strikethrough', 'text_link']:
                                    continue

                                if inner_text:
                                    inner_result.append(inner_text)
                            elif type(text_entry) == str:
                                text_entry = strip_text(str(text_entry))
                                if text_entry:
                                    inner_result.append(text_entry)
                        text = ''.join(inner_result)
                    elif type(text) == str:
                        text = strip_text(text)
                    if "forwarded_from" in entry and len(text) > 100:  # 我们yan真是太聪明了！！
                        continue
                    elif text:
                        result.append(text)
            output.write('\n'.join(result))
    print("result has been saved to file data")


if __name__ == '__main__':
    main()
