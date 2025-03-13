from . import db
from datetime import datetime
import json

class Workflow(db.Model):
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    agent_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    nodes = db.Column(db.Text)  # JSON存储节点
    edges = db.Column(db.Text)  # JSON存储连接
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Workflow {self.name}>'
    
    @property
    def nodes_obj(self):
        if self.nodes:
            return json.loads(self.nodes)
        return []
    
    @nodes_obj.setter
    def nodes_obj(self, obj):
        self.nodes = json.dumps(obj)
    
    @property
    def edges_obj(self):
        if self.edges:
            return json.loads(self.edges)
        return []
    
    @edges_obj.setter
    def edges_obj(self, obj):
        self.edges = json.dumps(obj)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'agent_id': self.agent_id,
            'nodes': self.nodes_obj,
            'edges': self.edges_obj,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 