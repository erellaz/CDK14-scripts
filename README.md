# Scripts to receive data from the remote telescope
Processes on the Remote Telescope side:

Load image metadata -> 
Separates files with bad data, based on the metadata ->
Backup logs from NINA, PHD2, sequences and other stuff ->
Compress ->
Put in the sync folder ->
Post updates to Discord at each step.

Transfer of compressed files via Starlink:

The data gets synced by Syncthing in the background and appears on the server side.

Processes on the Server side, once the data has been received:

Move the data from Sync to the Stage folder ->
Decompress ->
Copy to archive and split to processing directories according to name ->
Clean up directories ->
Update the cloud for each target, calling rclone via Subprocess.
