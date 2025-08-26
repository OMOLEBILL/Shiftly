from models import *
from schemas import *
from sqlalchemy.orm import Session, or_
from typing import Optional
from datetime import date


class baseCRUD:
    def __init__(self, model):
        self.model = model

    def create(self, db:Session, data_obj:dict):
        db_obj = self.model(**data_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, db:Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
    
    def delete(self, db:Session, id: int):
        item = self.get_by_id(db, id)
        if item:
            db.delete(item)
            db.commit()
        return item
    
    def update(self, db:Session, id: int, items:dict):
        item = self.get_by_id(db, id)
        if not item:
            return None
        for key, value in items.items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item


    
def filter_talents(db: Session, role: str=None, contract: str=None, is_active: Optional[bool]=None):
    query = db.query(Talent)

    if role:
        query = query.filter(Talent.role == role)
    if contract:
        query = query.filter(Talent.contract_type == contract)
    if is_active is not None:
        query = query.filter(Talent.is_active == is_active)
    
    return query.all()

def search_talents(db: Session, name: str):
    search = db.query(Talent).filter(or_(
        Talent.firstname.ilike(f"%{name}%"),
        Talent.lastname.ilike(f"%{name}%")
    ))

    return search.all()



    






