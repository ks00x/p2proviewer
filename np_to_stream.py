import numpy as np
import os
import uuid

def np_to_csv_stream(im,fmt='%1.3f'): # a hack to get the csv data as a str. Is there a fast direct way?
    tmp = str(uuid.uuid4())
    x = np.savetxt(tmp, im, delimiter=',',fmt=fmt)
    with open(tmp) as f:
        csv = f.read()
    os.remove(tmp)
    return csv