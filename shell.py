import yeep


while True:
    text = input("yeep >> ")
    print(text)
    result, error = yeep.run(text)
    if error is None:
        print(result)
    else:
        print(error.as_string())

        
