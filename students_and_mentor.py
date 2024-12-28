class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __get_average_rate(self):
        average_rate = 0
        for rates in self.grades.values():
            average_rate += sum(rates) / len(rates)
        return average_rate / len(self.grades) if len(self.grades) else average_rate

    def __str__(self):
        average_rate = self.__get_average_rate()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {average_rate: .2f}\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}\nЗавершенные курсы: {', '.join(self.finished_courses)}"

    def __eq__(self, student):
        return self.__get_average_rate() == student.__get_average_rate()

    def set_course_in_progress(self, course):
        if course not in self.courses_in_progress:
            if course in self.finished_courses:
                self.finished_courses.remove(course)
            self.courses_in_progress.append(course)

    def set_finished_course(self, course):
        if course not in self.finished_courses:
            if course in self.courses_in_progress:
                self.courses_in_progress.remove(course)
            self.finished_courses.append(course)

    def rate_lecturers(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and (course in self.finished_courses or course in self.courses_in_progress) and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return "Ошибка"


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def set_course_attached(self, course):
        if course not in self.courses_attached:
            self.courses_attached.append(course)


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __get_average_rate(self):
        average_rate = 0
        for rates in self.grades.values():
            average_rate += sum(rates) / len(rates)
        return average_rate / len(self.grades) if len(self.grades) else average_rate

    def __str__(self):
        average_rate = self.__get_average_rate()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {average_rate: .2f}"

    def __eq__(self, lecturer):
        return self.__get_average_rate() == lecturer.__get_average_rate()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"


# Создание экземпляров класса Студент
first_student = Student("Ivan", "Petrov", "m")
second_student = Student("Inna", "Serova", "f")
# Установка значений курсов для экземпляров класса Студент
first_student.set_course_in_progress("Python")
first_student.set_course_in_progress("GIT")
first_student.set_finished_course("Введение в программирование")

second_student.set_course_in_progress("Python")
second_student.set_course_in_progress("GIT")
second_student.set_finished_course("Введение в программирование")

# Создание экземпляров класса Лектор
first_lecturer = Lecturer("Egor", "Tarelkin")
second_lecturer = Lecturer("Artem", "Kantov")
# Установка значений курсов для экземпляров класса Лектор
first_lecturer.set_course_attached("Python")
first_lecturer.set_course_attached("GIT")
second_lecturer.set_course_attached("GIT")

# Оценивание студентами лекторов
first_student.rate_lecturers(first_lecturer, "Python", 10)
first_student.rate_lecturers(first_lecturer, "GIT", 9)
first_student.rate_lecturers(second_lecturer, "GIT", 10)

second_student.rate_lecturers(first_lecturer, "Python", 8)
second_student.rate_lecturers(first_lecturer, "GIT", 7)
second_student.rate_lecturers(second_lecturer, "GIT", 10)

# Создание экземпляров класса Проверяющий
first_reviewer = Reviewer("Boris", "Ivanov")
second_reviewer = Reviewer("Irina", "Shishkova")

# Установка значений курсов для экземпляров класса Проверяющий
first_reviewer.set_course_attached("Python")
first_reviewer.set_course_attached("GIT")
second_reviewer.set_course_attached("GIT")

# Оценивание проверяющими студентов
first_reviewer.rate_hw(first_student, "Python", 10)
first_reviewer.rate_hw(first_student, "GIT", 10)
second_reviewer.rate_hw(second_student, "GIT", 10)

print(first_student, second_student, first_lecturer, second_lecturer, first_reviewer, second_reviewer, sep="\n\n")

print(f"Результат сравнения студентов: {first_student == second_student}")
print(f"Результат сравнения лекторов: {first_lecturer == second_lecturer}")


def count_grades_students(list_students, course):
    list_all_rate = []
    for student in list_students:
        if course in student.grades:
            list_all_rate += student.grades[course]
    print(f"Средняя оценка по курсу {course}: {sum(list_all_rate) / len(list_all_rate)}")


def count_grades_lecturers(list_lecturers, course):
    list_all_rate = []
    for lecturer in list_lecturers:
        if course in lecturer.grades:
            list_all_rate += lecturer.grades[course]
    print(f"Средняя оценка по курсу {course}: {sum(list_all_rate) / len(list_all_rate)}")


count_grades_students([first_student, first_student], "Python")
count_grades_lecturers([first_lecturer, second_lecturer], "GIT")
