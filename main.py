import os
from multiprocessing import Process, Queue, Value
from create import make_thumbnails 
from save import save_thumbnails    

def make_dir(path):
  
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    input_path = "img"
    output_path = "output"
    make_dir(input_path)
    make_dir(output_path)
    q = Queue(maxsize=8)
    count = Value('i', 0)
    print("starting producer & consumer...")
    p1 = Process(target=make_thumbnails, args=(q, input_path))
    p2 = Process(target=save_thumbnails, args=(q, output_path, count))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("done. total saved:", count.value)

if __name__ == "__main__":
    main()
