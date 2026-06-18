from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel, Field
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware


engine = create_engine("sqlite:///./testDatabase.db",connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

# Modelos
class Livro(base):
    __tablename__ = "Livros"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    autor = Column(String)
    editora = Column(String)
    ano = Column(Integer)
    edicao = Column(Integer)
    numero_pags = Column(Integer)
    categoria = Column(String)
    idioma = Column(String)
    emprestimo = Column(Integer, nullable=True)

class Aluno(base):
    __tablename__= "Alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso = Column(String)
    email = Column(String)
    endereco = Column(String)
    telefone = Column(String)

class Emprestimo(base):
    __tablename__ = "Emprestimos"

    id = Column(Integer, primary_key=True)
    aluno = Column(Integer, ForeignKey('Alunos.id'), nullable=False)
    livro = Column(Integer, ForeignKey('Livros.id'), nullable=False)
#     dta_emprestimo = Column
#     dta_devolucao = Column


base.metadata.create_all(bind=engine)

#Schema Livro
class LivroCreate(BaseModel):

    nome: str
    autor: str
    editora: str
    ano: int
    edicao: int
    numero_pags: int
    categoria: str
    idioma: str
    emprestimo: Optional[int] = None

class LivroResponse(BaseModel):

    id: int
    nome: str
    autor: str
    editora: str
    ano: int
    edicao: int
    numero_pags: int
    categoria: str
    idioma: str
    emprestimo: Optional[int]

    class Config:
        orm_mode = True

#Schema Aluno
class AlunoCreate(BaseModel):

    nome: str
    curso: str
    email: str
    endereco: str
    telefone: str

class AlunoResponse(BaseModel):

    id: int
    nome: str
    curso: str
    email: str
    endereco: str
    telefone: str

    class Config:
        orm_mode = True

#Schema Empréstimo
class EmprestimoCreate(BaseModel):

    aluno: int
    livro: int

class EmprestimoResponse(BaseModel):

    id: int
    aluno: int
    livro: int

    class Config:
        orm_mode = True

#SessionLocaal
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

#CRUD LIVRO
#CREATE
def create_livro(db: Session, livro: LivroCreate):
    db_livro = Livro(            
    nome = livro.nome,
    autor = livro.autor,
    editora = livro.editora,
    ano = livro.ano,
    edicao = livro.edicao,
    numero_pags = livro.numero_pags,
    categoria = livro.categoria,
    idioma = livro.idioma
    )
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

#Get id
def get_livro(db:Session, livro_id: int):
    return db.query(Livro).filter(Livro.id == livro_id).first()

#GET *
def get_livros(db: Session):
    return db.query(Livro).all()

#UpD8
def update_livro(db:Session, livro_id: int, livro: LivroCreate):
    db_livro = get_livro(db, livro_id)
    if db_livro is None:
        return None
    db_livro.nome = livro.nome
    db_livro.autor = livro.autor
    db_livro.editora = livro.editora
    db_livro.ano = livro.ano
    db_livro.edicao = livro.edicao
    db_livro.numero_pags = livro.numero_pags
    db_livro.categoria = livro.categoria
    db_livro.idioma = livro.idioma
    db.commit()
    db.refresh(db_livro)
    return db_livro

#CRUD ALUNO
#CREATE
def create_aluno(db: Session, aluno: AlunoCreate):
    db_aluno = Aluno(
        nome = aluno.nome,
        curso = aluno.curso,
        email = aluno.email,
        endereco = aluno.endereco,
        telefone = aluno.telefone
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

#Get *
def get_alunos(db:Session):
    return db.query(Aluno).all()

#get id
def get_aluno(db: Session, aluno_id: int,):
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()

#upd8
def update_aluno(db: Session, aluno_id: int, aluno: AlunoCreate):
    db_aluno = get_aluno(db,aluno_id)
    if db_aluno is None:
        return None
    db_aluno.nome = aluno.nome
    db_aluno.curso = aluno.curso
    db_aluno.email = aluno.email
    db_aluno.endereco = aluno.endereco
    db_aluno.telefone = aluno.telefone
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

#CRUD EMPRÉSTIMO
#CREATE
def create_emprestimo(db: Session, emprestimo:EmprestimoCreate):
    db_emprestimo = Emprestimo(
        aluno = emprestimo.aluno,
        livro = emprestimo.livro
    )
    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

#GET *
def get_emprestimos(db):
    return db.query(Emprestimo).all()

#Get_id
def get_emprestimo(db, emprestimo_id):
    return db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()


#API Endpoints
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ROTAs-Livros
@app.post("/livros/", response_model=LivroResponse)
def create_livro_endpoint(livro: LivroCreate, db: Session = Depends(get_db)):
    return create_livro(db, livro)

@app.get("/livros/", response_model=list[LivroResponse])
def get_livros_endpoint(db: Session = Depends(get_db)):
    return get_livros(db)

@app.get("/livros/{livro_id}", response_model=LivroResponse)
def get_livro_endpoint(livro_id: int, db: Session = Depends(get_db)):
    db_livro = get_livro(db, livro_id)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@app.put("/livros/{livro_id}", response_model=LivroResponse)
def update_livro_endpoint(livro_id: int, livro:LivroCreate, db: Session = Depends(get_db)):
    db_livro = update_livro(db, livro_id, livro)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro
    

#ROTAS-Alunos
@app.post("/alunos/", response_model=AlunoResponse)
def create_aluno_endpoint(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return create_aluno(db, aluno)

@app.get("/alunos/", response_model=list[AlunoResponse])
def get_alunos_endpoint(db: Session = Depends(get_db)):
    return get_alunos(db)

@app.get("/alunos/{aluno_id}", response_model=AlunoResponse)
def get_aluno_endpoint(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@app.put("/alunos/{aluno_id}", response_model=AlunoResponse)
def pootis_aluno_endpoint(aluno_id: int, aluno: AlunoCreate ,db: Session = Depends(get_db)):
    db_aluno = update_aluno(db, aluno_id, aluno)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno


#ROTAS-EMprestimo
@app.post("/emprestimos/", response_model=EmprestimoResponse)
def create_emprestimo_endpoint(emprestimo: EmprestimoCreate, db: Session = Depends(get_db)):
    return create_emprestimo(db, emprestimo)

@app.get('/emprestimos/', response_model=list[EmprestimoResponse])
def get_emprestimos_enpoint(db: Session = Depends(get_db)):
    db_emprestimos = get_emprestimos(db)
    if db_emprestimos is None:
        raise HTTPException(status_code=404, detail="Nenhum Empréstimo foim encontrado")
    return db_emprestimos

@app.get("/emprestimos/{emprestimo_id}", response_model=EmprestimoResponse)
def get_emprestismo_endpoint(emprestimo_id: int,db: Session = Depends(get_db)):
    db_emprestimo =  get_emprestimo(db, emprestimo_id)
    if db_emprestimo is None:
        raise HTTPException(status_code=404, detail="Emprestimo não encontrado")
    return db_emprestimo