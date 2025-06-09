The goal is to develop an application that checks whether students have found a way to insert an xss script into a website.
The malicious query can either be entered through an input Element of the class "searchInput" or directly via the url depending on the task.
The project should provide APIs for both fashions, that receive either the input query or the uri. When called they should run a browser (host system is headless) and return true once they receive PopUp. If after five seconds no pop up was triggered, the API should return false.
The applications should be dockerized. 