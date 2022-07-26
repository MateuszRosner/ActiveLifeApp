

from argparse import HelpFormatter
from audioop import ratecv
from pickle import NONE

from enum import Enum, unique

@unique
class Measurement_t(Enum):
    UNDEFINED = 0
    ECG = 1
    BIOZ =2

@unique
class InductionCurrent_t(Enum):
    UNDEFINED   = 0
    CURR_OFF    = 1
    CURR_8_UA   = 2
    CURR_16_UA  = 3
    CURR_32_UA  = 4
    CURR_48_UA  = 5
    CURR_64_UA  = 6
    CURR_80_UA  = 7
    CURR_96_UA  = 8 
@unique
class InductionFreq_t(Enum):
    UNDEFINED       = 0
    FREQ_128_KHZ    = 1
    FREQ_80_KHZ     = 2
    FREQ_40_KHZ     = 3
    FREQ_10_KHZ     = 4
    FREQ_8_KHZ      = 5
    FREQ_4_KHZ      = 6
    FREQ_2_KHZ      = 7
    FREQ_1_KHZ      = 8
    FREQ_500_HZ     = 9
    FREQ_250_HZ     = 10
    FREQ_125_HZ     = 11

@unique
class BIOZ_HPF_t(Enum):
    UNDEFINED       = 0
    HPF_BYPASS      = 1
    HPF_4_HZ        = 2
    HPF_8_HZ        = 3
    HPF_16_HZ       = 4

@unique
class BIOZ_LPF_t(Enum):
    UNDEFINED       = 0
    LPF_BYPASS      = 1
    LPF_125_HZ      = 2
    LPF_300_HZ      = 3
    LPF_800_HZ      = 4
    LPF_2000_HZ     = 5
    LPF_3700_HZ     = 6
    LPF_7200_HZ     = 7

@unique
class BIOZ_GAIN_t(Enum):
    UNDEFINED       = 0
    GAIN_10_VV      = 1
    GAIN_20_VV      = 2
    GAIN_40_VV      = 3
    GAIN_80_VV      = 4

@unique
class BIOZ_RATE_t(Enum):
    UNDEFINED       = 0
    RATE_FAST       = 1
    RATE_SLOW       = 2

@unique
class ECG_GAIN_t(Enum):
    UNDEFINED       = 0
    GAIN_20_VV      = 1
    GAIN_40_VV      = 2
    GAIN_80_VV      = 3
    GAIN_160_VV     = 4

@unique
class ECG_LPF_t(Enum):
    UNDEFINED       = 0
    LPF_BYPASS      = 1
    LPF_40_HZ       = 2
    LPF_100_HZ      = 3
    LPF_150_HZ      = 4

@unique
class ECG_HPF_t(Enum):
    UNDEFINED       = 0
    HPF_BYPASS      = 1
    HPF_0_5_HZ      = 2

@unique
class ECG_RATE_t(Enum):
    UNDEFINED       = 0
    RATE_SLOW       = 1
    RATE_NORMAL     = 2
    RATE_FAST       = 3

class BIOZ():
    def __init__(self) -> None:
        self.inductionCurrent = InductionCurrent_t.UNDEFINED
        self.inductionFreq    = InductionFreq_t.UNDEFINED
        self.hpf              = BIOZ_HPF_t.UNDEFINED
        self.lpf              = BIOZ_LPF_t.UNDEFINED
        self.gain             = BIOZ_GAIN_t.UNDEFINED
        self.rate             = BIOZ_RATE_t.UNDEFINED

    def __repr__(self) -> str:
        print("BIOZ")
        print(f"gain: {self.gain}")
        print(f"rate: {self.rate}")
        print(f"lpf: {self.lpf}")
        print(f"hpf: {self.hpf}")
        print(f"freq: {self.inductionFreq}")
        print(f"curr: {self.inductionCurrent}")
        return "Updated"

class ECG():
    def __init__(self) -> None:
        self.gain             = ECG_GAIN_t.UNDEFINED
        self.lpf              = ECG_LPF_t.UNDEFINED
        self.hpf              = ECG_HPF_t.UNDEFINED
        self.rate             = ECG_RATE_t.UNDEFINED

    def __repr__(self):
        print("ECG")
        print(f"gain: {self.gain}")
        print(f"rate: {self.rate}")
        print(f"lpf: {self.lpf}")
        print(f"hpf: {self.hpf}")
        return "Updated"

class max30001():
    def __init__(self):
        self.measurement_type = Measurement_t.UNDEFINED
        self.bioz             = BIOZ()
        self.ecg              = ECG() 

    def __repr__(self) -> str:
        print(self.measurement_type)
        print(self.bioz)
        print(self.ecg)
        return "Updated"
