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
    status = db.Column(db.String(20), default='draft')  # draft, published
    version = db.Column(db.String(20), default='1.0.0')
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
            'status': self.status,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_node_by_id(self, node_id):
        """根据ID获取节点"""
        for node in self.nodes_obj:
            if node.get('id') == node_id:
                return node
        return None
    
    def get_connected_nodes(self, node_id):
        """获取与指定节点相连的所有节点"""
        connected_nodes = []
        for edge in self.edges_obj:
            if edge.get('source') == node_id:
                target_id = edge.get('target')
                target_node = self.get_node_by_id(target_id)
                if target_node:
                    connected_nodes.append(target_node)
            elif edge.get('target') == node_id:
                source_id = edge.get('source')
                source_node = self.get_node_by_id(source_id)
                if source_node:
                    connected_nodes.append(source_node)
        return connected_nodes
    
    def get_start_node(self):
        """获取开始节点"""
        for node in self.nodes_obj:
            if node.get('type') == 'start':
                return node
        return None
    
    def get_end_nodes(self):
        """获取所有结束节点"""
        end_nodes = []
        for node in self.nodes_obj:
            if node.get('type') == 'end':
                end_nodes.append(node)
        return end_nodes 