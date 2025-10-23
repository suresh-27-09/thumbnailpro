import os
from multiprocessing import Value

END = None 

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_thumbnails(q, dest_folder, count: Value):
    create_dir(dest_folder)
    done = 0

    while True:
        item = q.get()

        if item is END:
            q.put(END)
            print("consumer finished all jobs.")
            break

        try:
            name, data = item
            new_name = f"{name}_thumb.jpg"
            save_path = os.path.join(dest_folder, new_name)

            with open(save_path, "wb") as f:
                f.write(data)
            with count.get_lock():
                count.value += 1
            done += 1
            print("saved:", new_name)

        except Exception as e:
            print("error saving:", e)

    print("total saved:", done)
