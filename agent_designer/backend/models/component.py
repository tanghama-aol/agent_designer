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
    
    # 关联工作流（一个Agent可以有多个工作流）
    workflows = db.relationship('Workflow', backref='agent', lazy=True)
    
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
    
    def get_lpi_details(self):
        """获取LPI组件的详细信息"""
        if self.component_type != 'lpi':
            return None
        
        content = self.content_obj
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'english_description': self.english_description,
            'api_type': content.get('api_type', ''),  # rest 或 python
            'endpoint': content.get('endpoint', ''),
            'method': content.get('method', ''),
            'input_params': content.get('input_params', []),
            'output_params': content.get('output_params', []),
            'examples': content.get('examples', [])
        }
    
    def get_agent_details(self):
        """获取Agent组件的详细信息"""
        if self.component_type != 'agent':
            return None
        
        content = self.content_obj
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'english_description': self.english_description,
            'input_params': content.get('input_params', []),
            'output_params': content.get('output_params', []),
            'examples': content.get('examples', []),
            'workflows': [workflow.to_dict() for workflow in self.workflows]
        }
    
    def get_common_details(self):
        """获取通用组件的详细信息"""
        if self.component_type != 'common':
            return None
        
        content = self.content_obj
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'english_description': self.english_description,
            'component_subtype': content.get('component_subtype', ''),  # condition, executor
            'config': content.get('config', {})
        } 