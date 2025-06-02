from textnode import TextNode, TextType

def main():
    dummy_obj = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy_obj)


if __name__ == "__main__":
    main()