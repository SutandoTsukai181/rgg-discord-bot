import zipfile
# returns (name, ext)


def split_ext(filename):
    index = filename.rindex('.') if '.' in filename else -1
    return (filename[:index], filename[index+1:]) if index != -1 else ('', '')


def check_size(files):
    size = 0
    for f in files:
        size += len(f.fp.getvalue())
    return size
