from pydantic import BaseModel
from typing import List, Optional

# Modelos Pydantic para validação de dados de perfil.
class PerfilBase(BaseModel):
    idade: int
    endereco: str

class PerfilCreate(PerfilBase):
    pass

class PerfilResponse(PerfilBase):
    # Permite construir respostas diretamente a partir de objetos ORM.
    class Config:
        from_attributes = True

# Modelos Pydantic para validação de dados de estudante.
class EstudanteBase(BaseModel):
    nome: str
    email: Optional[str] = None

class EstudanteCreate(EstudanteBase):
    perfil: PerfilCreate

class EstudanteResponse(EstudanteBase):
    id: int
    perfil: Optional[PerfilResponse] = None

    class Config:
        from_attributes = True

# Modelos Pydantic para validação de dados de professor.
class ProfessorBase(BaseModel):
    nome: str
    email: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorResponse(ProfessorBase):
    id: int

    class Config:
        from_attributes = True

class DisciplinaBase(BaseModel):
    nome: str
    professor_id: Optional[int] = None

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id: int

    class Config:
        from_attributes = True

class MatriculaBase(BaseModel):
    estudante_id: int
    disciplina_id: int

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaResponse(BaseModel):
    id: int
    estudante_nome: Optional[str] = None
    disciplina_nome: Optional[str] = None
    professor_nome: Optional[str] = None

    class Config:
        from_attributes = True