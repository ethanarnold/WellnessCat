import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

class Pet():
   def __init__(self):
       # Initialize the Tkinter window
       self.window = tk.Tk()

       # Load frames for the left, right and laying movement of the cat
       self.moveleft = [tk.PhotoImage(file='cat5_walkLeft.gif', format='gif -index %i' % i) for i in range(8)]
       self.moveright = [tk.PhotoImage(file='cat5_walkRight.gif', format='gif -index %i' % i) for i in range(8)]
       self.sleepAnimation = [tk.PhotoImage(file='cat5_sleeping.gif', format='gif -index %i' % i) for i in range(8)]

       # Initialize variables for frame index, current image, and timestamp
       self.frame_index = 0
       self.img = self.moveleft[self.frame_index]
       self.timestamp = time.time()
       self.is_stopped = False
       self.stop_duration = 2  # Stop duration in seconds
       self.options_window = None  # Keep track of the options window

       # Set up the window settings
       self.window.config(background='black')
       self.window.wm_attributes('-transparentcolor', 'black')
       self.window.overrideredirect(True)
       self.window.attributes('-topmost', True)


       # Create a label to display the pet image
       self.label = tk.Label(self.window, bd=0, bg='black')


       # Set initial position/display label, you can change these coordinates depending on your computer
       self.x = 1040
       self.y = 590
       self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
       self.label.configure(image=self.img, bg='black')  # Set label background color
       self.label.pack()


       # Set initial direction/start the update loop
       self.dir = -6
       self.window.bind('<Button-1>', self.stop_animation)
       self.window.after(0, self.update)
       self.is_stopped = False
       self.colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']  # Rainbow colors
       self.color_index = 0
       self.window.after(20000, self.display_message) #change the time when actually using, set to several seconds now for convenience
       self.window.after(10000, self.posture_reminder) #different start from the other dialogue box to prevent overlapping 
       self.window.mainloop()
    
   def display_message(self):
        if not self.is_stopped:
            message_window = tk.Toplevel(self.window)
            message_window.geometry('325x100+{}+{}'.format(str(self.x + 50), str(self.y - 100)))
            message_window.title('ATTENTION')
            message = "DRINK WATER NOW!"
            for i, char in enumerate(message):
                label = tk.Label(message_window, text=char, font=("Comic Sans MS", 12), fg=self.colors[i % len(self.colors)])
                label.pack(side=tk.LEFT, padx=2)
            
        if not self.is_stopped:
            self.window.after(20000, self.display_message) #change the time when actually using, set to several seconds now for convenience
   
   def posture_reminder(self):
        if not self.is_stopped:
            message_window = tk.Toplevel(self.window)
            message_window.geometry('150x75+{}+{}'.format(str(self.window.winfo_x() + 50), str(self.window.winfo_y() - 100)))
            message_window.title('Attention')

            message = "Fix your posture!"
            label = tk.Label(message_window, text=message, font=("Comic Sans MS", 12), fg='blue')
            label.pack(pady=20)

            self.window.after(20000, self.posture_reminder) #change the time when actually using, set to several seconds now for convenience
            
   def changetime(self, direction):
       # Change displayed image using direction/timestamp
       if time.time() > self.timestamp + 0.1:  # Increase the time interval to slow down the animation
           self.timestamp = time.time()
           self.frame_index = (self.frame_index + 1) % 8
           self.img = direction[self.frame_index]


   def changedir(self):
       # Change movement direction
       self.dir = -(self.dir)


   def stop_animation(self, event):
       # Stop the animation for a specified duration when clicked
       if not self.is_stopped:
           self.sleeping()
           self.show_options_window()

   def sleeping(self):
       # Stop the movement
       self.is_stopped = True

       # Change the animation to sleeping
       direction = self.sleepAnimation
       self.frame_index = 0  # Reset frame index to start from the first frame
       self.img = direction[self.frame_index]

       # Update the window
       self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
       self.label.configure(image=self.img)
       self.label.pack()

       # After stopping the animation, reset the frame index to zero
       self.frame_index = 0
    
   def go(self):
       if not self.is_stopped:
           # Update the x-coordinate using current direction
           self.x = self.x + self.dir
           # Determine current direction frames
           if self.dir < 0:
               direction = self.moveleft
           else:
               direction = self.moveright
           # Change image based on direction/timestamp
           self.changetime(direction)


   def update(self):
       # Update  position/direction/displayed image
       if not self.is_stopped:
           self.go()

           # Change direction when reaching specific x-coordinates
           if self.x < 220 or self.x > 1170:
               self.changedir()


       # Update window geometry/label image
       self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
       self.label.configure(image=self.img)  
       self.label.pack()

       self.window.after(135, self.update)

       # Ensure the window stays on top
       self.window.lift()
       
    # Exit out of the program entirely
   def exit_program(self):
        self.window.destroy()

    # Menu of options
   def show_options_window(self):
       self.options_window = tk.Toplevel(self.window)
       self.options_window.geometry('200x200+{}+{}'.format(str(self.x + 50), str(self.y - 200)))
       self.options_window.title('Options')

       label = tk.Label(self.options_window, text='Choose an option:')
       label.pack(pady=10)

       resume_button = tk.Button(self.options_window, text='Wake up', command=self.resume_animation)
       resume_button.pack(pady=5)

       cute_button = tk.Button(self.options_window, text='Cute Message', command=self.show_cute_dialogue)
       cute_button.pack(pady=5)

       exit_button = tk.Button(self.options_window, text='Exit', command=self.exit_program)
       exit_button.pack(pady=5)

   def resume_animation(self):
       if self.options_window:
           self.options_window.destroy()
           self.options_window = None
        
       self.is_stopped = False
       self.timestamp = time.time()
       self.frame_index = 0
       self.img = self.moveleft[self.frame_index]

       self.label.configure(image=self.img)  # Reset the image to walking animation

    # Cute dialogue box for cat nap
   def show_cute_dialogue(self):
       cute_message = ["Meow! Hi there! I'm taking a catnap. Wake me up with a click! :3", "You got this! MEOW;D","Don't forget to smile! Meow meow:3","You are doing fabbb! Keep going meow~"]
       messagebox.showinfo("Cute Cat", random.choice(cute_message))
       self.resume_animation() # Resume the animation (waking up cat)

Pet()
