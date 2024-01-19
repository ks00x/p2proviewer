import numpy as np
import io

def np_to_csv_stream(im,fmt='%1.2f')->str:        
        bio = io.BytesIO()
        np.savetxt(bio,im,fmt=fmt,delimiter=' ')
        return bio.getvalue().decode('latin1')       
