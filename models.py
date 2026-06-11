from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class Estudante(Base):
    __tablename__ = 'estudantes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String)

    # Relacionamento um-para-um com Perfil.
    # O perfil é excluído automaticamente quando o estudante é removido.
    perfil = relationship(
        "Perfil",
        back_populates="estudante",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Relacionamento de um estudante para muitas matrículas.
    matriculas = relationship(
        "Matricula",
        back_populates="estudante",
        cascade="all, delete-orphan"
    )

class Perfil(Base):
    __tablename__ = 'perfis'
    estudante_id = Column(Integer, ForeignKey("estudantes.id"), primary_key=True)
    idade = Column(Integer)
    endereco = Column(String)

    # Perfil compartilha a chave primária do estudante.
    estudante = relationship(
        "Estudante",
        back_populates='perfil'
    )

class Professor(Base):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String)

    disciplinas = relationship(
        "Disciplina",
        back_populates="professor"
    )

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=True)

    professor = relationship("Professor", back_populates="disciplinas")
    matriculas = relationship(
        "Matricula",
        back_populates="disciplina",
        cascade="all, delete-orphan"
    )

class Matricula(Base):
    __tablename__ = 'matriculas'
    id = Column(Integer, primary_key=True, index=True)

    estudante_id = Column(Integer, ForeignKey('estudantes.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))

    estudante = relationship("Estudante", back_populates="matriculas")
    disciplina = relationship("Disciplina", back_populates="matriculas")

    @property
    def estudante_nome(self):
        return self.estudante.nome if self.estudante else None

    @property
    def disciplina_nome(self):
        return self.disciplina.nome if self.disciplina else None

    @property
    def professor_nome(self):
        return self.disciplina.professor.nome if self.disciplina and self.disciplina.professor else None