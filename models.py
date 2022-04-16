from abc import ABC, abstractmethod
from atexit import register
from colorsys import yiq_to_rgb
from ctypes import resize
import datetime
from re import L
from tkinter.messagebox import RETRY
import traceback
from settings import db_path
import sqlite3


class BaseModel(ABC):

    def __init__(self, id=None) -> None:
        self.id = id
        self.__isValid = True

    @property
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    @abstractmethod
    def print():
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def objects():
        pass

    @classmethod
    @abstractmethod
    def get_by_id(id):
        pass


class Region(BaseModel):
    table = 'Regions'

    def __init__(self, name, id=None) -> None:
        super().__init__(id)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Region.table} ('Name')
                                VALUES ('{self.name}')
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row
                            conn.execute(f'''
                                UPDATE {Region.table} set Name = '{self.name}' where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Region.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Region.table}
                """
                for row in cursor.execute(query):
                    yield Region(row[1], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Region.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Region(res[1], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.name}'


class District(BaseModel):
    table = 'Districts'

    def __init__(self, name, regionId, id=None) -> None:
        super().__init__(id)
        self.name = name
        self.regionId = regionId

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    @property
    def regionId(self):
        return self.__regionId

    @regionId.setter
    def regionId(self, regionId):
        if isinstance(regionId, int) and Region.get_by_id(regionId) is not None:
            self.__regionId = regionId
        else:
            self.__regionId = None
            self.__isValid = False

    @property
    def region(self):
        return Region.get_by_id(self.regionId)

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {District.table} ('Name', RegionId)
                                VALUES ('{self.name}', {self.regionId})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {District.table} set Name = '{self.name}', RegionId={self.regionId} where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {District.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {District.table}
                """
                for row in cursor.execute(query):
                    yield District(row[1], row[2], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {District.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return District(res[1], res[2], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.region}\t | {self.name}'


class Student(BaseModel):
    table = 'Students'

    def __init__(self, fam, ism, tug_yil, mark, level, distictid, id=None) -> None:
        super().__init__(id)
        self.fam = fam
        self.ism = ism
        self.tug_yil = tug_yil
        self.mark = mark
        self.level = level
        self.distictid = distictid

    @property
    def fam(self):
        return self.__fam

    @fam.setter
    def fam(self, fam):
        if isinstance(fam, str):
            self.__fam = fam
        else:
            self.__fam = ''
            self.__isValid = False

    @property
    def ism(self):
        return self.__ism

    @ism.setter
    def ism(self, ism):
        if isinstance(ism, str):
            self.__ism = ism
        else:
            self.__ism = ''
            self.__isValid = False

    @property
    def tug_yil(self):
        return self.__tug_yil

    @tug_yil.setter
    def tug_yil(self, tug_yil):
        if isinstance(tug_yil, int):
            self.__tug_yil = tug_yil
        else:
            self.__tug_yil = 0
            self.__isValid = False

    @property
    def mark(self):
        return self.__mark

    @mark.setter
    def mark(self, mark):
        if isinstance(mark, int):
            self.__mark = mark
        else:
            self.__mark = 0
            self.__isValid = False

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        if isinstance(level, int):
            self.__level = level
        else:
            self.__level = 0
            self.__isValid = False

    @property
    def distictid(self):
        return self.__distictid

    @distictid.setter
    def distictid(self, distictid):
        if isinstance(distictid, int):
            self.__distictid = distictid
        else:
            self.__distictid = 0
            self.__isValid = False

    @property
    def district(self):
        return District.get_by_id(self.distictid)

    def del_by_id(id):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Student.table} where Id = {id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Student.table} (Fam, Ism, Tug_yili, Mark, Level, DistrctId)
                                VALUES ('{self.fam}', '{self.ism}', {self.tug_yil}, {self.mark}, {self.level}, {self.distictid})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Student.table} set
                                Fam = '{self.fam}',
                                Ism = '{self.ism}',
                                Tug_yili = {self.tug_yil},
                                Mark = {self.mark},
                                Level = {self.level},
                                DistrctId = {self.distictid}
                                where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                        raise
                return True
            except:
                print('Bog\'lanishda xatolik')
                raise

        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Student.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Student.table}
                """
                for row in cursor.execute(query):
                    yield Student(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        except:
            traceback.print_exc()
            print('Bog\'lanishda xatolik')

    def print():
        pass

    def get_by_id(id):
        pass
