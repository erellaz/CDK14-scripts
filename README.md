# Scripts to receive data from the remote telescope
Load image metadata -> 
Separates files with bad data, based on the metadata ->
Backup logs from NINA, PHD2, sequences and other stuff ->
Compress ->
Put in the sync folder ->
Post updates to Discord at each step.


The data gets synced by Syncthing in the background and appears on the server side.


Move the data from Sync to the Stage folder ->
Decompress ->
Copy to archive and split to processing directories according to name ->
Clean up directories ->
Update the cloud for each target, calling rclone via Subprocess.
