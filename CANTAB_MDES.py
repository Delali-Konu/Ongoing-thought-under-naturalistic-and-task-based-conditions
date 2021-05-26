#Written by Brontë McKeown and Theodoros Karapanagiotidis
from psychopy import visual 
from psychopy import gui, data, core,event
import csv
import time
from time import localtime, strftime, gmtime
from datetime import datetime
import os.path
import pyglet 
import pandas as pd
from itertools import groupby

# kill switch for Psychopy3
event.globalKeys.clear() # clear global keys 
esc_key= 'escape' # create global key for escape
# define function to quit programme
def quit():
    print ('User exited')
    win.close()
    core.quit()
# call globalKeys so that whenever user presses escape, quit function called
event.globalKeys.add(key=esc_key, func=quit)

# user should set cwd to the experiment directory.
os.chdir('R:\\Task_SGT\\cantab')
# user should set directory for output files to be stored. 
save_path= 'R:\\Task_SGT\\cantab\\output\\cantab_ESQ'

# user can update instructions for task here if required.
instructions = """You will now be asked to rate several statements about the ongoing thoughts you experienced during the last task block. 
\nTo rate these statements, hold 1 to move the marker left along the slider and hold 2 to move the marker right along the slider. When you are happy with your selection, please press 4 to move on to the next statement. 
\nPress enter to begin."""

# user can edit headers for output csv file here. 
fieldnames = ['Participant_number','task','Questionnaire_startTime','Questionnaire_endTime', 'TrialDuration','Focus','Future','Past','Self','Other','Emotion','Modality','Detailed','Deliberate','Problem','Diversity','Intrusive','Source', 'Arousal', 'Tense','Uncertainty'] 

# create a dictionary to store information from the dialogue box.
inputbox = {'expdate': datetime.now().strftime('%Y%m%d_%H%M'),'part_number':'','taskOrder':['a','b']}
# create dialogue box.
# user enters participant number + task order.
dlg=gui.DlgFromDict(inputbox, title = 'Input participation info',
                  	fixed='expdate',
                  	order=['expdate', 'part_number','taskOrder'])

# if the user doesn't press ok, the programme will quit and inform user.
if not dlg.OK:
	print ("User exited")
	core.quit()

def thought_probes (task, participant_number,last=0):
    """Presents thought probes, stores responses and presents break screens and end screen if it is the last trial"""

    # use trialhandler to present task, arousal and uncertainty questions from csv file in sequential order. 
    fixedQuestions = data.TrialHandler(nReps = 1, method = 'sequential', trialList = data.importConditions('references/fixedQuestions.csv'), name = 'fixedQuestions')

    # use trialhandler to present the remaining thought probes from csv file in random order. 
    Questionnaire = data.TrialHandler(nReps = 1, method = 'random', trialList = data.importConditions('references/questions.csv'), name = 'Questionnaire')

    # create rating scale for user to rate thought probes.
    ratingScale = visual.RatingScale(win, low=0, high=10, markerStart=5.0,
                precision=10,
                leftKeys='1', rightKeys='2', acceptKeys='4', scale = None, labels = None, acceptPreText = 'Press key', tickMarks = [1,10])

    # create text stimulus for thought probe presentation. 
    QuestionText = visual.TextStim(win, color = [-1,-1,-1], alignHoriz = 'center', alignVert= 'top', pos =(0.0, 0.3))
    # create text stimuli for low and high scale responses. 
    Scale_low = visual.TextStim(win, pos= (-0.5,-0.5), color ='black')
    Scale_high = visual.TextStim(win, pos =(0.6, -0.5), color ='black')

    # make thisRunDict global so that it can be accessed outside of function to write to outputfile. 
    global thisRunDict 
    # store participant number and task condition in thisRunDict to write to outputfile.  
    thisRunDict= {'Participant_number': str(participant_number),'task': task}

    # loop through each thought probe in the fixedQuestions created above using trialhandler.
    for question in fixedQuestions:
        ratingScale.noResponse = True

        # section for keyboard handling. 
        key = pyglet.window.key
        keyState = key.KeyStateHandler()
        win.winHandle.activate() # to resolve mouse click issue. 
        win.winHandle.push_handlers(keyState)
        pos = ratingScale.markerStart
        inc = 0.1 

        # while there is no response from user, present thought probe and scale.
        while ratingScale.noResponse:

            # use 1 and 2 keys to move left and right along scale. 
            if keyState[key._1] is True:
                pos -= inc
            elif keyState[key._2] is True:
                pos += inc
            if pos > 10: 
                pos = 10
            elif pos < 1:
                pos = 1
            ratingScale.setMarkerPos(pos)

            # set text of probe and responses 
            QuestionText.setText(question['Questions'])
            Scale_low.setText(question['Scale_low'])
            Scale_high.setText(question['Scale_high'])

            # draw text stimuli and rating scale
            QuestionText.draw()
            ratingScale.draw() 
            Scale_low.draw()
            Scale_high.draw()

            # store response using getRating function
            responded = ratingScale.getRating()
            win.flip()

        # reset marker to middle of scale each time probe is presented. 
        ratingScale.setMarkerPos((0.5))
        
        # for each probe, store probe label and response in thisRunDict. 
        thisRunDict[ str(question['Label'] )] = str(responded)


    # loop through each thought probe in the Questionnaire created above using trialhandler.
    for question in Questionnaire:
        ratingScale.noResponse = True

        # section for keyboard handling. 
        key = pyglet.window.key
        keyState = key.KeyStateHandler()
        win.winHandle.activate() # to resolve mouse click issue. 
        win.winHandle.push_handlers(keyState)
        pos = ratingScale.markerStart
        inc = 0.1 

        # while there is no response from user, present thought probe and scale.
        while ratingScale.noResponse:

            # use 1 and 2 keys to move left and right along scale. 
            if keyState[key._1] is True:
                pos -= inc
            elif keyState[key._2] is True:
                pos += inc
            if pos > 10: 
                pos = 10
            elif pos < 1:
                pos = 1
            ratingScale.setMarkerPos(pos)

            # set text of probe and responses 
            QuestionText.setText(question['Questions'])
            Scale_low.setText(question['Scale_low'])
            Scale_high.setText(question['Scale_high'])

            # draw text stimuli and rating scale.
            QuestionText.draw()
            ratingScale.draw() 
            Scale_low.draw()
            Scale_high.draw()

            # store response using getRating function.
            responded = ratingScale.getRating()
            win.flip()

        # reset marker to middle of scale each time probe is presented. 
        ratingScale.setMarkerPos((0.5))

        # for each probe, store probe label and response in thisRunDict. 
        thisRunDict[ str(question['Label'] )] = str(responded)

    # create text stimuli to be updated for breaks and end screen. 
    stim = visual.TextStim(win, "", color = [-1,-1,-1], wrapWidth = 1300, units = "pix", height=40)
    
        # present break screen at the end of each set of questions.
    if last==0:
        print ('break')
        stim.setText("""You have reached the end of the questions for this task block.
        \nPlease perform the next task block on the iPad. Return to the computer and press "Enter" when you see the "Next" button on the iPad""")
        stim.draw()
        win.flip()
        # Wait for user to press Return to continue. 
        key = event.waitKeys(keyList=(['return']), timeStamped = True)

    else:
        print ('end')
        # present end screen at the end of task. 
        stim.setText("""You have reached the end of the task. 
        \nPlease let the experimenter know you have finished. 
        \nThank you for your participation.""")
        stim.draw()
        win.flip()
        # wait for user to press escape to exit experiment. 
        key = event.waitKeys(keyList=(['return']), timeStamped = True)


# store participant number, task order and experiment date provided by user in input box as variables for later use. 
part_number = inputbox['part_number']
taskOrder = inputbox['taskOrder']
expdate = inputbox['expdate']

# create filename based on user input. 
filename = '{}_{}_{}_{}.csv'.format(part_number, expdate,taskOrder,'cantab')
# update filename to include absolute path so that it is stored in output directory. 
completeName = os.path.join(save_path, filename)
# open file for writing. 
outputfile = open(completeName, "w", newline = '')

# create variable which calls DictWriter to write to outputfile and specifies fieldnames.
writer = csv.DictWriter(outputfile, fieldnames)
# writes headers using fieldnames as specified above when creating writer variable.
writer.writeheader()

# use trialhandler to sequentially present films listed in filmlist csv file. 
cantabDict = data.TrialHandler(nReps = 1, method = 'sequential', trialList = data.importConditions('references/cantab_list.csv'), name = 'cantabList') 

# create white window for stimuli to be presented on throughout task. 
win = visual.Window(size=[1024, 768], color=[1,1,1,], monitor="testMonitor", fullscr= True, allowGUI = False)
# create text stimuli to be updated for start screen instructions.
stim = visual.TextStim(win, "", color = [-1,-1,-1], wrapWidth = 1300, units = "pix", height=40)

# update text stim to include instructions for task. 
stim.setText(instructions)
stim.draw()
win.flip()
# Wait for user to press 1 to continue. 
key = event.waitKeys(keyList=(['return']), timeStamped = True)

# start a clock right before the experiment starts
tasktime = core.Clock()
tasktime.reset()

for task in cantabDict:
    qstart = tasktime.getTime()
    
    # If statement to either present break screen or end screen
    nextTrial = cantabDict.getFutureTrial(n=1) # fixes error for end screen 
    if nextTrial is None or nextTrial[taskOrder] == None:
        # when the task has ended, call thought_probes function to present probes and rating scale
        thought_probes(task[taskOrder], part_number,1) 
    else:
        thought_probes(task[taskOrder], part_number)

    # store when the questions end to later store in outputfile, this qEnd uses clock created at start of experiment. 
    qEnd = tasktime.getTime()

    # calculate trial duration to store in outputfile. 
    trial_duration = (qEnd-qstart)

    # add timings to global thisRunDict to write to outputfile below.
    thisRunDict['Questionnaire_startTime']= str(qstart)
    thisRunDict['Questionnaire_endTime']= str(qEnd)
    thisRunDict['TrialDuration']= str(trial_duration)

    # write responses and timings stored in thisRunDict to outputfile. 
    writer.writerows([thisRunDict])
    outputfile.flush()