import yeep

print("\t\t\t\t\tYeep Programming Language")
print("\t\t\t\tProgramme Written and Developed by Yipmong Said")


while True:
	text = input('yeep > ')
	if text.strip() == "": continue
	result, error = yeep.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))