from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id          = Column(Integer, primary_key=True, index=True)
    repo_name   = Column(String, nullable=False)
    pr_number   = Column(Integer, nullable=False)
    pr_title    = Column(String, nullable=True)
    status      = Column(String, default="reviewed")
    created_at  = Column(DateTime, default=datetime.utcnow)
    reviews     = relationship("Review", back_populates="pull_request")

class Review(Base):
    __tablename__ = "reviews"

    id               = Column(Integer, primary_key=True, index=True)
    pull_request_id  = Column(Integer, ForeignKey("pull_requests.id"))
    total_issues     = Column(Integer, default=0)
    critical_count   = Column(Integer, default=0)
    warning_count    = Column(Integer, default=0)
    suggestion_count = Column(Integer, default=0)
    created_at       = Column(DateTime, default=datetime.utcnow)
    pull_request     = relationship("PullRequest", back_populates="reviews")
    issues           = relationship("Issue", back_populates="review")

class Issue(Base):
    __tablename__ = "issues"

    id          = Column(Integer, primary_key=True, index=True)
    review_id   = Column(Integer, ForeignKey("reviews.id"))
    severity    = Column(String, nullable=False)
    issue_type  = Column(String, nullable=False)
    message     = Column(Text, nullable=False)
    line_number = Column(String, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    review      = relationship("Review", back_populates="issues")