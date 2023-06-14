# Open the file in write mode
with open('dummy.txt', 'w') as file:
    # Write dummy data to the file
    file.write('This is line 1.\n')
    file.write('This is line 2.\n')
    file.write('This is line 3.\n')

print('Dummy data has been written to the file.')
