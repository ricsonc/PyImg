PyImg
=====

There are many screenshot uploading and sharing utilities. Gyazo is an example of one of these. 

Unfortunately, at the time when this script was created, all of these sharing utilities suffered from the same flaw -- the user would have to wait for the screenshot to be taken and uploaded before a shareable link was provided to the user. 

This resulted in several seconds of unacceptable delay. In order to remedy this, this script provides the user with a tinyurl link immediately before uploading the image. Once the image has been uploaded, the tinyurl link is redirected towards the image through an api. As a result, there is no delay for the user. 
