from seleniumbase import BaseCase
from bs4 import BeautifulSoup
import re


# might not need all of the fields, but just there in case. (most important are name, topic, time, instructor)
class Course:
    def __init__(self,class_id, name, professor, time, room, instruction_mode, status, course_topic):
        self.class_id = class_id
        self.name = name
        self.professor = professor 
        self.time = time 
        self.room = room 
        self.instruction_mode = instruction_mode 
        self.status = status
        self.course_topic = course_topic 
    
class InstitutionSelectionTest(BaseCase):
    def test_select_institutions(self):
        # open page
        self.open("https://globalsearch.cuny.edu/CFGlobalSearchTool/search.jsp")  # Replace URL_of_your_page with the actual URL

        # first page of form ---------------------------------------------------
        # not visible (have to do js script injection (clicks not working properly))
        # last resort js script execution due to visibility issue of the element.
        self.execute_script("document.getElementById('CSI01').click();")

        # term selection
        self.select_option_by_value("#t_pd", "1249")

        # SUBMIT first page of form
        self.click('input[name="next_btn"]')
        print('it passed?')


        # second page of form ---------------------------------------------------

        # select computer science courses from drop down 
        # select option where value="CMSC" (computer science classes)
        self.select_option_by_value("#subject_ld", "CMSC")

        # select undergrad courses from dropdown
        self.select_option_by_value("#courseCareerId", "UGRD")

        # submit form
        self.click('input[name="search_btn_search"]')


        # Third page (actual class list)
        # switch to beautiful soup (easier for scraping final page)
        html_source = self.get_page_source()
        soup = BeautifulSoup(html_source, 'html.parser')

        classNames = soup.find_all('div', class_="testing_msg")
        # drop the first 2 (title, description)
        classNames.pop(0)
        classNames.pop(0)

        classes = {}
        print("length", len(classNames))

        # creating a dict which maps topics -> class name (Data Structures -> CSC326)   
        # since the html structure is stupid (tables of classes aren't nested under common class title)
        # so i have to derive the class name from the topic for each class.
        for cs_class in classNames:
            # first get the name and label of the cs class
            class_text = cs_class.get_text()
            print(class_text)
            class_text.replace('\xa0', ' ')
            class_text.replace('\n', '')
            class_id, classname = class_text.split('-')
            class_id = class_id.lstrip().rstrip()
            class_id = class_id[0:3] + class_id[4:]
            classname = classname.lstrip().rstrip().replace('\xa0', ' ')

            classes[classname] = class_id 
            # print(class_id)
            # print(classname)
        
        print(classes)


        # getting all of the important values in the rows of the tables (section, professor, times, etc.)

        sections = soup.find_all("td", attrs={"data-label": "Section"})  
        # get it from hashmap using the course_topic
        instructors = soup.find_all("td", attrs={"data-label": "Instructor"}) 

        times = soup.find_all("td", attrs={"data-label": "DaysAndTimes"})
        
        rooms = soup.find_all("td", attrs={"data-label": "Room"})
        
        instructionModes = soup.find_all("td", attrs={"data-label": "Instruction Mode"})
        # figure this out later
        topic = soup.find_all("td", attrs={"data-label": "Course Topic"})

        print("LENS", len(sections))
        # testing if all same size
        print("TRUE?", len(sections) == len(times) == len(instructionModes) == len(instructors) == len(rooms) == len(topic))


        # store a list of the classes
        # the course object has many parameters
        # we probably just need class name, times / dates, professors names. (room, section id, etc. doens't matter much)
        ListOfClasses = []
        # create object for each class (store in Database later)
        for i in range(len(sections)):
            print(topic[i].get_text())
            course = Course(sections[i].get_text(), classes[topic[i].get_text()], instructors[i].get_text(), re.sub(r'([AP]M)(Mo|Tu|We|Th|Fr|Sa|Su)', r'\1 \2', times[i].get_text()), rooms[i].get_text(), instructionModes[i].get_text(), True, topic[i].get_text() )
            ListOfClasses.append(course)

        # check
        for c in ListOfClasses:
            print(c.class_id)
            print(c.name)
            print(c.course_topic)
            print(c.time)
            print(c.room)
            print(c.professor)
            print()
            
        # pause 
        # while True:
            # pass

"""
SAMPLE of scraped info

E001-LEC Regular
CSC115
Intro Comp Technolog
We 6:30PM - 7:20PM Mo 6:30PM - 8:10PM
2N 0012N 001
Daniel AgmanDaniel Agman

E003-LAB Regular
CSC117
Computer Technology Lab
We 7:30PM - 9:10PM
5N 106
Daniel Agman

F001-LAB Regular
CSC117
Computer Technology Lab
Mo 8:20PM - 10:00PM
5N 108
Daniel Agman

E001-LEC Regular
CSC119
Computer Technology Concepts
Tu 6:30PM - 8:10PM Th 6:30PM - 7:20PM
5N 1065N 106
Michael D'Eredita

01-LEC Regular
CSC126
Intro Computer Sci
We 12:20PM - 1:10PM Mo 12:20PM - 2:15PM
3N 1023N 102
Cong Chen

01L1-LAB Regular
CSC126
Intro Computer Sci
We 1:25PM - 3:20PM Mo 2:30PM - 3:20PM
3N 1023N 102
Cong Chen

01L2-LAB Regular
CSC126
Intro Computer Sci
We 1:25PM - 3:20PM Mo 2:30PM - 3:20PM
2N 1152N 115
Zhiqi Wang

01L3-LAB Regular
CSC126
Intro Computer Sci
We 3:35PM - 5:30PM Mo 3:35PM - 4:25PM
1N 0051N 005


02-LEC Regular
CSC126
Intro Computer Sci
Tu 9:05AM - 9:55AM Th 9:05AM - 11:00AM
1S 1161S 116
Sarah Zelikovitz

02L1-LAB Regular
CSC126
Intro Computer Sci
Tu 10:10AM - 12:05PM Th 11:15AM - 12:05PM
2N 1032N 103
Sarah Zelikovitz

02L2-LAB Regular
CSC126
Intro Computer Sci
Tu 10:10AM - 12:05PM Th 11:15AM - 12:05PM

Ziyi Xu

02L3-LAB Regular
CSC126
Intro Computer Sci
Tu 12:20PM - 2:15PM Th 12:20PM - 1:10PM
2N 1032N 103
Ziyi Xu

03-LEC Regular
CSC126
Intro Computer Sci
Mo 6:30PM - 8:10PM
6S 138
Dolores Hayes

03L1-LAB Regular
CSC126
Intro Computer Sci
We 7:30PM - 9:10PM Mo 8:20PM - 9:10PM
1N 0041N 004
Dolores Hayes

03L2-LAB Regular
CSC126
Intro Computer Sci
We 7:30PM - 9:10PM Mo 8:20PM - 9:10PM

Zaid Al-Mashhadani

03L3-LAB Regular
CSC126
Intro Computer Sci
We 7:30PM - 9:10PM Mo 8:20PM - 9:10PM

Fatma Kausar

E002-LEC Regular
CSC140
Computational Problem Solving
Mo 6:30PM - 9:50PM
TBA
TBA

D001-LEC Regular
CSC211
Intermediate Programming
We 11:15AM - 1:10PM We 10:10AM - 11:00AM Mo 12:20PM - 1:10PM Mo 10:10AM - 12:05PM
1N 0051N 0051N 0051N 005
Deborah Sturm

.....................
....................
.....................
more rows

"""