from . import db
from datetime import datetime
import json

class Component(db.Model):
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    english_description = db.Column(db.Text)
    component_type = db.Column(db.String(20), nullable=False)  # lpi, agent, common
    category = db.Column(db.String(50))
    content = db.Column(db.Text)  # JSON存储组件内容
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Component {self.name}>'
    
    @property
    def content_obj(self):
        if self.content:
            return json.loads(self.content)
        return {}
    
    @content_obj.setter
    def content_obj(self, obj):
        self.content = json.dumps(obj)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'english_description': self.english_description,
            'component_type': self.component_type,
            'category': self.category,
            'content': self.content_obj,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 