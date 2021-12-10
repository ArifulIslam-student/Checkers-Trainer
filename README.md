# Checkers-Trainer

How to run the Code

Install mysql workbench and server
Follow this video https://www.youtube.com/watch?v=u96rVINbAUI 
for root password use @19990629ai

After installation there should be a local instance, open the connection
Create a new schema called checkerdatabase

Install visual studio code if you don't have it

Download the zip folder from the Github
Extract all from the zip and open in visual studio

Go to terminal and click new terminal
Type python manage.py migrate
This will set up the checkerdatabase for use

After the command is done running type python manage.py runserver
If no errors occur the terminal will provide a link of the running application copy and paste it to a web browser of your chosing.
