
class validate_dataset:
    def __init__(self,path):
        self.path= path

    def check_two_folders(self,path):
        import os
        folderdir=[]
        files=os.listdir(path)
        for file in files:
            file=os.path.join(path,file)
            if os.path.isfile(file)==False:
                folderdir.append(file)
        if len(folderdir)!=2:
            return False
        else:
            return folderdir
        
    def validate(self):
        import os
        import json
        #check if path is an existing path
        if os.path.isdir(path)==False:
            result=json.dumps({'error':'true','message':'traning path provided not found'})
            return result
        else: 
            #check if path is a folder or file
            if os.path.isfile(path)==True:
                result=json.dumps({'error':'true','message':'invalid training path provided'})
                return result
            else:
                #check if dir is not empty
                if os.listdir(path)==[]:
                    result=json.dumps({'error':'true','message':'emptypath specified'})
                    return result
                else:
                    #check if the path contains two folders
                    check1=self.check_two_folders(path)
                    if (check1 == False):
                        result=json.dumps({'error':'true','message':'folder must contain 2 sub-folders'})
                        return result
                    
                    else:
                        #check if the contents of the folders are images
                        image_ext=['.jpeg','.jpg','.png','.gif','.tiff']
                        image=[]
                        for i, subs in enumerate (check1):
                            files= os.listdir(subs)
                            for file in files:
                                file_extention=os.path.splitext(file)[1].lower()
                                #print('file_ext',file_extention)
                                if file_extention in image_ext:
                                    image.append(True)
                                else:
                                    image.append(False)
                        if False in image:
                            result=json.dumps({'error':'true','message':f' either sub-folder contains a non-image file'})
                            return result
                        else:
                            result=json.dumps({'error':'false','message':'Validation Completed'})
                            return result


#how to call method
#create an instance of  the class e.g x= validate_dataset(path)
#then call the function validate e.g x.validate()
                                        
                                   
                                
                                    

    
                                        
                            
                            
                        
                        
                        
                        
                
