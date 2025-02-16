from typing import NamedTuple
from bs4 import BeautifulSoup
from datetime import datetime


class Lesson:
    def __init__(self, lesson_soup):
        first_column = lesson_soup.find("td", class_ = "first-column")
        self.title = first_column.find("span", class_ = "title").text.strip().split("\r")[0]
        self.room = first_column.find("span", class_ = "title").find("span", class_ = "room").text.strip()

        subject = lesson_soup.find("td", class_ = "subject")
        self.test_scheduled = bool(subject.find("span", class_ = "subject--scheduledTest"))
        self.topic = subject.find("p").text.strip() if subject.find("p") != None else None
        
        self.homework = lesson_soup.find("td", class_ = "hometask").text.strip()


class DayJournalModel:
    def __init__(self, header_journal_soup, day_journal_soup):
        self.date = datetime.strptime(header_journal_soup.text.strip().split(" ")[0].removesuffix("."), "%d.%m.%y")
        self.lessons = []
        
        lessons_soup = day_journal_soup.find_all("tr", class_ = None)
        for lesson_soup in lessons_soup:
            self.lessons.append(Lesson(lesson_soup))

    def __iter__(self):
        yield from self.lessons


class WeeklyJournalModel:
    def __init__(self, html):
        soup = BeautifulSoup(html, "lxml")
        journal_section = soup.find("section", class_ = "student-journal-lessons").find("div", class_ = "student-journal-lessons-table-holder hidden-xs")
        day_headers = journal_section.find_all("h2")
        day_journals = journal_section.find_all("tbody")

        self.days = {}  # Словарь для хранения дней
        for index, day_header in enumerate(day_headers):
            day_name = day_header.text.lower().strip()
            if "pirmdiena" in day_name:
                self.days["monday"] = DayJournalModel(day_header, day_journals[index])
            elif "otrdiena" in day_name:
                self.days["tuesday"] = DayJournalModel(day_header, day_journals[index])
            elif "trešdiena" in day_name:
                self.days["wednesday"] = DayJournalModel(day_header, day_journals[index])
            elif "ceturtdiena" in day_name:
                self.days["thursday"] = DayJournalModel(day_header, day_journals[index])
            elif "piektdiena" in day_name:
                self.days["friday"] = DayJournalModel(day_header, day_journals[index])
            elif "sestdiena" in day_name:
                self.days["saturday"] = DayJournalModel(day_header, day_journals[index])
            elif "svētdiena" in day_name:
                self.days["sunday"] = DayJournalModel(day_header, day_journals[index])

    def __getitem__(self, index):
        days_list = list(self.days.values())
        return days_list[index]

    def __len__(self):
        return len(self.days)

    def __iter__(self):
        yield from self.days.values()
