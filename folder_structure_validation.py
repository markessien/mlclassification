
class validate_dataset:
    def __init__(self,path):
        self.path= path

    def check_two_folders(self,path):
        import os
        folderdir=[]
        foldername=[]
        files=os.listdir(path)
        for file in files:
            file=os.path.join(path,file)
            if os.path.isfile(file)==False:
                folderdir.append(file)
                foldername.append(os.path.split(file)[1])
        if len(folderdir)!=2:
            return False
        else:
            return folderdir, foldername
        
    def validate(self):
        import os
        import json
        #check if path is an existing path
        if os.path.isdir(path)=='False':
            result=json.dumps({'error':'true','message':'traning path provided not found'})
            return result
        else: 
            #check if path is a folder or file
            if os.path.isfile(path)=='True':
                result=json.dumps({'error':'true','message':'invalid training path provided'})
                return result
            else:
                #check if dir is not empty
                if os.listdir(path)==[]:
                    result=json.dumps({'error':'false','message':'emptypath specified'})
                    return result

                else:
                    #check contents of the file
                    check1=self.check_two_folders(path)
                    if (check1 == False):
                        result=json.dumps({'error':'false','message':'folder contained in path is not equal to 2'})
                        return result
                        
                    else:
                        #check the names of the folder
                        folderdir,foldername=check1
                        if ((foldername[0]!='test_set') and (foldername[1]!='training_set')):
                            result=json.dumps({'error':'false','message':'folder not named correctly, pls name folders -test_set- and -traning_set- simultaneously'})
                            return result
                            
                        else:
                            for folder in folderdir:              
                                #check if each folder contains 2 folder each
                                check2=self.check_two_folders(folder)
                                if (check2 == False):
                                    result=json.dumps({'error':'false','message':'either folder does not contain 2 subfolders'})
                                    return result
                                else:
                                    folderdir,filename=check2
                                #check if the contents of the folders are images
                                image_ext=['.jpeg','.jpg','.png','.gif']
                                image=[]
                                for subs in folderdir:
                                    files= os.listdir(subs)
                                    for file in files:
                                        file_extention=os.path.splitext(file)[1].lower()
                                        #print('file_ext',file_extention)
                                        if file_extention in image_ext:
                                            image.append(True)
                                        else:
                                            image.append(False)
                            if False in image:
                                
                                result=json.dumps({'error':'false','message':'either sub-folder contains a non-image file'})
                                return result
                            else:
                                result=json.dumps({'error':'false','message':'Validation Completed'})
                                return result
                                        
                                   
                                
                                    

    
                                        
                            
                            
                        
                        
                        
                        
                
