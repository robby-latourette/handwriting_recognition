import tkinter as tk
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from skimage import io
from skimage import transform
from skimage.color import rgb2gray
from sklearn.ensemble import RandomForestClassifier

# Websites with info about Tkinter:
#  https://tkdocs.com/tutorial/widgets.html
#  https://tkdocs.com/tutorial/grid.html
#  https://www.askpython.com/python-modules/tkinter/python-tkinter-grid-example


################################################################################
#                         INITIALIZE DRAWING CONSTANTS                         #
################################################################################

# The user will be drawing on canvas but we can't just dump the pixels.
# Instead, we must either use platform-dependent code to take a screenshot or
# come up with some alternative. Our alternative is that we will generate an
# internal 2D array of pixels at the same time as we are drawing them.
black_pixel = np.full((1, 3), 0, dtype=np.uint8)
white_pixel = np.full((1, 3), 255, dtype=np.uint8)
test_sample = np.full((140, 140, 3), black_pixel, dtype=np.uint8)


################################################################################
#                           BUTTON HANDLERS FOR GUI                            #
################################################################################

def clear_drawing():
    ''' Clears the drawing canvas and internal array. '''

    cvs_drawspace.delete('all')  # drawing canvas
    lbl_result.config(text = "")
    test_sample[:] = black_pixel # internal representation of drawing

def draw_handwriting(event):
    ''' Draws on the canvas and internal array based on mouse coordinates. '''

    # xy-coordinates and radius of the circle being drawn
    x = event.x
    y = event.y
    r = 2
    cvs_drawspace.create_oval(x - r, y - r, x + r+1, y + r+1, fill='black')
    test_sample[y-2:y+3,x-2:x+3] = white_pixel

def classify_number():
    test_num = format_number()
    print(test_num)
    df = pd.read_csv('mnist_train.csv')
    df = df.astype(np.float32) / 255
    df = df.round()
    y = df['label']
    X = df.drop('label', axis='columns')
    rfor = RandomForestClassifier(n_estimators=600, criterion='entropy', random_state=20)
    rfor.fit(X, y)
    rfor_y_pred = rfor.predict(test_num)


def format_number():
    #print(test_sample)
    #print(len(test_sample))
    
    newTest = transform.resize(test_sample, output_shape=(28, 28))
    
    for x in newTest:
        for y in range(len(x)):
            x[y] = x[y] * 255

    newTest = newTest.astype(int)
    temp = []

    for x in newTest:
        for y in x:
            temp.append(y)

    columnNames = []
    for x in range(784):
        columnNames.append("pixel" + str(x))


    df = pd.DataFrame(temp)
    cols = [1,2]
    df = df.drop(df.columns[cols], axis=1)
    df = df.swapaxes("index", "columns")
    df = df.astype(np.float32) / 255
    df = df.round()
    df.columns = columnNames
    return df
    



################################################################################
#                                 DRAW THE GUI                                 #
################################################################################

# Create a GUI window with a certain size and title
window = tk.Tk()
window.geometry("350x450")
window.wm_title('Handwriting Project')

# Create all the buttons and stuff. Each column will be as wide as it's
# widest widget. So we make some artifically wide widgets.
lbl_title = tk.Label(text=f'Handwritten Digit Classifier')
lbl_result = tk.Label(text=f'')

# This drawing canvas will be very important for our ML model
rfc_accuracy = tk.Label(text= "Random Forest Accuracy = asl;dk h;lahbv;las") #fill in later
cvs_drawspace = tk.Canvas(width=140, height=140, bg='white', cursor='tcross',
                          highlightthickness=1, highlightbackground='steelblue')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#IMPortant
btn_classify = tk.Button(window, text='Classify Number', command=classify_number)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
btn_clear = tk.Button(window, text='Reset Everything', command=clear_drawing)

# The grid layout makes sense but is a bit tedious
lbl_title.grid(row=0, column=0, columnspan=5, pady=5, padx=25)

rfc_accuracy.grid(row=2, column=2, pady=5)
cvs_drawspace.grid(row=3, column=2, pady=5)
btn_classify.grid(row=4, column=2, pady=5)
lbl_result.grid(row=5, column=2, pady=5)
btn_clear.grid(row=6, column=2, pady=5)


cvs_drawspace.bind('<B1-Motion>', draw_handwriting)
cvs_drawspace.bind('<Button-1>', draw_handwriting)

default_background_color = lbl_title.cget('background')

window.resizable(False, False)
window.mainloop()
