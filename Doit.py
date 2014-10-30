'''
Created on Oct 13, 2014

@author: joro
'''
import os
from MakamScore import MakamScore
import glob
import numpy
import sys
from Decoder import Decoder
from LyricsWithModels import LyricsWithModels

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
pathUtils = os.path.join(parentDir, 'utilsLyrics')
sys.path.append(pathUtils )

pathHtk2Sp = os.path.join(parentDir, 'htk2s3')
pathHMM = os.path.join(parentDir, 'HMM')

sys.path.append(pathHtk2Sp)
sys.path.append(pathHMM)


from hmm.continuous.GMHMM  import GMHMM
from htk_converter import HtkConverter
from Utilz import writeListOfListToTextFile, writeListToTextFile,\
    getMeanAndStDevError

pathEvaluation = os.path.join(parentDir, 'Evaluation')
sys.path.append(pathEvaluation)
from WordLevelEvaluator import _evalAlignmentError

# sys.path.append('/Users/joro/Downloads/python-matlab-bridge-master')
# from pymatbridge import Matlab

numpy.set_printoptions(threshold='nan')

PATH_TO_HMMLIST='/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/'

HMMLIST_NAME = 'monophones0'

MODEL_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'

HMM_LIST_URI =  os.path.join(PATH_TO_HMMLIST + HMMLIST_NAME)

     


def loadLyrics(pathToComposition, whichSection):


#     expand phoneme list from transcript
    os.chdir(pathToComposition)
    pathTotxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
    pathToSectionTsv =  os.path.join(pathToComposition, glob.glob("*.tsv")[0])
    makamScore = MakamScore(pathTotxt, pathToSectionTsv )
        
    # phoneme IDs
    lyrics = makamScore.getLyricsForSection(whichSection)
    return lyrics
    


     

def loadMFCCsWithMatlab(URI_recording_noExt):
    print 'calling matlab'
#     mlab = Matlab(matlab='/Applications/MATLAB_R2009b.app/bin/matlab')
#     mlab.start()
#     res = mlab.run_func('/Users/joro/Documents/Phd/UPF/voxforge/myScripts/lyrics_magic/matlab_htk/writeMFC.m', {'filename':URI_recording_noExt})
#     print res['result']
#     mlab.stop()

def loadMFCCs(URI_recording_noExt): 
    '''
    for now lead extracted with HTK, read in matlab and seriqlized to txt file
    '''
    URI_recording_mfc_txt = URI_recording_noExt + '.mfc_txt'
    
    if not os.path.exists(URI_recording_mfc_txt):
#       loadMFCCsWithMatlab(URI_recording_noExt)
        print 'not impl'
    
    mfccsFeatrues = numpy.loadtxt(URI_recording_mfc_txt , delimiter=','  ) 
    
    return mfccsFeatrues 

def decodeAudio( URIrecording, decoder):
    
    
    observationFeatures = loadMFCCs(URIrecording) #     observationFeatures = observationFeatures[0:1000]
    path, psi, delta = decoder.decodeAudio(observationFeatures)
    writeListToTextFile(path, None, '/Users/joro/Downloads/path.test')
    detectedWordList = decoder.path2ResultWordList()
   
    return detectedWordList



def main(argv):
    
    if len(argv) != 4:
            print ("usage: {}  <pathToComposition> <whichSection> <URI_recording_no_ext>".format(argv[0]) )
            sys.exit();
    
    
    URIrecording = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/ISTANBUL/goekhan/02_Gel_3_zemin'
    URIrecording = argv[3]
    observationFeatures = loadMFCCs(URIrecording) #     observationFeatures = observationFeatures[0:1000]

            
    pathToComposition = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/nihavent--sarki--aksak--gel_guzelim--faiz_kapanci/'
    pathToComposition = argv[1]
    
    whichSection = 3
    whichSection = int(argv[2])
    
     

    lyrics = loadLyrics(pathToComposition, whichSection)
    
    lyricsWithModels = LyricsWithModels(lyrics.listWords, MODEL_URI, HMM_LIST_URI )
#     lyricsWithModels.printPhonemeNetwork()
    
    decoder = Decoder(lyricsWithModels)
    
    #################### decode
    
    detectedWordList = decodeAudio(URIrecording, decoder)
    
    alignmentErrors = _evalAlignmentError(URIrecording + '.TextGrid', detectedWordList, 1)
        
    mean, stDev, median = getMeanAndStDevError(alignmentErrors)
        
#         print "mean : ", mean, "st dev: " , stDev
    print "(", mean, ",", stDev, ")"   

if __name__ == '__main__':
    main(sys.argv)
