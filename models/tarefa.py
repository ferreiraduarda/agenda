from sqlite3 import Cursor
from models.database import Database
from typing import Any, Self, Optional
from datetime import datetime


class Tarefa:
    """
        Classe para representar uma tarefa, com métodos para salvar, obter, excluir e atualizar tarefas em um banco de dados usando a classe `Database`.
    """
    def __init__(self: Self, titulo_tarefa: Optional[str], data_conclusao: Optional[str] = None, id_tarefa: Optional[int] = None) -> None:
        self.titulo_tarefa: Optional[str] = titulo_tarefa
        self.data_conclusao: Optional[str] = data_conclusao
        self.id_tarefa: Optional[int] = id_tarefa

    # Tarefa(titulo_tarefa="Nova tarefa")
    # Tarefa(titulo_tarefa="Outra tarefa", data_conclusao="2026-02-03")
    # Tarefa(id-1)
    @property
    def concluida(self) -> bool:
        return self.data_conclusao is not None
    
    @classmethod
    def id(cls, id: int) -> Self:
        with Database() as db:
            query: str = 'SELECT titulo_tarefa, data_conclusao FROM tarefas WHERE id = ?;'
            params: tuple = (id,)
            resultado: list[Any] = db.buscar_tudo(query, params)
            # Desempacotamento de coleção

            [[titulo, data]] = resultado

        return cls(id_tarefa=id, titulo_tarefa=titulo, data_conclusao=data)

    # Simulando o conceito de sobrecarga
    # Tarefa('Título da tarefa')
    # Tarefa('Título da tarefa', '2026-02-03')
    # Tarefa.id(1)


    def salvar_tarefa(self) -> None:
        if self.data_conclusao == "":
            self.data_conclusao = None

        with Database() as db:
            query = """
            INSERT INTO tarefas (titulo_tarefa, data_conclusao)
            VALUES (?, ?);
            """
            params = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls):
        with Database() as db:
            query = 'SELECT titulo_tarefa, data_conclusao, id FROM tarefas;'
            resultados: list[Any] = db.buscar_tudo(query)
            tarefas: list[Self] = [cls(titulo, data, id) for titulo, data, id in resultados]
            return tarefas
        
    def excluir_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = 'DELETE FROM tarefas WHERE id = ?;'
            params: tuple = (self.id_tarefa,)
            resultado: Cursor = db.executar(query, params)
            return resultado
        
    def atualizar_tarefa(self) -> Cursor:
        if self.data_conclusao == "":
            self.data_conclusao = None

        with Database() as db:
            query: str = """
            UPDATE tarefas
            SET titulo_tarefa = ?, data_conclusao = ?
            WHERE id = ?;
            """
            params: tuple = (
                self.titulo_tarefa,
                self.data_conclusao,
                self.id_tarefa
            )

        resultado: Cursor = db.executar(query, params)

        return resultado
        
    def alterar_status(self) -> Cursor:

        with Database() as db:
            query_verificar = "SELECT data_conclusao FROM tarefas WHERE id = ?;"
            resultado = db.buscar_tudo(query_verificar, (self.id_tarefa,))

            data = resultado[0][0]
            if data is None:
                nova_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = """
                UPDATE tarefas
                SET data_conclusao = ?
                WHERE id = ?;
                """
                params = (nova_data, self.id_tarefa)
            else:
                query = """
                UPDATE tarefas
                SET data_conclusao = NULL
                WHERE id = ?;
                """
                params = (self.id_tarefa,)
            resultado_cursor = db.executar(query, params)

            return resultado_cursor