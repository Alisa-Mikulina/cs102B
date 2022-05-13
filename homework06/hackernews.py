# type: ignore
from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("C:\\Users\\ASUS\\Desktop\\VK\\homework06\\recommended.tpl", rows=rows)


@route("/add_label/")
def add_label():
    new_label = request.query.label
    new_id = request.query.id
    s = session()
    note = s.query(News).filter(News.id == new_id).all()[0]
    note.label = new_label
    s.add(note)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    new_news = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    for cur_news in new_news:
        print(cur_news)
        if (
            s.query(News).filter(News.author == cur_news["author"], News.title == cur_news["title"])
        ) is None:
            new_note = News(
                author=cur_news["author"],
                title=cur_news["title"],
                comments=cur_news["comments"],
                url=cur_news["url"],
                points=cur_news["points"],
                label=None,
            )
            s.add(new_note)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labelled = s.query(News).filter(News.label != None).all()
    new = s.query(News).filter(News.label == None).all()

    labelled_rows = [piece.title for piece in labelled]
    labels = [piece.label for piece in labelled]
    new_rows = [piece.title for piece in new]

    model = NaiveBayesClassifier()
    model.fit(labelled_rows, labels)
    predicted_news = model.predict(new_rows)
    for i in range(len(predicted_news)):
        new[i].label = predicted_news[i]
    classified_news = [x for x in new if x.label == "good"]
    classified_news.extend([x for x in new if x.label == "maybe"])
    classified_news.extend([x for x in new if x.label == "never"])
    return template(
        "C:\\Users\\ASUS\\Desktop\\VK\\homework06\\news_template.tpl",
        rows=classified_news,
    )


if __name__ == "__main__":
    run(host="localhost", port=8080)
