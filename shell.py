import yeep

print("\t\t\t\t\tYeep Programming Language")
print("\t\t\t\tProgramme Written and Developed by Yipmong Said")

# print("\t\t\t\t\t Copyright 2024 All Rights Reserved")
while True:
    text = input("yeep >> ")
    print(text)
    result = yeep.run("<stdin>", text)

    if isinstance(result, list):
        for error in result:
            print(error.as_string())
    else:
        print(result)
    if text == "exit()":
        break
