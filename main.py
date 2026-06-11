from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
import models
import schemas
from database import SessionLocal, engine

# O `engine` conecta ao PostgreSQL e `SessionLocal` cria sessões SQLAlchemy.
# `joinedload` é usado para carregar relacionamentos no mesmo SELECT quando necessário.
# `create_all` garante que as tabelas sejam criadas se ainda não existirem.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def homepage():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>API Escola</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f7fb; color: #333; }
        header { background: #2f6fed; color: white; padding: 24px 32px; text-align: center; }
        h1 { margin: 0; font-size: 2rem; }
        .subtitle { margin-top: 8px; color: #dbe5ff; }
        .container { max-width: 1200px; margin: 24px auto; padding: 0 16px; }
        .grid { display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
        .card { background: white; border-radius: 16px; box-shadow: 0 10px 28px rgba(15,23,42,.08); padding: 20px; }
        .card h2 { margin-top: 0; font-size: 1.2rem; }
        .code { font-family: monospace; background: #eef4ff; padding: 10px 12px; border-radius: 10px; display: block; margin-bottom: 14px; }
        .button, .submit-button { display: inline-block; margin-top: 12px; padding: 10px 16px; border-radius: 999px; border: none; background: #2f6fed; color: white; cursor: pointer; transition: background .2s ease; }
        .button:hover, .submit-button:hover { background: #214bbd; }
        .output { white-space: pre-wrap; font-family: monospace; background: #f7f9fd; border-radius: 12px; padding: 12px; min-height: 120px; overflow-x: auto; }
        .form-row { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
        .input { padding: 10px 12px; border-radius: 10px; border: 1px solid #d2d8e0; font-size: 0.95rem; }
        label { font-weight: bold; font-size: 0.95rem; }
        .section { margin-bottom: 20px; }
      </style>
    </head>
    <body>
      <header>
        <h1>API Escola</h1>
        <p class="subtitle">Painel interativo para consultar e cadastrar estudantes, professores, disciplinas e matrículas.</p>
      </header>
      <div class="container">
        <div class="grid">
          <div class="card">
            <h2>Estudantes</h2>
            <code class="code">GET /estudantes/</code>
            <button type="button" class="button" onclick="loadData('estudantes')">Carregar</button>
            <div id="estudantes" class="output">Clique em carregar.</div>
            <div class="section">
              <h3>Cadastrar estudante</h3>
              <div class="form-row">
                <label for="estudante-nome">Nome</label>
                <input id="estudante-nome" class="input" type="text" placeholder="Nome" />
                <label for="estudante-email">Email</label>
                <input id="estudante-email" class="input" type="email" placeholder="Email" />
                <label for="estudante-idade">Idade</label>
                <input id="estudante-idade" class="input" type="number" placeholder="Idade" />
                <label for="estudante-endereco">Endereço</label>
                <input id="estudante-endereco" class="input" type="text" placeholder="Endereço" />
                <button class="submit-button" onclick="submitForm('estudantes')">Enviar estudante</button>
              </div>
              <div class="form-row">
                <label for="estudante-delete-id">Excluir estudante ID</label>
                <input id="estudante-delete-id" class="input" type="number" placeholder="ID do estudante" />
                <button class="submit-button" onclick="deleteItem('estudantes')">Excluir estudante</button>
              </div>
            </div>
          </div>
          <div class="card">
            <h2>Professores</h2>
            <code class="code">GET /professores/</code>
            <button type="button" class="button" onclick="loadData('professores')">Carregar</button>
            <div id="professores" class="output">Clique em carregar.</div>
            <div class="section">
              <h3>Cadastrar professor</h3>
              <div class="form-row">
                <label for="professor-nome">Nome</label>
                <input id="professor-nome" class="input" type="text" placeholder="Nome" />
                <label for="professor-email">Email</label>
                <input id="professor-email" class="input" type="email" placeholder="Email" />
                <button class="submit-button" onclick="submitForm('professores')">Enviar professor</button>
              </div>
              <div class="form-row">
                <label for="professor-delete-id">Excluir professor ID</label>
                <input id="professor-delete-id" class="input" type="number" placeholder="ID do professor" />
                <button class="submit-button" onclick="deleteItem('professores')">Excluir professor</button>
              </div>
            </div>
          </div>
          <div class="card">
            <h2>Disciplinas</h2>
            <code class="code">GET /disciplinas/</code>
            <button type="button" class="button" onclick="loadData('disciplinas')">Carregar</button>
            <div id="disciplinas" class="output">Clique em carregar.</div>
            <div class="section">
              <h3>Cadastrar disciplina</h3>
              <div class="form-row">
                <label for="disciplina-nome">Nome</label>
                <input id="disciplina-nome" class="input" type="text" placeholder="Nome" />
                <label for="disciplina-professor-id">Professor ID (opcional)</label>
                <input id="disciplina-professor-id" class="input" type="number" placeholder="Professor ID" />
                <button class="submit-button" onclick="submitForm('disciplinas')">Enviar disciplina</button>
              </div>
              <div class="form-row">
                <label for="disciplina-delete-id">Excluir disciplina ID</label>
                <input id="disciplina-delete-id" class="input" type="number" placeholder="ID da disciplina" />
                <button class="submit-button" onclick="deleteItem('disciplinas')">Excluir disciplina</button>
              </div>
            </div>
          </div>
          <div class="card">
            <h2>Matriculas</h2>
            <code class="code">GET /matriculas/</code>
            <button type="button" class="button" onclick="loadData('matriculas')">Carregar</button>
            <div id="matriculas" class="output">Clique em carregar.</div>
            <div class="section">
              <h3>Cadastrar matrícula</h3>
              <div class="form-row">
                <label for="matricula-estudante-id">Estudante ID</label>
                <input id="matricula-estudante-id" class="input" type="number" placeholder="Estudante ID" />
                <label for="matricula-disciplina-id">Disciplina ID</label>
                <input id="matricula-disciplina-id" class="input" type="number" placeholder="Disciplina ID" />
                <button class="submit-button" onclick="submitForm('matriculas')">Enviar matrícula</button>
              </div>
              <div class="form-row">
                <label for="matricula-delete-id">Excluir matrícula ID</label>
                <input id="matricula-delete-id" class="input" type="number" placeholder="ID da matrícula" />
                <button class="submit-button" onclick="deleteItem('matriculas')">Excluir matrícula</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <script>
        window.loadData = async function(resource) {
          const target = document.getElementById(resource);
          target.textContent = 'Carregando...';
          try {
            const response = await fetch(`/${resource}/`);
            if (!response.ok) {
              target.textContent = `Erro: ${response.status} ${response.statusText}`;
              return;
            }
            const json = await response.json();
            target.textContent = JSON.stringify(json, null, 2);
          } catch (error) {
            target.textContent = `Falha ao carregar: ${error}`;
          }
        }

        window.submitForm = async function(resource) {
          const data = {};
          if (resource === 'estudantes') {
            data.nome = document.getElementById('estudante-nome').value;
            data.email = document.getElementById('estudante-email').value || null;
            data.perfil = {
              idade: Number(document.getElementById('estudante-idade').value) || 0,
              endereco: document.getElementById('estudante-endereco').value || ''
            };
          } else if (resource === 'professores') {
            data.nome = document.getElementById('professor-nome').value;
            data.email = document.getElementById('professor-email').value || null;
          } else if (resource === 'disciplinas') {
            data.nome = document.getElementById('disciplina-nome').value;
            const professorId = document.getElementById('disciplina-professor-id').value;
            if (professorId) {
              data.professor_id = Number(professorId);
            }
          } else if (resource === 'matriculas') {
            data.estudante_id = Number(document.getElementById('matricula-estudante-id').value);
            data.disciplina_id = Number(document.getElementById('matricula-disciplina-id').value);
          }

          const target = document.getElementById(resource);
          target.textContent = 'Enviando...';

          try {
            const response = await fetch(`/${resource}/`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(data)
            });
            if (!response.ok) {
              const errorText = await response.text();
              target.textContent = `Erro: ${response.status} ${response.statusText} - ${errorText}`;
              return;
            }
            const json = await response.json();
            target.textContent = 'Cadastrado com sucesso: ' + JSON.stringify(json, null, 2);
          } catch (error) {
            target.textContent = `Falha ao enviar: ${error}`;
          }
        }

        window.deleteItem = async function(resource) {
          let id = null;
          if (resource === 'estudantes') {
            id = document.getElementById('estudante-delete-id').value;
          } else if (resource === 'professores') {
            id = document.getElementById('professor-delete-id').value;
          } else if (resource === 'disciplinas') {
            id = document.getElementById('disciplina-delete-id').value;
          } else if (resource === 'matriculas') {
            id = document.getElementById('matricula-delete-id').value;
          }

          const target = document.getElementById(resource);
          if (!id) {
            target.textContent = 'Informe um ID para excluir.';
            return;
          }

          target.textContent = 'Excluindo...';
          try {
            const response = await fetch(`/${resource}/${id}`, {
              method: 'DELETE'
            });
            if (!response.ok) {
              const errorText = await response.text();
              target.textContent = `Erro: ${response.status} ${response.statusText} - ${errorText}`;
              return;
            }
            target.textContent = `Excluído com sucesso: ${id}`;
          } catch (error) {
            target.textContent = `Falha ao excluir: ${error}`;
          }
        }
      </script>
    </body>
    </html>
    """


def get_db():
    """Dependência FastAPI que cria e finaliza uma sessão de banco por requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/estudantes/', response_model=schemas.EstudanteResponse)
def criar_estudante(estudante: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    """Cria um estudante e seu perfil associado no banco de dados."""
    db_estudante = models.Estudante(
        nome=estudante.nome,
        email=estudante.email,
        perfil=models.Perfil(**estudante.perfil.model_dump())
    )
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante

@app.get('/estudantes/', response_model=List[schemas.EstudanteResponse])
def listar_estudantes(db: Session = Depends(get_db)):
    """Retorna todos os estudantes com seus perfis."""
    estudantes = db.query(models.Estudante).options(
        joinedload(models.Estudante.perfil)
    ).all()
    return estudantes

@app.delete('/estudantes/{estudante_id}')
def excluir_estudante(estudante_id: int, db: Session = Depends(get_db)):
    """Exclui um estudante e também seu perfil e matrículas relacionadas."""
    estudante = db.query(models.Estudante).filter(models.Estudante.id == estudante_id).first()
    if not estudante:
        raise HTTPException(status_code=404, detail='Estudante não encontrado')
    db.delete(estudante)
    db.commit()
    return {'detail': 'Estudante excluído'}

@app.post('/professores/', response_model=schemas.ProfessorResponse)
def criar_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    """Cria um novo professor no sistema."""
    db_professor = models.Professor(
        nome=professor.nome,
        email=professor.email
    )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get('/professores/', response_model=List[schemas.ProfessorResponse])
def listar_professores(db: Session = Depends(get_db)):
    """Lista todos os professores cadastrados."""
    return db.query(models.Professor).all()

@app.delete('/professores/{professor_id}')
def excluir_professor(professor_id: int, db: Session = Depends(get_db)):
    """Exclui um professor pelo ID."""
    professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail='Professor não encontrado')
    db.delete(professor)
    db.commit()
    return {'detail': 'Professor excluído'}

@app.post('/disciplinas/', response_model=schemas.DisciplinaResponse)
def criar_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    """Cria uma disciplina e associa um professor opcionalmente."""
    if disciplina.professor_id is not None:
        professor = db.query(models.Professor).filter(models.Professor.id == disciplina.professor_id).first()
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")

    db_disciplina = models.Disciplina(
        nome=disciplina.nome,
        professor_id=disciplina.professor_id
    )
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@app.get('/disciplinas/', response_model=List[schemas.DisciplinaResponse])
def listar_disciplinas(db: Session = Depends(get_db)):
    """Lista todas as disciplinas disponíveis."""
    return db.query(models.Disciplina).all()

@app.delete('/disciplinas/{disciplina_id}')
def excluir_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    """Exclui uma disciplina pelo ID."""
    disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail='Disciplina não encontrada')
    db.delete(disciplina)
    db.commit()
    return {'detail': 'Disciplina excluída'}

@app.post('/matriculas/', response_model=schemas.MatriculaResponse)
def criar_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    """Cria uma matrícula para um estudante em uma disciplina."""
    estudante = db.query(models.Estudante).filter(models.Estudante.id == matricula.estudante_id).first()
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == matricula.disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    db_matricula = models.Matricula(
        estudante_id=matricula.estudante_id,
        disciplina_id=matricula.disciplina_id
    )
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@app.get('/matriculas/', response_model=List[schemas.MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    """Retorna todas as matrículas com nomes de estudante, disciplina e professor."""
    return db.query(models.Matricula).options(
        joinedload(models.Matricula.estudante),
        joinedload(models.Matricula.disciplina).joinedload(models.Disciplina.professor)
    ).all()

@app.delete('/matriculas/{matricula_id}')
def excluir_matricula(matricula_id: int, db: Session = Depends(get_db)):
    """Exclui uma matrícula pelo ID."""
    matricula = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail='Matrícula não encontrada')
    db.delete(matricula)
    db.commit()
    return {'detail': 'Matrícula excluída'}