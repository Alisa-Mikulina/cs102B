# type: ignore
from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

# s = session()
# new_news = get_news("https://news.ycombinator.com/newest", n_pages=35)
# for cur_news in new_news:
#     new_note = News(
#         author = cur_news['author'],
#         title = cur_news['title'],
#         comments = cur_news['comments'],
#         url = cur_news['url'],
#         points = cur_news['points'],
#         )
#     s.add(new_note)
# s.commit()
