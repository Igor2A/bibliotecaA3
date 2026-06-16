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
def get_livros(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Livro).offset(skip).limit(limit).all()

#UpD8
def update_livro(db:Session, livro_id: int, livro: LivroCreate):
    db_livro = get_livro(db, livro_id)
    if db_livro is None:
        return None
    db_livro.nome = livro.nome,
    db_livro.autor = livro.autor,
    db_livro.editora = livro.editora,
    db_livro.ano = livro.ano,
    db_livro.edicao = livro.edicao,
    db_livro.numero_pags = livro.numero_pags,
    db_livro.categoria = livro.categoria,
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
@app.post("/livro/", response_model=LivroResponse)
def create_livro_endpoint(livro: LivroCreate, db: Session = Depends(get_db)):
    return create_livro(db, livro)

@app.get("/livro/", response_model=list[LivroResponse])
def get_livros_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_livros(db, skip=skip, limit=limit)

@app.get("/livro/{livro_id}", response_model=LivroResponse)
def get_livro_endpoint(livro_id: int, db: Session = Depends(get_db)):
    db_livro = get_livro(db, livro_id)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@app.put("/livro/{livro_id}", response_model=LivroResponse)
def update_livro_endpoint(livro_id: int, livro:LivroCreate, db: Session = Depends(get_db)):
    db_livro = update_livro(db, livro_id, livro)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro
    

#ROTAS-Alunos
@app.post("/aluno/", response_model=AlunoResponse)
def create_aluno_endpoint(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return create_aluno(db, aluno)

#ROTAS-EMprestimo
@app.post("/emprestimo/", response_model=EmprestimoResponse)
def create_emprestimo_endpoint(emprestimo: EmprestimoCreate, db: Session = Depends(get_db)):
    return create_emprestimo(db, emprestimo)