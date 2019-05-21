from .conventional import minmax_scale, scale
from .debackground import airPLS
from .denoise import dae, wavelet, savgol_filter
from .detect import get_transfered_model

model = get_transfered_model()
