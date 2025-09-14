from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func, extract, case

db = SQLAlchemy()

class Area(db.Model):
    __tablename__ = "areas"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    usuarios = db.relationship('Usuario', backref='area', lazy=True)
    pqrsd = db.relationship('PQRSD', backref='area', lazy=True)

    def __repr__(self):
        return f"<Area {self.nombre}>"


class Rol(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)
    
    def __repr__(self):
        return f"<Rol {self.nombre}>"


class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    historial = db.relationship('Historial', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nombre} - Rol {self.rol.nombre}>"


class PQRSD(db.Model):
    __tablename__ = "pqrsd"
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False) 
    descripcion = db.Column(db.Text, nullable=False)
    solicitante_nombre = db.Column(db.String(200), nullable=False)
    solicitante_identificacion = db.Column(db.String(50), nullable=False)
    solicitante_contacto = db.Column(db.String(200), nullable=False)
    medio = db.Column(db.String(20), nullable=False)
    tipo_peticionario = db.Column(db.String(50), nullable=False, default="Persona natural")
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    prioridad = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    fecha_limite = db.Column(db.DateTime, nullable=False)
    fecha_resolucion = db.Column(db.DateTime, nullable=True)
    respuesta = db.Column(db.Text, nullable=True)
    
    historial = db.relationship('Historial', backref='pqrsd', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PQRSD {self.id} {self.tipo}>"

    # ---------------------------
    # Métodos para dashboard
    # ---------------------------

    @staticmethod
    def volumen_por_periodo(periodo="mes"):
        if periodo == "mes":
            resultados = db.session.query(
                extract('year', PQRSD.fecha_creacion).label("año"),
                extract('month', PQRSD.fecha_creacion).label("mes"),
                func.count(PQRSD.id).label("total")
            ).group_by("año", "mes").all()
            return {f"{int(r.mes)}/{int(r.año)}": r.total for r in resultados}

        elif periodo == "trimestre":
            resultados = db.session.query(
                extract('year', PQRSD.fecha_creacion).label("año"),
                ((extract('month', PQRSD.fecha_creacion)-1)//3 + 1).label("trimestre"),
                func.count(PQRSD.id).label("total")
            ).group_by("año", "trimestre").all()
            return {f"T{int(r.trimestre)}/{int(r.año)}": r.total for r in resultados}

        elif periodo == "semestre":
            resultados = db.session.query(
                extract('year', PQRSD.fecha_creacion).label("año"),
                ((extract('month', PQRSD.fecha_creacion)-1)//6 + 1).label("semestre"),
                func.count(PQRSD.id).label("total")
            ).group_by("año", "semestre").all()
            return {f"S{int(r.semestre)}/{int(r.año)}": r.total for r in resultados}

        elif periodo == "año":
            resultados = db.session.query(
                extract('year', PQRSD.fecha_creacion).label("año"),
                func.count(PQRSD.id).label("total")
            ).group_by("año").all()
            return {str(int(r.año)): r.total for r in resultados}

    @staticmethod
    def clasificacion_por_tipo():
        resultados = db.session.query(
            PQRSD.tipo,
            func.count(PQRSD.id).label("total")
        ).group_by(PQRSD.tipo).all()
        labels = [r.tipo for r in resultados]
        data = [r.total for r in resultados]
        return labels, data

    @staticmethod
    def clasificacion_por_dependencia():
        resultados = db.session.query(
            Area.nombre,
            func.count(PQRSD.id).label("total")
        ).join(Area, PQRSD.area_id == Area.id).group_by(Area.nombre).all()
        labels = [r[0] for r in resultados]
        data = [r[1] for r in resultados]
        return labels, data

    @staticmethod
    def cumplimiento_plazos():
        resultados = db.session.query(
            func.sum(case([(PQRSD.fecha_resolucion <= PQRSD.fecha_limite, 1)], else_=0)).label("en_plazo"),
            func.sum(case([(PQRSD.fecha_resolucion > PQRSD.fecha_limite, 1)], else_=0)).label("extemporaneas")
        ).first()
        return {"en_plazo": resultados.en_plazo or 0, "extemporaneas": resultados.extemporaneas or 0}

    @staticmethod
    def clasificacion_por_peticionario():
        resultados = db.session.query(
            PQRSD.tipo_peticionario,  # cambio aquí
            func.count(PQRSD.id).label("total")
        ).group_by(PQRSD.tipo_peticionario).all()
        labels = [r[0] for r in resultados]
        data = [r[1] for r in resultados]
        return labels, data


class Historial(db.Model):
    __tablename__ = "historial"
    
    id = db.Column(db.Integer, primary_key=True)
    pqrsd_id = db.Column(db.Integer, db.ForeignKey('pqrsd.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    accion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Historial PQRSD:{self.pqrsd_id} - {self.accion}>"
