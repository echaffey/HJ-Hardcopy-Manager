import re

def parse_pdf(text):
    print('in')
    text_list = text.split('\n')

    #Remove excess empty string values
    while ('' in text_list):
        text_list.remove('')

    #Find the 'P&O' numbers
    PO_pos = text_list.index('P&O:')
    if PO_pos >= 0:
        PO_num = text_list[PO_pos + 1].strip()
        
    #Error checking to make sure we're getting the right value.
    #This needs to be updated later
    state = ''
    state_pos = text_list.index('STATE:')
    if state_pos >= 0:
        #Because reading is different on different computers
        #this checks all values +/- 5 items around where 'STATE:' was found
        for s in range(state_pos - 5, state_pos + 5):
            if text_list[s].strip() in states:
                state = text_list[s].strip()
                exit

    return PO_num, state
