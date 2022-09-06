import basic

while True:
    text = input("basic > ")
    res, error = basic.run("<stdin>", text)
    if error:
        print(error.as_string())
    else:
        print(res)
