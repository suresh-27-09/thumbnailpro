import os
import io
from PIL import Image


END_FLAG = None  

def is_img_file(fname):
    valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    return fname.lower().endswith(valid_ext)


def make_thumbnails(q, folder_path, size=(200, 200)):
    done_count = 0

    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print("folder not found:", folder_path)
        return

    for fname in sorted(files):
        fpath = os.path.join(folder_path, fname)
        if not os.path.isfile(fpath) or not is_img_file(fname):
            continue

        try:
            with Image.open(fpath) as img:
                img = img.convert("RGB")
                img.thumbnail(size)

                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                img_data = buf.getvalue()

                name = os.path.splitext(fname)[0]
                q.put((name, img_data))
                done_count += 1
                print("thumbnail created for:", fname)

        except Exception as e:
            print("error in:", fname, "-", e)

    q.put(END_FLAG)
    print("total thumbnails:", done_count)
