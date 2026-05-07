from functions.get_file_content import get_file_content
from config import MAX_CHARS


res = get_file_content("calculator", "lorem.txt")

print(len(res))
print(res[-60:])