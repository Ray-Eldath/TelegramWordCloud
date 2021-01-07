import click
from unicodedata import category


def strip_text(s: str):
    s = s.replace(",", " ").replace("https", "")
    s = ''.join(ch for ch in s if category(ch)[0] not in ['P', 'S'])
    return s.strip()


@click.command("TelegramWordCloud - cloud.py")
@click.option("--mode", type=click.Choice(['constant', 'group', 'group-freq', 'order'], False), help="""
Specify how to generate weight of words.
constant: every words get weight 1.
group: words will be sorted by frequencies,
then divided into N groups that specified by option --groups.
group-freq is like group, but partition is according to its frequency, not index.
Words in the same group will get same weight.
order: words will be sorted by frequencies, and their weight
is the position in the sorted list.""", default="group-freq")
@click.option("--groups", default=6)
@click.option("-n", default=100)
def main(mode: str, groups: int, n: int):
    with open("data_seg", "r", encoding="UTF-8") as file, open("stopwords.txt", "r", encoding="UTF-8") as sw_file:
        result = {}
        stop_flags = ["u", "p", "r", "m", "q", "y", "w", "d", "c"]
        sw = list(map(lambda e: strip_text(e), sw_file.readlines()))
        for line in file.readlines():
            for word in line.split(" "):
                word = word.strip()
                if word and not word.isspace():
                    word_split = list(map(lambda entry: entry.strip(), word.split("/")))
                    word = word_split[0]
                    if word_split[1] in stop_flags or word in sw:
                        continue
                    if word in result:
                        result[word] = result[word] + 1
                    else:
                        result[word] = 0
        with open("freq.csv", "w", encoding="UTF-8") as output:
            lines = []
            result = sorted(result.items(), key=lambda item: item[1], reverse=True)[:n]
            result_max = result[0][1]
            for index, (key, freq) in enumerate(result):
                key = strip_text(str(key))
                weight = freq // (result_max // groups) + 1  # weight_group
                if mode == "constant":
                    weight = 1
                elif mode == "order":
                    weight = n - index
                elif mode == "group":
                    weight = groups - index // (n // groups)

                if key:
                    lines.append(f"{weight},\"{key}\"")
            output.write("\n".join(lines))
    print("result has been saved to freq.csv.")


if __name__ == '__main__':
    main()
