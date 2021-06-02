# -*- coding: utf-8 -*-
"""Morse-code-translator """

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pdb #for debugging
import sys

# Fast Fourier Transform
def FFT(x):
  # getting the length of the data
  N = len(x)

  # initializing an array with all zeros and of type complex 
  X = np.zeros(N, complex)
  if N <= 1:
      return x                        
  try:
    # recursive manner 
    # compute FFT for even part
    even = FFT(x[0::2])
    # compute FFT for odd part
    odd = FFT(x[1::2])
    # Lambda functions to help in calculation
    lambda1 =lambda a : a/N
    lambda2 = lambda b: b + N // 2 
    # for loop for calculating the FFT
    for i in range(N // 2):
        l1 =  lambda1(i)
        l2 =  lambda2(i)
        
        # W_N
        W_N = np.exp(-2j * np.pi *l1 )
        
        #W_N/2
        W_N_div_2= np.exp(-2j * np.pi * l2/ N)
        
        X[i] = even[i] + odd[i] * W_N  
        X[i + N // 2] = even[i] + odd[i] * W_N_div_2  
   
    return X
  except: 
    # N should be a power of 2
    if N % 2 > 1:
        raise ValueError("x size should be a power of 2")


def decrypt_text(message):
  
    # extra space added at the end to access the
    # last morse code
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
  
        # checks for space
        if (letter != ' '):
  
            # counter to keep track of space
            i = 0
  
            # storing morse code of a single character
            citext += letter
  
        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1
  
            # if i = 2 that indicates a new word
            if i == 2 :
  
                 # adding space to separate words
                decipher += ' '
            else:
  
                # accessing the keys using their values (reverse of encryption)
                decipher += list(morse_code_characters.keys())[list(morse_code_characters.values()).index(citext)]
                citext = ''
  
    return decipher


def decrypt_audio(data,interval, freq_s,end_of_sequence,symbol):
      
  if end_of_sequence:
    return  
  new_char_interval=0
  new_char_freq=0

  d_fft = np.absolute(FFT(data[ interval : freq_s ]).real)
  next_d_fft = np.absolute(FFT(data[interval + 4410  :   freq_s +4410 ]).real)
  

  if len(d_fft) != 0 and np.max(d_fft)> 50:
    if len(next_d_fft)!= 0 and np.max(next_d_fft) > 50 :
      f = np.absolute(FFT(data[interval + 17640  :   freq_s +17640]).real)
      if len(f)==0:
        symbol.append('-')
        end_of_sequence = True
        return 
        
      elif np.max(f) <50:
            
        symbol.append('-')
        symbol.append(' ')
        interval+=13230
        freq_s+=13230
        
        while True:
          
          d = np.absolute(FFT(data[interval   :   freq_s]).real)
          if np.max(d) >50:
                new_char_interval = interval
                new_data = data[new_char_interval:]
                data = new_data    
                interval = 0
                freq_s =4410
                break
          interval +=4410
          freq_s+=4410
        decrypt_audio(data,interval,freq_s,end_of_sequence,symbol)
              

      else:
        symbol.append('-')
        interval += 17640
        freq_s +=17640
        decrypt_audio(data,interval,freq_s,end_of_sequence,symbol)



    elif len(next_d_fft)!= 0 and np.max(next_d_fft) < 50 :
      f = np.absolute(FFT(data[interval + 8820  :   freq_s +8820]).real)
      if len(f)==0:
        symbol.append('.')
        end_of_sequence = True
        return
        
      elif np.max(f) <50:
        New_character= True
        symbol.append('.')
        symbol.append(' ')
        interval+=4410
        freq_s+=4410
        while True:
              d = np.absolute(FFT(data[interval   :   freq_s]).real)
              if np.max(d) >100:
                    new_char_interval = interval
                    new_char_freq = freq_s
                    new_data = data[new_char_interval:]  
                    interval = 0
                    freq_s =4410
                    decrypt_audio(new_data,interval,freq_s,end_of_sequence,symbol)
                    break
              interval +=4410
              freq_s+=4410

      else:
        symbol.append('.')
        interval +=8820
        freq_s+=8820
        decrypt_audio(data,interval,freq_s,end_of_sequence,symbol)

# Dictionary representing the morse code chart
morse_code_characters = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

# audio file as an input
audiofile = sys.argv[1]

#audio read and extract data and sample rate
fs, data = wavfile.read(audiofile)


plt.figure(figsize=(15,5))
plt.plot(data)
plt.show()
# sample period
sample_period = 0.1

freq_s = int(sample_period * fs)
interval = 0
symbol= []
end_of_sequence = False
decrypt_audio( data , interval , freq_s , end_of_sequence, symbol )
#print(symbol)

characters = decrypt_text(symbol)
print(characters)