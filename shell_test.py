import yeep

print("Yeep Programming Language")
print("Programme Written and Developed by Yipmong Said")
while True:
    text = input("yeep >> ")
    print(text)

    ast, error = yeep.run("<stdin>", text)

    if error:
        print(error)
    else:
        print(ast)

    if text == "exit()":
        break
