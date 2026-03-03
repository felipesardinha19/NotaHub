import bcrypt
from app.models.usuarios import Usuarios
from app.repositories.usuario_repository import UsuarioRepository

class AuthService:

    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def registrar(self, nome: str, email: str, senha: str) -> int:
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

        usuario = Usuarios(
            nome=nome,
            email=email,
            senha_hash=senha_hash
        )

        return self.usuario_repo.criar(usuario)
        
    def autenticar(self, email: str, senha: str) -> Usuarios | None:
        usuario = self.usuario_repo.buscar_por_email(email)

        if not usuario:
            return None
        
        if bcrypt.checkpw(senha.encode(), usuario.senha_hash.encode()):
            return usuario
        
        return None