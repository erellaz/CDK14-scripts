# Scripts to receive data from the remote telescope
Load image metadata -> 
Move files with bad data ->
Back logs from NINA, PHD2, and sequences ->
Compress ->
Put in the sync folder ->
Post updates to Discord at each step


The data gets synced by Syncthing in the background and appears on the server side.


Move the data to the stage folder ->
Decompress ->
Copy to archive and processing according to name and working directories ->
Clean up ->
Update the cloud for each target, calling rclone via subprocess.
