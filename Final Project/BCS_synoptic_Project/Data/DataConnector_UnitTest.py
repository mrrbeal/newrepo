from DataConnector import ImageFile,CategoryList,MediaFile,MediaLibrary,PlaylistLibrary
import unittest,os,sys

unittest.TestLoader.sortTestMethodsUsing = None


class databasconnectortest(unittest.TestCase):

    if getattr(sys, 'frozen', False):
        dname = os.path.dirname(sys.executable)
    elif __file__:
        dname = os.path.dirname(__file__)


    global mediaLibrary
    global categoryList
    global playlistLibrary

    mediaLibrary = MediaLibrary()
    categoryList = CategoryList()
    playlistLibrary = PlaylistLibrary()

    global testimageFile
    global testMediaFile
    global testMediaFile2
    global testMediaFolder
    global file
    global file2
    global filetypes
    testimageFile =  dname +   r"\Test Documents\logo.gif"
    testMediaFile =   dname +  r"\Test Documents\Coldplay - Adventure Of A Lifetime.mp4"
    testMediaFile2 =  dname +  r"\Test Documents\Coldplay - Yellow.mp4"
    testMediaFolder = dname +  r"\Test Documents"
    print("FOLDER", testMediaFolder)
    file = None
    file2 = MediaFile(testMediaFile2)

    filetypes = "mp4"

    print("*****MediaFile*****") 

    def test_creation_mediaFile(self):
        """verify the creation of media fil object"""
        global file
        file = MediaFile(testMediaFile)
        self.assertEqual(file.file_name,"Coldplay - Adventure Of A Lifetime")
        self.assertEqual(file.file_type,"mp4")
        self.assertEqual(file.file_path,testMediaFile)
        self.assertEqual(file.file_comment,"")
        self.assertEqual(file.categories,[])


    def test_mediaFile_setImage(self):
        """verify the creation of media fil object"""
        global file
        file.setImage(testimageFile)
        self.assertEqual(file.image_path,testimageFile)
        self.assertEqual(file.image_name,"logo")

    print("*****MediaLibrary*****") 

    def test_mediaLibrary_addFile(self):
        global mediaLibrary
        mediaLibrary.add_file(testMediaFile)
        self.assertEqual(len(mediaLibrary.files),1)

    def test_mediaLibrary_addfolder(self):
        global mediaLibrary
        mediaLibrary.add_folder(testMediaFolder,"mp4")
        self.assertEqual(len(mediaLibrary.files),3)

    def test_mediaLibrary_get_file(self):
        global mediaLibrary
        file = mediaLibrary.get_file(1)
        self.assertEqual(file.file_name,"Coldplay - Adventure Of A Lifetime")
        self.assertEqual(file.file_type,"mp4")
        self.assertEqual(file.file_path,testMediaFile)
        self.assertEqual(file.file_comment,"")
        self.assertEqual(file.categories,[])

    def test_mediaLibrary_removeFile(self):
        fileid = 3
        filename = "Coldplay - Yellow"
        filetype = "mp4"
        mediaLibrary.removeFile(fileid,filename,filetype)
        self.assertEqual(len(mediaLibrary.files),2)

    def test_mediaLibrary_getSize(self):
        size = mediaLibrary.getSize()
        self.assertEqual(len(mediaLibrary.files),size)

    print("*****CategoryList*****") 

    def test_categoryList_createCategory(self):
        categoryList.createCategory("NewCategory")
        self.assertEqual(len(categoryList.categories),1)

    def test_categoryList_mupdateCategory(self):
        oldName = "NewCategory"
        newName = "RenamedCategory"
        categoryList.updateCategory(oldName,newName)
        self.assertEqual(categoryList.categories[0],"RenamedCategory")

    def test_categoryList_removeCategory(self):
        categoryList.removeCategory("RenamedCategory")
        self.assertEqual(len(categoryList.categories),0)


    print("*****PlaylistLibrary*****")   

    def test_playlistLibrary1_add_playlist(self):
        global playlistLibrary
        playlistLibrary.add_playlist("NewPlaylist")
        self.assertEqual(len(playlistLibrary.playlists),1)
    

    def test_playlistLibrary2_getSize(self):
        global playlistLibrary
        size = playlistLibrary.getSize()
        self.assertEqual(size,1)

    def test_playlistLibrary3_add_file_to_playlist(self):
        global playlistLibrary
        playlistLibrary.add_file_to_playlist("NewPlaylist",file)
        self.assertAlmostEqual(len(playlistLibrary.playlists["NewPlaylist"]),1)

    def test_playlistLibrary4_move_playlistFile(self):
        global playlistLibrary
        playlistLibrary.add_file_to_playlist("NewPlaylist",file2) 
        playlistLibrary.move_playlistFile("NewPlaylist",0,"down")
        self.assertNotEqual("Coldplay - Adventure Of A Lifetime",playlistLibrary.playlists["NewPlaylist"][0][1].file_name)

    def test_playlistLibrary5_delete_file_from_playist(self):
        global playlistLibrary
        playlistLibrary.delete_file_from_playist("NewPlaylist",1)
        self.assertEqual(len(playlistLibrary.playlists["NewPlaylist"]),1)

    def test_playlistLibrary6_rename_playlist(self):
        global playlistLibrary
        playlistLibrary.rename_playlist("NewPlaylist","renamedPlaylist")
        key = list(playlistLibrary.playlists)
        self.assertEqual(key[0],"renamedPlaylist") 

    def test_playlistLibrary7_delete_playlist(self):
        global playlistLibrary
        playlistLibrary.delete_playlist("renamedPlaylist")
        size = playlistLibrary.getSize()
        self.assertEqual(size,0)















