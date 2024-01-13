import rev

print("Yeep Programming Language")
print("Programme Written and Developed by Yipmong Said")
while True:
    text = input("yeep >> ")
    
    if text == "exit()":
        break

    ast, error = rev.run("<stdin>", text)

    if error:
        print(error)
    else:
        print(ast)
