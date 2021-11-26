import os,sys,json,pickle

def DEBUG(text):
    if DEBUGON == True:
        print("DataConnector:\n",text)

DEBUGON = True


class ImageFile:
    """Class Defines an Image file"""
    def __init__(self) -> None:
        #get current directory name
        if getattr(sys, 'frozen', False):
            dname = os.path.dirname(sys.executable)
        elif __file__:
            dname = os.path.dirname(__file__)

        self.image_path = rf'{dname}\no_image.png'
        self.image_name = os.path.split(self.image_path)[1].split(".")[0]

    def setImage(self,filePath)-> None:
        """Method for setting the image path after object creation"""
        self.image_path = filePath
        self.image_name = os.path.split(filePath)[1].split(".")[0]

class CategoryList:
    """Class Defines a category list and methods for managing"""
    def __init__(self) -> None:
        self.categories = []

    def getSize(self)->list:
        """Method returns the size of the list"""
        DEBUG(f"GETSIZE: {len(self.categories)}")
        return len(self.categories)

    def createCategory(self,name)->None:
        """Method for creating a category within the object"""
        self.categories.append(name)

    def removeCategory(self,categoryName)->None:
        """Method for deleting a category within the object"""
        self.categories.remove(categoryName)

    def updateCategory(self,oldName,newName)->None:
        """Method for renaming a category within the object"""
        for x in range(len(self.categories)):
            if self.categories[x] == oldName:
                self.categories[x] = newName



class MediaFile(ImageFile):
    """Class defines a Mediafile Object"""
    def __init__(self,filePath) -> None:
        ImageFile.__init__(self)
        self.file_path = filePath
        self.file_name = os.path.split(filePath)[1].split(".")[0]
        self.file_type = os.path.splitext(filePath)[1][1:]
        self.file_comment = ""
        self.categories = []

class MediaLibrary:
    """Class defines a media Library object"""
    def __init__(self) -> None:
        self.files = {}
        if self.getSize() == 0:
            self.keyCount = 1
        else:
            self.keyCount =  max(self.files.keys()) + 1

    def getSize(self)->dict:
        """Method returns the size of the list"""
        DEBUG(f"GETSIZE: {len(self.files)}")
        return len(self.files)

    def add_file(self,filePath):
        """Method adds a new key to the object dict where the value is a MediaFile object from a filepath"""
        self.files[self.keyCount] = (MediaFile(filePath))
        self.keyCount +=1

    def add_folder(self,folderDir,fileTypes):
        """Method adds a new keys to the object dict where the values are MediaFile objects from a selected directory"""
        for subdir, dir, files in os.walk(folderDir):
            for file in files:
                file_path = subdir + os.sep + file
                file_type = os.path.splitext(file)[1][1:]
                if file_type in fileTypes:
                    self.files[self.keyCount] = (MediaFile(file_path))
                    self.keyCount +=1

    def removeFile(self,fileid,filename,filetype):
        """Method removed a file from the MediaLibrary object"""
        DEBUG(f"GETSIZE BEFORE REMOVE: {len(self.files)}")
        for key, value in self.files.items():
            if value.file_name == filename and value.file_type == filetype and key == fileid:
                del self.files[key]
                DEBUG(f"GETSIZE AFTER REMOVE: {len(self.files)}")
                break
    
    def get_file(self,dictKey)->dict:
        return self.files.get(dictKey)


class PlaylistLibrary:
    def __init__(self) -> None:
        self.playlists = {}

    def getSize(self)->dict:
        """Method returns the size of the list"""
        DEBUG(f"GETSIZE: {len(self.playlists)}")
        return len(self.playlists)
    
    def add_playlist(self,name)->None:
        """Method adds a playlist"""
        self.playlists[name] =[]

    def delete_playlist(self,key)->None:
        """Method deletes a playlist"""
        self.playlists.pop(key, None)

    def rename_playlist(self,oldkey,newkey)->None:
        """Method renames a playlist"""
        if newkey!=oldkey:
            #grab new key and replace the old key
            self.playlists[newkey] = self.playlists[oldkey]
            del self.playlists[oldkey]
    
    def move_playlistFile(self,name,index,direction)->None:
        """Method moves a playlist file up or down"""
        reindex = index-1
        #if direction is up, then swap indexs and list locations with the file above
        if direction == "up":
            if reindex != 0:
                move_up_list = list(self.playlists[name][reindex])
                move_down_list = list(self.playlists[name][reindex-1])
                move_up_list[0] = index-1
                move_down_list[0] = index
                self.playlists[name][reindex] = tuple(move_up_list)
                self.playlists[name][reindex-1] = tuple(move_down_list)
                self.playlists[name][reindex], self.playlists[name][reindex-1] = self.playlists[name][reindex-1], self.playlists[name][reindex]
        
        else:
            #if direction is not up (down), select then select the file below and swap index and list position
            playlistlength = len(self.playlists[name])-1
            reindex += 1
            if reindex <= playlistlength:
                move_up_list = list(self.playlists[name][reindex])
                move_down_list = list(self.playlists[name][reindex-1])
                move_up_list[0] = index
                move_down_list[0] = index+1
                self.playlists[name][reindex] = tuple(move_up_list)
                self.playlists[name][reindex-1] = tuple(move_down_list)
                self.playlists[name][reindex], self.playlists[name][reindex-1] = self.playlists[name][reindex-1], self.playlists[name][reindex]

    def delete_file_from_playist(self,name,index)->None:
        """Method deletes a file from a playlist, it then re-indexes the remaining files"""
        #delete the selected file
        for i in self.playlists[name]:
            if i[0] == index:
                self.playlists[name].pop(self.playlists[name].index(i))
        reindex = 1
        #reindex remaining files
        for i in range(len(self.playlists[name])):
            edit = list(self.playlists[name][i])
            edit[0] = reindex
            self.playlists[name][i] = tuple(edit)
            reindex += 1

    def add_file_to_playlist(self,name,mediaFile)->None:
        """Method adds a mediafile object to a playlist"""
        tupToAdd = tuple((len(self.playlists[name])+1,mediaFile))
        DEBUG(f"add_file_to_playlist - Adding {tupToAdd}")
        self.playlists[name].append(tupToAdd)   


