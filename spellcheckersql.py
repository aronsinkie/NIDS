import mysql.connector
import chardet
RIBI = {
'ሐ':'ሕአ',
'ሑ':'ሕኡ',
'ሒ':'ሕኢ',
'ሓ':'ሕኣ',
'ሔ':'ሕኤ',
'ሕ':'ሕ',
'ሖ':'ሕኦ',
'𞟨':'𞟫አ',
'ሑ':'ሕኡ',
'𞟩':'𞟫ኢ',
'ሗ':'𞟫ኣ',
'𞟪':'𞟫ኤ',
'𞟫':'𞟫',
'ሖ':'ሕኦ',
'𞟠':'𞟥አ',
'𞟡':'𞟥ኡ',
'𞟢':'𞟥ኢ',
'𞟣':'𞟥ኣ',
'𞟤':'𞟥ኤ',
'𞟥':'𞟥',
'𞟦':'𞟥ኦ',
'ለ':'ልአ',
'ሉ':'ልኡ',
'ሊ':'ልኢ',
'ላ':'ልኣ',
'ሌ':'ልኤ',
'ል':'ል',
'ሎ':'ልኦ',
'መ':'ምአ',
'ሙ':'ምኡ',
'ሚ':'ምኢ',
'ማ':'ምኣ',
'ሜ':'ምኤ',
'ም':'ም',
'ሞ':'ምኦ',
'ᎀ':'ᎃአ',
'ሙ':'ምኡ',
'𞟭':'ᎃኢ',
'ሟ':'ᎃኣ',
'𞟮':'ᎃኤ',
'ᎃ':'ᎃ',
'ሞ':'ምኦ',
'ረ':'ርአ',
'ሩ':'ርኡ',
'ሪ':'ርኢ',
'ራ':'ርኣ',
'ሬ':'ርኤ',
'ር':'ር',
'ሮ':'ርኦ',
'ሰ':'ስአ',
'ሱ':'ስኡ',
'ሲ':'ስኢ',
'ሳ':'ስኣ',
'ሴ':'ስኤ',
'ስ':'ስ',
'ሶ':'ስኦ',
'ሸ':'ሽአ',
'ሹ':'ሽኡ',
'ሺ':'ሽኢ',
'ሻ':'ሽኣ',
'ሼ':'ሽኤ',
'ሽ':'ሽ',
'ሾ':'ሽኦ',
'ቀ':'ቅአ',
'ቁ':'ቅኡ',
'ቂ':'ቅኢ',
'ቃ':'ቅኣ',
'ቄ':'ቅኤ',
'ቅ':'ቅ',
'ቆ':'ቅኦ',
'ቈ':'ቅአ',
'ቁ':'ቅኡ',
'𞟰':'𞟲ኢ',
'ቋ':'𞟲ኣ',
'𞟱':'𞟲ኤ',
'𞟲':'𞟲',
'ቆ':'ቅኦ',
'ቐ':'ቕአ',
'ቑ':'ቕኡ',
'ቒ':'ቕኢ',
'ቓ':'ቕኣ',
'ቔ':'ቕኤ',
'ቕ':'ቕ',
'ቖ':'ቕኦ',
'በ':'ብአ',
'ቡ':'ብኡ',
'ቢ':'ብኢ',
'ባ':'ብኣ',
'ቤ':'ብኤ',
'ብ':'ብ',
'ቦ':'ብኦ',
'ᎄ':'ᎇአ',
'ቡ':'ብኡ',
'𞟳':'𞟳ኢ',
'ቧ':'ᎇኣ',
'𞟴':'ᎇኤ',
'ᎇ':'ᎇ',
'ቦ':'ብኦ',
'ተ':'ትአ',
'ቱ':'ትኡ',
'ቲ':'ትኢ',
'ታ':'ትኣ',
'ቴ':'ትኤ',
'ት':'ት',
'ቶ':'ትኦ',
'ቸ':'ችአ',
'ቹ':'ችኡ',
'ቺ':'ችኢ',
'ቻ':'ችኣ',
'ቼ':'ችኤ',
'ች':'ች',
'ቾ':'ችኦ',
'ነ':'ንአ',
'ኑ':'ንኡ',
'ኒ':'ንኢ',
'ና':'ንኣ',
'ኔ':'ንኤ',
'ን':'ን',
'ኖ':'ንኦ',
'ኘ':'ኝአ',
'ኙ':'ኝኡ',
'ኚ':'ኝኢ',
'ኛ':'ኝኣ',
'ኜ':'ኝኤ',
'ኝ':'ኝ',
'ኞ':'ኝኦ',
'አ':'አ',
'ኡ':'ኡ',
'ኢ':'ኢ',
'ኣ':'ኣ',
'ኤ':'ኤ',
'እ':'እ',
'ኦ':'ኦ',
'ከ':'ክአ',
'ኩ':'ክኡ',
'ኪ':'ክኢ',
'ካ':'ክኣ',
'ኬ':'ክኤ',
'ክ':'ክእ',
'ኮ':'ክኦ',
'ኰ':'𞟷አ',
'ኩ':'ክኡ',
'𞟵':'𞟷ኢ',
'ኳ':'𞟷ኣ',
'𞟶':'𞟷ኤ',
'𞟷':'𞟷',
'ኮ':'ክኦ',
'ኸ':'ኽአ',
'ኹ':'ኽኡ',
'ኺ':'ኽኢ',
'ኻ':'ኽኣ',
'ኼ':'ኽኤ',
'ኽ':'ኽ',
'ኾ':'ኽኦ',
'ወ':'ውአ',
'ዉ':'ውኡ',
'ዊ':'ውኢ',
'ዋ':'ውኣ',
'ዌ':'ውኤ',
'ው':'ው',
'ዎ':'ውኦ',
'ዐ':'ዕአ',
'ዑ':'ዕኡ',
'ዒ':'ዕኢ',
'ዓ':'ዕኣ',
'ዔ':'ዕኤ',
'ዕ':'ዕ',
'ዖ':'ዕኦ',
'ዘ':'ዝአ',
'ዙ':'ዝኡ',
'ዚ':'ዝኢ',
'ዛ':'ዝኣ',
'ዜ':'ዝኤ',
'ዝ':'ዝ',
'ዞ':'ዝኦ',
'ዠ':'ዥአ',
'ዡ':'ዥኡ',
'ዢ':'ዥኢ',
'ዣ':'ዥኣ',
'ዤ':'ዥኤ',
'ዥ':'ዥእ',
'ዦ':'ዥኦ',
'የ':'ይአ',
'ዩ':'ዩኡ',
'ዪ':'ይኢ',
'ያ':'ይኣ',
'ዬ':'ይኤ',
'ይ':'ይ',
'ዮ':'ይኦ',
'ደ':'ድአ',
'ዱ':'ድኡ',
'ዲ':'ድኢ',
'ዳ':'ድኣ',
'ዴ':'ድኤ',
'ድ':'ድ',
'ዶ':'ድኦ',
'ጀ':'ጅአ',
'ጁ':'ጅኡ',
'ጂ':'ጅኢ',
'ጃ':'ጅኣ',
'ጄ':'ጅኤ',
'ጅ':'ጅ',
'ጂ':'ጅኦ',
'ገ':'ግአ',
'ጉ':'ግኡ',
'ጊ':'ግኢ',
'ጋ':'ግኣ',
'ጌ':'ግኤ',
'ግ':'ግእ',
'ጎ':'ግኦ',
'ጐ':'ግአ',
'ጉ':'ግኡ',
'𞟸':'𞟺ኢ',
'ጓ':'𞟺ኣ',
'𞟹':'𞟺ኤ',
'𞟺':'𞟺',
'ጎ':'ገኦ',
'ጘ':'ጝአ',
'ጙ':'ጝኡ',
'ጚ':'ጝኢ',
'ጛ':'ጝኣ',
'ጜ':'ጝኤ',
'ጝ':'ጝ',
'ጞ':'ጝኦ',
'ጠ':'ጥአ',
'ጡ':'ጥኡ',
'ጢ':'ጥኢ',
'ጣ':'ጥኣ',
'ጤ':'ጥኤ',
'ጥ':'ጥ',
'ጦ':'ጥኦ',
'ጨ':'ጭአ',
'ጩ':'ጭኡ',
'ጪ':'ጭኢ',
'ጫ':'ጭኣ',
'ጬ':'ጭኤ',
'ጭ':'ጭእ',
'ጮ':'ጭኦ',
'ፈ':'ፍአ',
'ፉ':'ፍኡ',
'ፊ':'ፍኢ',
'ፋ':'ፍኣ',
'ፌ':'ፍኤ',
'ፍ':'ፍ',
'ፎ':'ፍኦ',
'ᎈ':'ᎋአ',
'ፉ':'ᎋኡ',
'𞟻':'ᎋኢ',
'ፏ':'ᎋኣ',
'𞟼':'ᎋኤ',
'ᎋ':'ᎋ',
'ፎ':'ፍኦ',
'ፐ':'ፕአ',
'ፑ':'ፕኡ',
'ፒ':'ፕኢ',
'ፓ':'ፕኣ',
'ፔ':'ፕኤ',
'ፕ':'ፕእ',
'ፖ':'ፕኦ',
'ᎌ':'ᎏአ',
'ፑ':'ፕኡ',
'𞟽':'ᎏኢ',
'𞟾':'ᎏኤ',
'ᎏ':'ᎏ',
}
# File paths
root = 'all_root.txt'
noun_list='Noun_root.txt'
verb_list='list of verbs_root.txt'
adj_list='Adjective_root.txt'

verb_prefix = 'prefixes_repition_removed.txt'
verb_sufix = 'suffixes removed repeation.txt'
noun_prefix = 'Noun_prefixes  filttered.txt'
noun_sufix = 'nound_suffixes filtered .txt'
adj_prefix = 'Adjective_suffixes  filttered.txt'
adj_sufix= 'Adjective_suffixes  filttered.txt'

DATABASE = 'Dictionary'

# Create the database and dictionary table
def create_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Aron123@aron123@'
    )
    c = conn.cursor()
    c.execute(f'CREATE DATABASE IF NOT EXISTS {DATABASE}')
    conn.database = DATABASE
    c.execute('''CREATE TABLE IF NOT EXISTS root
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS noun_list
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS verb_list
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS adj_list
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS noun_prefix
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS noun_sufix
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS verb_prefix
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS verb_sufix
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS adj_prefix
                 (word VARCHAR(255) PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS adj_sufix
                 (word VARCHAR(255) PRIMARY KEY)''')  
    c.execute('''CREATE TABLE IF NOT EXISTS VC_dictionary
                 (letter VARCHAR(255) NOT NULL,
                  Pronunce VARCHAR(255) PRIMARY KEY)''')
    with open(root, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO root (word) VALUES (%s)", [(word,) for word in words])
    with open(noun_list, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO  noun_list (word) VALUES (%s)", [(word,) for word in words])
    with open(verb_list, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO verb_list (word) VALUES (%s)", [(word,) for word in words])
    with open(adj_list, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO adj_list (word) VALUES (%s)", [(word,) for word in words])
    with open(noun_prefix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO noun_prefix (word) VALUES (%s)", [(word,) for word in words])
    with open(noun_sufix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO noun_sufix (word) VALUES (%s)", [(word,) for word in words])
    with open(verb_prefix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO verb_prefix (word) VALUES (%s)", [(word,) for word in words])
    with open(verb_sufix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO verb_sufix (word) VALUES (%s)", [(word,) for word in words])
    with open(adj_prefix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO adj_prefix (word) VALUES (%s)", [(word,) for word in words])
    with open(adj_sufix, 'r',encoding='utf-8') as f:
        words = set(f.read().splitlines())
        c.executemany("INSERT IGNORE INTO adj_sufix (word) VALUES (%s)", [(word,) for word in words])
    
    # Create a list of values from the entries dictionary
    values = [(letter, Pronunce) for letter, Pronunce in RIBI.items()]
    # Execute the INSERT statement with multiple values
    c.executemany("INSERT IGNORE INTO VC_dictionary (letter, Pronunce) VALUES (%s, %s);", values)
    conn.commit()
    conn.close()

# Check if a word is in the dictionary
def is_word_in_dictionary(word):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Aron123@aron123@',
        database=DATABASE
    )
    c = conn.cursor()
    c.execute("SELECT * FROM root WHERE word=%s", (word,))
    result = c.fetchone()
    conn.close()
    return result is not None


def read_prefixes_from_database(table):
    # Establish a connection to the database
    cnx = mysql.connector.connect( 
        host='localhost',
        user='root',
        password='Aron123@aron123@',
        database=DATABASE
    )

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Execute the SQL query to retrieve prefixes from the table
    query = "SELECT word FROM " + table + ";"
    cursor.execute(query)

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Extract prefixes from the fetched rows
    prefixes = [row[0] for row in rows]

    # Close the cursor and database connection
    cursor.close()
    cnx.close()

    return prefixes
def read_VC_dictionary():
    # Connect to the database
    cnx = mysql.connector.connect( 
        host='localhost',
        user='root',
        password='Aron123@aron123@',
        database=DATABASE
    )

    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Execute the SELECT query to fetch all entries from the 'dictionary' table
    query = "SELECT letter, Pronunce FROM VC_dictionary;"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Create an empty dictionary to store the entries
    entries = {}

    # Iterate over the rows and populate the dictionary
    for row in rows:
        letter, Pronunce = row
        entries[letter] = Pronunce
    keys=list(entries.keys())
    sorted_keys=sorted(keys)
    # Close the cursor and database connection
    cursor.close()
    cnx.close()

    # Return the dictionary
    return entries,sorted_keys