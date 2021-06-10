import os
import matplotlib.pyplot as plt
import numpy as np

txt_path = './analysis_result.txt'


def main():
    DRUM = 0
    PIANO = 0
    CHROMATIC_PERCUSSION = 0
    ORGAN = 0
    GUITAR = 0
    BASS = 0
    STRINGS = 0
    ENSEMBLE = 0
    BRASS = 0
    REED = 0
    PIPE = 0
    SYNTH_LEAD = 0
    SYNTH_PAD = 0
    SYNTH_EFFECTS = 0
    ETHNIC = 0
    PERCUSSIVE = 0
    SOUND_EFFECTS = 0
    i = 0 #line number

    f = open("analysis_result.txt", 'r')
    while 1:
        myline = f.readline()
        i+=1

        if not myline:
            break

        # line should start with 'Instrument'
        if myline[0:10] != 'Instrument':
            print("line :{} error!".format(i))
            continue
        
        my_list = myline.split(" ")
        # if is_drum == True
        if my_list[1][8:9] == 'T':
            # print("IS DRUM\n")
            DRUM+=1
        else:
            program_number = int(my_list[0][19:-1])
            if program_number//8 == 0:
                PIANO+=1
            elif program_number//8 == 1:
                CHROMATIC_PERCUSSION+=1
            elif program_number//8 == 2:
                ORGAN+=1
            elif program_number//8 == 3:
                GUITAR+=1
            elif program_number//8 == 4:
                BASS+=1
            elif program_number//8 == 5:
                STRINGS+=1
            elif program_number//8 == 6:
                ENSEMBLE+=1
            elif program_number//8 == 7:
                BRASS+=1
            elif program_number//8 == 8:
                REED+=1
            elif program_number//8 == 9:
                PIPE+=1
            elif program_number//8 == 10:
                SYNTH_LEAD+=1
            elif program_number//8 == 11:
                SYNTH_PAD+=1
            elif program_number//8 == 12:
                SYNTH_EFFECTS+=1
            elif program_number//8 == 13:
                ETHNIC+=1
            elif program_number//8 == 14:
                PERCUSSIVE+=1
            elif program_number//8 == 15:
                SOUND_EFFECTS+=1
            else:
                # non matched.. never reached?
                print("Nothing matched!!\n")

    
    #make it into dict
    instrument = {}
    instrument['Drum'] = DRUM
    instrument['Piano'] = PIANO
    instrument['Chromatic_percussion'] = CHROMATIC_PERCUSSION
    instrument['Organ'] = ORGAN
    instrument['Guitar'] = GUITAR
    instrument['Bass'] = BASS
    instrument['Strings'] = STRINGS
    instrument['Ensemble'] = ENSEMBLE
    instrument['Brass'] = BRASS
    instrument['Reed'] = REED
    instrument['Pipe'] = PIPE
    instrument['Synth_lead'] = SYNTH_LEAD
    instrument['Synth_pad'] = SYNTH_PAD
    instrument['Synth_effects'] = SYNTH_EFFECTS
    instrument['Ethnic'] = ETHNIC
    instrument['Percussive'] = PERCUSSIVE
    instrument['Sound_effects'] = SOUND_EFFECTS


    print(instrument)
    #not sure is this plot working...?
    plt.bar(list(instrument.keys()), instrument.values(), color='g')
    plt.show()


if __name__ == "__main__":
    main()