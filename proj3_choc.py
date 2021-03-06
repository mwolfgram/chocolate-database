import sqlite3
import csv
import json
#matthew wolfgram
#si 203 003

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'     #how to combine the both of the two into choc.db??
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

def init_db(db_name):

    try:
        #print('Creating Database...')
        conn = sqlite3.connect('choc.db')
        cur = conn.cursor()
    except:
        print('an error was encountered')

#------------------------------------------------------------- formation of countries table -------------------------------------------------------------

    statement = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'Countries';"
    table_exists = cur.execute(statement).fetchall()[0][0]
    if table_exists == 1:
        #user_input = input('this table already exists -- reset it by typing yes to and start fresh?')
        user_input = 'yes'
        if user_input == 'yes':
            statement = '''
                DROP TABLE IF EXISTS 'Countries';
            '''
            cur.execute(statement)
            conn.commit()

            statement = '''
                CREATE TABLE 'Countries' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Alpha2' TEXT NOT NULL,
                    'Alpha3' TEXT NOT NULL,
                    'EnglishName' TEXT NOT NULL,
                    'Region' TEXT NOT NULL,
                    'Subregion' TEXT NOT NULL,
                    'Population' INTEGER,
                    'Area' REAL
                );
            '''
            cur.execute(statement)
            conn.commit()

        else:
            return
    else:
        statement = '''
            CREATE TABLE 'Countries' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Alpha2' TEXT NOT NULL,
                'Alpha3' TEXT NOT NULL,
                'EnglishName' TEXT NOT NULL,
                'Region' TEXT NOT NULL,
                'Subregion' TEXT NOT NULL,
                'Population' INTEGER,
                'Area' REAL
            );
        '''
        cur.execute(statement)
        conn.commit()

    countries_json_file = open(COUNTRIESJSON, 'r')
    countries_contents = countries_json_file.read()
    countries_json_file.close()
    COUNTRIES_DICTION = json.loads(countries_contents)

    for x in COUNTRIES_DICTION:
        zero = None
        one = x['alpha2Code']
        two =  x['alpha3Code']
        three = x['name']
        four = x['region']
        five = x['subregion']
        six = x['population']
        seven = x['area']

        insertion = (zero, one, two, three, four, five, six, seven)
        statement = 'INSERT OR IGNORE INTO "Countries"'
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()

#------------------------------------------------------------- formation of bars table -------------------------------------------------------------

    statement = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'Bars';"
    table_exists = cur.execute(statement).fetchall()[0][0]
    if table_exists == 1:
        #user_input = input('this table already exists -- reset it by typing yes to and start fresh?')
        user_input = 'yes'
        if user_input == 'yes':
            statement = '''
                DROP TABLE IF EXISTS 'Bars';
            '''
            cur.execute(statement)
            conn.commit()

            statement = '''
                CREATE TABLE 'Bars' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Company' TEXT NOT NULL,
                    'SpecificBeanBarName' TEXT NOT NULL,
                    'REF' TEXT NOT NULL,
                    'ReviewDate' TEXT NOT NULL,
                    'CocoaPercent' REAL NOT NULL,
                    'CompanyLocation' TEXT NOT NULL,
                    'CompanyLocationId' INTEGER,
                    'Rating' REAL NOT NULL,
                    'BeanType' TEXT NOT NULL,
                    'BroadBeanOrigin' TEXT NOT NULL,
                    'BroadBeanOriginId' INTEGER
                );
            '''
            cur.execute(statement)
            conn.commit()

        else:
            return
    else:
        statement = '''
            CREATE TABLE 'Bars' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Company' TEXT NOT NULL,
                'SpecificBeanBarName' TEXT NOT NULL,
                'REF' TEXT NOT NULL,
                'ReviewDate' TEXT NOT NULL,
                'CocoaPercent' REAL NOT NULL,
                'CompanyLocation' TEXT NOT NULL,
                'CompanyLocationId' INTEGER,
                'Rating' REAL NOT NULL,
                'BeanType' TEXT NOT NULL,
                'BroadBeanOrigin' TEXT NOT NULL,
                'BroadBeanOriginId' INTEGER
            );
        '''
        cur.execute(statement)
        conn.commit()

    query = "SELECT * FROM Countries"
    cur.execute(query)

    country_mapping = {}

    for country in cur:
        id = country[0]
        name = country[3]
        country_mapping[name] = id
    country_mapping['Unknown'] = 0

    with open(BARSCSV) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader, None)

        for row in csvReader:
            the_none_thing = None
            company = row[0]
            specific_bean = row[1]
            REF = row[2]
            review_date = row[3]
            cocoapercent = row[4][:-1]
            CompanyLocation = row[5]
            try:
                fkey1 = country_mapping[CompanyLocation]
            except:
                fkey1 = 0
            rating = row[6]
            beantype = row[7]
            beanorig = row[8]
            try:
                fkey2 = country_mapping[beanorig]
            except:
                fkey2 = 0

            insertion = (the_none_thing, company, specific_bean, REF, review_date, cocoapercent, CompanyLocation, fkey1, rating, beantype, beanorig, fkey2)
            statement = 'INSERT OR IGNORE INTO "Bars"'
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()
    conn.close()

#Part 2: Implement logic to process user commands   #figure out how to deconstruct interactive prompt from part III's response -- if '=' in response -- then do response.split for each thing, how to do top too??
# def process_command(command):
def process_command(command):
    DB_NAME = 'choc.db'
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    query = "SELECT * FROM Countries"
    cur.execute(query)

    country_mapping = {}

    for country in cur:
        alpha2 = country[1]
        name = country[3]
        country_mapping[alpha2] = name

    if 'bars ' in command:
        barsplit = command.split()

        basicbars ='''
        SELECT SpecificBeanBarName , Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin
        FROM Bars
    	JOIN Countries as c
        '''

        strbars=str(basicbars)

        if 'sellcountry' in command:
            bars_sell_phrase = barsplit[1]
            if '=' in bars_sell_phrase:
                bars_sell_split = bars_sell_phrase.split('=')
                user_bars_sell_demand = bars_sell_split[1] #this is what you'd .format into the sql query add
                strbars += " WHERE Bars.CompanyLocationID = c.Id AND Bars.CompanyLocation = '{}'".format(country_mapping[user_bars_sell_demand]) #***change this to country_mapping[user_bars_sell_demand] later***
            else:
                strbars += " WHERE Bars.CompanyLocationID = c.Id"

        if 'sourcecountry' in command:
            bars_source_phrase = barsplit[1]

            if '=' in bars_source_phrase:
                bars_source_split = bars_source_phrase.split('=')
                user_bars_source_demand = bars_source_split[1] #this is what you'd .format into the sql query add
                strbars += " WHERE Bars.BroadBeanOriginID = c.Id AND Bars.BroadBeanOrigin = '{}'".format(user_bars_source_demand) #***change this to country_mapping[user_bars_source_demand] later***
            else:
                strbars += " WHERE Bars.BroadBeanOriginID = c.Id"

        if 'sellregion' in command:
            bars_sellreg_phrase = barsplit[1]

            if '=' in bars_sellreg_phrase:
                bars_sellreg_split = bars_sellreg_phrase.split('=')
                user_bars_sellreg_demand = bars_sellreg_split[1] #this is what you'd .format into the sql query add
                strbars += " WHERE Bars.CompanyLocationID = c.Id AND c.Region = '{}'".format(user_bars_sellreg_demand)
            else:
                strbars += " WHERE Bars.CompanyLocationID = c.Id"

        if 'sourceregion' in command:
            bars_sourcereg_phrase = barsplit[1]

            if '=' in bars_sourcereg_phrase:
                bars_sourcereg_split = bars_sourcereg_phrase.split('=')
                user_bars_sourcereg_demand = bars_sourcereg_split[1] #this is what you'd .format into the sql query add
                strbars += " WHERE Bars.BroadBeanOriginID = c.Id AND c.Region = '{}'".format(user_bars_sourcereg_demand)

            else:
                strbars += " WHERE Bars.BroadBeanOriginID = c.Id"

        trybool1 = bool('sellcountry' in command)
        trybool2 = bool('sourcecountry' in command)
        trybool3 = bool('sellregion' in command)
        trybool4 = bool('sourceregion' in command)
        test_str = str(trybool1) + str(trybool2) + str(trybool3) +str(trybool4)
        if test_str == 'FalseFalseFalseFalse':
            strbars += " WHERE Bars.CompanyLocationID = c.Id"

        trybool5 = bool('ratings' or 'cocoa' in barsplit)
        if trybool5 == False:
             strbars += " ORDER BY Bars.Rating"

        if 'ratings' in command:
            strbars += " ORDER BY Bars.Rating"

        if 'cocoa' in command:
            strbars += " ORDER BY Bars.CocoaPercent"

        if 'top' in command: #default is top = 10!
            bars_top_phrase = barsplit[-1]
            if '=' in bars_top_phrase:
                bars_top_split = bars_top_phrase.split('=')
                user_bars_top_demand = bars_top_split[1] #this is what you'd .format into the sql query add
                strbars += " DESC"  #highest first
                strbars += " LIMIT {}".format(user_bars_top_demand)

            else:
                strbars += " DESC"  #highest first

        if 'bottom' in command:
            bars_bottom_phrase = barsplit[-1]
            if '=' in bars_bottom_phrase:
                bars_bottom_split = bars_bottom_phrase.split('=')
                user_bars_bottom_demand = bars_bottom_split[1] #this is what you'd .format into the sql query add
                strbars += " ASC" #lowest first
                strbars += " LIMIT {}".format(user_bars_bottom_demand)

            else:
                strbars += " ASC" #lowest first

        bars_last_phrase = barsplit[-1]
        bool1 = bool('top' in bars_last_phrase)
        bool2 = bool('bottom' in bars_last_phrase)

        if (bool1, bool2) == (False, False):
            strbars += " DESC"   #defaults to top=10
            strbars += " LIMIT 10"
        cur.execute(strbars)
        bars_output_list = []
        for row in cur:
            bars_output = (row[0],row[1],row[2],(round(float(row[3]), 1)),((str(row[4])[:2]) + '%'),row[5]) #take out if you can't do extra???
            bars_output_list.append(bars_output)
        return bars_output_list

    if 'companies ' in command:
        compsplit = command.split()

        if 'country' or 'region' not in command:
            format2 = " " #default is none!!

        trybool = bool('ratings' or 'cocoa' in compsplit)
        if trybool == False:
             format1 = " ORDER BY Bars.Rating"
             format3 = " ORDER BY Bars.Rating"

        if 'country' in command:
            comp_country_phrase = compsplit[1]
            if '=' in comp_country_phrase:
                comp_country_split = comp_country_phrase.split('=')
                user_comp_country_demand = comp_country_split[1] #this is what you'd .format into the sql query add
                format2 = " AND c.EnglishName = '{}'".format(country_mapping[user_comp_country_demand]) #***change this to country_mapping[user_comp_country_demand] later***
            else:
                format2 = " "

        if 'region' in command:
            comp_region_phrase = compsplit[1]
            if '=' in comp_region_phrase:
                comp_region_split = comp_region_phrase.split('=')
                user_comp_region_demand = comp_region_split[1] #this is what you'd .format into the sql query add
                format2 = " AND c.Region = '{}'".format(user_comp_region_demand)
            else:
                format2 = " "

        if 'ratings' in command:
            format1 = " AVG(Bars.Rating)"
            format3 = " AVG(Bars.Rating)"

        if 'cocoa' in command:
            format1 = " AVG(Bars.CocoaPercent)"
            format3 = " AVG(Bars.CocoaPercent)"

        if 'bars_sold' in command:
            format1 = " COUNT(*)"
            format3 = " COUNT(*)"

        basiccompanies ='''
        SELECT Company, CompanyLocation,{}
        FROM Bars
        JOIN Countries AS c
         	ON Bars.CompanyLocationId = c.Id
         	GROUP BY Company
        HAVING COUNT(*) > 4
        {}
        ORDER BY {}
        '''.format(format1, format2, format3)

        strcomp=str(basiccompanies)

        if 'top' in command: #default is top = 10!
            comp_top_phrase = compsplit[-1]
            if '=' in comp_top_phrase:
                comp_top_split = comp_top_phrase.split('=')
                user_comp_top_demand = comp_top_split[1] #this is what you'd .format into the sql query add
                strcomp += " DESC"  #highest first
                strcomp += " LIMIT {}".format(user_comp_top_demand)

            else:
                strcomp += " DESC"  #highest first

        if 'bottom' in command:
            comp_bottom_phrase = compsplit[-1]
            if '=' in comp_bottom_phrase:
                comp_bottom_split = comp_bottom_phrase.split('=')
                user_comp_bottom_demand = comp_bottom_split[1] #this is what you'd .format into the sql query add
                strcomp += " ASC" #lowest first
                strcomp += " LIMIT {}".format(user_comp_bottom_demand)

            else:
                strcomp += " ASC" #lowest first

        comp_last_phrase = compsplit[-1]
        bool1 = bool('top' in comp_last_phrase)
        bool2 = bool('bottom' in comp_last_phrase)

        if (bool1, bool2) == (False, False):
            strcomp += " DESC"   #defaults to top=10
            strcomp += " LIMIT 10"
        cur.execute(strcomp)
        companies_output_list = []
        for row in cur:
            companies_output = (row[0],row[1], (int(row[2])) if int(row[2]) > 5 else round(float(row[2]), 1)) #take out if you can't do extra???
            companies_output_list.append(companies_output)
        return companies_output_list

    if 'countries ' in command:
        countrsplit = command.split()

        if 'country' or 'region' not in command:
            format5 = " " #default is none!!

        if 'sellers' or 'sources' not in command:
            format1 = " Bars.CompanyLocation"
            format3 = " Bars.CompanyLocationId = c.Id"
            format4 = " Bars.CompanyLocation"

        trybool = bool('ratings' or 'cocoa' in countrsplit)
        if trybool == False:
             format2 = " AVG(Bars.Rating)"
             format6 = " AVG(Bars.Rating)"

        if 'region' in command:
            count_region_phrase = countrsplit[1]
            if '=' in count_region_phrase:
                count_region_split = count_region_phrase.split('=')
                user_count_region_demand = count_region_split[1] #this is what you'd .format into the sql query add
                format5 = " AND c.Region = '{}'".format(user_count_region_demand)
            else:
                format5 = " "

        if 'sellers' in command:
            format1 = " Bars.CompanyLocation"
            format3 = " Bars.CompanyLocationId = c.Id"
            format4 = " Bars.CompanyLocation"

        if 'sources' in command:
            format1 = " Bars.BroadBeanOrigin"
            format3 = " Bars.BroadBeanOriginId = c.Id"
            format4 = " Bars.BroadBeanOrigin"

        if 'ratings' in command:
            format2 = " AVG(Bars.Rating)"
            format6 = " AVG(Bars.Rating)"

        if 'cocoa' in command:
            format2 = " AVG(Bars.CocoaPercent)"
            format6 = " AVG(Bars.CocoaPercent)"

        if 'bars_sold' in command:
            format2 = " COUNT(*)"
            format6 = " COUNT(*)"

        basiccountries ='''
        SELECT {}, c.Region, {}
            FROM Bars
            JOIN Countries AS c ON {}
            GROUP BY {}
            HAVING COUNT(*) > 4
            {}
            ORDER BY {}
        '''.format(format1, format2, format3, format4, format5, format6)

        strcount=str(basiccountries)

        if 'top' in command: #default is top = 10!
            count_top_phrase = countrsplit[-1]
            if '=' in count_top_phrase:
                count_top_split = count_top_phrase.split('=')
                user_count_top_demand = count_top_split[1] #this is what you'd .format into the sql query add
                strcount += " DESC"  #highest first
                strcount += " LIMIT {}".format(user_count_top_demand)

            else:
                strcount += " DESC"  #highest first

        if 'bottom' in command:
            count_bottom_phrase = countrsplit[-1]
            if '=' in count_bottom_phrase:
                count_bottom_split = count_bottom_phrase.split('=')
                user_count_bottom_demand = count_bottom_split[1] #this is what you'd .format into the sql query add
                strcount += " ASC" #lowest first
                strcount += " LIMIT {}".format(user_count_bottom_demand)
            else:
                strcount += " ASC" #lowest first

        count_last_phrase = countrsplit[-1]
        bool1 = bool('top' in count_last_phrase)
        bool2 = bool('bottom' in count_last_phrase)

        if (bool1, bool2) == (False, False):
            strcount += " DESC"   #defaults to top=10
            strcount += " LIMIT 10"

        cur.execute(strcount)
        countries_output_list = []
        for row in cur:
            countries_output = (row[0],row[1], (int(row[2])) if int(row[2]) > 5 else round(float(row[2]), 1)) #take out if you can't do extra???
            countries_output_list.append(countries_output)
        return countries_output_list

    if 'regions ' in command:
        regsplit = command.split()

        if 'seller' or 'sources' not in command:
            format2 = " Bars.CompanyLocationId = c.Id"

        trybool = bool('ratings' or 'cocoa' in regsplit)
        if trybool == False:
             format1 = "AVG(Rating)"
             format3 = "AVG(Rating)"

        if 'sellers' in command:
            format2 = " Bars.CompanyLocationId = c.Id"

        if 'sources' in command:
            format2 = " Bars.BroadBeanOriginId = c.Id"

        if 'ratings' in command:
            format1 = " AVG(Bars.Rating)"
            format3 = " AVG(Bars.Rating)"

        if 'cocoa' in command:
            format1 = " AVG(Bars.CocoaPercent)"
            format3 = " AVG(Bars.CocoaPercent)"

        if 'bars_sold' in command:
            format1 = " COUNT(*)"
            format3 = " COUNT(*)"

        basicreg = '''
         SELECT Region, {}
         FROM Bars
    	    JOIN Countries AS c
            ON {}
        GROUP BY Region
        HAVING COUNT(*) > 4
        ORDER BY {}
        '''.format(format1, format2, format3)

        streg=str(basicreg)

        if 'top' in command: #default is top = 10!
            reg_top_phrase = regsplit[-1]
            if '=' in reg_top_phrase:
                reg_top_split = reg_top_phrase.split('=')
                user_reg_top_demand = reg_top_split[1]
                streg += " DESC"  #highest first
                streg += " LIMIT {}".format(user_reg_top_demand)

            else:
                streg += " DESC"  #highest first

        if 'bottom' in command:
            reg_bottom_phrase = regsplit[-1]
            #print(reg_bottom_phrase)
            if '=' in reg_bottom_phrase:
                reg_bottom_split = reg_bottom_phrase.split('=')
                user_reg_bottom_demand = reg_bottom_split[1]

                streg += " ASC" #lowest first
                streg += " LIMIT {}".format(user_reg_bottom_demand)

            else:
                streg += " ASC" #lowest first

        reg_last_phrase = regsplit[-1]
        bool1 = bool('top' in reg_last_phrase)
        bool2 = bool('bottom' in reg_last_phrase)
        if (bool1, bool2) == (False, False):
            streg += " DESC"   #defaults to top=10
            streg += " LIMIT 10"

        cur.execute(streg)
        region_output_list = []
        for row in cur:
            region_output = (row[0], (int(row[1])) if int(row[1]) > 5 else round(float(row[1]), 1))
            region_output_list.append(region_output)
        return region_output_list

def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
init_db(DBNAME)
def interactive_prompt():
    init_db(DBNAME)
    help_text = load_help_text()
    response = ''
    while response.lower() != 'exit':
        response = input('Enter a command: ')

        if response.lower() == 'help':
            print(help_text)
            continue
        if response.lower() == 'exit':
            print('bye')
            break
        if 'bars' or 'companies' or 'countries' or 'regions' in response:
            try:
                commresponse = process_command(response)
                if len(commresponse[0]) == 6:
                    for x in commresponse:
                        proper_print_list = []
                        for thing in x:
                            working_string = str(thing)
                            if len(working_string) > 12:
                                working_string = working_string.replace(working_string[10:], '...')
                            proper_print_list.append(working_string)
                        bars_formatted = '{0:15} {1:15} {2:15} {3:5} {4:5} {5:5}'.format(*proper_print_list)
                        print(bars_formatted)

                if len(commresponse[0]) == 3:
                    for x in commresponse:
                        count_proper_print_list = []
                        for thing in x:
                            count_working_string = str(thing)
                            if len(count_working_string) > 12:
                                count_working_string = count_working_string.replace(count_working_string[10:], '...')
                            count_proper_print_list.append(count_working_string)
                        count_formatted = '{0:15} {1:15} {2:15}'.format(*count_proper_print_list)
                        print(count_formatted)

                if len(commresponse[0]) == 2:
                    for x in commresponse:
                        region_proper_print_list = []
                        for thing in x:
                            region_working_string = str(thing)
                            if len(region_working_string) > 12:
                                region_working_string = region_working_string.replace(region_working_string[10:], '...')
                            region_proper_print_list.append(region_working_string)
                        region_formatted = '{0:15} {1:15}'.format(*region_proper_print_list)
                        print(region_formatted)
            except:
                print('Command not recognized: {}'.format(response))

        else:
            print('Command not recognized: {}'.format(response))

if __name__=="__main__":
    interactive_prompt()
