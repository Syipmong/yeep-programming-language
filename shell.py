import yeep


while True:
    text = input("yeep >> ")
    print(text)
    error, result = yeep.run("<stdin>", text)
    if error:
        print(error.as_string())
    else:
        print(result)




