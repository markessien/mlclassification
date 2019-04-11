def validate(path):
    import os
    import json
    print(path)
    #check if path is an existing path
    if os.path.isdir(path)==False:
        result=json.dumps({'error':'true','message':'path provided not found'})
        return result
    else: 
        #check if path is a folder or file
        if os.path.isfile(path)==True:
            result=json.dumps({'error':'true','message':'Path should be a folder not a file'})
            return result
        else:
            #check if dir is not empty
            if os.listdir(path)==[]:
                result=json.dumps({'error':'true','message':'emptypath specified'})
                return result
            else:
                #check if the contents of the folders are images
                image_ext=['.jpeg','.jpg','.png','.gif','.tiff']
                image=[]
                files=os.listdir(path)
                for i, file in enumerate (files):
                    file_extention=os.path.splitext(file)[1].lower()
                    if file_extention in image_ext:
                        image.append(True)
                    else:
                        image.append(False)
                if False in image:
                    result=json.dumps({'error':'true','message':f' folder contains a non-image file'})
                    return result
                else:
                    result=json.dumps({'error':'false','message':'Validation Completed'})
                    return result


                                        
                                   
                                
                                    

    
                                        
                            
                            
                        
                        
                        
                        
                
