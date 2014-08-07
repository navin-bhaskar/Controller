This project lets you control perepherals such as GPIOs, ADCs and DACs on your dev boards
using a simple to use GUI tool written in python. 
The wx GUI tool kit is used via wxPython for implementing the GUI controls.
To run the application, connect your board (currently, Arduino, Arduino mega and mbed are suppourted)
and start the GUI app after installing the required dependencies. 

controller_gui
  Contains the python script that implements the GUI application
Controller
  Contains the Arduino project that you need to upload unto arduino for it to work with the GUI app.
  Select either arduino or MEGA using the proper define in "ArdPerAccess.h" file
 