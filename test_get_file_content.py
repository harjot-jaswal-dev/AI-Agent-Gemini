from functions.get_file_content import get_file_content
from config import MAX_CHARS


res = get_file_content("calculator", "lorem.txt")

print(len(res))
print(res[-60:])

main_test = get_file_content("calculator", "main.py")
print(main_test)

calculator_test = get_file_content("calculator", "pkg/calculator.py")
print(calculator_test)

error1_test = get_file_content("calculator", "/bin/cat")
print(error1_test)

error2_test = get_file_content("calculator", "pkg/does_not_exist.py")
print(error2_test)