import datetime
import traceback

# this is modified code from a private project


class Lesson:
    def __init__(
        self,
        name: str,
        teacher: str,
        ausfall: bool,
        student_id: int,
        student_data: dict,
    ):
        self.data = {}
        self.deletion_candiate = False
        if name == "":
            self.apply_for_deletion()
        elif name in ["Bio", "Chemie", "Informatik"]:
            if student_data[name] is True:
                pass
            else:
                self.apply_for_deletion()
                return
        elif name == "Kreatives Fach":
            name = student_data["Kreatives Fach"]
            teacher = student_data["kLehrer"]
        elif name == "Reli / Philo":
            name = student_data["Reli / Philo"]
            teacher = student_data["rLehrer"]

        self.name = name
        self.teacher = teacher
        self.ausfall = ausfall
        self.student_id = student_id
        self.data = {
            "name": name,
            "teacher": teacher,
            "ausfall": ausfall,
            "student_id": student_id,
        }

    def apply_for_deletion(self):
        self.deletion_candiate = True
        self.data.update({"name": " ", "teacher": " ", "ausfall": True})
        self.name = " "
        self.teacher = " "
        self.ausfall = True


class Day:
    def __init__(
        self,
        fortnight_day: int,
        even_week: bool,
        day_data: list[list[str, str, float]],
        student_id: int,
        student_data: dict,
    ):
        self.lessons = []
        self.fortnight_day = fortnight_day
        self.even_week = even_week
        self.student_id = student_id
        for lesson_data in day_data:
            self.lessons.append(
                Lesson(
                    lesson_data[0],
                    lesson_data[1],
                    lesson_data[2],
                    student_id,
                    student_data,
                )
            )
        self.cleanup()

    def actual_lessons(self):
        lessons = 0
        for lesson in self.lessons:
            if lesson.ausfall == False:
                lessons += 1
        return lessons

    def showself(self, today=True):
        self.cleanup()
        return_string = ""
        cancelled = 0
        for lesson in self.lessons:
            cancelled += 1 if lesson.ausfall == True else 0
        if len(self.lessons) == 0 or cancelled == len(self.lessons):
            if today == True:
                return_string += "Heute ist schulfrei, schon vergessen?"
            else:
                return_string += "Morgen ist schulfrei, schon vergessen?"
        else:
            lessons = self.actual_lessons()
            if today == True:
                date = datetime.datetime.today().strftime("%d.%m.%Y")
                return_string += (
                    f"Heute, am {date}, hat <@{self.student_id}> {lessons} Blöcke.\n"
                )
                return_string += "------------\n"
                for lesson in self.lessons:
                    return_string += "**" + lesson.name + "**\n"
                    return_string += lesson.teacher + "\n"
                    return_string += "------------\n"
                    if self.lessons.index(lesson) == 2 and len(self.lessons) > 3:
                        return_string += "------------\n"
            else:
                datetime_tomorrow = datetime.datetime.today() + datetime.timedelta(
                    days=1
                )
                date = datetime_tomorrow.strftime("%d.%m.%Y")
                return_string += (
                    f"Am {date} hat <@{self.student_id}> {lessons} Blöcke.\n"
                )
                return_string += "------------\n"
                for lesson in self.lessons:
                    return_string += "**" + lesson.name + "**\n"
                    return_string += lesson.teacher + "\n"
                    return_string += "------------\n"
                    if self.lessons.index(lesson) == 2 and len(self.lessons) > 3:
                        return_string += "------------\n"
        return return_string

    def get_lesson(self, lesson, data):
        try:
            i = self.lessons[lesson]
        except IndexError:
            return " "
        else:
            return self.lessons[lesson].data[data]

    def cleanup(self):
        for lesson in self.lessons[::-1]:
            if lesson == self.lessons[-1] and lesson.deletion_candiate == True:
                self.lessons.remove(lesson)


class Stundenplan:
    def __init__(self, member_id, data):
        self.member_id = member_id
        self.days = []
        self.profil = data[member_id]["Profil"]
        self.data = data[self.profil]
        for day_data in self.data:
            even_week = False if self.data.index(day_data) > 6 else True
            self.days.append(
                Day(
                    self.data.index(day_data),
                    even_week,
                    day_data,
                    member_id,
                    data[member_id],
                )
            )

    def heute(self):
        weekday = datetime.datetime.today().weekday()
        if int(datetime.datetime.today().strftime("%V")) % 2 == 0:
            fortnight_day = weekday + 7
        else:
            fortnight_day = weekday
        if weekday > 13:
            weekday -= 14
        return self.days[fortnight_day].showself(today=True)

    def morgen(self):
        weekday_tomorrow = datetime.datetime.today().weekday() + 1
        if int(datetime.datetime.today().strftime("%V")) % 2 == 0:
            fortnight_day = weekday_tomorrow + 7
        else:
            fortnight_day = weekday_tomorrow
        if fortnight_day > 13:
            fortnight_day -= 14
        try:
            return self.days[fortnight_day].showself(today=False)
        except IndexError:
            print(traceback.format_exc())
            return f"Fehler! {fortnight_day} < 13. Pingt mich solange ich den befehl nicht selber eingegeben habe:\n ```{traceback.format_exc()}```"

    def row_splitter(self):
        return (
            "+"
            + 12 * "-"
            + "+"
            + 12 * "-"
            + "+"
            + 12 * "-"
            + "+"
            + 12 * "-"
            + "+"
            + 12 * "-"
            + "+"
            + "\n"
        )
        # +------------+------------+------------+------------+------------+\n

    def show_week(self):
        return_string = ""
        weekdays = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]
        return_string += f"Heute ist {weekdays[datetime.datetime.today().weekday()]}. "
        even_week = (
            True if int(datetime.datetime.today().strftime("%V")) % 2 == 0 else False
        )
        if datetime.datetime.today().weekday() > 4:
            return_string += f"Hier ist der Stundenplan von <@{self.member_id}> für **nächste** Woche:"
            even_week = not even_week
        else:
            return_string += (
                f"Hier ist der Stundenplan von <@{self.member_id}> für **diese** Woche:"
            )
        return_string += "```\n"
        return_string += self.row_splitter()
        day_numbers = [0, 1, 2, 3, 4] if even_week == False else [7, 8, 9, 10, 11]
        for lesson in [0, 1, 2, 3, 4]:
            if lesson == 3:
                return_string += self.row_splitter()
            for data in ["name", "teacher"]:
                return_string += "|"
                for day in day_numbers:
                    return_string += " "
                    lesson_data = self.days[day].get_lesson(lesson, data)
                    return_string += lesson_data
                    return_string += (11 - len(lesson_data)) * " "
                    return_string += "|"
                return_string += "\n"
            return_string += self.row_splitter()
        return_string += "```"
        return return_string


mats_data = {
    399183833901170689: {
        "Profil": "Physik",
        "Reli / Philo": "Philo",
        "rLehrer": "Priebe",
        "Kreatives Fach": "Musik",
        "kLehrer": "Wellner",
        "Chemie": False,
        "Bio": False,
        "Informatik": True,
    },
    "Physik": [
        [  # mon
            ["Latein", "Derlien", False],
            ["Physik", "Büsser", False],
            ["Deutsch", "Balasus", False],
            ["Bio", "Hudzik", False],
        ],
        [  # tue
            ["Englisch", "Bach", False],
            ["Latein", "Derlien", False],
            ["WiPo", "Becker", False],
            ["Physik", "Büsser", False],
            ["Deutsch", "Balasus", False],
        ],
        [  # wed
            ["Mathe", "Stamm", False],
            ["Chemie", "Weber", False],
            ["Englisch", "Bach", False],
        ],
        [  # thur
            ["Reli / Philo", "rLehrer", False],
            ["Erdkunde", "Boysen", False],
            ["Kreatives Fach", "kLehrer", False],
            ["Informatik", "Stieglitz?", False],
            ["Geschichte", "Heberlein", False],
        ],
        [
            ["", "", True],
            ["Sport", "Pilarczyk", False],
            ["Mathe", "Stamm", False],
        ],  # fri
        [],  # sat
        [],  # sun
        [  # mon
            ["Latein", "Derlien", False],
            ["Physik", "Büsser", False],
            ["Deutsch", "Balasus", False],
            ["Bio", "Hudzik", False],
        ],
        [  # tue
            ["Bio", "Hudzik", True],
            ["BerOri", "Bach", False],
            ["WiPo", "Becker", False],
            ["Physik", "Büsser", False],
        ],
        [  # wed
            ["Mathe", "Stamm", False],
            ["Chemie", "Weber", False],
            ["Englisch", "Bach", False],
            ["Informatik", "Stieglitz?", False],
        ],
        [  # thur
            ["Reli / Philo", "rLehrer", False],
            ["Erdkunde", "Boysen", False],
            ["Kreatives Fach", "kLehrer", False],
            ["Informatik", "Stieglitz?", False],
            ["Geschichte", "Heberlein", False],
        ],
        [
            ["", "", True],
            ["Sport", "Pilarczyk", False],
            ["WiPo", "Becker", False],
        ],  # fri
        [],  # sat
        [],  # sun
    ],
}
mats_stundenplan = Stundenplan(399183833901170689, mats_data)
