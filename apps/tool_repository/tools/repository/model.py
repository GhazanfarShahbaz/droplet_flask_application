from sqlalchemy import (ARRAY, Boolean, Column, DateTime, Float, Integer, 
                        String, Text, ForeignKey)
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from get_db_engine import get_engine

Engine: Engine = get_engine()
Session = sessionmaker(Engine)
Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    EventId = Column("EventId", Integer, primary_key=True, autoincrement=True)
    ReccuranceId = Column("RecurranceId", Integer, nullable=True)

    Name = Column("Name", String(256), nullable=False)
    StartDate = Column("StartDate", DateTime(timezone=True), nullable=False)
    EndDate = Column("EndDate", DateTime(timezone=True), nullable=False)
    Type = Column("Type", String(32), nullable=False)
    Location = Column("Location", String(1024), nullable=False)
    ReccuranceType = Column("ReccurranceType", String(64), nullable=True)
    Description = Column("Description", String(512), nullable=True)

    def __init__(self, event_information: dict) -> None:
        self.ReccuranceId = event_information.get("ReccuranceId")
        self.Name = event_information.get("Name")
        self.StartDate = event_information.get("StartDate")
        self.EndDate = event_information.get("EndDate")
        self.Location = event_information.get("Location")
        self.Type = event_information.get("Type")
        self.ReccuranceType = event_information.get("ReccuranceType")
        self.Description = event_information.get("Description")
    
    def to_dict(self) -> dict:
        return {
            "Id": self.EventId,
            "ReccuranceId": self.ReccuranceId,
            "Name": self.Name,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "Type": self.Type,
            "Description": self.Description,
            "ReccuranceType": self.ReccuranceType
        }

class Class(Base):
    __tablename__ = "classes"

    ClassId = Column("ClassId", Integer, primary_key=True, autoincrement=True)

    Department = Column("Department", String(128), nullable=False)
    CourseNumber = Column("CourseNumber", Integer, nullable=False)
    Professor = Column("Professor", String(128), nullable=False)
    Name = Column("Name", String(128), nullable=False)
    Semester = Column("Semester", String(128), nullable=False)

    Syllabus = relationship("Syllabus", backref="classes",
                            cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, class_inforamtion: dict) -> None:
        self.ClassId = class_inforamtion.get("ClassId")
        self.Department = class_inforamtion.get("Department")
        self.Professor = class_inforamtion.get("Professor")
        self.Name = class_inforamtion.get("Name")
        self.Semester = class_inforamtion.get("Semester")
        self.Syllabus = class_inforamtion.get("Syllabus")
    
    def to_dict(self) -> dict:
        return {
            "ClassId": self.ClassId,
            "Department": self.Department,
            "Professor": self.Professor,
            "Name": self.Name,
            "Semester": self.Semester,
            "Syllabus": self.Syllabus,
        }


class Syllabus(Base):
    __tablename__ = "syllabi"

    ClassId = Column("ClassId", ForeignKey(
        "classes.ClassId", ondelete="CASCADE"))
    SectionId = Column("SectionId", String(64), primary_key=True)

    Section = Column("Section", String(64), nullable=False)
    Percentage = Column("Percentage", Integer, nullable=False)
    Droppable = Column("Droppable", Integer, nullable=False, default=0)

    Assignments = relationship(
        "Assignment", backref="syllabi", cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, syllabus_information: dict) -> None:
        self.ClassId = syllabus_information.get("ClassId")
        self.SectionId = syllabus_information.get("SectionId")
        self.Section = syllabus_information.get("Section")
        self.Percentage = syllabus_information.get("Percentage")
        self.Droppable = syllabus_information.get("Droppable")
    
    def to_dict(self) -> dict:
        return {
            "ClassId": self.ClassId,
            "SectionId": self.SectionId,
            "Section": self.Section,
            "Percentage": self.Percentage,
            "Droppable": self.Droppable,
        }


class Assignment(Base):
    __tablename__ = "assignments"

    SectionId = Column("SectionId", ForeignKey(
        "syllabi.SectionId", ondelete="CASCADE"))
    AssignmentId = Column("AssignmentId", Integer,
                          autoincrement=True, primary_key=True)


    Name = Column("Name", String(64), nullable=False)
    Grade = Column("Grade", Integer, nullable=False)
    DateAssigned = Column("DateAssigned", DateTime(timezone=True), nullable=True)
    DateDue = Column("DateDue", DateTime(timezone=True), nullable=True)
    Submitted = Column("Submitted", Boolean, nullable=False, default=False)


    def __init__(self, assignment_information: dict) -> None:
        self.SectionId = assignment_information.get("ClassId")
        self.AssignmentId = assignment_information.get("AssignmentId")
        self.Grade = assignment_information.get("Grade")
        self.DateAssigned = assignment_information.get("DateAssigned")
        self.DateDue = assignment_information.get("DateDue")
        self.Submitted = assignment_information.get("Submitted")
    
    def to_dict(self) -> dict:
        return {
            "ClassId": self.ClassId,
            "AssignmentId": self.AssignmentId,
            "Grade": self.Grade,
            "DateAssigned": self.DateAssigned,
            "DateDue": self.DateDue,
            "Submitted": self.Submitted,
        }



class Definition(Base):
    __tablename__ = "definitions"
    
    DefinitionId = Column("DefinitionId", Integer, autoincrement=True, primary_key=True)
    
    ClassName = Column("ClassName", String(128), nullable=False)
    FileName = Column("FileName", String(128), nullable=False)
    Definition = Column("Definition", Text, nullable=True)

    def __init__(self, assignment_information: dict) -> None:
        self.DefinitionId = assignment_information.get("DefinitionId")
        self.ClassName = assignment_information.get("ClassName")
        self.FileName = assignment_information.get("FileName")
        self.Definition = assignment_information.get("Definition")
    
    def to_dict(self) -> dict:
        return {
            "DefinitionId": self.DefinitionId,
            "ClassName": self.ClassName,
            "FileName": self.FileName,
            "Definition": self.Definition
        }


class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    QuestionId = Column("QuestionId", String(64), primary_key=True)
    QuestionLink = Column("QuestionLink", String(256), nullable=True)
    QuestionName = Column("QuestionName", String(128), nullable=True)
    Difficulty = Column("Difficulty", String(32), nullable=True)
    AcceptanceRate = Column("AcceptanceRate", Float, nullable=True)
    Tags = Column("Tags", ARRAY(Integer), nullable=True)
    RequiresSubscription = Column("RequiresSubscription", Boolean, nullable=True)

    def __init__(self, question_information: dict) -> None:
        self.QuestionId = question_information.get("QuestionId")
        self.QuestionName = question_information.get("QuestionName")
        self.QuestionLink = question_information.get("QuestionLink")
        self.Difficulty = question_information.get("Difficulty")
        self.AcceptanceRate = question_information.get("AcceptanceRate")
        self.Tags = question_information.get("Tags")
        self.RequiresSubscription = question_information.get("RequiresSubscription")

    def to_dict(self) -> dict:
        return {
            "QuestionId": self.QuestionId,
            "QuestionLink": self.QuestionLink,
            "QuestionName": self.QuestionName,
            "Difficulty": self.Difficulty,
            "AcceptanceRate": self.AcceptanceRate,
            "Tags": self.Tags,
            "RequiresSubscription": self.RequiresSubscription
        }

def init_db():
    global Base, Engine
    Base.metadata.create_all(bind=Engine)
    print("Created Model")