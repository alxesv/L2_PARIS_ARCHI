from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Culture(Base):
    __tablename__ = "culture"
    identifiant_culture: Mapped[int] = mapped_column(primary_key=True)
    no_parcelle: Mapped[int] = mapped_column(ForeignKey("parcelle.no_parcelle"))
    code_production: Mapped[int] = mapped_column(ForeignKey("production.code_production"))
    date_debut: Mapped[str] = mapped_column(String(255))
    date_fin: Mapped[str] = mapped_column(String(255))
    qte_recoltee: Mapped[int]
    parcelle: Mapped["Parcelle"] = relationship(back_populates="cultures")
    production: Mapped["Production"] = relationship(back_populates="cultures")


class Production(Base):
    __tablename__ = "production"
    code_production: Mapped[int] = mapped_column(primary_key=True)
    un: Mapped[str] = mapped_column(ForeignKey("unite.un"))
    nom_production: Mapped[str] = mapped_column(String(20))
    cultures: Mapped[List["Culture"]] = relationship(
        back_populates="production", cascade="all, delete-orphan"
    )
    unite: Mapped["Unite"] = relationship(back_populates="productions")


class Parcelle(Base):
    __tablename__ = "parcelle"
    no_parcelle: Mapped[int] = mapped_column(primary_key=True)
    surface: Mapped[int]
    nom_parcelle: Mapped[str] = mapped_column(String(20))
    coordonnees: Mapped[str] = mapped_column(String(20))
    cultures: Mapped[List["Culture"]] = relationship(
        back_populates="parcelle", cascade="all, delete-orphan"
    )
    epandres: Mapped[List["Epandre"]] = relationship(
        back_populates="parcelle", cascade="all, delete-orphan"
    )


class Epandre(Base):
    __tablename__ = "epandre"
    id_engrais: Mapped[int] = mapped_column(ForeignKey("engrais.id_engrais"), primary_key=True)
    no_parcelle: Mapped[int] = mapped_column(ForeignKey("parcelle.no_parcelle"), primary_key=True)
    date_fk: Mapped[str] = mapped_column(ForeignKey("date.date"), primary_key=True)
    qte_epandue: Mapped[int]
    parcelle: Mapped["Parcelle"] = relationship(back_populates="epandres")
    engrais: Mapped["Engrais"] = relationship(back_populates="epandres")
    date: Mapped["Date"] = relationship(back_populates="epandres")


class Date(Base):
    __tablename__ = "date"
    date: Mapped[str] = mapped_column(String(255), primary_key=True)
    epandres: Mapped[List["Epandre"]] = relationship(
        back_populates="date", cascade="all, delete-orphan"
    )


class Engrais(Base):
    __tablename__ = "engrais"
    id_engrais: Mapped[int] = mapped_column(primary_key=True)
    un: Mapped[str] = mapped_column(ForeignKey("unite.un"))
    nom_engrais: Mapped[str] = mapped_column(String(20))
    epandres: Mapped[List["Epandre"]] = relationship(
        back_populates="engrais", cascade="all, delete-orphan"
    )
    posseder: Mapped[List["Posseder"]] = relationship(
        back_populates="engrais", cascade="all, delete-orphan"
    )
    unite: Mapped["Unite"] = relationship(back_populates="engrais")


class Posseder(Base):
    __tablename__ = "posseder"
    id_engrais: Mapped[int] = mapped_column(ForeignKey("engrais.id_engrais"), primary_key=True)
    code_element: Mapped[str] = mapped_column(ForeignKey("element_chimique.code_element"), primary_key=True)
    valeur: Mapped[int]
    engrais: Mapped["Engrais"] = relationship(back_populates="posseder")
    element_chimique: Mapped["ElementChimique"] = relationship(back_populates="posseder")


class ElementChimique(Base):
    __tablename__ = "element_chimique"
    code_element: Mapped[str] = mapped_column(String(5), primary_key=True)
    un: Mapped[str] = mapped_column(ForeignKey("unite.un"))
    libelle_element: Mapped[str] = mapped_column(String(20))
    posseder: Mapped[List["Posseder"]] = relationship(
        back_populates="element_chimique", cascade="all, delete-orphan"
    )
    unite: Mapped["Unite"] = relationship(back_populates="element_chimiques")


class Unite(Base):
    __tablename__ = 'unite'
    un: Mapped[str] = mapped_column(String(20), primary_key=True)
    productions: Mapped[List["Production"]] = relationship(
        back_populates="unite", cascade="all, delete-orphan"
    )
    engrais: Mapped[List["Engrais"]] = relationship(
        back_populates="unite", cascade="all, delete-orphan"
    )
    element_chimiques: Mapped[List["ElementChimique"]] = relationship(
        back_populates="unite", cascade="all, delete-orphan"
    )


class Compteur(Base):
    __tablename__ = "compteur"
    id_compteur: Mapped[int] = mapped_column(primary_key=True)
    horodatage: Mapped[str] = mapped_column(String(50))
    route: Mapped[str] = mapped_column(String(255))
    methode: Mapped[str] = mapped_column(String(10))
