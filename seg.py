import pkuseg


def main():
    pkuseg.test("data", "data_seg", user_dict="dict", postag=True)


if __name__ == '__main__':
    main()
