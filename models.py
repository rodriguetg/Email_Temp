from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON)
    
    channels = relationship('Channel', back_populates='user')
    rules = relationship('Rule', back_populates='user')
    messages = relationship('Message', back_populates='user')

class Channel(Base):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    platform = Column(String(50), nullable=False)
    channel_id = Column(String(100), nullable=False)
    name = Column(String(100))
    credentials = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    
    user = relationship('User', back_populates='channels')
    messages = relationship('Message', back_populates='channel')

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    channel_id = Column(Integer, ForeignKey('channels.id'))
    external_id = Column(String(100))
    sender = Column(String(100))
    content = Column(String)
    attachments = Column(JSON)
    message_data = Column(JSON)
    received_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    
    user = relationship('User', back_populates='messages')
    channel = relationship('Channel', back_populates='messages')

class Rule(Base):
    __tablename__ = 'rules'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    conditions = Column(JSON)
    actions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='rules')

class AutoResponse(Base):
    __tablename__ = 'auto_responses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    template_name = Column(String(100))
    content = Column(String)
    conditions = Column(JSON)
    schedule = Column(JSON)
    is_active = Column(Boolean, default=True)

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    platform = Column(String(50))
    message_count = Column(Integer, default=0)
    response_time_avg = Column(Integer)
    message_metadata = Column(JSON)
