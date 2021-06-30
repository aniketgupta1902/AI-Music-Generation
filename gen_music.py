#!/usr/bin/env python
# coding: utf-8

# In[5]:


from music21 import converter, instrument, note, chord, stream
import glob
import pickle
import numpy as np
from keras.utils import np_utils



# In[7]:


with open('notes', 'rb')  as f:
    notes = pickle.load(f)


# In[8]:


n_vocab = len(set(notes))




# In[10]:


#How many elements LSTM input should consider
sequence_length = 100


# In[11]:


pitchnames = sorted(set(notes))


# In[12]:


#Mapping bw elements to integer value
ele_to_int = dict((ele,num) for num, ele in enumerate(pitchnames))


# In[13]:


from keras.models import Sequential, load_model
from keras.layers import *
from keras.callbacks import ModelCheckpoint, EarlyStopping


# In[14]:


model = load_model('model.hdf5')


# In[16]:


network_input = []
for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i+sequence_length] #Contains 100 values
    network_input.append([ele_to_int[c] for c in seq_in])


# In[17]:


start = np.random.randint(len(network_input) - 1)

#Mapping int_to_ele
int_to_ele = dict((num, ele) for num, ele in enumerate(pitchnames))

#Initial Pattern
pattern = network_input[start]
prediction_output = []

#generate 200 elements
for note_index in range(200):
    prediction_input= np.reshape(pattern, (1,len(pattern), 1))
    prediction_input = prediction_input/float(n_vocab)

    prediction = model.predict(prediction_input, verbose=0)

    idx = np.argmax(prediction)
    result = int_to_ele[idx]
    prediction_output.append(result)

    pattern.append(idx)
    pattern = pattern[1:]


# In[19]:


# ## Create Midi File

# In[27]:


offset = 0 #Time
output_notes = []

for pattern in prediction_output:
    #If pattern is a chord
    
    if ('+' in pattern) or pattern.isdigit():
        notes_in_chord = pattern.split('+')
        temp_notes = []
        for current_note in notes_in_chord:
            new_note = note.Note(int(current_note)) #Create Note object for each note in the chord
            new_note.storedInstrument = instrument.Piano()
            temp_notes.append(new_note)
            
        new_chord = chord.Chord(temp_notes) #Creates the chord object
        new_chord.offset = offset
        output_notes.append(new_chord)
        
    #If pattern is a note
    else:
        new_note = note.Note(pattern)
        new_note.offset = offset
        new_note.storedInstrument = instrument.Piano()
        output_notes.append(new_note)
    
    offset += 0.5


# In[29]:
#Create a stream object from the generated notes
def generate_new():
    start = np.random.randint(len(network_input) - 1)

#Mapping int_to_ele
    int_to_ele = dict((num, ele) for num, ele in enumerate(pitchnames))

    #Initial Pattern
    pattern = network_input[start]
    prediction_output = []

    #generate 200 elements
    for note_index in range(200):
        prediction_input= np.reshape(pattern, (1,len(pattern), 1))
        prediction_input = prediction_input/float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        idx = np.argmax(prediction)
        result = int_to_ele[idx]
        prediction_output.append(result)

        pattern.append(idx)
        pattern = pattern[1:]
        
    offset = 0 #Time
    output_notes = []

    for pattern in prediction_output:
        #If pattern is a chord

        if ('+' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('+')
            temp_notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note)) #Create Note object for each note in the chord
                new_note.storedInstrument = instrument.Piano()
                temp_notes.append(new_note)

            new_chord = chord.Chord(temp_notes) #Creates the chord object
            new_chord.offset = offset
            output_notes.append(new_chord)

        #If pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp = 'static/test_output.mid')


# In[ ]:




