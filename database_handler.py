import csv
import sqlite3

import csv, sqlite3

class DatabaseHandler():
    def __init__(self):
        self.conn = sqlite3.connect("stations.db")
    
    def check_station(self,station_name):
        query = """SELECT * FROM stations WHERE (longname = '"""+station_name+"""')
                                          OR (longname LIKE '"""+station_name+""" %')
                                          OR (longname LIKE '% """+station_name+"""')
                                          OR (longname LIKE '% """+station_name+""" %');"""
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if len(rows)==0:
            return False
        return rows

    def get_station_code(self,station_name):
        query = """SELECT code FROM stations
                WHERE name='"""+station_name+"""';"""
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows[0][0]

    def create_table(self,statement):
        cur = self.conn.cursor()
        cur.execute(statement)

    def add_station(self,station):
        sql = ''' INSERT INTO stations(name,longname,code,tiploc)
              VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, station)
        self.conn.commit()
        return cur.lastrowid
        
        
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    stations_database = DatabaseHandler()

    # create_table_query = """ CREATE TABLE IF NOT EXISTS stations (
    #                     id integer PRIMARY KEY,
    #                     name text NOT NULL,
    #                     longname text NOT NULL,
    #                     code text NOT NULL,
    #                     tiploc integer NOT NULL
    #                     ); """
    # stations_database.create_table(create_table_query)
    # import csv
    # import re
    # array = []
    # with open("stations.csv",newline='') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',',)
    #     skipfirst=True
    #     for row in reader:
    #         if skipfirst:
    #             skipfirst=False
    #             pass
    #         else:
    #             station = (row[0]).lower()
    #             station=re.sub("['\(\)]","",station)
    #             station_longname = (row[1]).lower()
    #             if station_longname == "\\n":
    #                 station_longname=station
    #             station_longname=re.sub("['\(\)]","",station_longname)
    #             station = (station,station_longname,row[3],row[4])
    #             stations_database.add_station(station)
    # print("Table has been created and populated")

    station = ("norwich", "norwich", "Norwich", "Norwich")
    stations_database.add_station(station)
    stations_database.close()