import os
import zipfile
import shutil
from discord import SyncWebhook

ystr=r'2024-09-27'
target_list = ['Squid','M13','NGC7635','Sh2-155','NGC2170']

share_dir=r'F:\CDK14\Share'
stage_dir = r'F:\CDK14\Stage'
metasave=r"F:\CDK14\Sorted\Meta"
final=r"D:\Pixinsight\CDK14\Data"

target_zip='.zip'
target_fits='.fits'

move_to_dest= True # True False
upload_to_cloud= True # True False

# Web hook for the telescope Discord server
# Get Webhook from Discord>Server settings>Integration>webhooks
webhook=SyncWebhook.from_url(r"https://discord.com/api/webhooks/xxxxxxxxxxxxxxx")

# Verbosity: 0=quiet, 1 st dout, 2 std out and discord
verbosity=2


#______________________________________________________________________________
def Talk(verbosity, message, webhook=None):
    if verbosity >= 1:
        print(message)
    if verbosity >= 2 and webhook is not None:  
       try:
           webhook.send(message)
       except Exception as e:
           print("Exception while posting to Discord",e,message)

#______________________________________________________________________________
def target_files(source_dir,target_pattern):
    for filename in os.listdir(source_dir):
        if filename.endswith(target_pattern):
            yield filename
#______________________________________________________________________________
def FitsDeCompressor(source_dir,dest_dir,target_pattern):
    """ DeCompress all the zip files in a directory"""

    os.chdir(source_dir)  # To work around zipfile limitations

    for target_filename in target_files(source_dir,target_zip):
 
        file_root = os.path.splitext(target_filename)[0]
        zip_file_name = file_root + target_pattern
        zip_file_path = os.path.join(source_dir, zip_file_name)
        print("Decompressing",target_filename)
        with zipfile.ZipFile(zip_file_path, mode='r') as zf:
            zf.extractall(dest_dir)
            zf.close() #file should be closed automatically in a with statement
        #os.remove(target_filename)        
    os.chdir(dest_dir)

    
#______________________________________________________________________________
#______________________________________________________________________________
# Move to Stage

today_share=os.path.join(share_dir,ystr)
today_save=os.path.join(stage_dir,ystr)
try:
    # Trick: to get a folder up just use os.path.dirname twice back to back
    shutil.copytree(today_share,today_save) 
    #shutil.movetree(today_share,today_save)
    message="Data received on Houston server for: "+ystr+"\n Copied: " + today_share + " to " + today_save
    Talk(verbosity, message, webhook)
    
except:
    print("Failed to copy production to backup directory: "+ today_share + " to " + today_save)
 
os.chdir(stage_dir)
 
#______________________________________________________________________________
# Decompress
message="File decompression...."
Talk(verbosity, message, webhook)
FitsDeCompressor(today_save,stage_dir,target_zip)  
trash_dir=os.path.join(today_save,"Trash")
FitsDeCompressor(trash_dir,trash_dir,target_zip) 

#______________________________________________________________________________
# copy to final destination
#move_to_dest= False # True False
if move_to_dest is True:
    message="Copying to final destination...."
    Talk(verbosity, message, webhook)
    for fname in target_files(stage_dir,target_fits):
        for t in target_list:
            if t in fname:
                final_dir=os.path.join(final,t)
                if not os.path.exists(final_dir):
                    print("Creating directory"+final_dir)
                    try:
                        os.makedirs(final_dir)
                    except:
                        print("Failed to create directory"+final_dir)
                try:
                    print("Copying "+ os.path.join(stage_dir,fname)+ " to " + final_dir)
                    shutil.copy2(os.path.join(stage_dir,fname), final_dir)
                except:
                    print("Fail to copy:",os.path.join(stage_dir,fname)," to ", final_dir)
#______________________________________________________________________________
# Save meta directory
print("Saving metafile....")
metapath=os.path.join(today_save,"Meta"+ystr)
metasavedir=os.path.join(metasave,"Meta"+ystr)
try:
    # Trick: to get a folder up just use os.path.dirname twice back to back
    shutil.copytree(metapath,metasavedir) 
    print("Copied: " + metapath + " to " + metasavedir)
except:
    print("Failed to copy production to backup directory: "+ metapath + " to " + metasavedir)

#______________________________________________________________________________
os.chdir(stage_dir)
try:
    print("Cleaning the Share folder")
    shutil.rmtree(today_share)
except:
    print("Failed to remove: "+ today_share)
#______________________________________________________________________________
import subprocess
import posixpath

#upload_to_cloud= False # True False
if upload_to_cloud is True:
    message="Uploading to cloud storage now...."
    Talk(verbosity, message, webhook)
    
    for t in target_list:
        # Works for whatever OS you are running this scripts on
        a=os.path.join(r'D:\Pixinsight\CDK14\Data',t)
        
        # S3 is POSIX, so use POSIX PATH
        b=posixpath.join(r'cdk14prodguillaume:/cdk14prod',t)
        
        
        result = subprocess.run([r'F:\CDK14\rclone\rclone', 'copy',a , b ])
        print(result)       
    
    message="Cloud storage up to date. "
    Talk(verbosity, message, webhook)