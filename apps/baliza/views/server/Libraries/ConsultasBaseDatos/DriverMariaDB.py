import MySQLdb


class MariaDB:
    def __init__(self, HOST, USER, PWD, DB):
        self.miConexion = MySQLdb.connect(host=HOST, user=USER, passwd=PWD, db=DB)
        self.cursorDB = self.miConexion.cursor()

    def EjecutarConsulta(self, consulta):
        self.cursorDB.execute(consulta)
        response = self.cursorDB.fetchall()
        return response

    def Insertar(self, comandoMySql):
        self.cursorDB.execute(comandoMySql)
        self.miConexion.commit()
        id = self.cursorDB.lastrowid
        return id

    def CloseConection(self):
        self.miConexion.close()
