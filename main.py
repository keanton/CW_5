from src.utils import main
import time


start_time = time.time()
main()

end_time = time.time()
total_time = end_time - start_time

print(f"Время выполнения программы: {total_time} секунд")