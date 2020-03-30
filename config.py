import os

#Output folder for parsed PDFs. 
if os.path.exists(os.path.join('F:', 'USERS', 'PUBLIC', 'Hardcopy Storage', 'CSR Hardcopies')):
    SAVE_FOLDER = os.path.join('F:', 'USERS', 'PUBLIC', 'Hardcopy Storage', 'CSR Hardcopies') #r'F:\\USERS\\PUBLIC\\Hardcopy Storage\\CSR Hardcopies'
elif os.path.exists(os.path.join('F:', 'PUBLIC', 'Hardcopy Storage', 'CSR Hardcopies')):
    SAVE_FOLDER = os.path.join('F:', 'PUBLIC', 'Hardcopy Storage', 'CSR Hardcopies')
else:
    print('--ERROR FINDING OUTPUT FOLDER--')

print(SAVE_FOLDER)
#Flask session key.
SECRET_KEY = r'3a64f0f7203e1b00167826e9'