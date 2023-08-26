import pyautogui
import cv2
import pytesseract
from PIL import ImageTk, Image
from deep_translator import GoogleTranslator
import numpy as np
import tkinter as tk

def select_area():
    # Create an empty list to store the coordinates of the selected area
    coordinates = []

    # Mouse callback function to handle the selection of area
    def mouse_callback(event, x, y, flags, param):
        nonlocal coordinates

        if event == cv2.EVENT_LBUTTONDOWN:
            # Add the coordinates of the clicked point to the list
            coordinates.append((x, y))

            # Draw a circle to mark the clicked point on the image
            cv2.circle(screenshot, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select Area", screenshot)

    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Create a window to display the screenshot and select the area
    cv2.namedWindow("Select Area")
    cv2.setMouseCallback("Select Area", mouse_callback)

    while True:
        # Display the screenshot with the selected points
        cv2.imshow("Select Area", screenshot)

        # Check if the user pressed the 'Enter' key
        if cv2.waitKey(1) == 13:  # 13 is the ASCII code for 'Enter' key
            break

    # Close the window
    cv2.destroyAllWindows()

    # Check if the user selected at least two points
    if len(coordinates) < 2:
        print("Area selection canceled.")
        return

    # Extract the top-left and bottom-right coordinates of the selected area
    start_x, start_y = coordinates[0]
    end_x, end_y = coordinates[-1]

    # Crop the selected area from the screenshot
    selected_area = screenshot[start_y:end_y, start_x:end_x]

    # Save the selected area as an image file
    cv2.imwrite("selected_area.png", selected_area)

    # Perform OCR on the selected area to extract the text
    extracted_text = pytesseract.image_to_string(selected_area, lang="deu")

    # Preprocess the extracted text
    lines = extracted_text.strip().split("\n")
    print(lines)

    preprocessed_text = " ".join(lines)
    print(preprocessed_text)

    # Create the GUI window
    window = tk.Tk()
    window.title("Image Translation")


    # Create a label to display the selected image
    image_label = tk.Label(window)
    image_label.pack()

    # Display the selected image in the label
    selected_image = cv2.cvtColor(selected_area, cv2.COLOR_BGR2RGB)
    selected_image = Image.fromarray(selected_image)


    image = ImageTk.PhotoImage(selected_image)
    image_label.configure(image=image)
    image_label.image = image

    # Create a label and text box for the extracted text
    text_label = tk.Label(window, text="Extracted Text:")
    text_label.pack()

    text_box = tk.Text(window, height=20, width=40)
    text_box.insert(tk.END, preprocessed_text)
    text_box.pack()

    # Function to translate the text
    def translate_text():
        text = text_box.get("1.0", tk.END).strip()
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        translated_text_box.delete("1.0", tk.END)
        translated_text_box.insert(tk.END, translated_text)

    # Create a button to translate the text
    translate_button = tk.Button(window, text="Translate", command=translate_text)
    translate_button.pack()

    # Create a label and text box for the translated text
    translated_label = tk.Label(window, text="Translated Text:")
    translated_label.pack()

    translated_text_box = tk.Text(window, height=20, width=40)
    translated_text_box.pack()

    # Pack the window to automatically adjust its size


    # Start the Tkinter event loop
    window.mainloop()

# Call the function to select the area and perform text translation
select_area()
