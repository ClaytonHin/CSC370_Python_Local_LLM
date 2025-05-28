#import the libraries needed for this project
#scrolledtext is a feature within the tkinter library
from tkinter import scrolledtext
#This is the library that allows for "Conversation" with the llama LLM
from llama_cpp import Llama
#Import for a open source TKinter library "Update/Modernization"
import customtkinter
#Set the default appearance to be based on the current system settings
customtkinter.set_appearance_mode("System")

#Initialize the LLM class
llm = Llama(
    #Give the file path for the downloaded LLM
    model_path="Dolphin3.0-Llama3.1-8B_Q5_K_M.gguf",
    #Define the maximum number of input and output tokens for the model
    n_ctx=2048,
    #Maxmimum batch size for prompt processing
    n_batch = 1024,
    #Physical batch size for prompt processing
    n_ubatch = 1024,
    #Temperature defines the randomness of the LLM response
    temperature = 0.4,
    #Number of GPU layers the model can use to generate responses, -1 allocates for all layers on the GPU
    n_gpu_layers=-1,
    #Let the model produce debug/extra text of what is happening
    verbose=True
)

#Create the main window
root = customtkinter.CTk()
#Give the window created above a title
root.title("Custom LLM Assistant in Python")
#Define the size of the window
root.geometry("720x480")

#Make a function that will get input from the user, and then get the response from the LLM based on the user's prompt
def send_message():
    #Get the users message
    user_input = entry.get()
    #Ensure that the message send was not empty
    if not user_input.strip():
        return
    #Clear the message input field/message window
    entry.delete(0, customtkinter.END)
    #Add the user's input message to the Message Box, So the user can see the history of the current conversation
    chat_display.insert(customtkinter.END, f"User: {user_input} \n\n")
    #Generate a response from the LLM based on the user's input and store it in the response variable to be printed out
    response = llm(
        f"User: {user_input}\nAssistant: \n",
        #Define the max amout of tokens the model can output
        max_tokens=1024,
        stop = ["User:"],
        #Stop the program from echoing the users input into the message window
        echo = False
    )
    #Add the LLM's response to the message window
    chat_display.insert(customtkinter.END, f"Assistant: \n{response['choices'][0]['text']}\n\n")
    #Automatically scroll down to the bottom of the message window, After the LLM has responded
    chat_display.see(customtkinter.END)

#Create a function to clean up the resources when the window is closed
def on_closing():
    #Destroy the Tkinter window, and all of it's included components
    root.destroy()

#Create the grid layout 
root.grid_columnconfigure(0, weight=1) #User Input field 
root.grid_columnconfigure(1, weight=0) #Send Button
root.grid_columnconfigure(2, weight=0) #Exit Button
root.grid_rowconfigure(0, weight=1) #Chat Display Row
root.grid_rowconfigure(1, weight=0) #Input and buttons row 

#Create a label to clearly define the chat_display box to the user
chat_label = customtkinter.CTkLabel(root, text="\tChat History: ",fg_color="transparent", anchor="center")
#Place the label above the chat_display box in our grid
chat_label.grid(row=0, column=0, sticky="sw")

#Create scrolled text widget to show the chat history
chat_display = scrolledtext.ScrolledText(root, wrap=customtkinter.WORD, height=20)
#Change the background color of the chat display
chat_display.configure(bg="lightgrey")
#Place the scrolled text widget within the grid system
chat_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

#Create a label for the input box, to be more clear to direct the user more clearly
entry_label = customtkinter.CTkLabel(root, text="Input: ", fg_color="transparent", anchor="center")
#Place the label above the input box
entry_label.grid(row=2, column=0, sticky="nsew")

#Create a entry field to obtain user input
entry = customtkinter.CTkEntry(root, bg_color="lightgrey")
#Place the entry component on the grid system
entry.grid(row=3, column=0, padx=(10, 5), pady=10, sticky="ew")

#Create the send button
send_button = customtkinter.CTkButton(root, text="Send", command=send_message, fg_color="blue")
#Place the send button component on the grid system
send_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

#Create the exit button
exit_button = customtkinter.CTkButton(root, text="Exit", command=on_closing, fg_color="green")
#Place the exit button component on the grid system
exit_button.grid(row=3, column=2, padx=(5, 10), pady=5, sticky="ew")

#Create a bind that will allow the enter key on a keyboard to call the send_message function
root.bind('<Return>', lambda e: send_message())
#Register the closing event, which delete the main window when it is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

#Start the main loop
root.mainloop()

#Cleanup the rest of the resources
print("Cleaning up Resources...")
#Remove the LLM from computer memory
del llm
#Display that this has been cleaned up!
print("All finished, Resources are now free!")
