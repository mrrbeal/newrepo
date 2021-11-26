import sqlite3
from typing import Dict, List

def DEBUG(text):
    if DEBUGON == True:
        print(text)

DEBUGON = True

class MediaDataBase:
    next_state = 1
    def __init__(self,name, current_session_state = None) -> None:
        self.DBname = name
        self.connection = sqlite3.connect(self.DBname)
        self.crsr = self.connection.cursor()
        self.database_connect()
        self.session_state = current_session_state
        if self.session_state == None:
            self.create_state()


    
    def set_session_state(self,state_id)-> None:
        DEBUG(f"STATE ID INPUT: , {state_id}")
        records = []
        try:
            with self.connection as con:
                records += con.execute('SELECT * FROM states WHERE state_id = ? ;',(state_id,))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        DEBUG(f"RECORDS GOT: , {records}")
        if len(list(records)) > 0 :
            for record in records:
                DEBUG(f"FOR RECORD: , {record}")
                if record[0] == state_id:
                    self.session_state = record[0]
                    DEBUG(f"SESSION STATE IS: , {self.session_state}")
                    break
        else:
            self.create_state()

    def create_state(self):
        records = []
        try:
            with self.connection as con:
                records = con.execute('SELECT * FROM states ;')
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        try:
            with self.connection as con:
                con.execute('INSERT INTO states(state_name) VALUES(?);',("new_state",))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        
        self.session_state = len(list(records)) + 1
        DEBUG(f"SESSION STATE IS: , {self.session_state}")

### SET UP INITAL DATABASE START ########################################################################
    def database_connect(self) -> None:
        create_files_table = """                            
                                CREATE TABLE IF NOT EXISTS "files" (
                                "file_ID"	INTEGER UNIQUE,
                                "file_name"	VARCHAR(255) NOT NULL,
                                "file_path"	VARCHAR(255) NOT NULL,
                                "file_type"	VARCHAR(255) NOT NULL,
                                "file_comment"	VARCHAR(255),
                                "category_ID"	INTEGER,
                                "file_image_path"	VARCHAR(255),
                                "fok_state_id"	INTEGER NOT NULL,
                                PRIMARY KEY("file_ID" AUTOINCREMENT),
                                FOREIGN KEY("category_ID") REFERENCES "categories"("category_id"),
                                FOREIGN KEY("fok_state_id") REFERENCES "states"("state_id"));
                                """

        create_playlists_table = """
                                CREATE TABLE IF NOT EXISTS playlists (
                                playlist_id	INTEGER UNIQUE,
                                playlist_name VARCHAR(255),
                                "fok_state_id"	INTEGER NOT NULL,
                                PRIMARY KEY("playlist_id" AUTOINCREMENT),
                                FOREIGN KEY("fok_state_id") REFERENCES "states"("state_id"));
                                """
        create_categories_table = """
                                CREATE TABLE IF NOT EXISTS categories (
                                category_id	INTEGER UNIQUE,
                                category_name VARCHAR(255),
                                "fok_state_id"	INTEGER NOT NULL,
                                PRIMARY KEY("category_id" AUTOINCREMENT),
                                FOREIGN KEY("fok_state_id") REFERENCES "states"("state_id"));
                                """
        create_playlist_songs_table = """
                                CREATE TABLE IF NOT EXISTS "playlist_songs" (
                                "ID"	INTEGER NOT NULL,
                                "fok_playlist_id"	INTEGER NOT NULL,
                                "fok_file_id"	INTEGER NOT NULL,
                                "fok_state_id"	INTEGER NOT NULL,
                                PRIMARY KEY("fok_playlist_id" AUTOINCREMENT),
                                FOREIGN KEY("fok_file_id") REFERENCES "files"("file_ID"),
                                FOREIGN KEY("fok_state_id") REFERENCES "states"("state_id"));
                                """
        create_State_table = """
                                CREATE TABLE IF NOT EXISTS "states" (
                                "state_id"	INTEGER UNIQUE,
                                state_name VARCHAR(255),
                                PRIMARY KEY("state_id" AUTOINCREMENT));
                                """

        try:
            with self.connection as con:
                con.execute(create_files_table)
                con.execute(create_playlists_table)
                con.execute(create_categories_table)
                con.execute(create_playlist_songs_table)
                con.execute(create_State_table)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
### SET UP INITAL DATABASE END ########################################################################        


### Code for handling categories START ########################################################################
    def database_category_insert(self,to_insert) -> None:
        records = [(to_insert,self.session_state)]
        DEBUG(f"DB CATAGORY INSERT, {to_insert}, {self.session_state}")
        try:
            with self.connection as con:
                con.execute('INSERT INTO categories(category_name, fok_state_id) VALUES(?,?);',(to_insert,self.session_state))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def database_category_query(self,queryStr = None) -> List:
        DEBUG(f"DB CATAGORY QUERY: ,{queryStr}")
        records = []
        if queryStr == None:
            try:
                with self.connection as con:
                    records += con.execute('SELECT * FROM categories WHERE fok_state_id =?;',(self.session_state,))
                    DEBUG(f"RESULTS: ,{records}")
                    return list(records)
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])
        else:
            try:
                with self.connection as con:
                    records += con.execute('SELECT * FROM categories WHERE category_name = ? AND fok_state_id =?;',(queryStr,self.session_state))
                    DEBUG(f"RESULTS: ,{records}")
                    return list(records)
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])

    def database_category_update(self,catagory_id, catagory_name) -> None:
        records = (catagory_name,catagory_id,self.session_state)
        DEBUG(f"DB CATAGORY UPDATE, {records}")
        try:
            with self.connection as con:
                con.execute("""UPDATE categories
                               SET category_name = ?
                               WHERE category_id = ? AND fok_state_id = ?;""",records)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
    
    def database_category_delete(self,catagory_id,catagory_name) -> None:
        records = (catagory_id,catagory_name,self.session_state)
        DEBUG(f"DB CATAGORY DELETE, {records}")
        try:
            with self.connection as con:
                con.execute("""DELETE FROM categories
                               WHERE category_id = ? AND category_name = ? AND fok_state_id = ?;""",records)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
### Code for handling categories END ########################################################################
    
    
    
    def database_delete(self) -> None:
        pass

    def database_get_files(self) -> List:
        tableFiles = []
        with self.connection as con:
            records = con.execute("SELECT * FROM files")
        return list(records)
        pass

    def database_insert_files(self,records) -> None:
        try:
            with self.connection as con:
                con.executemany('INSERT INTO files(file_name, file_path, file_type,fok_state_id) VALUES(?,?,?,?);',records)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def database_update_files(self) -> None:
        pass

    def database_delete_files(self,input) -> None:
        try:
            with self.connection as con:
                con.execute('DELETE FROM files WHERE file_ID = ?;',(input,))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
    
    def database_search_files(self,input,state_id) -> List:
        DEBUG(f"DB FILES QUERY: , {input},  {state_id}")
        records = []
        try:
            with self.connection as con:
                records += con.execute('SELECT * FROM files WHERE (file_name LIKE ? OR file_type LIKE ?) AND fok_state_id = ?;',('%'+input+'%','%'+input+'%',state_id))
                DEBUG(f"{records}")
                return records
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
    
    def database_search_files_by_ID(self,input,state_id) -> List:
        DEBUG(f"DB FILES QUERY BY ID:  {input},{state_id}")
        records = []
        try:
            with self.connection as con:
                records += con.execute('SELECT * FROM files WHERE (file_id = ?) AND fok_state_id = ?;',(input,state_id))
                DEBUG(f"{records}")
                return records
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

# WITH C AS
# (
# SELECT
#    CAD.id, CAD.name, CAD.gender, CAD.age,
#    PRO.name,
#    AG.desc,
#    AT.name
# FROM file INNER JOIN category As CAT ON file.fok_category_id = CAT.category_name
# )

# SELECT * FROM C;



### TESTING
if __name__ == '__main__':

    cheese = MediaDataBase("cheese1.db")
    cheese.database_connect()
    print(cheese.set_session_state(40))
    cheese.database_category_delete(8,"CHECHEFGG")
    cheese.database_category_query()
    cheese.database_insert_files([("file_name", "file_path", "file_type",40)])
    ret = cheese.database_search_files("type",40)

    #print(cheese.database_search_files("mp3"))

    import os
    def get_folder_files(rootdir) -> List:
        filetypes = ["M4A",
                    "FLAC",
                    "MP3",
                    "MP4",
                    "WAV",
                    "WMA",
                    "AAC"]
        files_to_add = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                #print(os.path.join(subdir, file))
                file_path = subdir + os.sep + file
                file_name  = os.path.splitext(file)[0]
                file_type = os.path.splitext(file)[1][1:]
                if file_type.upper() in filetypes:
                    record = (file_name,fr"{file_path}",file_type)
                    files_to_add.append(record)
        return files_to_add

        

